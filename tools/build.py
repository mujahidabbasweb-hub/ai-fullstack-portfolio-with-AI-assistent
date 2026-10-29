"""Generates every page. Edit SETTINGS / PROJECTS, then run:  python tools/build.py"""
import json, os, html, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------- SETTINGS ----------------
BASE = "https://mujahidabbasweb.netlify.app"
NAME = "Mujahid Abbas"
WA = "923219153891"
PHONE = "+92 321 9153891"
EMAIL = "mujahidabbas.offical@gmail.com"
LOCATION = "Rawalpindi / Islamabad, Pakistan (remote worldwide)"
SOCIALS = {"LinkedIn": "https://www.linkedin.com/in/mujahid-abbas-dev", "GitHub": "https://github.com/mujahidabbasweb-hub"}
LIVE = {
    "casameds": "https://casameds.com",
    "cafebliss": "https://cafebliss-demo.netlify.app/",
    "clinix": "https://clinix.infinityfreeapp.com/",
    "palettify": "https://palettifyai.infinityfreeapp.com/",
}  # live URLs by project key
ME = "/images/myimage/mujahid-abbas.webp"
CERT = "/images/certificates/npxsoft-web-development-certificate.webp"
DATE = "2026-10-14"
AREAS = [{"@type": t, "name": n} for t, n in [("City", "New York"), ("City", "London"), ("City", "Dubai"), ("City", "Riyadh"), ("Country", "United States"), ("Country", "United Kingdom"), ("Country", "United Arab Emirates"), ("Country", "Saudi Arabia")]]
# ------------------------------------------

E = html.escape
def fname(p): return "404.html" if p == "/404.html" else ("index.html" if p == "/" else p.strip("/").replace("/", "-") + ".html")
def clean(p): return "/" if p == "/" else "/" + fname(p)[:-5]
def rel(m):
    a, u = m.group(1), m.group(2); b, _, h = u.partition("#")
    r = "css/style.css" if b == "/assets/css/style.css" else "js/script.js" if b == "/assets/js/site.js" else b[1:] if b.startswith("/images/") else fname(b)
    return f'{a}="{r}' + ("#" + h if h else "") + '"'
NAV = [("Home", "/"), ("About", "/about/"), ("Services", "/services/"), ("Projects", "/projects/"), ("Blog", "/blog/"), ("Contact", "/contact/")]
SOC = {k: v for k, v in SOCIALS.items() if v}
TEL = PHONE.replace(" ", "")
WAURL = f"https://wa.me/{WA}?text=Hi%20Mujahid,%20I%20want%20to%20discuss%20a%20project!"
STACK = ["Laravel", "Flutter", "Dart", "Firebase", "n8n", "Zapier", "Make", "OpenAI APIs", "Claude Code", "WordPress", "WooCommerce", "MySQL"]
SKILLS = [("AI and workflows", ["n8n", "Zapier", "Make", "Cursor IDE", "Claude Code", "GitHub Copilot", "OpenAI and LLM APIs"]),
          ("Web and mobile", ["Flutter", "Dart", "Firebase", "PHP", "Laravel", "MySQL", "REST APIs", "JavaScript"]),
          ("CMS and cloud", ["WordPress", "Elementor Pro", "WooCommerce", "cPanel", "SSL", "Page speed 90+"])]
PROJECTS = [
 dict(k="almalitha", img="/images/projects/al-malitha-trading-contracting-website.webp", w=1376, h=768, tag="Corporate website", title="Al Malitha Trading & Contracting",
  alt="Al Malitha Trading and Contracting website on laptop, tablet and phone", desc="Responsive corporate website for a GRP water tank, waterproofing and construction company, with clear service sections and a direct contact path.", chips=["GRP water tanks", "Waterproofing", "Construction"]),
 dict(k="casameds", img="/images/projects/casameds-healthcare-website.webp", w=1376, h=768, tag="Healthcare website", title="CasaMeds",
  alt="CasaMeds healthcare website showing online consultations and medicine delivery", desc="Healthcare website offering online consultations, prescription delivery and medicine delivery, with a customer account login.", chips=["Healthcare", "Online consultations", "Account login"]),
 dict(k="icsst", img="/images/projects/icsst-fire-safety-training-platform.webp", w=1376, h=768, tag="E-learning platform", title="ICSST: Institute of Civil Safety & Security Training",
  alt="ICSST online fire safety training platform with course dashboard", desc="Online training platform for fire safety and emergency response courses, with certification and a course dashboard.", chips=["E-learning", "Certification", "Course dashboard"]),
 dict(k="nishat", img="/images/projects/ar-academy-nishat-learning-portal.webp", w=1376, h=768, tag="Education website", title="AR Academy Nishat",
  alt="AR Academy Nishat interactive learning portal on desktop and mobile", desc="Interactive learning portal for a Cambridge IGCSE and O-Level academy, with faculty profiles, student success stories and online resources.", chips=["Cambridge IGCSE / O-Level", "Faculty profiles", "Online resources"]),
 dict(k="orhan", img="/images/projects/orhan-contracting-website.webp", w=1536, h=1024, tag="Corporate website", title="Orhan Contracting",
  alt="Orhan Contracting corporate website for construction, residential and industrial services", desc="Corporate website for a contracting company covering construction, residential, industrial and design-and-build services.", chips=["Construction", "Residential", "Industrial", "Design & build"]),
 dict(k="grandarab", img="/images/projects/grand-arab-corporate-branding.webp", w=1672, h=941, tag="Corporate branding and web", title="Grand Arab",
  alt="Grand Arab corporate brand signage in front of a Gulf city skyline", desc="Corporate web presence and brand visuals for Grand Arab.", chips=["Corporate", "Branding"]),
 dict(k="cafebliss", img="/images/projects/cofeeills.webp", w=1896, h=816, tag="Cafe website", title="Cafe Bliss",
  alt="Cafe Bliss coffee shop website", desc="A polished cafe website that presents the brand, coffee offerings and a welcoming browsing experience.", chips=["Cafe", "Coffee", "Responsive website"]),
 dict(k="clinix", img="/images/projects/clinix.webp", w=1904, h=810, tag="Healthcare website", title="Clinix",
  alt="Clinix healthcare website", desc="A healthcare website that presents clinic services and helps visitors find care information in a clear, accessible layout.", chips=["Healthcare", "Clinic", "Responsive website"]),
 dict(k="palettify", img="/images/projects/Plattifyai_colour_picker.webp", w=1920, h=876, tag="AI color tool", title="Palettify AI",
  alt="Palettify AI color palette tool", desc="An AI-powered color palette tool for exploring and creating coordinated color combinations for design projects.", chips=["AI", "Color palettes", "Design tool"]),
]

