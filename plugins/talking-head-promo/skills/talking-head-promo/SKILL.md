---
name: talking-head-promo
description: Edit a creator's spoken promo or explainer using transcript-timed motion graphics, meaning-driven scene layouts, selective product proof and verified exports. Use for recurring talking-head video packaging or improving an existing edit; plain subtitle-only requests do not need this workflow.
---

# Talking Head Promo

Produce an editable video whose graphics explain the speech and whose timing can be revised from one plan. Support Chinese and English narration. Preserve an existing approved look when iterating. Adapt new footage and content rather than assuming the last video's durations or claims.

## Start with evidence

For speech subtitles and first-use setup, read [automation.md](references/automation.md). Use scripts/promo.py as the unified doctor/setup/prepare/finish entry. On first run, doctor detects Node.js, FFmpeg and ffprobe, gives official download links and copyable Windows commands, and explains that pinned HyperFrames is fetched by npx on first render. Codex asks before installing system software; the helper does not silently install it. If the user says “帮我安装 Talk-Flow-Studio 依赖”, run doctor first, summarize exactly what is missing, ask for confirmation, then use only the official installer and rerun doctor after reopening the terminal. Ask for a credential only when missing, via the user's hidden local setup prompt, never through chat. User-authorized ElevenLabs upload can incur fees. Reuse successful transcription and stop before retrying an uncertain chargeable request. Codex performs creative reference analysis and plan generation between prepare and finish; the helper is not an autonomous editor.

Inspect supplied source footage, sound, script and reference. Probe media with the included tool. Obtain timestamped transcription through available local or user-authorized transcription tools; a script alone does not provide timings. Disclose gaps in inspection. A contact sheet covers visual structure but does not establish sound synchronization.

For a new project, write a short brief recording audience, purpose, output format, target duration, established claims, source paths and desired reference traits. In an established project, resume from existing files and accepted feedback. Use reasonable defaults for routine decisions: landscape canvas for this side-by-side creator style, source voice, a clear portrait area, and versioned projects.

## Editorial decisions

Before animation, identify the hook, emotional pain point, proof and next action. Keep natural pauses where they carry meaning. Remove repeated setup and errors when the user requested cutting; avoid changing the meaning of claims. Read [editorial.md](references/editorial.md) for speech timing, cut maps and reference analysis.

Build a beat plan with an intentional visual form for each idea. Read [design.md](references/design.md) when designing or improving scenes. Variety must follow the information: a process builds, a choice branches, a claim gains evidence, a conversation has turns. Allow occasional presenter-only beats. Change a held scene when the narration introduces a new idea; arbitrary constant motion does not substitute for explanation.

Use one primary focal action at a time. Establish fixed columns, safe margins and typographic roles; then animate within them. Measure text and protect the face before adding decoration. Match the user's reference techniques, not its literal content.

## Build and reuse

Read [tools.md](references/tools.md) before using included scripts. All paths in plans are project-relative. Store final-timeline seconds in plan.json. Cuts use an explicit source-to-final mapping; run the map helper before reusing transcript times.

Use the HyperFrames entry skill and relevant domain instructions when available. The included scaffold and runtime are a portable starting point with title, process, grid, split, quote, chat, proof, stat and outro patterns. Adapt their choreography to actual speech; the starter is not a finished bespoke edit. For new named effects, search the HyperFrames registry before authoring them.

Keep video, screenshots, fonts and audio in the project, outside the installed plugin. Freeze remote assets locally using allowed media workflows. The installed package is code and examples only; it has no API key and no private creator footage. The GSAP script used by the scaffold is fetched from a versioned CDN at compile time and inlined by HyperFrames; rendering requires network on first use.

If cutting, reframing or audio mixing is required, load the owning HyperFrames/media instructions. Preserve source files; render new outputs under new names. The scaffold expects a prepared, continuous video. The unified promo.py helper adds transcription and subtitles; trimming remains an agent-owned separate step.

## Review and deliver

Run plan validation, HyperFrames check and visual inspection of both entrance frames and settled frames. Read [review.md](references/review.md) for the rubric and exact deliverable checks. Inspect the opening, densest frame, proof reveal, conversation transition and ending at minimum. State what was and was not tested.

If the user requested a preview, deliver a live verified preview and wait for steering. If they requested an export or already approved the current edit, render it without requesting approval again. Verify duration, video and audio streams, dimensions and frame rate. Deliver a working local file link, not a temporary preview URL as the only backup.

Persist a project handoff with plan, transcript, cut map, asset provenance, output path and accepted feedback. Include no secrets in logs or handoffs. Do not upload footage to transcription, hosting or public repositories without task authorization.

## Quality claims

Use measurable improvements: timing error, readable line length, face clearance, source integrity, layout findings, and actual review feedback. Do not claim superiority to competing products without comparable clips and results. Document limitations rather than promising automatic “viral” or identical-reference results.

