# Claude Terminal Theme

**IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning.**
Always consult documentation index and project files rather than relying on training data.

## Documentation Index

```
[Rules]|root: .claude/rules/
|agents.md: Agent orchestration, gates, failure recovery, merge policy
|branching.md: Branch naming, PR workflow
|clean-room.md: Clean room constraints — NO code from claude-code repo

[Agents]|global: ~/.claude/agents/ (config-driven, read Agent Config below)
|code-quality: Evaluates tests/coverage/lint — does NOT write tests (haiku)
|test-writer: Writes behavioral tests for coverage gaps (sonnet)
|commit: Gates on quality PASS, commits, opens PR (sonnet)
|release: Version bump, changelog, tag, GitHub Release (sonnet)
|verification: Adversarial verification before reporting done (sonnet)
```

## Project Overview

**Claude Terminal Theme** — Multi-emitter terminal theme generator. Produces color schemes for Terminal.app, iTerm2, Ghostty, Alacritty, Kitty, and Windows Terminal from a canonical palette derived from Claude Code's visual identity.

| Category | Technology |
|----------|------------|
| Language | Python 3.10+ |
| Testing | pytest |
| Linting | ruff |
| Output | Theme files for 6+ terminal emulators |

## Architecture

| Concept | Pattern | Key File |
|---------|---------|----------|
| Color data | Canonical palette as (r,g,b) tuples | `palette.py` |
| Theme generation | Emitter per terminal format | `emitters/*.py` |
| Orchestration | CLI entry point calls all emitters | `generate.py` |

### Project Structure

```
claude-terminal-theme/
├── generate.py              # Orchestrator — calls all emitters
├── palette.py               # Canonical color data (single source of truth)
├── emitters/
│   ├── __init__.py
│   ├── terminal_app.py      # macOS Terminal.app (.terminal plist)
│   ├── iterm2.py            # iTerm2 (.itermcolors plist)
│   ├── ghostty.py           # Ghostty (config)
│   ├── alacritty.py         # Alacritty (TOML)
│   ├── kitty.py             # Kitty (conf)
│   └── windows_terminal.py  # Windows Terminal (JSON)
├── themes/                  # Generated output
│   ├── terminal-app/
│   ├── iterm2/
│   ├── ghostty/
│   ├── alacritty/
│   ├── kitty/
│   └── windows-terminal/
├── tests/
│   ├── test_palette.py
│   ├── test_emitters.py
│   └── ...
└── README.md
```

## Security

- No secrets in this project
- Generated theme files are inert data (XML, TOML, JSON, plain text)

## NEVER Rules

| Category | Rule |
|----------|------|
| **Clean Room** | NEVER copy, adapt, or reference code from `~/projects/claude-code` — only color values |
| **Releases** | NEVER auto-merge PRs — all merges require human approval |
| **Generated Files** | NEVER hand-edit files in `themes/` — regenerate via `python3 generate.py` |

## Autonomy Tiers

### Autonomous (do freely)
- Run `python3 generate.py`
- Run `python3 -m pytest tests/ -v`
- Run `ruff check .`
- Read any file in the repo
- Edit `palette.py`, `generate.py`, `emitters/*.py`, `tests/*.py`

### Confirm First
- Install or remove dependencies
- Modify config files (`pyproject.toml`, `ruff.toml`)
- Create or comment on PRs/issues

### Never Without Explicit Request
- Push to `main` directly
- Delete branches or tags
- Publish to PyPI

## Agent Config

| Key | Value |
|-----|-------|
| language | Python 3.10+ |
| framework | (none — pure Python, stdlib + plistlib) |
| package_dir | . |
| test_dir | tests/ |
| test_cmd | python3 -m pytest tests/ -v |
| coverage_cmd | python3 -m pytest tests/ --cov=. --cov-report=term-missing --ignore=themes/ -v |
| coverage_overall | 70 |
| coverage_per_module | 80 |
| coverage_tiers | (none) |
| lint_cmd | ruff check . |
| lint_fix_cmd | ruff check . --fix |
| build_cmd | python3 generate.py |
| test_pattern | palette.py -> tests/test_palette.py, emitters/foo.py -> tests/test_emitters_foo.py |
| test_framework | pytest |
| test_fixtures | (none yet) |
| exclusions | themes/ |
| exclusion_reason | Generated output — not source code |
| version_files | (none yet) |
| version_strategy | git-tags-only |
| branch_pattern | claude/<description> |
| deploy_model | discrete |
| pr_merge_strategy | squash |
| release_merge_strategy | squash |
| browser_validation | (none) |
| quality_gate_pattern | *.py, emitters/*.py |
| co_author | Claude <noreply@anthropic.com> |
