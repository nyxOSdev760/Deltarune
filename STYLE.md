# Art style: Deltarune-style pixel art

## Resolution
- Draw at a low native resolution (about 160x284 for 9:16), then upscale with nearest-neighbor only. No smoothing, no anti-aliasing, no blur. Every pixel must stay square and crisp.
- Character sprites are small and chunky, roughly 20-40 px tall at native resolution. Close-up shots can use larger sprites with the same rules.

## Sprites
- Flat shading with 2-3 tones per color area: base, one shadow, one highlight. No gradients inside sprites.
- Bold, simple shapes. Heads are large relative to bodies. Faces use a few dots and lines for eyes, mouth and brows.
- Outlines are 1 px and dark, tinted toward the sprite's own color (dark navy, dark brown), not pure black. Some sprites have a light outline against dark backgrounds.
- Limited palette per character, with 1-2 accent colors that stand out (a pink cheek, a yellow badge, a green sweater).
- Idle animations use 2-4 frames. Walk cycles use 4 frames. Expressions swap whole face frames instead of morphing.

## Backgrounds
- Tile-based rooms with repeated patterns (carpet diamonds, wood panels, doors with a single bright knob).
- Warm interiors: orange, brown, tan, with a darker band for walls and a lighter band for floor.
- Dark or magical scenes: deep purple, blue and violet, with a soft vertical light beam in lighter blue and sparse single-pixel sparkles.
- Backgrounds are simpler and lower contrast than characters so the sprites pop.

## Effects
- Fire: 3-tone flame sprites (white-yellow core, orange middle, red edge) that flicker between 2-3 frames, placed in a loop along the floor and rising.
- Screen shake: 1-2 px jitter on frames, no easing.
- Red tint for anger: a flat overlay at about 20-30% opacity, fading in over several frames.
- Text uses a clean pixel font with a white or yellow fill and a dark border.

## Motion
- Low frame rate feel: animate on 2s or 3s (8-12 fps), and hold key poses for a beat so jokes read.
- Snappy cuts, hard cuts for punchlines, and a loopable last frame.

## Output
- 9:16 vertical, 1080x1920, MP4 at 24-30 fps (hold frames to keep the choppy pixel timing).
- Leave safe margins (about 10%) on top and bottom for platform UI. Put any watermark at the corner, small.
