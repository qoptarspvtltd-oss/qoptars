#!/usr/bin/env python3
"""Generates the static Qoptars site. Run from this folder: python3 build.py
All claims and specs come from the supplied Homepage / About Us / All Products pages."""
import html, json, os

OUT = os.path.dirname(os.path.abspath(__file__))
EMAIL, PHONE, WA = "welcome@qoptars.com", "+91 97071 14708", "919707114708"
ARROW = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
e = html.escape

CATS = {
    "Surveillance": ("Surveillance & reconnaissance", "ISR, perimeter security, infrastructure monitoring"),
    "Tactical": ("Tactical operations", "Precision strike, payload delivery, persistent overwatch"),
    "Agriculture": ("Agriculture & industrial", "Precision spraying, institutional deployment"),
}

PRODUCTS = [
    dict(slug="vayu", name="Vayu", cat="Surveillance", sub="Made for inspection", img="vayu.webp",
         alt="Qoptars Vayu surveillance drone beside its ground controller",
         desc="A next-generation autonomous surveillance platform built for continuous security and industrial monitoring, with AI-assisted threat detection and real-time streaming.",
         specs=[("Camera", "4K / EO-IR / 30x"), ("Endurance", "35 min"), ("Range", "~6 km"), ("Modes", "Manual / auto")],
         uses=["Day/night surveillance", "Photogrammetry", "Perimeter security"],
         feat=["4K RGB and EO-IR payload with 30x optical zoom", "Manual or fully autonomous flight", "Runs the common Qoptars AI vision stack"]),
    dict(slug="day-surveillance-drone", name="Day Surveillance Drone", cat="Surveillance", sub="Unblinking eyes in daylight", img="day-surveillance.webp",
         alt="Qoptars day surveillance drone on its transport case",
         desc="Engineered for tactical daylight ISR, perimeter monitoring and convoy overwatch, with secure, indigenous components and real-time command transmission.",
         specs=[("Camera", "EO + laser range finder"), ("Endurance", "45–60 min"), ("Range", "15–20 km"), ("Security", "Freq-hopping")],
         uses=["ISR", "Border & perimeter security", "Convoy overwatch"],
         feat=["30x zoom EO camera with laser range finder", "Frequency-hopping communications", "Non-Chinese components"]),
    dict(slug="day-night-surveillance-drone", name="Day/Night Surveillance Drone", cat="Surveillance", sub="Relentless eyes, day or night", img="day-night-surveillance.webp",
         alt="Qoptars day/night surveillance drone with its ground controller",
         desc="Built for 24/7 ISR with dual EO and thermal sensors, combining stealthy flight and secure communications for cross-border and urban monitoring.",
         specs=[("Camera", "Dual EO + thermal"), ("Endurance", "45–60 min"), ("Range", "15–20 km"), ("Gimbal", "3-axis stabilised")],
         uses=["Cross-border surveillance", "Night reconnaissance", "Critical infrastructure"],
         feat=["Dual EO and thermal payload", "3-axis stabilised gimbal", "Secure, frequency-hopping communications"]),
    dict(slug="kamikaze-drone", name="Kamikaze Drone", cat="Tactical", sub="Precision strike platform", img="kamikaze.webp", ill=True,
         alt="Operator carrying an FPV strike drone",
         desc="An FPV loitering munition engineered for one-way offensive missions, combining speed, stealth and modular payloads for precision strikes.",
         specs=[("Payload", "Shaped charge, custom"), ("Speed", "Up to 150 km/h"), ("Range", "5–8 km"), ("Guidance", "GPS, AI, manual FPV")],
         uses=["Border defence", "Swarm operations", "Anti-armor strikes"],
         feat=["Modular payload: shaped charge, PEK or custom", "GPS, AI-assisted and manual FPV guidance"]),
    dict(slug="payload-dropping-drone", name="Payload Dropping Drone", cat="Tactical", sub="Tactical delivery, precision release", img="payload-drop.webp",
         alt="Qoptars payload dropping drone with its ground controller at dusk",
         desc="Built for tactical precision with single or dual servo-controlled release, supporting lethal and non-lethal payloads across multiple operating modes.",
         specs=[("Payload", "Up to 5 kg"), ("Release", "Single/dual servo"), ("Endurance", "Up to 45 min"), ("Range", "5–7 km (LOS)")],
         uses=["Precision delivery", "Non-lethal deployment", "Swarm ops"],
         feat=["Manual, autonomous and swarm-enabled operation", "Supports lethal and non-lethal payloads"]),
    dict(slug="tethered-drone", name="Tethered Drone", cat="Tactical", sub="Designed for police", metric=("12 hrs", "tethered endurance"),
         desc="Delivers persistent aerial coverage through a lightweight tether, supporting EO/IR cameras, comms relays or custom sensors for zero-downtime monitoring.",
         specs=[("Endurance", "Up to 12 hrs"), ("Payload", "Up to 15 kg"), ("Altitude", "Up to 200 m"), ("Mobility", "Vehicle / portable")],
         uses=["24/7 surveillance", "Disaster response", "Event security"],
         feat=["Supports EO/IR cameras, comms relays or custom sensors", "Vehicle-mounted, portable or fixed station"]),
    dict(slug="agriculture-spray-drone-10l", name="Agriculture Spray Drone 10L", cat="Agriculture", sub="Precision spraying, institutional scale", img="agri-spray.webp", ill=True,
         alt="Spray drone flying low over a green field",
         desc="Delivers precise, uniform spraying with smart automation and obstacle-aware flight, built for institutional agricultural programs.",
         specs=[("Tank", "10 L, smart flow"), ("Spray width", "Up to 5 m"), ("Flight time", "Up to 20 min"), ("Build", "IP65, radar avoidance")],
         uses=["Pesticide & fertilizer spraying", "Weed & crop care", "Precision farming"],
         feat=["Dual centrifugal nozzles", "Obstacle avoidance radar", "IP65 build"]),
]
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

