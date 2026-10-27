"""Small project-local pointers for documented native instruction files."""
from pathlib import Path
import re


GUIDES = {
    'codex': ('https://learn.chatgpt.com/docs/codex/cli', 'Install the Codex command connection, then open Codex and sign in with your supported account.'),
    'claude': ('https://code.claude.com/docs/en/quickstart', 'Install Claude Code for your computer, then open it and sign in. A Claude desktop sign-in alone may not expose its command connection.'),
    'pi': ('https://pi.dev/docs/latest', 'Install Pi using its setup guide, then open Pi and connect your model account or local model.'),
    'omp': ('https://github.com/can1357/oh-my-pi#installation', 'Install OMP using its setup guide, then open OMP and connect your model account or local model.'),
    'hermes': ('https://hermes-agent.nousresearch.com/docs/getting-started/installation', 'Install Hermes using its platform guide, then open Hermes and complete its model connection.'),
    'antigravity': ('https://antigravity.google/download/', 'This connection needs the agy command. If your app does not provide it, paste the connection instructions below into your AI app for help.'),
}


def attach(kind, product, workspace):
    product, workspace = Path(product).resolve(), Path(workspace).resolve()
    name = {'claude':'CLAUDE.md', 'pi':'AGENTS.md', 'omp':'AGENTS.md'}.get(kind)
    if kind == 'claude' and not (workspace / name).exists() and (workspace / '.claude/CLAUDE.md').is_file():
        name = '.claude/CLAUDE.md'
    if kind == 'pi' and (workspace / 'AGENTS.override.md').exists():
        name = 'AGENTS.override.md'
    if kind == 'hermes':
        name = next((n for n in ('.hermes.md','HERMES.md','AGENTS.override.md','AGENTS.md','CLAUDE.md') if (workspace/n).exists()), 'AGENTS.md')
    if not name:
        return {'status':'request-guidance', 'note':'AURA guidance is supplied with requests from this interface.'}
    path = workspace / name
    if path.is_symlink() or not path.resolve().is_relative_to(workspace):
        raise ValueError('Workspace instructions are linked elsewhere. Ask your AI to attach AURA without replacing them.')
    current = path.read_text(encoding='utf-8') if path.exists() else ''
    if workspace == product and path.is_file():
        return {'instructions':str(path), 'status':'project-guidance'}
    start, end = '<!-- AURA workspace attachment -->', '<!-- /AURA workspace attachment -->'
    if (start in current) != (end in current):
        raise ValueError('An unfinished AURA instruction was found. Ask your AI to check it; existing instructions were kept.')
    block = (start + f'\nFor organizational work, read `{product / "AGENTS.md"}` and '
             f'`{product / "skills/viraltrac-aura/SKILL.md"}`.\nOrganization workspace: `{workspace}`. '
             'Use AURA helpers with BUSINESSOS_WORKSPACE set to this folder. Resolve the intended business; do not guess across businesses.\n' + end)
    pattern = re.escape(start) + r'[\s\S]*?' + re.escape(end)
    updated = re.sub(pattern, lambda _:block, current) if start in current else current.rstrip() + '\n\n' + block + '\n'
    if updated != current:
        temporary = path.with_suffix(path.suffix + '.aura-tmp')
        temporary.write_text(updated.lstrip('\n'), encoding='utf-8')
        temporary.replace(path)
    # Preparing a native instruction is not a claim the host has loaded it.
    return {'instructions':str(path), 'status':'prepared'}


def refresh(product, workspace):
    """Refresh only existing managed pointers when opening with a newer AURA."""
    workspace = Path(workspace).resolve()
    for name in ('CLAUDE.md','.claude/CLAUDE.md','AGENTS.md','AGENTS.override.md','.hermes.md','HERMES.md'):
        path = workspace / name
        if path.is_file() and path.resolve() == path:
            text = path.read_text(encoding='utf-8')
            start, end = '<!-- AURA workspace attachment -->', '<!-- /AURA workspace attachment -->'
            if start in text and end in text:
                block = (start + f'\nFor organizational work, read `{Path(product) / "AGENTS.md"}` and '
                         f'`{Path(product) / "skills/viraltrac-aura/SKILL.md"}`.\nOrganization workspace: `{workspace}`. '
                         'Use AURA helpers with BUSINESSOS_WORKSPACE set to this folder. Resolve the intended business; do not guess across businesses.\n' + end)
                updated = re.sub(re.escape(start)+r'[\s\S]*?'+re.escape(end), lambda _:block, text)
                if updated != text:
                    temporary = path.with_suffix(path.suffix + '.aura-tmp')
                    temporary.write_text(updated, encoding='utf-8')
                    temporary.replace(path)
    skill = workspace / '.agents/skills/viraltrac-aura/SKILL.md'
    if skill.is_file() and not skill.is_symlink() and '<!-- AURA native Skill pointer -->' in skill.read_text(encoding='utf-8'):
        import workspace_codex
        workspace_codex.attach(product, workspace)
