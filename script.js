// Mobile nav toggle
const navToggle = document.getElementById("navToggle");
const navLinks = document.getElementById("navLinks");

navToggle.addEventListener("click", () => {
  const isOpen = navLinks.classList.toggle("open");
  navToggle.setAttribute("aria-expanded", String(isOpen));
});

navLinks.querySelectorAll("a").forEach((link) => {
  link.addEventListener("click", () => {
    navLinks.classList.remove("open");
    navToggle.setAttribute("aria-expanded", "false");
  });
});

// Footer year
document.getElementById("year").textContent = new Date().getFullYear();

// Animated stat counters, triggered once when scrolled into view
const statNumbers = document.querySelectorAll(".stat-number");

function animateCount(el) {
  const target = Number(el.dataset.target);
  const duration = 1400;
  const start = performance.now();

  function tick(now) {
    const progress = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - progress, 3);
    el.textContent = Math.floor(eased * target).toLocaleString("pt-BR");
    if (progress < 1) requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);
}

const statsObserver = new IntersectionObserver(
  (entries, observer) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        animateCount(entry.target);
        observer.unobserve(entry.target);
      }
    });
  },
  { threshold: 0.6 }
);

statNumbers.forEach((el) => statsObserver.observe(el));

// Live status badge
// Checking real Twitch live status requires a backend call with an API token
// (the Twitch Helix API needs a client secret, which can't live in frontend code).
// Wire this up to your own backend/serverless endpoint that proxies Helix,
// then replace this stub with the real fetch.
const statusBadge = document.getElementById("statusBadge");
const statusText = document.getElementById("statusText");

function setLiveStatus(isOnline) {
  statusBadge.classList.toggle("online", isOnline);
  statusText.textContent = isOnline
    ? "Ao vivo agora"
    : "Offline — confira a agenda abaixo";
}

setLiveStatus(false);
