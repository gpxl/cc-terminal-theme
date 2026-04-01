# Branch Workflow (MANDATORY)

## NEVER push directly to main

All changes must go through pull requests.

## NEVER merge PRs without user approval

After creating a PR, **stop and report the PR URL**. Do not merge.
The user will review and decide when to merge.

### Workflow

1. Create a branch from main:
   ```bash
   git checkout -b claude/<descriptive-name>
   ```

2. Make changes, commit to the branch

3. Push the branch:
   ```bash
   git push -u origin claude/<descriptive-name>
   ```

4. Create a PR:
   ```bash
   gh pr create --title "..." --body "..."
   ```

5. **Stop.** Report the PR URL and wait for user to approve/merge.

### Branch Naming

| Actor | Pattern | Example |
|-------|---------|---------|
| Claude Code | `claude/<description>` | `claude/add-iterm2-emitter` |
| Developer | `feat/<description>`, `fix/<description>` | `fix/ansi-red-alignment` |
