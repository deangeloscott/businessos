# Optional Local Capability Packs

AURA remains portable without extra local software. Optional local capability packs make trusted, high-leverage deterministic tools easier to discover, install, update, verify, and bind when the user wants a higher execution ceiling.

## Principle

A capability pack is **not another AURA edition** and is never a hard dependency. It is a small, inspectable definition of trusted local tools that can satisfy provider-neutral capabilities in the current environment.

Examples include media acquisition/processing tools such as `yt-dlp`, `ffmpeg`, and `ffprobe`, or built-in operating-system scheduling surfaces.

## Resolution order

1. Use an existing healthy host/tool binding first.
2. If a required/valuable capability is missing, check whether an installed trusted local pack can satisfy it.
3. If the tool is present and healthy, bind it without reinstalling it.
4. If it is missing, incompatible, or broken, AURA may offer the pack's known installation/update/repair path.
5. Installing, upgrading, reinstalling, or changing system software requires explicit user authorization. Recommendation is not authorization.
6. If the user declines or the environment cannot install it, continue through another provider or manual/assisted fallback.

## Safety and trust

- Never search the web for an arbitrary executable and run the first installer found.
- Pack definitions live in the AURA product and use fixed, reviewable executable names, health checks, capability mappings, and installation recipes.
- Prefer reputable package managers/project distribution channels; run commands as argument lists, never through an interpolated shell command.
- Do not silently add browser cookies, credentials, authentication material, or privileged access to make a tool work.
- Do not replace a healthy user-installed tool simply because AURA has a preferred recipe.
- If a tool is too old for AURA's minimum supported behavior or fails its health check, label it incompatible/broken and offer update/repair rather than pretending the capability is available.
- Tool installation state is environment state, not business truth. Persist only non-secret executable/version/binding metadata in the workspace environment overlay.

A short user-facing responsibility note is enough for general-purpose tools: **Use local tools responsibly and only on content/systems you are allowed to access.** AURA does not need to police ordinary lawful use of tools on the user's own machine, but it must not itself bypass access controls or fabricate authorization.

## Local media pack

The initial local media pack treats the tools separately:

- `yt-dlp` supplies permitted public/authorized media, subtitle/transcript, and media-metadata acquisition mechanics.
- `ffprobe` supplies deterministic media inspection/metadata mechanics.
- `ffmpeg` supplies deterministic clip/transcode/audio/frame/render mechanics.
- A model/harness still performs semantic visual/audio interpretation. Installing FFmpeg does not mean AURA has "watched" or understood a video.

A healthy existing `ffmpeg` installation is valid. On Homebrew environments AURA may offer the official `ffmpeg-full` formula as the enhanced install path when the user wants broad codec/filter support; the executable capability is still `ffmpeg`/`ffprobe`.

## Local automation pack

Built-in OS scheduling tools may satisfy `automation.schedule.manage` when they are actually available. That capability only means the environment can manage schedule mechanics; a recurring AURA monitor still needs a compatible worker/harness command and a verified scheduler binding before it may be called active automatic monitoring.

## User experience

Normal users should not need to understand bindings. AURA should communicate simply, for example:

- "Video research can be deeper on this computer with the optional local media toolkit. FFmpeg is already available; yt-dlp is missing. Want me to set it up?"
- "Your monthly monitor is saved, but this environment has no active scheduler. I will surface it when it is due the next time AURA runs."

Advanced operators may inspect/manage packs with `scripts/manage_local_capabilities.py`.
