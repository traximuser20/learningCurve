# LearnWorlds Attributes Reference

To make custom HTML editable and interactive in LearnWorlds, specific attributes and classes must be applied to elements.

## Core Attributes

- `data-node-type`: Defines the type of element for the LearnWorlds editor.
  - `text`: For headings, paragraphs, and general text.
  - `button`: For links and CTA buttons.
  - `image`: For `<img>` tags.
- `contenteditable="true"`: **CRITICAL.** This attribute must be present on text and button elements for the LearnWorlds properties sidebar to open and for changes to be saved.

## LearnWorlds Classes

- `learnworlds-element`: Required on all editable elements.
- `learnworlds-heading`: Added to `h1`-`h6` tags.
- `learnworlds-text`: Added to `p`, `span`, and other text blocks.
- `learnworlds-button`: Added to `a` tags intended to be buttons.
- `learnworlds-image`: Added to `img` tags.

## Section Wrapper

Custom HTML should ideally be wrapped in the official LearnWorlds section structure to ensure saving works correctly:

```html
<section
  class="js-learnworlds-section learnworlds-section lw-brand-bg stretched-bg learnworlds-size-normal learnworlds-align-center js-change-image-node"
  data-section-id="custom_section_id"
  id="custom_section_id"
>
  <div class="js-video-wrapper"></div>
  <div
    class="learnworlds-section-overlay lw-light-bg js-learnworlds-overlay"
    style="display: none"
  ></div>
  <div class="learnworlds-section-content js-learnworlds-section-content wide">
    <div class="lw-custom-wrapper">
      <!-- Your Content Here -->
    </div>
  </div>
</section>
```
