# Public submission checklist

Proposed name: Talk-Flow-Studio
Short description: Captions, motion graphics and pacing for spoken videos.
Category: Productivity
Type: Skills only

Description: Package a spoken creator video into an editable landscape composition with timed kinetic overlays, optional authorized product evidence, subtitles and export checks. Includes nine starter visual forms, cut-to-final transcript mapping, configurable speaker framing and an illustrative demo. Includes dependency diagnosis with official links and copyable commands, guided credential setup, authorized ElevenLabs transcription, cache reuse and strict quota preflight. Requires Python 3.10+, Node.js 22+, FFmpeg and HyperFrames; creative review remains necessary. It does not silently install software or automatically create a bespoke edit from an API key alone.

Functional evidence: a private, user-authorized 10-second ElevenLabs transcription and H.264/AAC landscape subtitle export succeeded. Exported-frame review caught face occlusion that browser checks missed; framing was corrected. No private test video or credential is included in the public bundle. This is a short functional test, not a full-length or cross-platform certification.

Publication route: https://developers.openai.com/plugins/deploy/submission . Public listing requires verified developer identity and portal review/approval before publication. Local installation or a ZIP does not mean public listing.

Test prompt: Use $talking-head-promo to build the included illustrative example into a new directory, run its checks, preview its four beats, and explain how to replace the placeholder with right-framed footage.
Test prompt: Given timestamped speech and a cut ledger, remap cues without presenting partial text as verified transcription.
Test prompt: Reject overlapping scenes and unsafe relative paths; do not overwrite an existing project.

Pending owner input: verified OpenAI publisher organization; public website, support, privacy and terms URLs; chosen redistribution license; final logo and public source/release location.
Also confirm intended country/region availability. Individual verified publishers are supported; a company identity is not mandatory.
Do not submit fake URLs, personal media, private handoff notes or service credentials. Do not claim market-leading quality without comparative evidence.

## Portal test cases

These are reviewer scenarios, not claims that every scenario has been end-to-end tested.

Positive 1: Build the bundled example into an empty folder. Fixture: examples/plan.json. Expected: editable 1280x720 project and valid plan; presenter placeholder explicitly illustrative.
Positive 2: Prepare a user-authorized short speech clip with a valid scoped ElevenLabs key. Fixture: reviewer-owned clip and free account with verified quota. Expected: progress messages, timestamped JSON/SRT; credentials absent from project. Live private 10-second test succeeded; reviewer must use their own authorized fixture.
Positive 3: Repeat prepare on the same successfully transcribed source. Fixture: valid matching cached transcript. Expected: cache reused without another speech upload. Covered by automated test.
Positive 4: Map timestamped segments through chronological cuts. Fixture: inline segments/cuts from studio.test.mjs. Expected: final-timeline windows; truncated text marked for review, not inferred. Covered by automated test.
Positive 5: Compile a plan with speakerOffsetX=160 and captions. Fixture: bundled plan with reviewer-owned footage and generated cues. Expected: configurable video position, readable caption layer, unchanged audio timing; visual and listening review still required. Compiler positioning covered by automated test; actual private corrected frame inspected.

Negative 1: Attempt speech upload with inaccessible quota, unknown extension limit or insufficient reserve. Expected: stop before transcription upload and explain required account settings; no bypass. Covered by quota unit tests.
Negative 2: Supply traversal source paths, overlapping scenes or invalid speaker offset. Expected: plan rejected before project build. Covered by automated tests.
Negative 3: Build into an existing nonempty project or silently retry an uncertain chargeable upload. Expected: preserve files; stop and require explicit retry direction rather than risk duplicate billing. Compiler refusal covered by automated test; inspect retry marker logic for upload scenario.

Release notes: Initial submission candidate. Adds dependency guidance, local encrypted Windows credential setup, scoped ElevenLabs transcription, conservative free-tier quota preflight, transcript reuse, subtitles, nine starter forms, configurable speaker framing, human exported-frame review and verified media metadata. Short functional test and 20 automated tests passed on Windows; no cross-platform certification or competitor superiority claim.

