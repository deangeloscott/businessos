# Interface design

AURA should feel familiar to people who use Claude Code, Codex or Claude: a sidebar, the chat front and centre, quiet colours and plain words. Polish comes from consistency and restraint, not decoration. A change that looks better but makes a core task slower is worse.

**Core tasks to keep fast:** start a chat with the right context; find a saved result; set up something that repeats.

Use what already exists before adding anything new. Everything below lives in `interface/style.css` (tokens at the top, shared components at the end) and `interface/app.js`.

## Tokens

Use tokens, never raw values, so themes, text size and density keep working.

| Kind | Tokens | Notes |
|---|---|---|
| Text | `--text-xs` 11 · `--text-sm` 12 · `--text-md` 13 · `--text-base` 14 · `--text-body` 15 · `--text-lg` 17 · `--text-xl` 20 · `--text-2xl` 26 · `--text-3xl` 30 | Sizes at the standard text setting. All follow `--ui-text-size`, so Personalization → Text size scales the whole interface. 11px is for badges and keyboard hints only; readable text starts at 12. |
| Colour | `--ink`, `--muted`, `--faint`, `--line`, `--line-strong`, `--paper`, `--surface`, `--sidebar`, `--hover`, `--accent`, `--accent-soft`, `--accent-strong`, `--on-accent` | Neutral greys; the accent is the only hue. Defined for light and dark, and for the four accents (Forest, Ocean, Clay, Mono). |
| Meaning | `--success`, `--warning`, `--danger` (each with `-soft`), `--danger-solid` for badges | Use for status only. Orange or red is never decoration. |
| Shape | `--radius-sm` 6 · `--radius-md` 8 · `--radius-lg` 12 · `--radius-full` | Controls use `md`, cards and panels `lg`, chips `full`. |
| Depth | `--shadow-sm`, `--shadow-md`, `--shadow-lg` | Popovers `md`, dialogs and toasts `lg`. |
| Size | `--control-height` | 34px; 30px in Compact density. |
| Motion | `--fast` (.15s), `--ease` | Motion shows where something came from and is off with reduced motion. |
| Spacing | 4px grid (2px allowed below 12px) | |
| Breakpoints | 480 · 600 · 1000 | Phone, small, tablet. |

## Styles

A style (Personalization → Style, `data-style` on the root) restyles the whole interface without changing layout or behaviour: Modern, Classic mono, 90s desktop, 90s console, 2000s desktop and 2000s console. Every style works in light and dark (`data-theme`) and has its own accents (`data-accent`); an accent sets the colour plus one signature detail of that era. The style list lives in `STYLES` in `app.js` and `STYLE_ACCENTS` in `scripts/workspace_ui.py`; keep them in step. In `style.css`, each style's rules follow one order: base (light), base dark, accents (light), accents dark, then component rules that read only tokens and the style's own variables. New components that use tokens and the shared classes pick up every style automatically; check a new component in at least one retro style in both modes. Styles evoke an era without copying any company's logos, names or fonts.

## Components

- **Buttons:** `primary` (one per area, the main action), `secondary` (other actions), `text-button` (links and low-weight actions), `icon-button` (with an `aria-label` and `title`). Add `compact` for inline actions. Every "add" action is `secondary compact add-button` labelled with a verb and noun ("Add goal").
- **Inputs and selects:** one height (`--control-height`) and one focus style.
- **Chips:** filters and suggestions share one pill shape; the active filter uses `--accent-soft`.
- **Empty states:** `empty(title, text, prompt, label)` explains the place and offers one first step, usually asking the AI to do it ("Suggest goals"). The prompt fills the chat box; nothing runs without the person sending it.
- **Side panel:** `details(title, html, 'context')` opens a saved item beside the page or chat, with Expand. Use it for anything someone looks at while working. Use the default dialog for settings and short forms, and `'page'` for whole destinations.
- **Toast:** `toast(text, undo)` confirms an action. Pass `undo` whenever the action can be reversed, instead of asking "Are you sure?".
- **Provenance:** results show where they came from the same way everywhere: your correction, the number of sources and when they were checked, or "No source".
- **Findings:** a finding shows its status as one chip, the same everywhere: Supported, Unverified, Challenged, Needs review or Replaced, with its evidence counts. It opens in one finding panel.
- **Result cards:** what the AI saved or checked during a reply appears as a card in the chat that opens the result.
- **Settings:** one grouped page with search. Add a setting as a row in `settingsGroups`.
- **Ctrl+K actions:** add an action to `shellCommands()`. Actions click the same control a person would, so there is one code path.
- **Activity:** running work and notifications share the bell.
- **Terminal:** one dock under the work area (Ctrl+`), never a dialog, so it stays while you move around. Its colours come from the current style's tokens.
- **Continue in another app:** one dialog for every app pair; the option says how the work moves (Full conversation or Handoff), what carries over, the cost and the permission setting.

## Words

- One name per place, everywhere: **Business & memory**, **Files & media**, **Library** (with Agents as a tab), **Scheduled tasks**, **Activity**, **Settings**.
- Sentence case. Buttons say what they do ("Save goal", "Connect Claude"), not "OK" or "Submit".
- Plain errors that say what happened and what to do next.

## Guardrails

- Keep the information density. Modern does not mean bigger padding and fewer things on screen.
- No actions that appear only on hover, no icons without labels, no gestures you have to discover.
- Scrollbars sit at the edge of what scrolls (the window edge for pages), never against the text: pages keep `--page-gutter` before the scrollbar and panels keep about 10px.
- Keyboard: every action is reachable, focus is always visible, shortcuts are shown in menus.
- Check every change in light and dark, at the largest text size, and at phone width (no sideways scrolling).
