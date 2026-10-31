# Audio assets

| File | Used for | Source |
|---|---|---|
| `music_playful_chiptune.wav` | Game music (0:00–0:04) and the loop tail | Generated with vidIQ AI music (royalty-free, original). Prompt: playful mischievous 8-bit chiptune, bouncy RPG town theme, 125 BPM, instrumental. 48 s. |
| `music_rage_chiptune.wav` | Pip's rage and the room fire (0:11.5–0:15.5) | Generated with vidIQ AI music (royalty-free, original). Prompt: intense chaotic 8-bit chiptune boss battle, 165 BPM, instrumental. 73 s; cued from 9.0 s. |

Small sound effects (pen scribbles, "ez" talk blips, record scratch, crickets, win jingle,
boom, fire crackle) are still synthesized in `pixelshort/audio.py`.
Cue points live at the bottom of `scenes/siblings.py` (`PLAYFUL_IN`, `RAGE_IN`).
