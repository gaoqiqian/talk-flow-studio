# Design decisions

## Frame geometry

For 1280×720, start with 40–56px outer margins, a left information region around 500–560px wide, and a protected speaker area on the right. Adapt to the actual face and gestures. The included starter assumes a right-side speaker; if the footage is centered or vertical, use a separate portrait region or another layout. Do not cover or stretch the face to fit the starter.

Use consistent left edges, baselines, card padding and radii. Example typographic roles: hero 42–56px, scene heading 30–40px, body 18–24px, metadata 12–15px. Check the intended phone viewing scale as well as full resolution. Pair a dark ink color with a pale surface and one strong accent; use secondary color only for meaning.

Keep headline lines short, body line-height near 1.5–1.65, and Chinese headlines near 1.15–1.3. If text exceeds its slot, shorten it or change the layout rather than shrinking every font. Use actual measured frames to decide. Maintain at least 4.5:1 body contrast and 3:1 large-text contrast.

## Visual grammar

| Idea | Form | Useful choreography |
| --- | --- | --- |
| Key sentence | Title or quote | Line reveal, emphasis, clean hold |
| Steps | Process or grid | Progressive arrival, active step, completion |
| Two choices | Split | Shared premise, branch, one side highlighted |
| Coaching | Chat | Context arrives, teacher turn, student turn, follow-up |
| Product evidence | Proof | Labeled real capture, readable crop, related callout |
| Credibility number | Stat | Number reveal and clear label; never fake data |
| Final action | Outro | One action and a readable URL |

Rotate forms according to narrative structure. A screen of empty space needs meaningful information, a different framing, or a presenter-only moment. Adding unrelated decorative cards is not a solution.

## Motion craft

Use controlled direction and easing. Favor a confident settle; reserve strong overshoot for a deliberately playful moment. Give entering and exiting objects a reason to move in their direction. Pair small emphasis with major motion sparingly. Every animation must be deterministic and seek-safe; no page-load clocks, infinite repeats or random state.

For processes, make the active step visible on its spoken cue. For branches, connect the premise and endpoints. For chat, map thinking and speaking states to actual turns or label them as illustration. A waveform made from generic oscillation is illustrative, not an audio measurement.

## Product proof

Use real captured content only when authorized. Keep screenshots proportional and label them accurately. For actual operation recordings, reveal the action and result, not a tiny full page. Cropping, masks and selection outlines may be intentional, but all explanatory text must remain legible. Never claim a static screenshot is an interactive recording.
