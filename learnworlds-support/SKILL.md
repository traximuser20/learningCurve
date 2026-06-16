---
name: learnworlds-support
description: Guidance for developing, transforming, and troubleshooting custom HTML components for the LearnWorlds platform. Use when working on custom LearnWorlds sections, fixing editability issues (sidebar not opening, changes not saving), or implementing SVG/progress bar animations.
---

# Learnworlds Support

## Overview

This skill provides expert guidance for preparing custom HTML/CSS/JS for LearnWorlds sections. It focuses on ensuring that elements are editable within the LearnWorlds editor and that custom animations work reliably.

## Key Concepts

- **Native Editability**: For elements to be editable, they must use `contenteditable=""` (empty string) and `tabindex="0"`.
- **Standard Button Pattern**: Buttons should use a parent `<a>` tag with `contenteditable="false"` and an internal `<span>` with `contenteditable=""` for the text. This preserves link functionality while allowing text edits.
- **Saving Fix**: Sections must be wrapped in the official `learnworlds-section` and `learnworlds-section-content` classes. Explicitly setting `contenteditable=""` on leaf nodes is required for the platform to track changes.
- **Full-Width Breaking**: Use `width: 100vw`, `left: 50%`, and `margin-left: -50vw` on a main wrapper to force full-width display regardless of container constraints.
- **Editor-Specific CSS**: Use the `.learnworlds-editor` class to apply specific styles (like changing `position: fixed` to `absolute` for navbars) to prevent elements from blocking interactions in the editor.

## Workflow: Preparing a Custom Section

1. **Extract Content**: Separate the HTML body, CSS, and JS from your source file.
2. **Inject Attributes**: Apply `learnworlds-*` classes, `data-node-type`, `contenteditable=""`, and `tabindex="0"`.
3. **Wrap for Platform**: Wrap the HTML in a standard LearnWorlds section container (`js-learnworlds-section`).
4. **Refine JS**: Implement manual animation triggers with a delay (e.g., 600ms) to ensure the DOM is ready in the editor.

## Resources

### References

- [lw_attributes.md](references/lw_attributes.md): Detailed list of required attributes and classes.
- [mockup_animations.md](references/mockup_animations.md): Code patterns for SVG graphs and progress bar animations.

### Scripts

- [transform_html.py](scripts/transform_html.py): A Python script to automatically inject LearnWorlds attributes into an HTML file.

## Troubleshooting

- **Properties Sidebar Not Opening**: Check if the element has `class="learnworlds-element"`, a valid `data-node-type`, and `tabindex="0"`.
- **Changes Not Saving**: Ensure the component is wrapped in a `<section class="learnworlds-section" ...>` structure and leaf nodes use `contenteditable=""`.
- **Editor Interactions Blocked**: Use `.learnworlds-editor` CSS overrides to disable fixed positioning or pointer-event blocking on overlay elements.
