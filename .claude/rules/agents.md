# Agent Workflow

## Agents

| Agent | Trigger | What it does |
|-------|---------|-------------|
| `code-quality` | After logic changes | Evaluates tests, coverage (80%/module), lint, test quality — **does not write tests** |
| `test-writer` | After code-quality FAIL | Writes/fixes tests for coverage gaps and quality failures |
| `commit` | "commit", "push", "open a PR" | Gates on code-quality PASS, commits, pushes, opens PR — **never merges** |
| `release` | "release", "cut a release" | Evaluates if release needed, bumps version, tags, publishes |
| `verification` | After non-trivial implementation | Runs build, tests, lint, adversarial checks — returns PASS/FAIL/PARTIAL |

## Enforcement Rules (CRITICAL)

### Code-Quality Gate

The code-quality agent **must** run before the commit agent for any change
that touches `*.py` or `emitters/*.py`. This is not optional.

| Rule | Detail |
|------|--------|
| **REQUIRED** | Run code-quality agent before invoking commit agent |
| **REQUIRED** | Include `CODE QUALITY RESULT: PASS` output when delegating to commit |
| **BLOCKED** | Commit agent will refuse to proceed without code-quality evidence |
| **EXCEPTION** | Changes that ONLY touch tests, docs, config, or generated themes/ are exempt |

### Failure Recovery

When code-quality reports FAIL:

1. Invoke the **test-writer** agent with the code-quality report
2. Re-run **code-quality** to verify the fixes
3. If PASS → proceed to commit
4. If FAIL again → stop and ask the user for guidance (max 1 retry)

### Warning Tracking

When code-quality reports PASS with test quality warnings (Q3-Q8):

1. Create beads tasks for each warning (`bd create --type=task --priority=3`)
2. Proceed to commit — warnings do not block
3. Warnings become backlog items tracked in beads

### Workflow

```
code change → code-quality (evaluate) → FAIL? → test-writer → code-quality (re-verify)
                                       → PASS  → bd create tasks for warnings → commit (gate + ship) → user merges → release
```

## Merge Policy (CRITICAL)

**No agent may merge a feature PR autonomously.** After pushing a branch and
opening a PR, stop and report the PR URL. The user decides when to merge.

## Post-Merge Release Check

After the user merges a PR to main, invoke the release agent to evaluate
whether a release should be cut.
