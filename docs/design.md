# Interface design

This is guidance, not a rulebook. It describes what good looks like in AURA and the defaults that usually get there, so the person or model doing the work can use their judgement. A few things protect people and are not up for trade; they are listed under **Musts**. Everything else is a strong default: depart from it when the result is clearly better for the person using AURA, and say why.

## The idea

A good mouse looks simple because someone decided exactly where each finger rests. AURA should feel the same: people do what they came to do without thinking about the interface, and the care that made it easy stays out of sight.

- **Design for the person using it, not for other designers.** Every visual choice should help someone do or understand something. Personality is welcome when it serves them: the aura and the styles make AURA feel like theirs, and that is part of why people come back.
- **Important things look important.** Each screen has one thing that matters most, and it is obvious within a few seconds. Detail is one step away, never in the way.
- **Calm by default.** Things that need nobody stay quiet at the edge of attention. They come forward only when they need someone, and go back afterwards.
- **Plain words.** Say what happened and what to do, in the person's language, not the system's.
- **Nothing breaks.** Every screen works at phone, tablet, laptop and wide desktop sizes, in every style, light and dark, and at the largest text size.

## What people come to AURA to do

AURA keeps what a business knows and works with any AI app or model, so people can do their work wherever they like and stay current. Every screen should serve one of these jobs, roughly in this order of importance:

1. **Do work with AI.** Start or continue a chat, with the right context already in place.
2. **Stay up to date.** What changed, what is running, what needs me.
3. **Reuse what has been done.** Saved results, files, collections and proven methods.
4. **Keep work going by itself.** Scheduled tasks that stay healthy.
5. **Teach AURA the business.** Goals, facts and preferences, and correcting it when it is wrong.
6. **Move between AI apps and businesses** without losing anything.

When something on screen serves none of these, it belongs one level down, or nowhere.

## Importance

Give each thing on a screen one of three levels, and let the level decide its treatment:

| Level | Examples | Treatment |
|---|---|---|
| **Act** | Needs you, the message box, the main action of a page | Largest type on the screen, the one accent-filled button, nearest the top |
| **Check** | Results, changes, goals, running work, lists of items | Body text, clear rows, no decoration beyond what separates them |
| **Look up** | Sources, history, IDs, settings, how something works | Smaller, secondary colour, or one click away in the side panel or "⋯" |

Two levels of disclosure is the limit: a page, and the side panel or a dialog over it. Never a panel inside a panel. If something needs a third level, simplify it.

## Musts

These protect people, so they always hold:

- Text and controls meet WCAG AA contrast in every style, accent and mode.
- Everything works by keyboard, focus is always visible, and shortcuts are shown where the action is.
- No sideways scrolling at any width; nothing overlaps or clips at the largest text size.
- Touch targets are at least 44px where the pointer is coarse.
- Motion stops with reduced motion. Nothing flashes.
- Never fake life: every number, movement and status traces to a saved record or real running work.
- AURA never starts work the person did not send.

## Foundations

Everything lives in `interface/style.css` (tokens at the top, shared components after, styles at the end) and `interface/app.js`. Use tokens rather than raw values, so styles, text size and density keep working.

**Type.** All sizes follow `--ui-text-size` (15px at Standard), so Personalization → Text size scales everything.

| Token | Size | Use |
|---|---|---|
| `--text-xs` | 12 | Badges, keyboard hints, the smallest metadata |
| `--text-sm` | 13 | Secondary text, metadata, labels |
| `--text-md` | 14 | Dense lists, controls |
| `--text-base`, `--text-body` | 15 | Reading text, row titles |
| `--text-lg` | 17 | Section headings |
| `--text-xl` | 20 | Panel and dialog titles |
| `--text-2xl` | 26 | Page titles |
| `--text-3xl` | 30 | The one greeting or hero line |

Two or three weights are enough: regular, medium (`500`) for titles and labels, semibold (`600`) for page titles.

**Space.** A 4px scale: `--space-1` 4 · `--space-2` 8 · `--space-3` 12 · `--space-4` 16 · `--space-5` 24 · `--space-6` 32 · `--space-7` 48 · `--space-8` 64. Related things sit close; separate groups with space before reaching for a line or a box.

**Surfaces and edges.** Separate with space and a change of surface, not borders. Borders are for fields and the thin divider between rows. Avoid a box inside a box: a section on a page is usually just a heading and its content.

**Roles.** Components describe what something is, and each style decides how it looks:

| Role | Tokens |
|---|---|
| Page, raised, sunken and floating surfaces | `--surface`, `--raised-bg`, `--raised-edge`, `--sunken-bg`, `--sunken-edge`, `--float-edge` |
| Emphasis | `--primary-bg`, `--primary-ink`, `--primary-edge`; `--secondary-bg`, `--secondary-edge`; `--quiet-hover` |
| Status | `--attention`, `--working`, `--success`, `--warning`, `--danger` (each with `-soft`) |
| Character | `--heading-font`, `--heading-weight`, `--heading-case`, `--heading-tracking`, `--control-radius`, `--surface-radius` |

A new component that uses roles looks right in all six styles with no extra work. A style adds its own selectors only for signature details that roles cannot express.

**Layout.** Pages lay out by the window (media queries at 600 and 1000px). Components lay out by the space they actually get (container queries on the work area, the side panel and shared cards), because the sidebar and side panel change that space. The side panel sits beside the page when there is room and over it when there is not; on a phone it fills the screen.

## Shared pieces