def faq(items):
    h = '<div class="faq">' + "".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in items) + "</div>"
    ld = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}
    return h, ld

FAQ_GEN = [
    ("Who is Mujahid Abbas?", "Mujahid Abbas is a full-stack developer and AI solutions specialist based in Rawalpindi / Islamabad, Pakistan. He builds AI web apps, custom SaaS, Laravel and Flutter products, and n8n, Zapier and Make automations for clients worldwide."),
    ("What services does Mujahid Abbas offer?", "He offers custom Laravel web apps and SaaS, Flutter mobile apps, OpenAI and LLM integrations, workflow automation with n8n, Zapier and Make, and WordPress and WooCommerce development with page speed optimization."),
    ("Does Mujahid Abbas work with clients in the US, UK and Gulf?", "Yes. He works remotely with startups and enterprises in the United States, the United Kingdom and the Gulf (GCC), including clients in New York, London, Dubai and Riyadh."),
    ("Can Mujahid Abbas automate business workflows with n8n, Zapier or Make?", "Yes. He builds automations that connect CRMs, email, forms, databases and AI models so repetitive tasks run without manual work."),
    ("How do I contact Mujahid Abbas?", f"Email {EMAIL}, message {PHONE} on WhatsApp, or use the Hire Me page. The brief form opens WhatsApp with your message ready to send."),
]
FAQ_SVC = [
    ("What is the difference between a Laravel web app and a WordPress site?", "A Laravel web app is custom-built for specific business logic such as bookings, billing or user roles. WordPress suits content sites and stores where existing plugins cover most needs."),
    ("Can one Flutter app run on both Android and iOS?", "Yes. Flutter uses a single codebase to build for both platforms, which usually reduces build time and maintenance effort compared with two native apps."),
    ("Can you add AI features to an existing product?", "Yes. Typical additions are chat assistants, document processing and smart search using OpenAI or other LLM APIs, connected to your app through secure APIs."),
    ("Can you automate my workflows with n8n, Zapier or Make?", "Yes. Typical automations connect forms, CRMs, email, spreadsheets and databases, and can include AI steps such as classification or summarizing."),
    ("Do you fix or speed up an existing website?", "Yes. Speed tuning toward 90+ page speed benchmarks, bug fixing and security hardening are available for WordPress, WooCommerce and Laravel projects."),
]
FAQ_HIRE = [
    ("How do I hire Mujahid Abbas?", "Fill in the brief on this page. It opens WhatsApp with your message ready to send, and the conversation continues there. You can also email " + EMAIL + "."),
    ("What should I include in my project brief?", "Describe your goal, who will use the product, the platforms you need (web, Android, iOS), any tools you want connected and your deadline. A rough budget helps with planning."),
    ("Do you work on fixed-price projects or ongoing work?", "Both. A fixed scope suits a defined product, and ongoing remote work suits products that keep growing."),
    ("Will I own the code?", "Ownership terms are agreed in writing before work starts, so you know exactly what you receive."),
]

def cta(title="Have a project in mind?", text="Send a short brief and get a reply on WhatsApp with questions and next steps."):
    return f'''<div class="wrap" style="margin-top:clamp(40px,6vw,80px)"><div class="cta"><div><h2>{title}</h2><p style="margin-top:14px">{text}</p></div>
<div class="row"><a class="btn p" href="/hire-me/">Hire me</a><a class="btn g" style="background:transparent;color:#fff;border-color:rgba(255,255,255,.35)" href="{WAURL}" target="_blank" rel="noopener">WhatsApp</a></div></div></div>'''

