(() => {
  const root = document.documentElement;
  root.classList.add("js");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  document.getElementById("yr").textContent = new Date().getFullYear();

  // Nav gains a background once the page scrolls (state change feedback).
  const nav = document.getElementById("nav");
  const onScroll = () => nav.classList.toggle("scrolled", scrollY > 12);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // Reveal on scroll: content enters in reading order.
  const els = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    els.forEach((e) => e.classList.add("in"));
  } else {
    const io = new IntersectionObserver(
      (entries) => entries.forEach((en) => {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      }),
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    els.forEach((e) => io.observe(e));
  }

  if (!reduce) {
    // Hero image drifts slower than the page: depth cue, written outside any render loop.
    const img = document.querySelector("[data-parallax]");
    let ticking = false;
    const par = () => {
      ticking = false;
      if (scrollY < innerHeight * 1.2) img.style.transform = `translate3d(0,${scrollY * -0.06}px,0)`;
    };
    addEventListener("scroll", () => { if (!ticking) { ticking = true; requestAnimationFrame(par); } }, { passive: true });

    // Magnetic buttons: pointer pull with eased return.
    if (matchMedia("(hover: hover)").matches) {
      document.querySelectorAll("[data-magnetic]").forEach((b) => {
        b.addEventListener("pointermove", (e) => {
          const r = b.getBoundingClientRect();
          const x = (e.clientX - r.left - r.width / 2) * 0.22;
          const y = (e.clientY - r.top - r.height / 2) * 0.3;
          b.style.transform = `translate(${x}px,${y}px)`;
        });
        b.addEventListener("pointerleave", () => { b.style.transform = ""; });
      });
    }
  }

  // Form: inline validation, labelled errors, no network call (demo handler).
  const form = document.getElementById("form");
  const status = document.getElementById("status");
  const rules = {
    name: (v) => (v.trim() ? "" : "Enter your name."),
    email: (v) => (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? "" : "Enter a valid email address, like name@company.com."),
    msg: (v) => (v.trim().length >= 10 ? "" : "Add a few details about the project, at least 10 characters."),
  };
  const check = (f) => {
    const field = f.closest(".field");
    const msg = rules[f.name](f.value);
    field.toggleAttribute("data-invalid", !!msg);
    f.setAttribute("aria-invalid", msg ? "true" : "false");
    document.getElementById(f.id + "-e").textContent = msg;
    return !msg;
  };
  form.querySelectorAll("input,textarea").forEach((f) => {
    f.addEventListener("blur", () => check(f));
    f.addEventListener("input", () => f.closest(".field").hasAttribute("data-invalid") && check(f));
  });
  form.addEventListener("submit", (e) => {
    e.preventDefault();
    const fields = [...form.querySelectorAll("input,textarea")];
    const ok = fields.map(check).every(Boolean);
    if (!ok) { fields.find((f) => f.getAttribute("aria-invalid") === "true").focus(); status.textContent = ""; return; }
    // TODO: connect to a real endpoint or mail service before launch.
    status.textContent = "Thanks. Your message is ready to send once the form endpoint is connected.";
    form.reset();
  });
})();
