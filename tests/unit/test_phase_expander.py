# Copyright: Your Name. Apache 2.0
"""Unit tests for :mod:`motion.services.phase_expander`.

The expander wraps Claude; no real API calls are made here. The anthropic
client is stubbed via ``monkeypatch`` so tests stay hermetic and fast.
"""

from __future__ import annotations

from typing import Any

import pytest

from motion.services import phase_expander
from motion.services.phase_expander import (
    _filter_actions,
    _validate_action,
    expand_phase_from_narrative,
)

# ---------------------------------------------------------------------------
# Fake anthropic client plumbing.
# ---------------------------------------------------------------------------


class _FakeContentBlock:
    def __init__(self, text: str) -> None:
        self.text = text


class _FakeMessage:
    def __init__(self, text: str) -> None:
        self.content = [_FakeContentBlock(text)]


class _FakeMessages:
    def __init__(self, text: str, raise_exc: Exception | None = None) -> None:
        self._text = text
        self._raise_exc = raise_exc
        self.last_kwargs: dict[str, Any] | None = None

    def create(self, **kwargs: Any) -> _FakeMessage:
        self.last_kwargs = kwargs
        if self._raise_exc is not None:
            raise self._raise_exc
        return _FakeMessage(self._text)


class _FakeAnthropic:
    def __init__(self, text: str = "[]", raise_exc: Exception | None = None) -> None:
        self.messages = _FakeMessages(text, raise_exc)


def _install_fake_client(
    monkeypatch: pytest.MonkeyPatch,
    text: str = "[]",
    raise_exc: Exception | None = None,
) -> _FakeAnthropic:
    """Stub the anthropic module so no HTTP calls are made."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    fake = _FakeAnthropic(text=text, raise_exc=raise_exc)

    class _FakeModule:
        Anthropic = staticmethod(lambda: fake)

    import sys

    monkeypatch.setitem(sys.modules, "anthropic", _FakeModule)
    return fake


# ---------------------------------------------------------------------------
# Graceful fallbacks.
# ---------------------------------------------------------------------------


def test_returns_empty_when_api_key_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No API key → return ``[]`` silently without importing anthropic."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = expand_phase_from_narrative(
        phase_label="Phase 2: Flare",
        phase_text="4 flares to the corner while 2 curls off 5.",
        player_ids=["1", "2", "3", "4", "5"],
    )
    assert result == []


def test_returns_empty_when_phase_text_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Empty prose → return ``[]`` without bothering the LLM."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    assert (
        expand_phase_from_narrative(
            phase_label="Phase 1",
            phase_text="   ",
            player_ids=["1", "2"],
        )
        == []
    )


def test_returns_empty_when_player_ids_empty(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """No players → ``[]``."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    assert (
        expand_phase_from_narrative(
            phase_label="Phase 1",
            phase_text="Something happens.",
            player_ids=[],
        )
        == []
    )


def test_returns_empty_on_malformed_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Claude returning non-JSON → ``[]`` (no crash)."""
    _install_fake_client(monkeypatch, text="not valid json at all }]]")
    result = expand_phase_from_narrative(
        phase_label="Phase 2",
        phase_text="2 cuts to the wing.",
        player_ids=["1", "2"],
    )
    assert result == []


def test_returns_empty_on_non_list_json(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Claude returning an object (not a list) → ``[]``."""
    _install_fake_client(monkeypatch, text='{"from":"1","to":"2","type":"pass"}')
    result = expand_phase_from_narrative(
        phase_label="Phase 2",
        phase_text="Something.",
        player_ids=["1", "2"],
    )
    assert result == []