def bento():
    return '''<div class="bento">
<a class="bx w d" href="/services/#web"><span class="ic">W</span><h3>Custom web apps and SaaS</h3><p>Laravel and PHP platforms with secure roles, dashboards and clean REST APIs, built to scale with your customers.</p><ul class="chips"><li>Laravel</li><li>PHP</li><li>MySQL</li><li>REST APIs</li></ul></a>
<a class="bx" href="/services/#mobile"><span class="ic">F</span><h3>Flutter mobile apps</h3><p>Android and iOS apps in Flutter and Dart with Firebase.</p></a>
<a class="bx t" href="/services/#ai"><span class="ic">AI</span><h3>AI solutions</h3><p>OpenAI and LLM integrations, assistants and smart features.</p></a>
<a class="bx" href="/services/#auto"><span class="ic">n8n</span><h3>Workflow automation</h3><p>n8n, Zapier and Make workflows that remove repetitive work.</p></a>
<a class="bx" href="/services/#wp"><span class="ic">WP</span><h3>WordPress and WooCommerce</h3><p>Elementor Pro sites and stores tuned for 90+ page speed.</p></a></div>'''

def skills():
    return '<div class="skills">' + "".join(f'<div class="glass"><h3>{t}</h3><ul class="chips">{"".join(f"<li>{i}</li>" for i in items)}</ul></div>' for t, items in SKILLS) + '</div>'

def pgrid(n=None):
    out = ""
    for p in PROJECTS[:n]:
        live = LIVE.get(p["k"])
        btn = f'<a class="btn g" href="{live}" target="_blank" rel="noopener">Visit live site</a>' if live else ""
        chips = "".join(f"<li>{E(c)}</li>" for c in p["chips"])
        out += f'<article class="pc"><div class="pimg"><img src="{p["img"]}" alt="{E(p["alt"])}" width="{p["w"]}" height="{p["h"]}" loading="lazy" decoding="async"></div><div class="pbody"><span class="tag">{E(p["tag"])}</span><h3>{E(p["title"])}</h3><p>{E(p["desc"])}</p><ul class="chips">{chips}</ul>{btn}</div></article>'
    return '<div class="pgrid">' + out + '</div>'

STEPS = '''<ol class="steps"><li><h3>Scope</h3><p>We agree on goals, users and what ships first.</p></li><li><h3>Design</h3><p>Screens, data model and automations are planned before any code.</p></li><li><h3>Build</h3><p>Laravel, Flutter or n8n, tested as it grows.</p></li><li><h3>Launch</h3><p>Deployment, handover and fixes after go-live.</p></li></ol>'''

def form(budget=False):
    b = '<div class="fld"><label for="bd">Budget range</label><select id="bd" name="budget"><option value="">Not sure yet</option><option>Under $500</option><option>$500 to $2,000</option><option>$2,000 to $5,000</option><option>Above $5,000</option></select></div>' if budget else ""
    return f'''<div class="formbox" data-wa-form><div class="fld"><label for="nm">Your name</label><input id="nm" name="name" autocomplete="name" placeholder="Ayesha Khan"></div>
<div class="fld"><label for="ty">Project type</label><select id="ty" name="type"><option>Custom web app or SaaS</option><option>Flutter mobile app</option><option>AI solution or LLM integration</option><option>Workflow automation (n8n, Zapier, Make)</option><option>WordPress or WooCommerce site</option><option>Something else</option></select></div>{b}
<div class="fld"><label for="ms">What do you need?</label><textarea id="ms" name="msg" placeholder="An AI-assisted booking platform for my clinics, with an admin dashboard."></textarea></div>
<a class="btn l" data-wa-send href="{WAURL}" target="_blank" rel="noopener">Send on WhatsApp</a><p class="hint">Opens WhatsApp with your message filled in. Nothing is stored on this site.</p></div>'''

def person():
    p = {"@type": "Person", "@id": BASE + "/#person", "name": NAME, "url": BASE + "/", "image": BASE + ME, "jobTitle": "Full-Stack Developer and AI Solutions Specialist",
         "email": "mailto:" + EMAIL, "telephone": TEL, "areaServed": AREAS,
         "description": "Full-stack developer and AI solutions specialist building AI web apps, SaaS, Laravel and Flutter products and n8n, Zapier and Make automations.",
         "address": {"@type": "PostalAddress", "addressLocality": "Rawalpindi", "addressRegion": "Punjab", "addressCountry": "PK"},
         "knowsAbout": ["Laravel", "Flutter", "Dart", "Firebase", "PHP", "MySQL", "REST APIs", "n8n", "Zapier", "Make", "OpenAI API", "LLM integration", "WordPress", "WooCommerce", "SaaS development", "AI automation"],
         "hasCredential": {"@type": "EducationalOccupationalCredential", "name": "Certificate of Professional Excellence in Web Development", "credentialCategory": "certificate", "recognizedBy": {"@type": "Organization", "name": "NPXSoft Engineering Group"}}}
    if SOC: p["sameAs"] = list(SOC.values())
    return p