def short(p):  # nav-friendly title
    return p["name"]

# ---------- shared chrome ----------
def head(R, title, desc, page):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="theme-color" content="#0a0d10">
<meta name="color-scheme" content="dark">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:type" content="website">
<link rel="icon" href="{R}assets/img/logo.png">
<link rel="preload" href="{R}assets/fonts/manrope.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{R}assets/css/site.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{header(R, page)}
'''

def header(R, page):
    def cur(p): return ' aria-current="page"' if page == p else ""
    links = [("solutions", "Solutions", f"{R}solutions.html"), ("company", "Company", f"{R}company.html"),
             ("cert", "Certifications", f"{R}company.html#certifications"), ("contact", "Contact", f"{R}contact.html")]
    nav = "".join(f'<a href="{h}"{cur(k)}>{t}</a>' for k, t, h in links)
    mob = "".join(f'<a href="{h}">{t}</a>' for k, t, h in links)
    return f'''<header class="site-header">
  <a class="logo" href="{R}index.html" aria-label="Qoptars home"><img src="{R}assets/img/logo.png" alt="Qoptars" width="116" height="28"></a>
  <nav class="nav" aria-label="Primary">{nav}</nav>
  <div class="hdr-right">
    <a class="btn btn-sm" href="{R}contact.html">Request briefing</a>
    <button class="hamburger" id="burger" aria-label="Open menu" aria-expanded="false" aria-controls="mobile-menu"><span></span><span></span><span></span></button>
  </div>
