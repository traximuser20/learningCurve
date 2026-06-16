# CaseClinical — Agent Guide

## Project Overview

Premium clinical documentation platform. Source is a single-file HTML page (`src/ClaudeCode.html`) with embedded CSS and JS, transformed into LearnWorlds-compatible components.

## Build & Format

```bash
npm install          # Install prettier
npm run format       # Format all files with prettier
python3 transform_full.py  # Generate LearnWorlds output → learnWorlds/dist/
```

No test suite exists. No lint/typecheck configured.

## Key Files

- `src/ClaudeCode.html` — **Primary source**. Single-file HTML with CSS tokens (design system) and JS animations.
- `transform_full.py` — Main transform script. Extracts body/CSS/JS, injects LearnWorlds attributes, outputs to `learnWorlds/dist/`.
- `learnWorlds/dist/` — Production-ready LearnWorlds section HTML and CSS.
- `learnworlds-support/SKILL.md` — LearnWorlds platform rules (read before editing transforms).
- Other `transform_*.py` scripts — Earlier iterations; `transform_full.py` is canonical.

## Architecture

The source HTML uses CSS custom properties for theming (`:root` tokens). The transform script:

1. Scopes CSS to `.lw-caseclinical-wrapper` (replaces `:root`)
2. Renames `.navbar` → `.lw-navbar` to avoid conflicts
3. Adds `learnworlds-element`, `contenteditable`, `tabindex` attributes to all editable nodes
4. Extracts only hamburger/nav JS (not all scripts)
5. Wraps in LearnWorlds `<section>` container with full-width overrides

## LearnWorlds Editability Rules

- All editable elements need: `class="learnworlds-element"`, `data-node-type="text|button|image"`, `contenteditable=""`, `tabindex="0"`
- Buttons: parent `<a>` with `contenteditable="false"`, inner `<span>` with `contenteditable=""`
- Saving requires section wrapper (`js-learnworlds-section`) structure
- Full-width via `100vw` + `left: 50%` + `margin-left: -50vw` on wrapper

## Conventions

- Prettier config: 2-space indent, single quotes, trailing commas, 100 char width
- CSS uses BEM-like naming with `lw-` prefix for LearnWorlds namespace
- Animations must be manually triggered (no IntersectionObserver in LW editor) — use 600ms+ delay for DOM readiness