def test_returns_empty_when_sdk_raises(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Any upstream exception degrades to ``[]`` (no crash)."""
    _install_fake_client(monkeypatch, raise_exc=RuntimeError("rate limit"))
    result = expand_phase_from_narrative(
        phase_label="Phase 2",
        phase_text="2 cuts to the wing.",
        player_ids=["1", "2"],
    )
    assert result == []


# ---------------------------------------------------------------------------
# Happy path + validation.
# ---------------------------------------------------------------------------


def test_happy_path_parses_valid_actions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Well-formed JSON array round-trips through the validator."""
    fake = _install_fake_client(
        monkeypatch,
        text=(
            '[{"from":"2","to":"right_wing","type":"cut"},'
            '{"from":"4","to":"2","type":"screen"},'
            '{"from":"1","to":"2","type":"pass"}]'
        ),
    )
    result = expand_phase_from_narrative(
        phase_label="Phase 2: Wing Exchange",
        phase_text="2 cuts to the right wing off 4's screen; 1 passes to 2.",
        player_ids=["1", "2", "3", "4", "5"],
        preceding_actions=[{"from": "1", "to": "right_wing", "type": "dribble"}],
    )
    assert result == [
        {"from": "2", "to": "right_wing", "type": "cut"},
        {"from": "4", "to": "2", "type": "screen"},
        {"from": "1", "to": "2", "type": "pass"},
    ]
    # Claude call carried the system + user kwargs we expect.
    kwargs = fake.messages.last_kwargs
    assert kwargs is not None
    assert kwargs["model"] == "claude-sonnet-4-6"
    assert kwargs["temperature"] <= 0.2
    assert "system" in kwargs
    assert len(kwargs["messages"]) == 1
    assert kwargs["messages"][0]["role"] == "user"


def test_happy_path_strips_markdown_fences(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """LLM wrapping in ```json ... ``` is tolerated."""
    _install_fake_client(
        monkeypatch,
        text='```json\n[{"from":"1","to":"top","type":"dribble"}]\n```',
    )
    result = expand_phase_from_narrative(
        phase_label="Phase 1",
        phase_text="1 dribbles to the top.",
        player_ids=["1", "2"],
    )
    assert result == [{"from": "1", "to": "top", "type": "dribble"}]


# ---------------------------------------------------------------------------
# Schema validator — pure unit coverage of the filter.
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "bad_action",
    [
        # Wrong type.
        {"from": "1", "to": "2", "type": "teleport"},
        # "from" not in player_ids.
        {"from": "9", "to": "2", "type": "pass"},
        # "to" is neither a known player id nor a role token.
        {"from": "1", "to": "moon", "type": "pass"},
        # Missing field.
        {"from": "1", "type": "pass"},
        # Not even a dict.
        "some-string",
        # Explicitly wrong types on the required fields.
        {"from": 1.5, "to": "2", "type": "pass"},
    ],
)
def test_validate_action_rejects_malformed(bad_action: object) -> None:
    allowed = frozenset({"1", "2", "3", "4", "5"})
    assert _validate_action(bad_action, allowed) is None


def test_validate_action_accepts_role_token() -> None:
    allowed = frozenset({"1", "2", "3"})
    assert _validate_action(
        {"from": "2", "to": "basket", "type": "drive"}, allowed
    ) == {"from": "2", "to": "basket", "type": "drive"}


def test_validate_action_lowercases_type() -> None:
    """Action type is normalized to lowercase even if Claude uppercases."""
    allowed = frozenset({"1", "2"})
    assert _validate_action(
        {"from": "1", "to": "2", "type": "PASS"}, allowed
    ) == {"from": "1", "to": "2", "type": "pass"}


def test_filter_actions_drops_invalid_keeps_valid() -> None:
    """Mixed list: keep the good entries, drop the bad ones."""
    candidates = [
        {"from": "1", "to": "2", "type": "pass"},
        {"from": "9", "to": "2", "type": "pass"},  # bad from
        {"from": "2", "to": "space-mountain", "type": "cut"},  # bad to
        {"from": "3", "to": "right_wing", "type": "cut"},
    ]
    result = _filter_actions(candidates, ["1", "2", "3"])
    assert result == [
        {"from": "1", "to": "2", "type": "pass"},
        {"from": "3", "to": "right_wing", "type": "cut"},
    ]


def test_filter_actions_handles_non_list() -> None:
    """Non-list inputs never raise."""
    assert _filter_actions(None, ["1"]) == []
    assert _filter_actions({"from": "1"}, ["1"]) == []
    assert _filter_actions("not a list", ["1"]) == []


# ---------------------------------------------------------------------------
# Smoke: module-level wiring isn't broken.
# ---------------------------------------------------------------------------


def test_module_exports_public_callable() -> None:
    assert callable(phase_expander.expand_phase_from_narrative)