</header>
<div class="mobile-menu" id="mobile-menu">{mob}<a class="btn" href="{R}contact.html">Request briefing</a></div>
'''

def footer(R):
    return f'''<footer class="site-footer">
  <div class="wrap">
    <div class="foot">
      <div><a class="logo" href="{R}index.html"><img src="{R}assets/img/logo.png" alt="Qoptars" width="108" height="26"></a>
        <p>Qoptars Private Limited<br>TIP, IIT Hyderabad, Telangana</p></div>
      <div><h4>Solutions</h4>
        <a href="{R}solutions.html#surveillance">Surveillance &amp; reconnaissance</a>
        <a href="{R}solutions.html#tactical">Tactical operations</a>
        <a href="{R}solutions.html#agriculture">Agriculture &amp; industrial</a></div>
      <div><h4>Company</h4>
        <a href="{R}company.html">About</a>
        <a href="{R}company.html#certifications">Certifications</a>
        <a href="{R}company.html#team">Team</a></div>
      <div><h4>Contact</h4>
        <a href="tel:+919707114708">{PHONE}</a>
        <a href="mailto:{EMAIL}">{EMAIL}</a></div>
    </div>
    <div class="foot-bottom"><span>&copy; <span id="yr">2026</span> Qoptars Private Limited. All rights reserved.</span></div>
  </div>
</footer>
<a class="wa" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="Chat on WhatsApp"><svg width="28" height="28" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2 22l5.29-1.39c1.45.79 3.08 1.21 4.75 1.21h.01c5.46 0 9.91-4.45 9.91-9.91 0-2.65-1.03-5.14-2.9-7.01A9.87 9.87 0 0012.04 2m0 1.8c2.15 0 4.16.84 5.68 2.36a7.98 7.98 0 012.35 5.67c0 4.42-3.6 8.02-8.03 8.02a8.01 8.01 0 01-4.08-1.11l-.29-.17-3.03.8.81-2.95-.19-.3a7.96 7.96 0 01-1.23-4.26c0-4.42 3.6-8.06 8.02-8.06"/></svg></a>
<script src="{R}assets/js/site.js" defer></script>
</body>
</html>
'''

def cta(R, title="Ready to talk requirements?", text="Speak with our team about specifications, deployment, or procurement through GeM."):
    return f'''<section class="cta"><div class="wrap"><h2 class="reveal">{title}</h2><p class="reveal" style="--d:.05s">{text}</p>
<a class="btn reveal" style="--d:.1s" href="{R}contact.html">Request briefing</a></div></section>'''

def card(R, p):
    href = f"{R}solutions/{p['slug']}.html"
    if "img" in p:
        ill = '<span class="ill">Illustrative image</span>' if p.get("ill") else ""
        media = f'<div class="card-img"><span class="tag">{p["cat"]}</span><img src="{R}assets/img/{p["img"]}" alt="{e(p["alt"])}" loading="lazy" width="1400" height="900">{ill}</div>'
    else:
        big, small = p["metric"]
        media = f'<div class="card-img metric-img"><span class="tag">{p["cat"]}</span><b>{big}</b><span>{small}</span></div>'
    specs = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["specs"])
    return f'''<article class="card reveal" data-cat="{p["cat"]}">{media}
<div class="card-body"><h3>{e(p["name"])}</h3><p class="sub">{e(p["sub"])}</p><dl class="specs">{specs}</dl>
<a class="link-arrow" href="{href}" aria-label="View {e(p["name"])} details">View details {ARROW}</a></div></article>'''

def page(path, R, title, desc, pg, body):
    full = head(R, title, desc, pg) + '<main id="main">\n' + body + "\n</main>\n" + footer(R)
    os.makedirs(os.path.dirname(os.path.join(OUT, path)), exist_ok=True)
    with open(os.path.join(OUT, path), "w", encoding="utf-8") as f:
        f.write(full)

def page_head(R, crumb, h1, lede):
    return f'''<section class="page-head"><div class="wrap">
