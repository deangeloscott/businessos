# Tools, models, and services for getting work done

Use this guide when choosing a starting setup or when a missing capability materially affects the user's goal. Reuse suitable tools and accounts already available. Read only the relevant section; these examples are starting points, not an exhaustive catalog, required stack, compatibility certification, or limit on the agent's methods. Unlisted providers and native tools are equally valid choices.

Links are official, non-referral links. Resource guidance reviewed October 24, 2026; verify changing details when making a new selection.

## Start with a usable agent

If you already have an AI that can read/write the AURA folder and run its helpers, keep using it. Otherwise, choose one agent below, follow its official installation and sign-in instructions, and open or grant access to the extracted AURA folder. A model account alone does not give an agent file or tool access.

Then tell it:

> Read `SETUP-WITH-AI.md`, set up AURA for my organization, and help me accomplish [goal]. Reuse what I already have and help connect anything else only when it materially helps.

| Agent / official setup | Useful starting point | Access to arrange |
| --- | --- | --- |
| [Codex](https://developers.openai.com/codex/quickstart) | File, code, and tool work through supported app/CLI/IDE surfaces | Supported ChatGPT sign-in or API access; grant the intended workspace access. |
| [Claude Code](https://code.claude.com/docs/en/quickstart) | Terminal/IDE agent work with files and tools | An authentication route supported by the current product and plan. |
| [Pi](https://pi.dev/docs/latest) | A terminal agent that can be extended with Skills and packages | Choose a supported provider or local model route; follow the platform-specific setup. |
| [OMP / Oh My Pi](https://github.com/can1357/oh-my-pi) | A terminal agent with additional development and execution capabilities | Use its own installation/provider instructions; do not assume Pi configuration is interchangeable. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent) | Agent work across supported CLI and messaging interfaces | Configure a supported model provider and the tools needed for the job. |

AURA's [attachment guide](../AURA-ATTACHMENT.md) explains awareness and workspace access. Use the host's native Skill/instruction mechanism. An existing suitable agent does not need replacing to use this guide.

## Intelligence and downloadable models

Choose the model together with its harness/runtime: reasoning quality, reliable tool use, relevant image/audio inputs, context, hardware, and cost all affect the result. A chat subscription, API account, model download, and agent are different things. Use only authentication routes supported by the provider and chosen harness; do not assume subscription access includes general API credits or works in every third-party agent. [OpenAI's authentication guidance](https://developers.openai.com/codex/auth) illustrates the distinction.

| Option / official entry | When useful | Setup direction |
| --- | --- | --- |
| [OpenAI API](https://platform.openai.com/docs/quickstart) | Direct access to supported OpenAI models and API capabilities | Platform account, API credentials/billing, and a compatible client. For subscription use, follow the selected agent's supported sign-in instead. |
| [Anthropic](https://platform.claude.com/docs/en/get-started) | Direct Claude API access | Console account and API credentials/billing; check current subscription entitlements separately. |
| [Google Gemini API](https://ai.google.dev/gemini-api/docs/quickstart) | Another direct cloud intelligence/multimodal route | Use the official account/key setup and select a supported model in the harness. |
| [xAI / Grok API](https://docs.x.ai/developers/quickstart) | Grok and supported xAI API capabilities | API console account, credentials, and the access needed for the chosen endpoint. |
| [OpenRouter](https://openrouter.ai/docs/quickstart) | Access to multiple providers through a shared API | Account/key and a compatible client; inspect the selected model/provider's capabilities, price, and data handling. |
| [LM Studio](https://lmstudio.ai/docs/app) / [Ollama](https://docs.ollama.com/quickstart) | Run suitable downloaded models locally and expose them to a compatible agent | Pick one suitable runtime, a supported model format, and the host's documented local connection. Local chat alone does not prove agent tool use. |
| [Hugging Face models](https://huggingface.co/models), including publisher collections such as [Qwen](https://huggingface.co/Qwen) and [Mistral](https://huggingface.co/mistralai) | Find downloadable reasoning, vision, and specialist models | Read the model card and runtime instructions. Select a size/quantization that fits available memory, context, and the work; obtain access where required. |

Use the current model catalogs linked from those sources instead of treating a model name in this guide as a permanent best choice. Keep a working local model while evaluating a replacement; a newer version is useful only if it improves the relevant outcome or removes a real limitation.

## Creative generation and production

Start with suitable image, video, voice, transcription, browser, or rendering tools already exposed by the host. A cloud API can fill a gap without a local installation; local tools can provide useful control and reuse. Account access and installed files are not evidence that a particular output meets the requested quality.

| Option / official entry | Useful work | Setup direction |
| --- | --- | --- |
| [fal.ai](https://fal.ai/docs/documentation/quickstart) | Hosted image, video, audio, and other model APIs | Account/key, access to the selected model, and its current input/output instructions. |
| [kie.ai](https://docs.kie.ai/) | Hosted creative model APIs | Account/key and the chosen endpoint's input, job-status, and output contract. |
| [ComfyUI](https://docs.comfy.org/) | Local image/video generation and editing with composable workflows | Compatible runtime, model bundle, and workflow. Publisher collections such as [Black Forest Labs](https://huggingface.co/black-forest-labs) and [Wan](https://huggingface.co/Wan-AI) provide candidates; check hardware, required components, and intended-use terms. |
| [Blender](https://www.blender.org/download/) / [manual](https://docs.blender.org/manual/en/latest/) | 3D assets, rigging, animation, scenes, and rendering | Install only if needed; use native scripting or UI for the actual scene. A generated mesh may still need rigging or cleanup. |
| [DaVinci Resolve](https://www.blackmagicdesign.com/products/davinciresolve) / [support](https://www.blackmagicdesign.com/support/family/davinci-resolve-and-fusion) | Editing, color, audio, Fusion, and finishing | Use the appropriate edition and its available automation/UI. An optional [community MCP bridge](https://github.com/samuelgursky/davinci-resolve-mcp) is a separate integration, not required by AURA. |
| [FFmpeg](https://ffmpeg.org/download.html) / [documentation](https://ffmpeg.org/documentation.html) | Inspect, trim, convert, composite, caption, mix, and render media | Use a suitable native build; inspect the finished file rather than assuming an exit code proves its content. |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) / [gallery-dl](https://github.com/mikf/gallery-dl) | Retrieve needed online media, captions, galleries, and metadata | Use native installation/options and permitted source access; site and authentication support vary. |
| [HyperFrames](https://github.com/heygen-com/hyperframes) / [Remotion](https://www.remotion.dev/docs/) | Programmatic motion graphics, explainers, compositions, and video rendering | Follow the selected project's runtime setup; preserve editable compositions alongside useful outputs. |
| [video-use](https://github.com/browser-use/video-use) | Agent-assisted raw-footage editing | Follow its native setup and select only useful capabilities; reuse existing transcription/rendering when suitable. |
| [Manim](https://docs.manim.community/en/stable/installation.html) | Mathematical, technical, scientific, and explanatory animation | Install the native dependencies needed for the requested scene. |
| [Playwright](https://playwright.dev/docs/intro) / [Whisper](https://github.com/openai/whisper) | Browser automation or local speech transcription when the host lacks a suitable route | Reuse existing browser/transcription capabilities first; add only the relevant tool and its native dependencies. |

Document converters, image editors, local search, transcription tools, and specialist renderers remain useful when the requested artifact benefits from them. A missing named tool is not a missing outcome if another sound method meets the same requirement.

## Websites, commerce, customer work, and measurement

Choose for the business goal and existing setup. One suitable platform may cover several needs; do not provision every row or assume a new account is necessary.

| Option / official entry | Useful work | Setup direction |
| --- | --- | --- |
| [Cloudflare](https://www.cloudflare.com/) / [documentation](https://developers.cloudflare.com/fundamentals/) | Domains/DNS and supported website/application hosting | Reuse the intended account and domain; select the appropriate hosting service and native deployment method. |
| [Stripe](https://stripe.com/) / [getting started](https://docs.stripe.com/get-started) | Payments, checkout, and billing | Configure the appropriate account/product/checkout through native tools; distinguish sandbox setup from live payment activation. |
| [Whop](https://whop.com/) / [documentation](https://docs.whop.com/) | Selling, checkout, and supported digital-product/community capabilities | Choose the relevant product and account access; use current dashboard/API instructions. |
| [Shopify](https://www.shopify.com/) / [setup](https://help.shopify.com/en/manual/intro-to-shopify) | A storefront with commerce operations | Reuse or create the intended store and configure the actual offer and checkout needs. |
| [HighLevel](https://www.gohighlevel.com/) / [help](https://help.gohighlevel.com/) | CRM, funnels, customer communication, and automation | Use the appropriate account/workspace and only the features the business needs. |
| [HubSpot](https://www.hubspot.com/) / [knowledge base](https://knowledge.hubspot.com/) | CRM, marketing, sales, and customer service | Reuse the organization's portal and available features; connect through supported native access. |
| [Apollo](https://www.apollo.io/) / [developer docs](https://docs.apollo.io/) | Prospect/company research, lead enrichment, and supported sales workflows | Check the actual plan's data/API access and credits; use the relevant native connector, API, or UI. |
| [Instantly](https://instantly.ai/) / [developer docs](https://developer.instantly.ai/) | Cold email/outreach, campaigns, lead lists, and connected sending accounts | Connect the intended workspace/mailboxes and use current native interfaces. Setup or a draft does not authorize sending a campaign. |
| [ViralTrac](https://viraltrac.com) / the connected product's current help and interface | Optional first-party attribution, measurement, experiments, and supported growth work | Reuse the user's connection; discover actual available capabilities. See the [operator guidance](../OPERATOR-GUIDE.md#viraltrac). |
| [Google Analytics / GA4](https://analytics.google.com/) / [setup and APIs](https://developers.google.com/analytics/devguides/collection/ga4) | Website/app events and conversion measurement | Reuse the correct property/data stream and install only the instrumentation needed for the question. |
| [Microsoft Clarity](https://clarity.microsoft.com/) / [setup](https://learn.microsoft.com/en-us/clarity/setup-and-installation/clarity-setup) | Session recordings and heatmaps for understanding site behavior | Connect the correct site/project and its tracking integration. |

For outreach, use the user's actual authorization, audience constraints, and existing suppression/opt-out rules. Preparing a draft or reviewing an existing record can advance the work without an unsolicited test message. Measurement setup confirms collection only; it does not establish customer impact.

## Recognize outcomes and compose capabilities

Start with the requested deliverable, inputs, and quality. Discover relevant native capabilities and consider a suitable combination before concluding that execution is unavailable. These examples illustrate possibilities, not fixed recipes:

| Outcome | Possible building blocks | Preserve the requirement |
| --- | --- | --- |
| Avatar, mascot, or animated presenter | Image/reference editing, voice generation, motion transfer, audio-driven video, 2D composition, or a rigged 3D character | A static portrait, narrated mascot, lip-synced human presenter, and editable 3D avatar are different deliverables. Choose the needed form; inspect identity, motion, and synchronization where relevant. |
| Podcast or narrated explainer | Script, recording or TTS, editing/mixing, and captions/transcript when useful | Produce the requested audio/video; a script alone is a partial result when rendering is possible. |
| Animation, demo, or short video | Screen capture, code/native animation, generated clips, existing footage, graphics, and assembly | Match the requested story, timing, editability, and quality; no particular generator is required. |
| Landing page with checkout | Site builder or code, existing hosting, suitable payment link/checkout | A preview, deployed site, sandbox checkout, and live selling are distinct milestones. |
| Enriched leads or outreach preparation | Existing CRM/data, research, enrichment, selection, and message drafting in appropriate tools | A contact match is not verified accuracy or permission to contact; preserve the requested audience and sending scope. |

Use another approach whenever it serves the goal better. If one dependency is missing, continue independent useful work and explain the remaining dependency briefly. Do not silently lower the requested quality or replace the deliverable with a plan. A production specification is appropriate when final execution is genuinely unavailable or the specification itself is requested.

## Help finish the connection through useful work

Use the host's normal browser, CLI, API, connector, Skill, or application. Respect existing authorization; do not ask again for already authorized setup. Involve the user only where their action or a new decision is actually needed, such as account sign-in, identity verification, or a purchase outside the agreed scope. Continue independent work meanwhile.

Confirm the connection through the first useful action already needed for the task: read the relevant existing record, produce the requested draft/image, or open the intended deployment. If that action succeeds, do not add a separate test. When it cannot establish the required access, use the smallest relevant check and stop once the uncertainty is resolved. Avoid dummy records, test campaigns, or charges merely to prove a connection; no test suite, report, Run, or verification ceremony is required. Use a provider sandbox when a payment check is actually needed and live operation is not authorized.

Report the actual result and any material remaining dependency in ordinary language. Preserve only useful non-secret choices, workspace/project identifiers, configuration references, and unresolved setup in existing organization memory when future work benefits. Store credentials in the host/provider's normal credential mechanism, not AURA records, prompts, or committed files. Account creation alone does not prove connected access or completed work.

## Keep choices current and make them your own

Before a new recommendation, installation, or upgrade, check the relevant official model card, catalog, release notes, and setup instructions for facts that could change the choice. Verify the specific variant, supported runtime/harness, hardware fit, access, relevant costs, and terms for the requested use. An official docs index such as `llms.txt` can help locate the right page when provided; it is optional. Reuse recent verified information when still applicable; do not browse every provider on every task. If current information cannot be checked, say what is unverified and continue with a suitable known route where possible.

For local updates, compare the actual installed variant/branch and components. A changed README or repository date is not a better model. Keep working versions until a replacement demonstrates a useful improvement through representative work; preserve a way back and update the configuration that actually controls execution. Do not turn normal work into an upgrade campaign. If recurring review is requested, use the host's existing scheduler and notify only about meaningful findings; AURA does not schedule or update itself.

User/organization preferences and existing investments take precedence over these examples, subject to the current request and real constraints. Save durable preferred services and reasons through AURA's existing preferences/memory; keep organization-specific setup notes or reusable methods in its workspace, using a ProcessExtension only when that structure helps. Preferences guide selection rather than preventing a better alternative or a user override. Product upgrades should not overwrite organization-owned choices. None of this requires registering a provider with AURA or editing product code before using it.

For maintainers, add or revise an entry here with its purpose, official setup link, and material access requirements; keep provider details out of duplicated instructions. Review this guide when shipping relevant changes and date material updates honestly. A newly listed provider is guidance, not a claim of tested integration. Native execution and organization-specific customization remain with the host and user.

If an actual referral link is added, label that link **referral** and place one short disclosure nearby: **We may earn a commission.** Keep official setup/docs links available, select for user fit, and do not repeat disclosures in dialogs or add approval steps. Use only supplied/verified referral links and check the program's attribution terms; do not invent tracking codes or assume agent-assisted signup earns a reward.
