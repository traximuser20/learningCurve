<div align="center">

<div>
<span style="font-size: 50px;">🩺 </span>
  <img src="assets/CaseClinical.png" alt="CaseClinical Logo" width="400" />
</div>

#

### _The Future of Clinical Documentation & Case Management_

[![License: ISC](https://img.shields.io/badge/License-ISC-blue.svg)](https://opensource.org/licenses/ISC)
[![Built with HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat-square&logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5)
[![Styled with CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat-square&logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)
[![Scripted with JS](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat-square&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![Formatted with Prettier](https://img.shields.io/badge/Code_Style-Prettier-F7B93E?style=flat-square&logo=prettier&logoColor=white)](https://prettier.io/)

**[Demo Site](#) • [Documentation](final/ClaudeCode.html) • [Report Bug](https://github.com/yourusername/caseclinical/issues)**

</div>

---

## 🌟 Overview

**CaseClinical** is a premium, high-performance web documentation platform designed specifically for medical case studies and clinical data visualization. Built with a focus on **elegance, accessibility, and fluid interaction**, it provides a modern interface for healthcare professionals to document and showcase clinical breakthroughs.

---

## 🎓 LearnWorlds Integration

The project includes a robust pipeline for transforming standard HTML components into **LearnWorlds-compatible custom sections**.

### 🔄 Transformation Pipeline

- **`transform_full.py`**: The primary script that converts `src/ClaudeCode.html` into a production-ready LearnWorlds component. It automatically injects required platform attributes, handles full-width layouts, and optimizes animations.
- **`learnWorlds/dist/`**: Contains the output files (`section_html.html` and `site_custom_code.css`) ready for deployment.

### 🛠️ Key Compatibility Patterns

- **Editability**: All text elements use `contenteditable=""` and `tabindex="0"`.
- **Button Structure**: Buttons follow the native `Link + Inner Span` pattern to ensure they are both linkable and editable.
- **Full-Width Layout**: CSS overrides force the section to span the full viewport width (`100vw`) even when nested in platform containers.
- **Mockup Animations**: Custom JavaScript manually initializes SVG charts, progress bars, and count-up counters to ensure they work reliably in the LearnWorlds editor.

---

## 🤖 Gemini CLI Skills

We have developed a specialized skill for Gemini CLI to assist with LearnWorlds development:

### **learnworlds-support**

Provides expert guidance on:

- Preparing custom HTML for LearnWorlds.
- Troubleshooting editability and saving issues.
- Implementing robust animations for mockup components.

**To install:**

```bash
gemini skills install learnworlds-support.skill
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.x (for running transformation scripts)
- A modern web browser

### Building for LearnWorlds

To generate the latest LearnWorlds assets:

```bash
python3 transform_full.py
```

The results will be in `learnWorlds/dist/`.

---

## 🏗️ Project Structure

```text
├── learnWorlds/     # LearnWorlds specific assets and outputs
│   ├── dist/        # Production-ready HTML/CSS for LearnWorlds
│   └── example_code.html # Platform reference code
├── src/            # Core source files (HTML, CSS, JS)
├── transform_full.py # Main LearnWorlds transformation script
└── learnworlds-support.skill # Gemini CLI specialized skill
```

---

<div align="center">
  <sub>Built with ❤️ by the CaseClinical Team</sub>
</div>