<p class="crumbs"><a href="{R}index.html">Home</a> / {crumb}</p><h1>{h1}</h1><p class="lede">{lede}</p></div></section>'''

# ---------- Home ----------
def home():
    R = ""
    fork = [("Defence & paramilitary", "Operational specs and deployment", "solutions.html#tactical"),
            ("Government & PSU", "Compliance and certifications", "company.html#certifications"),
            ("GeM procurement", "OEM status and listings", "company.html#certifications"),
            ("International", "Export posture and capacity", "contact.html")]
    forks = "".join(f'<a href="{h}"><h3>{t}{ARROW}</h3><p>{s}</p></a>' for t, s, h in fork)
    why = [("End-to-end manufacturing", "From airframe to flight software, designed and built in-house, not assembled from unverified imports."),
           ("Field-tested reliability", "Rugged, secure, repairable designs engineered for continuous operation in demanding environments."),
           ("Procurement-ready", "GeM OEM status and documentation built around how defence and PSU buyers evaluate vendors."),
           ("Secure by design", "Encrypted, frequency-hopping communications and non-Chinese components across the surveillance line."),
           ("Software-defined and AI-native", "One common autonomy and vision stack on every platform, updated in software, not just hardware.")]
    whyh = "".join(f'<div class="why-card{" hi" if i == 4 else ""}"><p class="n">0{i+1}</p><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate(why))
    badges = [("gem.png", "GeM OEM"), ("iith.png", "i-TIC, IIT Hyderabad"), ("msme.png", "MSME"), ("dpiit.png", "DPIIT recognised")]
    badgeh = "".join(f'<div class="badge"><img src="assets/img/{i}" alt="" loading="lazy">{t}</div>' for i, t in badges)
    pills = '<div class="pills reveal" role="group" aria-label="Filter platforms">' + "".join(
        f'<button class="pill" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>'
        for k, l in [("all", "All"), ("Surveillance", "Surveillance"), ("Tactical", "Tactical"), ("Agriculture", "Agriculture")]) + "</div>"
    logos = [("iith.png", "IIT Hyderabad"), ("iiitdm.png", "IIITDM Kurnool"), ("ntpc.png", "NTPC"), ("amrita.png", "Amrita"), ("gem.png", "Government e-Marketplace")]
    logoh = "".join(f'<img src="assets/img/{i}" alt="{a}" loading="lazy">' for i, a in logos)
    body = f'''<section class="hero" aria-label="Introduction">
  <div class="hero-bg">
    <img class="active" src="assets/img/hero-1.webp" alt="Qoptars surveillance drone in flight with an operator behind it" fetchpriority="high" width="1600" height="1066">
    <img src="assets/img/hero-2.webp" alt="Qoptars drone hovering over grass" width="1600" height="1067">
    <img src="assets/img/hero-3.webp" alt="Qoptars drone and ground control unit in the field" width="1600" height="1200">
  </div>
  <div class="hero-inner">
    <p class="eyebrow">Indigenous UAV manufacturer · Made in India</p>
    <h1>Precision drones for defence, government and industry</h1>
    <p class="lede">GeM-registered OEM incubated at IIT Hyderabad. Designed and built in India for Army, police, PSU and industry.</p>
    <div class="cta-row"><a class="btn" href="solutions.html">Explore solutions</a><a class="btn btn-ghost" href="contact.html">Request briefing</a></div>
  </div>
  <div class="hero-dots" role="group" aria-label="Choose hero image"><button type="button" aria-label="Image 1" aria-current="true"></button><button type="button" aria-label="Image 2"></button><button type="button" aria-label="Image 3"></button></div>
</section>

<nav class="wrap fork" aria-label="Who we serve">{forks}</nav>

