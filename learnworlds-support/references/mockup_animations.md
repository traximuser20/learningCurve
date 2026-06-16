# LearnWorlds Mockup Animations Guide

Custom animations (like SVG graphs or progress bars) often fail in the LearnWorlds editor due to its internal DOM management or scroll tracking. Use the following patterns for robust animations.

## Manual Initialization Pattern

Avoid relying solely on `IntersectionObserver`. Use a manual `init` function triggered on `DOMContentLoaded` or with a short timeout.

```javascript
(function () {
  function init() {
    const section = document.getElementById('your_section_id');
    if (!section) return;

    setTimeout(() => {
      // Trigger Reveal Elements
      section.querySelectorAll('[data-reveal]').forEach((el) => {
        el.classList.add('visible');
        el.style.opacity = '1';
        el.style.transform = 'none';
      });

      // Trigger Specific Animations
      animateDonutCharts(section);
      animateProgressBars(section);
    }, 600);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    setTimeout(init, 300);
  }
})();
```

## Donut Chart Animation

```javascript
function animateDonutCharts(section) {
  section.querySelectorAll('.donut-container').forEach((container) => {
    const circles = container.querySelectorAll('.segment');
    const radius = 45; // Adjust based on your SVG
    const circumference = 2 * Math.PI * radius;
    let accumulatedPercent = 0;

    circles.forEach((circle, index) => {
      const percent = Number(circle.dataset.percent);
      const dashLength = (percent / 100) * circumference;
      const gapLength = circumference - dashLength;

      circle.style.strokeDasharray = `${dashLength} ${gapLength}`;
      circle.style.strokeDashoffset = circumference;

      const offset = circumference * (1 - accumulatedPercent / 100);
      accumulatedPercent += percent;

      setTimeout(() => {
        circle.style.strokeDashoffset = offset;
      }, index * 200);
    });
  });
}
```

## Progress Bar Animation

```javascript
function animateProgressBars(section) {
  const bar = section.querySelector('#progress-bar-fill');
  if (bar) {
    bar.style.width = bar.dataset.targetWidth || '78%';
  }
}
```
