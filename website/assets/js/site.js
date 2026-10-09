(() => {
  const root = document.documentElement;
  root.classList.add("js");
  const reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;

  // header turns solid after scroll
  const hdr = document.querySelector(".site-header");
  const onScroll = () => hdr.classList.toggle("solid", scrollY > 40);
  addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  // mobile menu
  const burger = document.getElementById("burger");
  const menu = document.getElementById("mobile-menu");
  const setMenu = (open) => {
    burger.setAttribute("aria-expanded", open);
    burger.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menu.classList.toggle("open", open);
    document.body.style.overflow = open ? "hidden" : "";
  };
  burger.addEventListener("click", () => setMenu(burger.getAttribute("aria-expanded") !== "true"));
  menu.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => setMenu(false)));
  addEventListener("keydown", (e) => e.key === "Escape" && setMenu(false));

  // scroll reveal
  const items = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    items.forEach((e) => e.classList.add("in"));
  } else {
    const io = new IntersectionObserver((es) => es.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
    }), { threshold: 0.12, rootMargin: "0px 0px -6% 0px" });
    items.forEach((e) => io.observe(e));
  }

  // hero crossfade (skipped for reduced motion; dots let people choose)
  const slides = document.querySelectorAll(".hero-bg img");
  if (slides.length > 1) {
    const dots = document.querySelectorAll(".hero-dots button");
    let i = 0, timer;
    const show = (n) => {
      slides[i].classList.remove("active"); dots[i].removeAttribute("aria-current");
      i = n; slides[i].classList.add("active"); dots[i].setAttribute("aria-current", "true");
    };
    const start = () => { if (!reduce) timer = setInterval(() => show((i + 1) % slides.length), 6000); };
    dots.forEach((d, n) => d.addEventListener("click", () => { clearInterval(timer); show(n); start(); }));
    document.addEventListener("visibilitychange", () => { clearInterval(timer); if (!document.hidden) start(); });
    start();
  }

  // product filter (cards hide, pills report state)
  const pills = document.querySelectorAll(".pill");
  if (pills.length) {
    const cards = document.querySelectorAll("[data-cat]");
    const apply = (cat) => {
      pills.forEach((p) => p.setAttribute("aria-pressed", p.dataset.filter === cat));
      cards.forEach((c) => { c.hidden = cat !== "all" && c.dataset.cat !== cat; });
      document.querySelectorAll("[data-group]").forEach((g) => {
        g.hidden = ![...g.querySelectorAll("[data-cat]")].some((c) => !c.hidden);
      });
    };
    pills.forEach((p) => p.addEventListener("click", () => apply(p.dataset.filter)));
    const hash = location.hash.replace("#", "");
    if (["surveillance", "tactical", "agriculture"].includes(hash)) apply(hash === "surveillance" ? "Surveillance" : hash === "tactical" ? "Tactical" : "Agriculture");
  }

  // contact form: validates, then opens the visitor's email app with details filled in
  const form = document.getElementById("brief-form");
  if (form) {
    const sel = form.elements.interest;
    const wanted = new URLSearchParams(location.search).get("product");
    if (wanted) [...sel.options].forEach((o) => { if (o.dataset.slug === wanted) sel.value = o.value; });
    const rules = {
      name: (v) => (v.trim() ? "" : "Enter your name."),
      org: (v) => (v.trim() ? "" : "Enter your organisation."),
      email: (v) => (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v) ? "" : "Enter a valid email address, like name@organisation.in."),
      msg: (v) => (v.trim().length >= 10 ? "" : "Describe the requirement in at least 10 characters."),
    };
    const check = (f) => {
      const msg = rules[f.name](f.value);
      f.closest(".field").toggleAttribute("data-invalid", !!msg);
      f.setAttribute("aria-invalid", msg ? "true" : "false");
      document.getElementById(f.id + "-e").textContent = msg;
      return !msg;
    };
    const fields = [...form.querySelectorAll("[name=name],[name=org],[name=email],[name=msg]")];
    fields.forEach((f) => {
      f.addEventListener("blur", () => check(f));
      f.addEventListener("input", () => f.closest(".field").hasAttribute("data-invalid") && check(f));
    });
    form.addEventListener("submit", (e) => {
      e.preventDefault();
      const ok = fields.map(check).every(Boolean);
      const st = document.getElementById("form-status");
      if (!ok) { fields.find((f) => f.getAttribute("aria-invalid") === "true").focus(); st.textContent = ""; return; }
      const v = form.elements;
      const body = `Name: ${v.name.value}\nOrganisation: ${v.org.value}\nEmail: ${v.email.value}\nPhone: ${v.phone.value || "-"}\nInterested in: ${v.interest.value}\n\n${v.msg.value}`;
      location.href = `mailto:welcome@qoptars.com?subject=${encodeURIComponent("Technical briefing request: " + v.interest.value)}&body=${encodeURIComponent(body)}`;
      st.textContent = "Your email app should open with the request filled in. If it does not, write to welcome@qoptars.com.";
    });
  }

  const yr = document.getElementById("yr");
  if (yr) yr.textContent = new Date().getFullYear();
})();