<section class="section" id="company"><div class="wrap split">
  <figure class="photo reveal"><img src="assets/img/hero-3.webp" alt="Qoptars team field operation with a drone and controller" loading="lazy" width="1600" height="1200">
    <figcaption class="stat"><b>6+</b><span>Active platforms</span></figcaption></figure>
  <div class="reveal" style="--d:.08s">
    <h2>Engineering aerial intelligence for missions that can't afford to fail</h2>
    <p>Qoptars designs and manufactures autonomous UAV systems for surveillance, tactical operations and precision agriculture, built to operate reliably in the field, not just on a spec sheet.</p>
    <p>Every platform runs on one onboard AI vision stack: real-time EO/IR video processing, object detection and classification, and autonomous tracking computed at the edge.</p>
    <p class="caption">Founded 2019, Hyderabad · 10+ institutional relationships</p>
    <div class="badges">{badgeh}</div>
  </div></div></section>

<section class="section alt"><div class="wrap">
  <div class="sec-head"><h2 class="reveal">Built for the field, not the demo</h2>
    <p class="reveal" style="--d:.06s">A software-defined drone company at the core. The same AI-native mission stack scales across every platform.</p></div>
  <div class="why-grid reveal">{whyh}</div></div></section>

<section class="ai"><img src="assets/img/hero-2.webp" alt="" loading="lazy" width="1600" height="1067">
  <div class="wrap"><div class="reveal" style="max-width:600px">
    <h2>AI autonomy on every platform</h2>
    <p>A common onboard stack for real-time detection, tracking and autonomous decision-making, purpose-built for defence and industrial edge cases.</p>
    <ul class="checks"><li>Real-time EO/IR video processing</li><li>Object detection and classification</li><li>Autonomous tracking, computed at the edge</li></ul>
    <a class="btn btn-ghost" href="solutions.html">See the platforms</a></div></div></section>

<section class="section" id="solutions"><div class="wrap">
  <div class="sec-head"><h2 class="reveal">Solutions across the mission</h2>
    <p class="reveal" style="--d:.06s">Surveillance, tactical operations and precision agriculture platforms.</p></div>
  {pills}
  <div class="grid feat-last">{"".join(card(R, p) for p in PRODUCTS)}</div></div></section>

<section class="section alt" style="padding-block:64px"><div class="wrap reveal"><div class="logos">{logoh}</div></div></section>
{cta(R)}'''
    page("index.html", R, "Qoptars | Indigenous UAV systems for defence, government and industry",
         "Qoptars designs and manufactures autonomous UAV systems in India for defence, government, PSU and industrial operations. GeM-registered OEM, incubated at IIT Hyderabad.", "home", body)

# ---------- Solutions ----------
def solutions():
    R = ""
    groups = ""
    for k, (title, sub) in CATS.items():
        items = [p for p in PRODUCTS if p["cat"] == k]
        groups += f'''<div data-group id="{k.lower()}" style="margin-bottom:72px"><div class="sec-head" style="margin-bottom:28px"><h2 class="reveal" style="font-size:clamp(1.5rem,2.6vw,2rem)">{title}</h2><p class="reveal">{sub}</p></div>
<div class="grid {"two" if len(items) == 2 else ""}">{"".join(card(R, p) for p in items)}</div></div>'''
    pills = '<div class="pills" role="group" aria-label="Filter platforms">' + "".join(
        f'<button class="pill" type="button" data-filter="{k}" aria-pressed="{"true" if k == "all" else "false"}">{l}</button>'
        for k, l in [("all", "All products"), ("Surveillance", "Surveillance & reconnaissance"), ("Tactical", "Tactical operations"), ("Agriculture", "Agriculture & industrial")]) + "</div>"
    body = page_head(R, "Solutions", "Platforms for surveillance, tactical operations and agriculture",
                     "Every platform is designed, engineered and assembled in India, with the same onboard AI vision stack across the line.") + f'''
