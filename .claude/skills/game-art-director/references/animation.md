# Animation — honest frames, not motion

Image models generate FRAMES. Two real routes in this project:

1. **In-game character motion is already solved in 3D** — the People
   system (measured procedural gait/idle/work on the rigged bodies) and
   the hero stage. If the request is "make the archer walk in the game" or
   "commander idle animation", that is the `hero3d` skill, not image
   generation. Do not build sprite sheets for things the rig already does.
2. **Image frame sets** serve 2D needs: an effect flipbook (the chest-open
   4-frame sequence is shipped precedent), a marketing GIF, or input to an
   image-to-video tool.

## Frame-set templates (pose deltas per frame)

- idle breathe (4): chest rise 1 → settle → shoulders drop 1 → return
- walk cycle (8): contact L → down → pass → up → contact R → down → pass → up
- attack swing (6): anticipation ×2 (wind back, weight loading) → strike ×1
  (full extension) → follow-through ×2 (blade past, weight forward) →
  recover ×1
- death (5): hit recoil → knees give → fall through → ground contact → settle
- build-hammer (4): raise → apex pause → strike → rebound
- collect-sparkle (4): bloom small → full → scatter on a size ramp → fade
- gate open (5): bar lifts → first swing → half → wide → settled open

## Consistency armour (every frame prompt, no exceptions)

Each frame repeats the FULL character/object description + the master
style block, then locks: *"same character, same outfit, same lighting,
same camera, only the pose changes as follows:"* + that frame's pose
delta. Camera lock stated outright: identical angle, distance and light
in all frames; plain chroma-flat background (the magenta-key language)
for cutout.

## Game-feel notes

- Anticipation frames are LONGER in count than the strike (2:1) — snappy
  reads come from a held wind-up and a one-frame hit.
- Overshoot on recovers (the blade travels past the rest pose by a few
  degrees, then settles) or the motion reads mechanical.
- Counters/collect effects: roll-then-land, never a linear fade.

## Output format

A numbered list, one complete prompt per frame (frames may be shorter
than 200 words but must each carry the full consistency armour), then
one line on assembly: lay frames left-to-right into a sprite sheet at
the group size, transparent background from the key. Alternative route:
generate frame 1 as a still, hand it to an image-to-video tool with the
motion described in one sentence, and mute any generated audio.
