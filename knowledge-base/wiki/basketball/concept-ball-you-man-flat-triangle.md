---
type: concept
level: beginner
positions: [PG, SG, SF, PF, C]
tags: [defense, help-side, positioning, man-to-man, off-ball-defense]
source_count: 1
last_updated: 2026-04-26
# Cross-ref edge — concept-as-rule schema. See backend/spec/crossref-anatomy-chain.md §4.5
rule_family: positioning
domain: off-ball-defense
geometry:
  shape: flat-triangle
  vertices: [ball, defender, assignment]
  defender_anchor:
    distance_ratio_from_ball: 0.667
    perpendicular_offset: one-step
vision_constraint:
  mode: peripheral
  simultaneous_targets: [ball, assignment]
  head_movement: forbidden
motion_constraint:
  slide_triggers: [pass, dribble]
  continuity: continuous
  invariant: distance_ratio_from_ball
stance:
  weight_foot: ball-side
  hips_orientation: open-to-passing-lane
failure_modes:
  - id: ball-fixation
    category: vision
    correction: peripheral-vision
    exploit: backdoor-cut
  - id: assignment-fixation
    category: vision
    correction: peripheral-vision
    exploit: drive-past
  - id: half-distance-positioning
    category: geometry
    correction: ratio-2-3
    exploit: [no-intercept, no-deny]
  - id: static-defender
    category: motion
    correction: continuous-slide
    exploit: triangle-collapse
  - id: head-movement
    category: vision
    correction: peripheral-vision
    exploit: rotation-telegraphed
trained_by_drills:
  - id: drill-help-side-drill
    emphasis: primary
  - id: drill-interception-stance
    emphasis: primary
  - id: drill-close-the-gap-stance
    emphasis: secondary
  - id: drill-dual-help-drill
    emphasis: secondary
extends:
  - id: man-to-man-defense
prerequisite_for:
  - id: weak-side-help-defense
  - id: closing-the-gap
---

# Ball-You-Man / Flat Triangle

## Summary
The ball-you-man principle is the foundational positioning rule for off-ball defenders in man-to-man defense. It states that every defender must be able to see both the ball and their assigned player simultaneously, without moving their head. The **flat triangle** is the geometric tool that achieves this: the defender positions one step off the direct line between ball and assignment, at two-thirds of the distance from the ball.

This principle is taught explicitly in youth basketball as the cornerstone of help-side man-to-man defense [S15, pp.274-275].

## When to Use
- Any time the ball is passed away from a defender's assignment (defender becomes a help-side defender)
- Applies to all off-ball defenders — whether one pass, two passes, or three passes away from the ball
- Must be maintained continuously as the ball moves via dribble or pass

## Key Principles
1. **Ball-You-Man**: *Ball* is where the basketball is. *Man* is where your assignment is. *You* must see both simultaneously. "Ball you must see. Man you must see." [S15, p.275]
2. **Flat triangle positioning**: Draw a line from ball to assignment. Place the defender one step off that line, two-thirds of the distance from the ball toward the assignment.
3. **Geometric construction** of the flat triangle:
   - Step 1: Draw a line between the ball and your assignment
   - Step 2: Place yourself two-thirds of that distance from the ball
   - Step 3: Step one step off the ball-to-assignment line
   - Result: a flat triangle with ball, you, and assignment as the three points
4. **Peripheral vision is mandatory**: The defender must never look at only the ball or only the assignment — both must be seen simultaneously without head movement.
5. **The flat triangle must adjust constantly** as the ball moves via dribble or pass — the defender slides to maintain the 2/3-1/3 ratio at all times.
6. **Interception stance within the flat triangle**: The defender should be in fence-slide/interception stance with pressure on the foot nearest the ball — this enables both pass interceptions AND quick movement to cover the assignment.

## Player Responsibilities
- **All positions**: Immediately jump toward the ball when a pass leaves your assignment, sliding into the flat triangle before the receiver catches it.

## Variations
### One Pass Away
Defender is in the flat triangle with interception stance — must be able to deflect a pass back to their assignment and deny the assignment moving back to the ball.

### Two or More Passes Away
Defender can sag further into the paint (help-the-helper position), but the flat triangle principle still governs — just at a wider angle.

### Ball Dribbled Along the Sideline
As the ball moves via dribble, the defender slides continuously to maintain the flat triangle — the 2/3 distance from ball reference point moves with the ball.

## Common Mistakes
1. **Watching only the ball** → assignment cuts backdoor for an easy layup; correct by using peripheral vision
2. **Watching only the assignment** → miss early help cues when the ball drives; correct by keeping ball in peripheral view
3. **Positioning at half distance** between ball and man → too far from the ball to intercept; too far from the man to deny; correct with the precise 2/3–1/3 ratio
4. **Not sliding as the ball moves** → flat triangle breaks down, leaving gaps; correct by moving on every pass and dribble
5. **Moving the head to see both** → telegraphs defensive rotations and slows reaction; correct by developing true peripheral vision

## Related Concepts
- [[drill-help-side-drill]] — primary practice drill for ball-you-man positioning
- [[drill-interception-stance]] — the stance used within the flat triangle
- [[drill-close-the-gap-stance]] — how to respond when the ball drives toward your assignment
- [[weak-side-help-defense]] — related system using similar shadow/tilt principles
- [[drill-dual-help-drill]] — advanced application helping on both lob passes and drives

## Sources
- [S15, pp.274-275] — Drill #133 (Help-Side Drill) teaching points on Flat Triangle and Ball-You-Man