<section class="section" style="padding-top:56px"><div class="wrap">{pills}{groups}</div></section>
{cta(R, "Need a spec sheet for a specific mission?", "Tell us the requirement and we will walk you through which platform fits.")}'''
    page("solutions.html", R, "Solutions | Qoptars UAV platforms", "Seven UAV platforms from Qoptars: surveillance, tactical and agricultural drones designed and built in India.", "solutions", body)

# ---------- Product pages ----------
def product(p):
    R = "../"
    if "img" in p:
        ill = '<span class="ill">Illustrative image</span>' if p.get("ill") else ""
        media = f'<figure class="photo"><img src="{R}assets/img/{p["img"]}" alt="{e(p["alt"])}" width="1400" height="1000" fetchpriority="high">{ill}</figure>'
    else:
        big, small = p["metric"]
        media = f'<figure class="photo"><div class="metric-img"><b>{big}</b><span>{small}</span></div></figure>'
    specs = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in p["specs"])
    uses = "".join(f"<li>{e(u)}</li>" for u in p["uses"])
    feat = "".join(f"<li>{e(f)}</li>" for f in p["feat"])
    others = [q for q in PRODUCTS if q["slug"] != p["slug"] and q["cat"] == p["cat"]]
    others += [q for q in PRODUCTS if q["slug"] != p["slug"] and q["cat"] != p["cat"]]
    rel = "".join(card(R, q) for q in others[:3])
    cat_title = CATS[p["cat"]][0]
    body = f'''<section class="page-head"><div class="wrap">
<p class="crumbs"><a href="{R}index.html">Home</a> / <a href="{R}solutions.html">Solutions</a> / {e(p["name"])}</p>
<div class="pd"><div><p class="eyebrow">{cat_title}</p><h1 style="font-size:clamp(2rem,4.2vw,3.3rem)">{e(p["name"])}</h1>
<p class="sub" style="margin-top:14px">{e(p["sub"])}</p><p class="pd-desc">{e(p["desc"])}</p>
<div class="cta-row"><a class="btn" href="{R}contact.html?product={p["slug"]}">Request briefing</a><a class="btn btn-ghost" href="{R}solutions.html">All solutions</a></div></div>{media}</div></div></section>

<section class="section" style="padding-bottom:0"><div class="wrap"><h2 class="reveal" style="margin-bottom:32px">Key specifications</h2>
<dl class="spec-grid reveal">{specs}</dl>
<p class="muted reveal" style="margin-top:16px;font-size:14px">Headline figures only. Full specification sheets are shared in a technical briefing.</p></div></section>

<section class="section"><div class="wrap split" style="align-items:start">
<div class="reveal"><h2 style="margin-bottom:24px">Built for</h2><ul class="uses">{uses}</ul></div>
<div class="reveal" style="--d:.08s"><h2 style="margin-bottom:24px">What sets it apart</h2><ul class="feat">{feat}<li>Shares the common Qoptars AI vision and autonomy stack</li></ul></div></div></section>

