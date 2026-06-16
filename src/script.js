// Parallax for the device area and subtle entrance animations
const deviceArea = document.querySelector('.device-area');
if (deviceArea) {
  deviceArea.addEventListener('mousemove', (e) => {
    const rect = deviceArea.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width - 0.5;
    const y = (e.clientY - rect.top) / rect.height - 0.5;
    const laptop = deviceArea.querySelector('.laptop-mock');
    const phone = deviceArea.querySelector('.phone-mock');
    if (laptop) laptop.style.transform = `translate(${x * 18}px, ${y * -12}px)`;
    if (phone) phone.style.transform = `translate(${x * 28}px, ${y * -18}px) rotate(-6deg)`;
  });
  deviceArea.addEventListener('mouseleave', () => {
    const laptop = deviceArea.querySelector('.laptop-mock');
    const phone = deviceArea.querySelector('.phone-mock');
    if (laptop) laptop.style.transform = '';
    if (phone) phone.style.transform = '';
  });
}

// Simple fade-in on scroll for sections
const io = new IntersectionObserver(
  (entries) => {
    entries.forEach((e) => {
      if (e.isIntersecting) e.target.classList.add('inview');
    });
  },
  { threshold: 0.18 }
);
document.querySelectorAll('section').forEach((s) => io.observe(s));

// Small ripple for buttons
const style = document.createElement('style');
style.textContent = `
.btn{position:relative;overflow:hidden}
.btn .ripple{position:absolute;border-radius:50%;transform:scale(0);background:rgba(255,255,255,0.35);animation:ripple 600ms linear}
@keyframes ripple{to{transform:scale(4);opacity:0}}
`;
document.head.appendChild(style);

document.querySelectorAll('.btn').forEach((btn) => {
  btn.addEventListener('click', function (e) {
    const r = document.createElement('span');
    r.className = 'ripple';
    this.appendChild(r);
    const d = Math.max(this.clientWidth, this.clientHeight);
    r.style.width = r.style.height = d + 'px';
    r.style.left = e.offsetX - d / 2 + 'px';
    r.style.top = e.offsetY - d / 2 + 'px';
    setTimeout(() => r.remove(), 900);
  });
});

// Smooth scroll for nav
document.querySelectorAll('.main-nav a').forEach((a) => {
  a.addEventListener('click', (e) => {
    e.preventDefault();
  });
});