- **Buttons:** `primary` (one per area, the main action), `secondary` (other actions), `text-button` (low-weight actions and links), `icon-button` (with an `aria-label` and `title`). `compact` for inline actions.
- **Page header:** title, one line of description, the main action on the right, everything else in "⋯". Pages refresh themselves; refreshing by hand lives in "⋯" and Ctrl+K.
- **Inputs and selects:** one height (`--control-height`) and one focus style.
- **Chips:** filters and suggestions share one pill shape; the active filter uses `--accent-soft`.
- **Rows, not cards, for lists.** A card is for something with a picture or a preview.
- **Empty states:** `empty(title, text, prompt, label)` names the place and offers one first step, usually preparing a request for the AI. The prompt fills the message box; nothing runs until the person sends it.
- **Side panel:** `details(title, html, 'context')` opens an item beside the page or chat, with Expand. Use the default dialog for settings and short forms, and `'page'` for whole destinations.
- **Toast:** `toast(text, undo)` confirms an action. Offer Undo when it can be reversed, rather than asking "Are you sure?".
- **Provenance:** results show where they came from the same way everywhere: your correction, the number of sources and when they were checked, or "No source". Short on the row, full in the panel.
- **Findings:** one status chip, the same everywhere: Supported, Unverified, Challenged, Needs review or Replaced.
- **Result cards:** what the AI saved or checked during a reply appears as a card in the chat that opens the result.
- **Settings:** one grouped, searchable page. Add a setting as a row in `settingsGroups`.
- **Ctrl+K:** add an action to `shellCommands()`. Actions click the same control a person would, so there is one code path.
- **Terminal:** one dock under the work area (Ctrl+`), never a dialog.
- **Continue in another app:** one dialog for every app pair; it says how the work moves, what carries over, the cost and the permission setting.

## AI work

- **Show the context.** A chat says what it is using (business, project, files), and that opens the details. This is what AURA adds, so people should be able to see it.
- **Show real progress.** Running work says what it is doing in specific words ("Checking 8 competitors on Google Maps"), not a spinner alone, and Stop is always available.
- **Make correcting easy.** Wrong facts are one click from being corrected; dismissing a suggestion costs nothing.
- **Tell people about changes** in one place (Home and Activity), once, with what to do next.

## Home and the aura

- **Home** answers "what needs me, and what's new?" in a few seconds. A compact message box sits on top. Below it, in order and each only when real records fill it: Needs you, Running now, Pick up where you left off, This week, Goals, Collections. Every row opens the record behind it and every number is a count of saved records. New chat stays a clear chat with nothing else on the page.
- **The aura** is the business's face: its colours come from the chosen focus areas, so it stays recognisable wherever the business appears (the switcher, Home, chats). It has one living signal: it moves only while the AI is working. Beside it, a plain status says what matters ("Up to date", "2 working", "1 needs you"), and clicking it opens Activity. It is drawn only from saved state and never decorative.

## Styles

A style (Personalization → Style, `data-style` on the root) is a complete interpretation, not a wallpaper. Each works in light and dark (`data-theme`) and has its own accents (`data-accent`). It sets roles and character tokens, then adds a few signature details. Layout and behaviour stay the same, so everything learned in one style works in every other. Styles evoke an era without copying any company's logos, names or fonts. The list lives in `STYLES` in `app.js` and `STYLE_ACCENTS` in `scripts/workspace_ui.py`; keep them in step.

| Style | Character | Importance shows as | Signature |
|---|---|---|---|
| **Modern** | Neutral greys, one accent hue, soft corners, quiet depth | Size, weight and the one accent-filled button | Calm; the content is the colour |
| **Classic mono** | One-bit black and white, crisp outlines, hard shadows | Inverted (filled) controls and heavy outlines | Striped title bars, checkered scrollbars; accent tints the selection |
| **90s desktop** | Grey window faces, bevelled 3D, square corners, Tahoma-like type | A raised button with a dark outline; selection as a title-bar colour | Gradient title bars, the desktop colour behind the chat home |
| **90s console** | A grey or charcoal case, chunky glossy buttons, blocky headings | Big glossy buttons and bold capitals | Four coloured dots or a four-colour stripe, by accent |
| **2000s desktop** | Cream windows, glossy rounded title bars | A friendly green "go" button; orange glow on hover | Gloss and rounded window tops |
| **2000s console** | A dashboard of rounded glass tiles and pill buttons | A glowing ring around the selection | A soft wave of colour behind the work |

Check a new component in Modern and at least one retro style, in both modes.

## Words

- One name per place, everywhere: **Home**, **Knowledge**, **Files**, **Library**, **Schedules**, **Activity**, **Settings**.
- Sentence case. Buttons say what they do ("Save goal", "Connect Claude").
- Errors and warnings say what happened and what to do, once. One message per problem, with the fix as a button.
- Translate system terms. People see "Map pack rank · 2 · Nov 9", not a record ID; "Couldn't check: the scheduled task was removed from Codex", not "linked task no longer listed". Leave out a field that says nothing useful ("Coverage unknown").
- Keyboard hints belong to keyboards: hide them on touch screens.

## Checking the work

- `node tools/ui-snapshots.mjs --business <id> --out <folder>` captures the main screens in every style, light and dark, at phone, tablet and desktop widths, with a gallery (`index.html`). Look through it before calling interface work done.
- Walk through the six jobs in the running interface and fix whatever makes one slower or less clear.
- `python tests/run_all.py` still passes.