<section class="section alt"><div class="wrap"><div class="sec-head"><h2 class="reveal">Other platforms</h2></div><div class="grid">{rel}</div></div></section>
{cta(R)}'''
    page(f"solutions/{p['slug']}.html", R, f"{p['name']} | Qoptars", f"{p['name']}: {p['desc']}", "solutions", body)

# ---------- Company ----------
def company():
    R = ""
    team = [("MP", "Manash P", "Founder & CEO", "Leads product strategy, BD and procurement."),
            ("P", "Pritam", "Co-founder & CTO", "Leads engineering across flight stack and AI vision."),
            ("R", "Rohan", "Product Lead", "Owns spec and definition across product lines."),
            ("A", "Ashwin", "Advisor & Investor", "India CEO, ex-Fusion Inc. IIT Hyderabad."),
            ("DS", "Dr. Saroj", "Mentor", "Sr. Data Scientist, DCS. IIT Mandi."),
            ("T", "Tushar", "Mentor", "Dir. Engineering, Google. Ex-CIO, Fitbit.")]
    teamh = "".join(f'<article class="card person reveal" style="--d:{(i%3)*.06}s"><div class="mono-av" aria-hidden="true">{a}</div><div><h3>{n}</h3><p class="role">{r}</p><p>{d}</p></div></article>' for i, (a, n, r, d) in enumerate(team))
    caps = [("Defence & security", "ISR and tactical platforms built for contested environments.", ["Surveillance", "Tactical strike", "Reconnaissance", "Threat detection"]),
            ("Industrial inspection", "Aerial diagnostics that catch failures before they cost you.", ["Infrastructure monitoring", "Industrial security", "Maintenance & reporting", "Progress monitoring"]),
            ("Traffic & urban management", "Real-time oversight for cities that can't pause to check.", ["Waste management", "Traffic management", "Crowd monitoring", "Construction progress"]),
            ("Agriculture", "Precision inputs that protect yield and cut waste.", ["Precision farming", "Pesticide spraying", "Granular seeding", "Crop & disease detection"])]
    caph = "".join(f'<article class="card cap reveal" style="--d:{(i%2)*.06}s"><p class="n">0{i+1}</p><h3>{t}</h3><p>{d}</p><ul>{"".join(f"<li>{x}</li>" for x in l)}</ul></article>' for i, (t, d, l) in enumerate(caps))
    certs = [("gem.png", "GeM OEM", "Registered Original Equipment Manufacturer on the Government e-Marketplace."),
             ("msme.png", "MSME", "Registered micro, small and medium enterprise, Make in India."),
             ("dpiit.png", "DPIIT recognised", "Recognised under Startup India."),
             (None, "IEC", "Import Export Code registered for cross-border engagement.")]
    certh = "".join(f'<article class="card cert reveal" style="--d:{(i%4)*.05}s">' + (f'<img src="assets/img/{im}" alt="" loading="lazy">' if im else '<div class="ico">IEC</div>') + f'<h3>{t}</h3><p>{d}</p></article>' for i, (im, t, d) in enumerate(certs))
    body = page_head(R, "Company", "Engineering aerial intelligence for the missions that can't afford to fail",
                     "Founded in 2019 and incubated at i-TIC, IIT Hyderabad, Qoptars designs and manufactures autonomous UAV systems for defence, government and industrial operations.") + f'''
<section class="section"><div class="wrap split">
  <div class="reveal"><h2>Built around a simple test: does it work in the field, not just in the demo</h2>
    <p>Qoptars started as a small engineering team working out of i-TIC, IIT Hyderabad, building UAV platforms for defence, paramilitary and industrial use. The brief has not changed since: every system has to survive contact with a real deployment, not just a controlled trial.</p>
    <p>That means designing and manufacturing in-house rather than reselling imported components, and building one common AI and autonomy stack that scales across every product line.</p>
    <div class="cta-row" style="margin-top:28px"><a class="btn" href="solutions.html">Explore solutions</a><a class="btn btn-ghost" href="contact.html">Contact us</a></div></div>
  <figure class="photo reveal" style="--d:.08s"><img src="assets/img/hero-1.webp" alt="Qoptars drone in flight with an operator holding the controller" loading="lazy" width="1600" height="1066"><figcaption class="stat"><b>2019</b><span>Founded, Hyderabad</span></figcaption></figure></div></section>

<section class="wrap reveal"><div class="numbers"><div><b>6+</b><span>Active platforms</span></div><div><b>10+</b><span>Institutional relationships</span></div><div><b>2019</b><span>Founded, Hyderabad</span></div><div><b>GeM</b><span>Registered OEM</span></div></div></section>

<section class="section"><div class="wrap"><h2 class="dream reveal" style="max-width:30ch">A safer, smarter, more connected world, where operators aren't risking themselves to do what a drone can do better.</h2>
<div class="dream-more reveal"><p>Disaster response teams with eyes before they arrive. Industries catching failures before they become losses. Farmers covering more ground with less effort.</p>
<p>And soldiers equipped with precise, dependable technology built for the terrain they actually operate in. Every platform we ship is a step toward that.</p></div></div></section>

