# Portable tools

For automated speech transcription, encrypted key setup and prepare/finish orchestration, use automation.md and scripts/promo.py. Requirements for that workflow are Python 3.10+ and Node.js 22+. The lower-level studio.mjs compiler below still does not transcribe by itself.

Requires Node.js 20+; FFmpeg/ffprobe and network access for the pinned HyperFrames CLI and GSAP CDN. No account or transcription service is bundled. Supply a timestamped transcript or use an available transcription tool with user authorization. Never put service keys in project files.

Run `node scripts/studio.mjs check examples/plan.json` from this skill directory.
Run `node scripts/studio.mjs build examples/plan.json /absolute/new/project` to generate an editable project. Output must be new or empty. On Windows quote paths containing spaces.
From the generated project run `npm run check`, `npm run preview`, and `npm run render`.
Verify an export with `node scripts/studio.mjs verify /absolute/video.mp4 /absolute/project/plan.json`.
Run tests with `node --test scripts/studio.test.mjs`.

## Plan contract

Canvas: width 1280, height 720, fps 24/30/60, positive duration in seconds. Optional source is a project-relative prepared continuous video path, forward slashes only. The compiler does not cut footage or transcribe automatically. Prepare the edit separately; keep its cut ledger. Video position assumes the speaker is on the right; inspect and adapt CSS before using centered footage.

Scenes: unique lowercase id; pattern title/process/grid/split/quote/chat/proof/stat/outro; start and end in final edit seconds; title; optional kicker/body/items. Each item has text and absolute final-timeline at. Scenes cannot overlap. Split takes exactly two items. Chat must declare illustration:true unless replaced with actual evidence by custom code. Proof takes asset and assetLabel; use actual authorized evidence or label a mockup honestly.

Captions: [{start,end,text}], chronological non-overlapping final-timeline intervals. Do not fabricate transcription.
Speaker framing: optional speakerOffsetX, a finite pixel offset from -320 to 320. The compiler applies it to the video only, preserving source audio and timing. Choose it from inspected footage, never reuse 160 universally. Shifting can expose background or crop gestures; inspect both edges and the face at multiple times. Omission with a source emits a framing warning. This is not face detection or an automatic clearance guarantee.
Theme: optional ink/paper/accent six-digit hex colors.

`node scripts/studio.mjs map transcript.json cuts.json` returns final windows and remapped segments. Cuts use sourceStart/sourceEnd. Segments intersecting a cut are flagged needsTextReview: the helper does NOT infer which words survived. Manually recheck or transcribe the final edit.

These checks detect timing/schema/media errors, not visual beauty, truth of claims, caption accuracy or intelligibility. Review rendered frames and listen to the exported audio. Timed items use one deterministic paused timeline. For long or crowded material, customize the design rather than cramming the starter.
