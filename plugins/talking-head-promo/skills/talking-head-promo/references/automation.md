# Unified speech workflow

## First-use message

Default quota protection is strict free-account mode: before each fresh upload query the subscription endpoint. Require tier=free, max_credit_limit_extension=0, complete remaining-credit data and sufficient conservative duration-based reserve. Missing account read permission, unknown settings, paid tier, exhausted/low quota or query errors stop before the chargeable request. Ask users to grant subscription/account read permission in addition to STT. Existing transcripts still work offline without a quota query. The reserve is not a verified API entitlement or exact price; the plugin does not change provider billing settings. API dollar billing, other clients sharing quota and provider changes mean a local precheck cannot guarantee zero charges. Do not advertise an absolute no-charge promise or silently bypass the guard. Require provider-side overage disabled and explain the remaining limitation. Official schema: https://elevenlabs.io/docs/api-reference/user/subscription/get .

Show links as clickable Markdown when helping a user. Run `python scripts/promo.py onboarding` for structured onboarding data; setup and a missing credential also display it. Do not require users to run other technical commands manually when Codex can orchestrate them.

> 首次使用，请[注册或登录 ElevenLabs](https://elevenlabs.io/app)，然后[创建 API Key](https://elevenlabs.io/app/developers/api-keys)。开启“限制密钥”，将“语音转文本 / Speech to Text”和“用户 / User”都设为“访问 / Access”，其余保持“无权限”。建议开启“泄露后自动禁用”并设置有效期，最后点击“创建密钥”或“保存更改”。在本机隐藏提示中安全输入即可。配置一次后，提交口播和参考即可开始。依赖缺失时会引导安装。

The actual UI shown by the user labels the subscription-reading scope “用户 / User” with Access, not a separate “Subscription Read” selector. Explain the exact two selections, not an unspecified account permission. If UI changes, inspect its current labels; never instruct enabling all scopes. Permission changes do not establish that a 401 is fixed, and they do not disable usage-based billing.
>
> [免费套餐与积分](https://elevenlabs.io/pricing) · [API 转写价格](https://elevenlabs.io/pricing/api)。免费额度和可用转写时长以账号显示为准。插件不会购买套餐、充值或修改计费设置；账户已有付费/超额计费可能适用。请勿将密钥发送到聊天或公开分享。

Pricing checked 2026-09-18: general pricing lists Free 10,000 monthly credits and approximately 330 credits/minute for STT (arithmetic estimate ~30 minutes if that rate applies and all credits are available). The dedicated STT page lists Free UI 12 minutes; API pricing states dollar-based billing. These are not interchangeable entitlements. Never advertise a guaranteed 30 free API minutes. Recheck official pricing before answering later pricing questions. Example clips consume the uploaded audio's duration, not necessarily the final shortened video's duration. Cached transcripts need no further STT calls; fresh uploads may consume quota.

Runtime clarification: use Node.js 22+ for HyperFrames. Audio extraction now writes a unique temporary FLAC and promotes it only after success; interrupted temporary files do not count as completed audio. A per-project lock prevents concurrent uploads. After a hard crash, remove the lock only after verifying no workflow process is running. Saving a credential configures it; a live request is still needed to verify service permissions and billing.

Requires Python 3.10+, Node.js 22+, FFmpeg/ffprobe. `python scripts/promo.py doctor` checks available binaries and gives install guidance; installing system packages remains a separate authorized operation. No Python packages needed.

Windows first use: user opens their own terminal and runs `python scripts/promo.py setup`. Hidden secure prompt saves current-user DPAPI ciphertext under LocalAppData/TalkingHeadPromo, outside plugin/projects. Do not ask users to paste keys into chat or place keys in command arguments. Other platforms use a secret-manager-provided ELEVENLABS_API_KEY environment variable. Credential validation occurs on the first API call; merely saving a key does not prove it works. Never reuse a key leaked into a chat in public examples.

When a user has authorized ElevenLabs upload/billing, Codex runs:
`python scripts/promo.py prepare --video /absolute/prepared-video.mp4 --project /absolute/new-work --allow-upload`

This extracts mono FLAC, requests Scribe v2 word timestamps, saves raw transcript, captions.json and subtitles.srt. Use the actual prepared final edit, not uncut footage, to avoid timing drift. Saved source hash and model prevent reusing another video's transcript. Existing successful raw transcription is reused even if the previous caption step failed. An uncertain request is not resent automatically; explain possible repeated billing and only pass --retry-upload after explicit retry authorization. Never fabricate progress percentages or promise a fixed waiting time. Heartbeats show elapsed time, rendering exposes renderer progress. Interrupted audio extraction may leave an incomplete FLAC: inspect it and rename it before retrying extraction; do not silently overwrite source media.

After transcription, the Codex agent inspects footage/reference and creates project/plan.json with source and evidence files relative to project, preserving the intended design. This creative step is performed by Codex, not automatically generated by the Python helper. Use captions to anchor motion cues; review recognition errors and punctuation. Long single words need manual splitting, and multilingual line wrapping needs visual inspection.

`python scripts/promo.py finish --project /absolute/work --render` merges captions into a new composition, checks it, renders and probes the output. A failed render can resume; changed plans require a new version rather than overwriting manual edits. A present export is verified, not blindly rerendered. Only deliver after listening to audio and reviewing frames. Do not promise unattended creative quality or infer that metadata checks validate subtitle accuracy.

Natural language entry: “这是我的口播，按这个参考风格剪，导出横屏视频。” Codex orchestrates these commands. First-use missing credential or missing authorization is the only necessary pause; keep ordinary config and commands away from users.