<section class="section alt"><div class="wrap"><div class="sec-head"><h2 class="reveal">A complete range, one common stack</h2>
<p class="reveal">Fully autonomous systems, high-speed FPVs and mission-specific UAVs, integrating AI analytics, real-time data links and advanced sensors.</p></div>
<div class="grid two">{caph}</div></div></section>

<section class="section" id="certifications"><div class="wrap"><div class="sec-head"><h2 class="reveal">Verified foundation</h2>
<p class="reveal">Incubated at the Technology Innovation Park, IIT Hyderabad, with direct access to the research, testing and academic infrastructure behind every platform.</p></div>
<div class="grid four">{certh}</div>
<div class="note-card reveal"><b>DGCA type certification</b><span>Not yet held. We state this plainly rather than leave it ambiguous. Get in touch if certification status affects your evaluation.</span></div></div></section>

<section class="section alt" id="team"><div class="wrap"><div class="sec-head"><h2 class="reveal">The team behind the airframes</h2>
<p class="reveal">A small core team backed by advisors from industry and academia.</p></div><div class="team">{teamh}</div></div></section>
{cta(R, "Want to talk to the team directly?")}'''
    page("company.html", R, "Company | Qoptars", "Qoptars was founded in 2019 and is incubated at i-TIC, IIT Hyderabad. GeM OEM, MSME and DPIIT recognised UAV manufacturer.", "company", body)

# ---------- Contact ----------
def contact():
    R = ""
    opts = '<option value="General enquiry">General enquiry</option>' + "".join(f'<option value="{e(p["name"])}" data-slug="{p["slug"]}">{e(p["name"])}</option>' for p in PRODUCTS)
    def field(i, label, typ="text", help_="", auto="", req=True):
        return f'<div class="field"><label for="{i}">{label}</label><input id="{i}" name="{i}" type="{typ}"{f" autocomplete={chr(34)}{auto}{chr(34)}" if auto else ""} aria-describedby="{i}-h {i}-e"{" required" if req else ""}><p class="help" id="{i}-h">{help_}</p><p class="err" id="{i}-e" role="alert"></p></div>'
    body = page_head(R, "Contact", "Request a technical briefing", "Speak with our team about specifications, deployment, or procurement through GeM.") + f'''
<section class="section" style="padding-top:64px"><div class="wrap contact">
<div class="reveal"><h2>Talk to us directly</h2><dl>
<div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
<div><dt>Phone</dt><dd><a href="tel:+919707114708">{PHONE}</a></dd></div>
<div><dt>WhatsApp</dt><dd><a href="https://wa.me/{WA}" rel="noopener">Message the team</a></dd></div>
<div><dt>Address</dt><dd>Qoptars Private Limited<br>TIP, IIT Hyderabad, Telangana</dd></div></dl></div>
<form class="form reveal" id="brief-form" novalidate style="--d:.08s">
<div class="row2">{field("name", "Name", auto="name")}{field("org", "Organisation", auto="organization")}</div>
<div class="row2">{field("email", "Work email", "email", "We only use this to reply.", "email")}{field("phone", "Phone (optional)", "tel", "", "tel", False)}</div>
<div class="field"><label for="interest">Interested in</label><select id="interest" name="interest">{opts}</select></div>
<div class="field"><label for="msg">Requirement</label><textarea id="msg" name="msg" required aria-describedby="msg-h msg-e"></textarea><p class="help" id="msg-h">Mission, quantity, timeline and whether you buy through GeM.</p><p class="err" id="msg-e" role="alert"></p></div>
<button class="btn" type="submit">Send request</button>
<p class="status" id="form-status" role="status" aria-live="polite"></p>
</form></div></section>'''
    page("contact.html", R, "Contact | Qoptars", "Request a technical briefing from Qoptars about specifications, deployment or GeM procurement.", "contact", body)

if __name__ == "__main__":
    home(); solutions(); company(); contact()
    for p in PRODUCTS: product(p)
    print("built", 4 + len(PRODUCTS), "pages")