OFFERS = {"@type": "OfferCatalog", "name": "Development services", "itemListElement": [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": n}} for n in ["Custom Laravel web apps and SaaS", "Flutter mobile apps", "AI and LLM integration", "Workflow automation with n8n, Zapier and Make", "WordPress and WooCommerce development"]]}
PAGES = []
def page(path, title, desc, body, ld=None, crumbs=None, og=None, ptype="website", is_home=False, nonindex=False):
    graph = [person()]
    if is_home:
        graph += [{"@type": "WebSite", "@id": BASE + "/#site", "url": BASE + "/", "name": NAME + " Portfolio", "publisher": {"@id": BASE + "/#person"}, "inLanguage": "en"},
                  {"@type": "ProfessionalService", "name": NAME + ", AI Web, Mobile and Automation Development", "url": BASE + "/", "image": BASE + ME, "areaServed": AREAS, "founder": {"@id": BASE + "/#person"},
                   "email": EMAIL, "telephone": TEL, "address": {"@type": "PostalAddress", "addressLocality": "Rawalpindi", "addressCountry": "PK"},
                   "serviceType": ["Custom web application development", "Flutter mobile app development", "AI and LLM integration", "Workflow automation with n8n, Zapier and Make", "WordPress and WooCommerce development"], "hasOfferCatalog": OFFERS}]
    if crumbs:
        items = [("Home", "/")] + crumbs
        graph.append({"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + clean(u)} for i, (n, u) in enumerate(items)]})
    if ld: graph += ld if isinstance(ld, list) else [ld]
    url = BASE + clean(path)
    og = og or ME
    nav = "".join(f'<a href="{u}"' + (' aria-current="page"' if (u == path or (u != "/" and path.startswith(u))) else "") + f'>{n}</a>' for n, u in NAV)
    socials = "".join(f'<li><a href="{u}" target="_blank" rel="noopener me">{n}</a></li>' for n, u in SOC.items())
    contact = f'<li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="tel:{TEL}">{PHONE}</a></li><li style="color:var(--muted)">{LOCATION}</li>'
    robots = "noindex, follow" if nonindex else "index, follow, max-image-preview:large, max-snippet:-1"
    crumb_html = ""
    if crumbs:
        crumb_html = '<nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / ' + " / ".join(f'<a href="{u}">{E(n)}</a>' if i < len(crumbs) - 1 else E(n) for i, (n, u) in enumerate(crumbs)) + "</nav>"
    body = body.replace("<!--CRUMBS-->", crumb_html)
    out = f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><meta name="author" content="{NAME}"><meta name="robots" content="{robots}">
<meta name="keywords" content="Mujahid Abbas, AI web developer, AI mobile app developer, Laravel developer, Flutter developer, n8n automation expert, Zapier automation, workflow automation, custom SaaS development, hire full-stack developer, AI application developer London, Laravel SaaS expert Dubai, Flutter mobile developer New York, n8n automation specialist Riyadh, New York, London, Dubai, Riyadh">
<meta name="google-site-verification" content="1XQmjNyiIIK-j20ARlomHc1Aq3tJAM2Nl7tjtEy2dhs"><meta name="geo.region" content="PK-PB"><meta name="geo.placename" content="Rawalpindi">
<link rel="canonical" href="{url}"><link rel="alternate" hreflang="en" href="{url}"><link rel="alternate" hreflang="x-default" href="{url}">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='16' fill='%236366f1'/%3E%3Ctext x='32' y='42' font-size='28' font-weight='800' text-anchor='middle' fill='white' font-family='sans-serif'%3EMA%3C/text%3E%3C/svg%3E">
<meta name="theme-color" content="#090d16"><meta property="og:type" content="{ptype}"><meta property="og:site_name" content="{NAME} Portfolio"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE + og}"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE + og}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<script>try{{document.documentElement.setAttribute('data-theme',localStorage.getItem('theme')||'dark')}}catch(e){{document.documentElement.setAttribute('data-theme','dark')}}</script>
<link rel="stylesheet" href="/assets/css/style.css">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script></head>
<body data-wa="{WA}"><div class="aurora" aria-hidden="true"><i></i><i></i><i></i></div><canvas id="bg" aria-hidden="true"></canvas><a class="skip" href="#main">Skip to content</a>
<header class="site"><div class="wrap bar"><a class="brand" href="/" aria-label="{NAME}, home"><b>MA</b>{NAME}</a>
<nav class="nav" id="nav" aria-label="Main">{nav}<a class="btn p" href="/hire-me/">Hire me</a></nav>
<button class="tt" id="tt" type="button" aria-label="Toggle light and dark mode"></button><button class="menu" id="menu" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="nav">&#9776;</button></div></header>
<main id="main">{body}</main>
<footer><div class="wrap"><div class="fg"><div><a class="brand" href="/"><b>MA</b>{NAME}</a><p class="muted" style="margin-top:14px;max-width:40ch">Full-stack developer and AI solutions specialist building AI web apps, Laravel and Flutter products, and n8n, Zapier and Make automations. Available for remote work worldwide.</p></div>
<div><h3>Pages</h3><ul>{"".join(f'<li><a href="{u}">{n}</a></li>' for n, u in NAV[1:] + [("Hire me", "/hire-me/")])}</ul></div>
<div><h3>Connect</h3><ul><li><a href="{WAURL}" target="_blank" rel="noopener">WhatsApp</a></li>{contact}{socials}</ul></div></div>
<div class="copy"><span>&copy; 2026 {NAME}. All rights reserved.</span><span>Rawalpindi / Islamabad, Pakistan</span></div></div></footer>
<script src="/assets/js/site.js" defer></script></body></html>'''
    out = re.sub(r'(href|src)="(/[^"]*)"', rel, out)
    open(os.path.join(ROOT, fname(path)), "w", encoding="utf-8").write(out)
    if not nonindex: PAGES.append(path)

def ph(h1, lede):
    return f'<div class="wrap page-h"><!--CRUMBS--><h1>{h1}</h1><p class="lede">{lede}</p></div>'

# ---------------- HOME ----------------
fh, fl = faq(FAQ_GEN)
mq = "".join(f"<span>{s}</span>" for s in STACK)
PH = ["AI Web & Mobile App Developer", "n8n & Zapier Automation Expert", "Laravel & Flutter Architect"]
def stat(n, suf, label): return f'<div class="st glass"><b data-count="{n}" data-suffix="{suf}">{n}{suf}</b><span>{label}</span></div>'
page("/", "Mujahid Abbas | WordPress, Laravel & AI Automation Expert",
 "Hire Mujahid Abbas, a freelance WordPress, Laravel and AI automation developer (n8n, Zapier, OpenAI) working remotely with clients in the US, UK and UAE.",
 f'''<div class="hero"><div class="wrap hg"><div><span class="pill"><i aria-hidden="true"></i>Available for freelance and remote work</span>
<h1>Hi, I'm <span class="gt">Mujahid Abbas</span><span class="role"><span id="typing" data-phrases="{E(json.dumps(PH))}">{E(PH[0])}</span><span class="caret" aria-hidden="true"></span></span></h1>
<p class="lede">Full-Stack Developer and AI Solutions Specialist. I build AI-powered web apps, custom SaaS, Flutter apps and workflow automations for startups and enterprises in the US, UK and Gulf.</p>
<div class="row"><a class="btn p" href="/projects/">View my work</a><a class="btn g" href="{WAURL}" target="_blank" rel="noopener">WhatsApp chat</a></div>
<ul class="facts"><li>AI and automation</li><li>Laravel and Flutter</li><li>Clean, secure code</li></ul></div>
<div class="por"><img src="{ME}" alt="Portrait of Mujahid Abbas, full-stack developer and AI solutions specialist, at his desk" width="1121" height="1403" fetchpriority="high"><span class="chip a">Claude Code</span><span class="chip b">n8n Automation</span><span class="chip c">Available now</span><span class="chip d">Laravel + Flutter</span></div></div></div>
<div class="mq" aria-hidden="true"><div>{mq}{mq}</div></div>
<section style="padding-bottom:0"><div class="wrap"><div class="stats">{stat(50, "+", "Projects completed")}{stat(35, "+", "Happy clients")}{stat(3, "+", "Years of experience")}{stat(100, "%", "Client satisfaction")}</div></div></section>
<section><div class="wrap"><div class="head"><h2>What I build</h2><p>AI web apps, mobile apps, automations and stores, handled by one developer from database to launch.</p></div>{bento()}</div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>AI, web and cloud stack</h2><p>The tools I use to ship faster without cutting corners.</p></div>{skills()}</div></section>
<section><div class="wrap"><div class="head"><h2>Featured projects</h2><p>Websites and platforms built for businesses across construction, healthcare, education and training.</p></div>{pgrid(3)}<p style="margin-top:28px"><a class="btn g" href="/projects/">All projects</a></p></div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>Remote-first for the US, UK and Gulf</h2><p>I work with startups and enterprises across three regions, delivering AI web apps, SaaS products and automations remotely.</p></div>
<div class="pgrid"><a class="mk glass" href="/services/#ai"><h3>AI application developer for London</h3><p>AI-powered web apps and LLM integrations for UK teams that want to ship faster.</p></a>
<a class="mk glass" href="/services/#web"><h3>Laravel SaaS expert for Dubai</h3><p>Secure, scalable Laravel platforms for businesses in the UAE and wider Gulf.</p></a>
<a class="mk glass" href="/services/#mobile"><h3>Flutter mobile developer for New York</h3><p>Cross-platform Android and iOS apps for US startups, built on one codebase.</p></a>
<a class="mk glass" href="/services/#auto"><h3>n8n automation specialist for Riyadh</h3><p>n8n, Zapier and Make workflows that remove manual work for Saudi companies.</p></a></div>
<div class="geo"><span>New York</span><span>London</span><span>Dubai</span><span>Riyadh</span><span>Worldwide remote</span></div></div></section>
<section><div class="wrap"><div class="head"><h2>How a project runs</h2></div>{STEPS}</div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>What you can count on</h2></div><div class="trio"><div><h3>Fast, lean code</h3><p>Efficient builds that keep pages quick and apps responsive.</p></div><div><h3>Secure by default</h3><p>Role-based access, sanitized inputs and safe API patterns protect your operations.</p></div><div><h3>Looks right everywhere</h3><p>Interfaces that stay clear on phones, tablets and desktops.</p></div></div></div></section>
<section><div class="wrap"><div class="head"><h2>Quick answers</h2></div>{fh}</div></section>{cta()}''', ld=[fl], is_home=True)

# ---------------- ABOUT ----------------
page("/about/", "About Mujahid Abbas | AI Solutions Specialist & Full-Stack Developer", "Learn how Mujahid Abbas, a full-stack developer and AI solutions specialist in Pakistan, builds AI web apps, Flutter and Laravel products and automations for US, UK and Gulf clients.",
 f'''{ph("About Mujahid Abbas", "A developer focused on products that work reliably, look clear and keep growing.")}
<section style="padding-top:20px"><div class="wrap ab"><img src="{ME}" alt="Mujahid Abbas, full-stack developer and AI solutions specialist" width="1121" height="1403" loading="lazy">
<div><p class="ans"><strong>Mujahid Abbas</strong> is a full-stack developer and AI solutions specialist based in Rawalpindi / Islamabad, Pakistan. He works remotely with clients in the US, UK and Gulf (GCC), building AI web apps, Laravel and Flutter products, and n8n, Zapier and Make automations.</p>
<p>I work with businesses that have a clear idea and need it built properly: a secure backend, a clean interface and an app that stays fast as more people use it.</p>
<p>For AI and automation, I connect OpenAI and other LLM APIs to real workflows, and I use Cursor IDE, Claude Code and GitHub Copilot to build faster. For the web and mobile, I use Laravel, PHP and MySQL, Flutter, Dart and Firebase. When a content site or store fits better, I build it in WordPress, Elementor Pro and WooCommerce.</p>
<p>Every project starts with a short conversation about goals and users, so we build the right thing first.</p>
<div class="row"><a class="btn p" href="/hire-me/">Hire me</a><a class="btn g" href="/projects/">See my work</a></div></div></div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>Skills and tools</h2></div>{skills()}</div></section>
<section><div class="wrap two"><div><h2>Certified in web development</h2><p class="muted" style="margin-top:14px">In January 2026, NPXSoft Engineering Group awarded me a Certificate of Professional Excellence in Web Development for completion and demonstrated mastery of the subject.</p></div>
<figure class="cert glass"><img src="{CERT}" alt="Certificate of Professional Excellence in Web Development awarded to Mujahid Abbas by NPXSoft Engineering Group, January 2026" width="1600" height="1131" loading="lazy"><figcaption>NPXSoft Engineering Group, Certificate of Professional Excellence, January 2026</figcaption></figure></div></section>{cta()}''',
 crumbs=[("About", "/about/")], ld={"@type": "ProfilePage", "mainEntity": {"@id": BASE + "/#person"}})

# ---------------- SERVICES ----------------
sh, sl = faq(FAQ_SVC)
def sr(i, t, p, chips):
    return f'<article class="sr" id="{i}"><h3>{t}</h3><div><p>{p}</p><ul class="chips">{"".join(f"<li>{c}</li>" for c in chips)}</ul></div></article>'
page("/services/", "Services | AI Web Apps, Flutter, Laravel & n8n Automation", "Custom Laravel and SaaS apps, Flutter mobile apps, OpenAI and LLM integrations, n8n, Zapier and Make automation, and WordPress or WooCommerce by Mujahid Abbas for US, UK and Gulf clients.",
 f'''{ph("AI, web and automation services", "Everything from the database to the screen to the workflow behind it, handled by one developer.")}
<section style="padding-top:20px"><div class="wrap"><div class="svc">
{sr("web", "Custom web apps and SaaS", "Laravel and PHP platforms with role-based access, dashboards, billing and clean REST APIs, built to scale with your customers.", ["Laravel", "PHP", "MySQL", "REST APIs", "SaaS"])}
{sr("mobile", "Flutter mobile apps", "Cross-platform Android and iOS apps in Flutter and Dart, with Firebase or a custom backend. Built for real users on real phones.", ["Flutter", "Dart", "Firebase"])}
{sr("ai", "AI solutions", "OpenAI and LLM API integrations, AI assistants and smart search added to your product. I use Cursor IDE, Claude Code and GitHub Copilot to ship faster without cutting corners.", ["OpenAI", "LLM APIs", "Claude Code", "Cursor IDE", "GitHub Copilot"])}
{sr("auto", "Workflow automation", "Automations in n8n, Zapier and Make that connect your CRM, email, forms and databases and remove repetitive manual work.", ["n8n", "Zapier", "Make"])}
{sr("wp", "WordPress and WooCommerce", "Elementor Pro sites and WooCommerce stores with cPanel hosting, SSL and page speed tuned toward 90+ benchmarks.", ["WordPress", "Elementor Pro", "WooCommerce", "cPanel", "SSL"])}
</div></div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>How a project runs</h2></div>{STEPS}</div></section>
<section><div class="wrap"><div class="head"><h2>Service questions</h2></div>{sh}</div></section>{cta()}''', crumbs=[("Services", "/services/")], ld=[sl])

# ---------------- PROJECTS ----------------
page("/projects/", "Projects | Websites, Platforms & AI Tools", "Projects by Mujahid Abbas: Al Malitha Trading & Contracting, CasaMeds, ICSST, AR Academy Nishat, Orhan Contracting, Grand Arab, Cafe Bliss, Clinix and Palettify AI.",
 f'''{ph("Projects", "Selected websites, healthcare and education platforms, and creative digital tools.")}
<section style="padding-top:20px"><div class="wrap">{pgrid()}</div></section>{cta("Want a product like these?")}''', crumbs=[("Projects", "/projects/")], og=PROJECTS[0]["img"],
 ld={"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": p["title"]} for i, p in enumerate(PROJECTS)]})

# ---------------- BLOG ----------------
POSTS = [
 ("laravel-app-cost", "What affects the cost of a custom Laravel web app?", "The main cost drivers for a Laravel web app, and how to scope a project so the estimate stays realistic.",
  "A custom Laravel web app costs more or less depending on its features, user roles, integrations and design needs. There is no single price, but you can predict the range by listing what the app must do.",
  [("Features and user roles", "Every extra role, such as admin, staff or customer, adds screens, permissions and testing. List the roles first."),
   ("Integrations", "Payments, messaging, maps and AI services each need secure API work. Name the ones you need on day one."),
   ("Design and languages", "Bilingual interfaces and custom dashboards take more time than a single-language standard layout."),
   ("Scope control", "Launch with the core workflow, then add features in phases. This keeps the first release fast and the budget clear.")]),
 ("flutter-vs-native", "Flutter or native: which is right for your app?", "A plain comparison of Flutter and native development to help you choose for your next mobile app.",
  "Flutter is the better choice for most business apps that must run on both Android and iOS, because one codebase serves both. Native fits apps that depend heavily on platform-specific features.",
  [("When Flutter fits", "Business apps, dashboards, booking and training apps work well. You ship to both stores faster and maintain one codebase."),
   ("When native fits", "Apps built around advanced camera, sensors or platform-only features may need native code for the best result."),
   ("Backend matters equally", "Either way, a secure API and database decide how reliable the app feels. Plan the backend with the app."),
   ("How to decide", "List your must-have features and platforms. If both stores matter and features are standard, start with Flutter.")]),
 ("n8n-vs-zapier-vs-make", "n8n, Zapier or Make: which automation tool should you use?", "A practical comparison of n8n, Zapier and Make for business workflow automation.",
  "Zapier is the quickest to start, Make suits visual multi-step scenarios, and n8n gives the most control when you need custom logic, AI steps or self-hosting. The right choice depends on workflow complexity and who will maintain it.",
  [("Zapier", "Best for simple, well-supported app-to-app connections that non-technical teammates can manage."),
   ("Make", "Best for visual, multi-branch scenarios with data transformation between steps."),
   ("n8n", "Best for custom logic, AI and LLM steps, and teams that want more control over where workflows run."),
   ("How to decide", "Map the workflow first. If it is a straight line, start simple. If it branches, calls APIs or uses AI, choose a tool with more control.")]),
]
def art(slug, title, desc, lead, secs):
    b = "".join(f"<h2>{h}</h2><p>{t}</p>" for h, t in secs)
    page(f"/blog/{slug}/", title + " | Mujahid Abbas", desc,
     f'<div class="wrap page-h"><!--CRUMBS--><h1>{title}</h1><p class="meta">By {NAME} &middot; <time datetime="{DATE}">14 October 2026</time></p></div><section style="padding-top:10px"><div class="wrap art"><p class="ans">{lead}</p>{b}<p style="margin-top:34px"><a class="btn p" href="/hire-me/">Discuss your project</a></p></div></section>',
     crumbs=[("Blog", "/blog/"), (title, f"/blog/{slug}/")], ptype="article",
     ld={"@type": "BlogPosting", "headline": title, "description": desc, "datePublished": DATE, "dateModified": DATE, "author": {"@id": BASE + "/#person"}, "mainEntityOfPage": BASE + clean(f"/blog/{slug}/"), "image": BASE + ME})
for p in POSTS: art(*p)
cards = "".join(f'<a class="post" href="/blog/{s}/"><small>14 October 2026</small><h3>{t}</h3><p>{d}</p></a>' for s, t, d, _, _ in POSTS)
page("/blog/", "Blog | AI, Web, Mobile & Automation Guides", "Practical guides on Laravel, Flutter and workflow automation by Mujahid Abbas.",
 f'{ph("Blog", "Practical answers about planning and building web, mobile and automation products.")}<section style="padding-top:20px"><div class="wrap"><div class="posts">{cards}</div></div></section>{cta()}', crumbs=[("Blog", "/blog/")])

# ---------------- HIRE ME ----------------
hh, hl = faq(FAQ_HIRE)
page("/hire-me/", "Hire Mujahid Abbas | Freelance AI, Laravel & Flutter Developer", "Hire Mujahid Abbas for an AI web app, Laravel or Flutter product, or n8n, Zapier and Make automation. Send a brief and get a reply on WhatsApp.",
 f'''{ph("Hire an AI, Laravel and Flutter developer", "Tell me what you want to build. You will get questions, a rough plan and next steps on WhatsApp.")}
<section style="padding-top:20px"><div class="wrap two"><div><div class="opt"><h3>Fixed-scope project</h3><p>A defined product such as a SaaS platform, mobile app or store, delivered from design to launch.</p></div><div class="opt"><h3>Ongoing remote work</h3><p>A developer who joins your product and keeps shipping features, fixes and automations.</p></div><div class="opt"><h3>Automate or speed up</h3><p>Workflow automation, bug fixes, speed tuning and security hardening for existing systems.</p></div></div>{form(True)}</div></section>
<section class="alt"><div class="wrap"><div class="head"><h2>How a project runs</h2></div>{STEPS}</div></section>
<section><div class="wrap"><div class="head"><h2>Hiring questions</h2></div>{hh}</div></section>''', crumbs=[("Hire me", "/hire-me/")], ld=[hl])

# ---------------- CONTACT ----------------
soc = "".join(f'<p><strong>{n}:</strong> <a href="{u}" target="_blank" rel="noopener me">{u}</a></p>' for n, u in SOC.items())
page("/contact/", "Contact Mujahid Abbas | AI, Laravel & Flutter Developer", "Contact Mujahid Abbas by form, email or WhatsApp to discuss an AI web app, Laravel SaaS, Flutter app or n8n automation project.",
 f'''{ph("Contact", "Send a message, or reach me directly on WhatsApp or email.")}
<section style="padding-top:20px"><div class="wrap two"><div><p><strong>WhatsApp:</strong> <a href="{WAURL}" target="_blank" rel="noopener">{PHONE}</a></p><p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>{soc}
<p><strong>Location:</strong> {LOCATION}</p><p class="muted">Serving clients in the US, UK and Gulf (GCC).</p></div>
<form class="formbox" name="contact" method="POST" action="contact.html?sent=true" data-netlify="true" netlify-honeypot="bot-field"><input type="hidden" name="form-name" value="contact"><p hidden><label>Leave empty <input name="bot-field"></label></p>
<p class="sent" id="sent" role="status" hidden>Thank you! Your message was sent. I will reply soon.</p>
<div class="fld"><label for="c1">Your name</label><input id="c1" name="name" autocomplete="name" required></div>
<div class="fld"><label for="c2">Email</label><input id="c2" name="email" type="email" autocomplete="email" required></div>
<div class="fld"><label for="c3">Project type</label><select id="c3" name="project-type"><option>Custom web app or SaaS</option><option>Flutter mobile app</option><option>AI solution or LLM integration</option><option>Workflow automation (n8n, Zapier, Make)</option><option>WordPress or WooCommerce site</option><option>Something else</option></select></div>
<div class="fld"><label for="c4">Message</label><textarea id="c4" name="message" required></textarea></div>
<div class="row"><button class="btn l" type="submit">Send message</button><a class="btn g" href="{WAURL}" target="_blank" rel="noopener">WhatsApp instead</a></div></form></div></section>
<section style="padding-top:0"><div class="wrap"><div class="head"><h2>Based in Rawalpindi / Islamabad</h2><p>Working remotely with clients worldwide.</p></div>
<div class="map"><iframe title="Map of Rawalpindi and Islamabad, Pakistan" src="https://www.google.com/maps?q=Rawalpindi%2C%20Islamabad%2C%20Pakistan&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div></div></section>''', crumbs=[("Contact", "/contact/")],
 ld={"@type": "ContactPage", "url": BASE + "/contact"})

page("/404.html", "Page not found | Mujahid Abbas", "This page does not exist.",
 '<div class="wrap page-h"><h1>Page not found</h1><p class="lede">The page you want has moved or never existed.</p><div class="row" style="margin-top:20px"><a class="btn p" href="/">Go home</a><a class="btn g" href="/projects/">See projects</a></div></div>', nonindex=True)

# ---------------- SEO / GEO files ----------------
sm = "".join(f"<url><loc>{BASE}{clean(p)}</loc><lastmod>{DATE}</lastmod></url>" for p in PAGES)
open(os.path.join(ROOT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>')
bots = ["GPTBot", "OAI-SearchBot", "ChatGPT-User", "ClaudeBot", "Claude-SearchBot", "PerplexityBot", "Google-Extended", "Applebot-Extended"]
open(os.path.join(ROOT, "robots.txt"), "w").write("User-agent: *\nAllow: /\n\n" + "".join(f"User-agent: {b}\nAllow: /\n\n" for b in bots) + f"Sitemap: {BASE}/sitemap.xml\n")
open(os.path.join(ROOT, "llms.txt"), "w").write(f"""# {NAME}

> {NAME} is a full-stack developer and AI solutions specialist from Rawalpindi / Islamabad, Pakistan. He builds AI web apps, custom SaaS, Laravel and Flutter products and n8n, Zapier and Make automations for clients in the US, UK and Gulf (GCC).

## Key facts
- Role: Full-Stack Developer and AI Solutions Specialist (freelance, remote)
- Location: {LOCATION}
- Markets: United States, United Kingdom, UAE, Saudi Arabia (New York, London, Dubai, Riyadh)
- Core stack: Laravel, PHP, MySQL, Flutter, Dart, Firebase, REST APIs, WordPress, WooCommerce, n8n, Zapier, Make, OpenAI APIs, Claude Code, Cursor IDE
- Contact: {EMAIL}, WhatsApp {PHONE}

## Pages
- [Home]({BASE}/): overview and quick answers
- [About]({BASE}/about): background, skills and certification
- [Services]({BASE}/services): web apps and SaaS, Flutter apps, AI solutions, workflow automation, WordPress
- [Projects]({BASE}/projects): Al Malitha Trading & Contracting, CasaMeds, ICSST, AR Academy Nishat, Orhan Contracting, Grand Arab
- [Blog]({BASE}/blog): guides on Laravel cost, Flutter vs native, n8n vs Zapier vs Make
- [Hire me]({BASE}/hire-me): how to start a project
- [Contact]({BASE}/contact)
""")
open(os.path.join(ROOT, "_headers"), "w").write("/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n/css/*\n  Cache-Control: public, max-age=86400\n/js/*\n  Cache-Control: public, max-age=86400\n/images/*\n  Cache-Control: public, max-age=31536000\n")
print("Built", len(PAGES), "pages")
