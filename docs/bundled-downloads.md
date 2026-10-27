# Open AURA without installing Python

Choose the bundled download for your operating system and processor from the official GitHub release. Extract the complete folder, then open its launcher:

| Download | Launcher |
|---|---|
| Windows x64: most Intel/AMD Windows PCs | Open AURA.cmd |
| Windows ARM64: Windows on ARM PCs | Open AURA.cmd |
| macOS ARM64: Apple Silicon Macs | Open AURA.command |
| macOS x64: Intel Macs | Open AURA.command |
| Linux x64: Intel/AMD Linux desktops using glibc | Open AURA.sh |
| Linux ARM64: ARM Linux desktops using glibc | Open AURA.sh |

The launcher opens the local workspace in your browser. Keep its terminal open while using this view; close the terminal to stop it. On Linux, choose **Run as Program**, or run `./"Open AURA.sh"`. These Linux builds target glibc systems, not Alpine/musl.

Follow the short workspace/AI connection setup. If you do not have an AI app yet, use the download/sign-in links there. The interface can open before an AI is connected. An AI account, API access, or a separately configured local model is still needed to do AI work. Optional tools such as FFmpeg are obtained when a task needs them, rather than installed for everyone.

macOS may ask you to approve the downloaded launcher in **Privacy & Security**. The current release is not Apple-notarized. Approve only a download you obtained from the official release; AURA does not remove quarantine flags or disable operating-system protections. The same normal download/security prompts may apply on other platforms.

## What is included

Each bundle contains the normal editable AURA product, a private Python runtime in `.aura-runtime/`, and the required PyYAML/jsonschema libraries with their dependencies. No system-wide Python installation or first-run package download is required. Keep the folder together.

The runtime comes from [Astral's python-build-standalone](https://github.com/astral-sh/python-build-standalone), with the exact runtime and wheel URLs and SHA-256 values recorded in `distribution/bundled-runtimes.json`. Bundles retain upstream license notices, plus `THIRD-PARTY-RUNTIME.md` and `BUNDLED-RUNTIME.json`. Python and third-party components retain their own licenses.

The platform-neutral ZIP remains available for existing AI/CLI environments that already provide Python and AURA's requirements. Native AI apps and the CLI can use the same files without this interface. The bundle does not include sign-ins, API keys, models, business data, or a required cloud service.

## Move, customize, and update

Business memory remains ordinary organization-owned files. Move or reuse those files on another supported computer; download that computer's runtime bundle and reconnect its AI app, credentials, and external folder links. The Python executables themselves are specific to an OS/processor.

Keep organization data separate from product source when updating. If your data is in the old product folder, follow `SETUP-WITH-AI.md` to preserve/migrate it before replacing anything. Interface customizations belong in an organization-owned copy; see [visual workspace customization](visual-workspace.md).

## Build and verify a bundle

Maintainers can run, on the target operating system and processor:

```text
python scripts/package_runtime.py --platform windows-x64 --output-dir /outside/source/bundles --cache-dir /outside/source/runtime-cache
```

Replace the target with one of the six IDs above (`macos-arm64`, for example). Build outputs and downloaded binaries stay outside product source. The builder verifies every downloaded runtime/wheel against its pinned SHA-256, uses the private interpreter to prepare the clean full product, then extracts the final archive to a new path containing spaces. Verification removes system Python from PATH and checks native libraries, Tcl resources, launcher startup, and real first-use organization setup with no AI connected or model request sent.

The manually triggered **Build bundled downloads** GitHub Actions workflow runs those native builds with read-only repository permissions. Windows bundles use ZIP; macOS/Linux use tar.gz to retain executable permissions and internal runtime links. The standard product release gate remains `python scripts/package_release.py`.
