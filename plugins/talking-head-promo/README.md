# Talk-Flow-Studio

A portable Codex skill plugin for speech-led creator videos: editorial planning, nine kinetic overlay forms, optional product evidence, caption timing and export checks. It is a production starter, not a promise of automatic professional design or better results than every competitor.

## Use

Key permissions: enable “Restrict key”; select Access for Speech to Text and User (account quota lookup), leave other endpoints disabled, then create/save. Enable auto-disable on leak and choose an expiry as appropriate. Account overage settings are separate. API-key page: https://elevenlabs.io/app/developers/api-keys .

First use: [sign in](https://elevenlabs.io/app), [create an API Key](https://elevenlabs.io/app/developers/api-keys) with Speech to Text permission, and enter it in the hidden local setup prompt. [Free-plan details](https://elevenlabs.io/pricing) and [API pricing](https://elevenlabs.io/pricing/api) determine your actual quota. The plugin does not purchase plans, top up balances or change billing settings; existing account billing can apply. Do not send keys through chat. Run `python skills/talking-head-promo/scripts/promo.py onboarding` for the complete guide.

Install the plugin in Codex, then ask: “Use $talking-head-promo to package this spoken video. Preserve the speaker, synchronize the explanation graphics, use these authorized screenshots, and export a verified landscape MP4.”

Provide footage, a brief, optional reference and authorized assets. Requires Python 3.10+, Node.js 22+, FFmpeg and HyperFrames. Run scripts/promo.py doctor on first use: it detects missing dependencies, shows official download links and copyable install commands, and explains the first-render HyperFrames download. It never silently installs system software; Codex asks for confirmation first. The convenience prompt is “帮我安装 Talk-Flow-Studio 依赖”; Codex checks first, installs only confirmed missing items, then verifies again. Run setup for a hidden Windows encrypted credential prompt. The unified prepare/finish workflow supports ElevenLabs word-timed transcription, SRT export, burned-in captions and resumable steps. Audio is uploaded only with authorization and can incur service fees.

See skills/talking-head-promo/references/tools.md for a runnable example and commands. Run `node --test skills/talking-head-promo/scripts/studio.test.mjs` for helper tests.

## Safety and limits

No API keys or private footage are included. The optional speech workflow uploads extracted audio to ElevenLabs with the user's key; rendering downloads the pinned HyperFrames package and loads GSAP from a versioned CDN. Review their licenses before redistributing dependency assets. It does not automatically cut or remove a background; Codex supplies the creative plan. Human review of copy, evidence, subtitle recognition, framing and exported sound is mandatory.

Public-directory publication is not complete. Publisher verification, support/website/legal URLs, distribution licensing and portal review must be resolved before submission. Talk-Flow-Studio is the proposed product name, not a verified publisher identity.

## License

Released under the [MIT License](LICENSE).

