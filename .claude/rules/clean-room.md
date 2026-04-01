# Clean Room Constraint (CRITICAL)

## NO code from claude-code

This project must be a clean room implementation. When referencing
`~/projects/claude-code`, you may observe:

| Allowed | Not Allowed |
|---------|-------------|
| Color hex/RGB values (visual outputs) | Copying Python/TypeScript code |
| Theme variant names and design rationale | Adapting functions or algorithms |
| Unicode glyph characters | Referencing implementation patterns |
| ANSI color slot mapping decisions | Using data structures from the source |
| File format specifications | Reusing utility functions |

All implementation code — Python generators, file format writers, data
structures, encoding logic — must be written from scratch.

## Why

The Claude Code source is proprietary. We extract publicly observable
visual properties (colors, glyphs) and implement our own theme generator
around them, the same way any user could create a theme by looking at
the terminal output.
