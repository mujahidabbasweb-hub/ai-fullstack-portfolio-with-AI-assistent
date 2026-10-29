(function () {
  var root = document.documentElement, WA = document.body.getAttribute('data-wa');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var tt = document.getElementById('tt');
  function icon() { tt.textContent = root.getAttribute('data-theme') === 'dark' ? '\u2600' : '\u263E'; }
  icon();
  tt.addEventListener('click', function () {
    var n = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-theme', n); icon();
    try { localStorage.setItem('theme', n); } catch (e) {}
  });

  var m = document.getElementById('menu'), nav = document.getElementById('nav');
  m.addEventListener('click', function () { m.setAttribute('aria-expanded', nav.classList.toggle('open')); });

  document.querySelectorAll('[data-wa-form]').forEach(function (f) {
    var out = f.querySelector('[data-wa-send]');
    function up() {
      var v = function (n) { var e = f.querySelector('[name=' + n + ']'); return e ? e.value.trim() : ''; };
      var txt = "Hi Mujahid, I'm " + (v('name') || 'a potential client') + '. Project type: ' + v('type') +
        (v('budget') ? '. Budget: ' + v('budget') : '') + '. ' + (v('msg') || "I'd like to discuss a project.");
      out.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(txt);
    }
    f.addEventListener('input', up); f.addEventListener('change', up); up();
  });

  /* typewriter */
  var ty = document.getElementById('typing');
  if (ty && !reduce) {
    var ph = JSON.parse(ty.dataset.phrases), i = 0, j = ph[0].length, del = true;
    (function tick() {
      var w = ph[i];
      if (del) {
        j--; ty.textContent = w.slice(0, j);
        if (j <= 0) { del = false; i = (i + 1) % ph.length; return setTimeout(tick, 300); }
        return setTimeout(tick, 26);
      }
      w = ph[i]; j++; ty.textContent = w.slice(0, j);
      if (j >= w.length) { del = true; return setTimeout(tick, 2000); }
      setTimeout(tick, 58);
    })();
  }

  /* count-up stats */
  var cs = document.querySelectorAll('[data-count]');
  if (cs.length && 'IntersectionObserver' in window && !reduce) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return; io.unobserve(e.target);
        var el = e.target, to = +el.dataset.count, suf = el.dataset.suffix || '', t0 = performance.now();
        (function s(t) {
          var p = Math.min((t - t0) / 1200, 1);
          el.textContent = Math.round(to * (1 - Math.pow(1 - p, 3))) + suf;
          if (p < 1) requestAnimationFrame(s);
        })(t0);
      });
    }, { threshold: .4 });
    cs.forEach(function (c) { io.observe(c); });
  }

  /* particle network background */
  var c = document.getElementById('bg');
  if (c && c.getContext) {
    var x = c.getContext('2d'), P = [], W, H, dpr = Math.min(window.devicePixelRatio || 1, 1.5), mo = { x: -999, y: -999 }, raf;
    function size() {
      W = innerWidth; H = innerHeight; c.width = W * dpr; c.height = H * dpr; x.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.min(70, Math.round(W * H / 18000)); P = [];
      for (var k = 0; k < n; k++) P.push({ x: Math.random() * W, y: Math.random() * H, vx: (Math.random() - .5) * .35, vy: (Math.random() - .5) * .35 });
    }
    function draw() {
      x.clearRect(0, 0, W, H);
      var light = root.getAttribute('data-theme') === 'light', rgb = light ? '14,116,144' : '34,211,238', k = light ? .7 : 1;
      for (var a = 0; a < P.length; a++) {
        var p = P[a];
        if (!reduce) { p.x += p.vx; p.y += p.vy; if (p.x < 0 || p.x > W) p.vx *= -1; if (p.y < 0 || p.y > H) p.vy *= -1; }
        x.fillStyle = 'rgba(' + rgb + ',' + .55 * k + ')'; x.beginPath(); x.arc(p.x, p.y, 1.6, 0, 6.283); x.fill();
        for (var b = a + 1; b < P.length; b++) {
          var q = P[b], dx = p.x - q.x, dy = p.y - q.y, d = dx * dx + dy * dy;
          if (d < 16900) { x.strokeStyle = 'rgba(' + rgb + ',' + (1 - d / 16900) * .22 * k + ')'; x.beginPath(); x.moveTo(p.x, p.y); x.lineTo(q.x, q.y); x.stroke(); }
        }
        var mx = p.x - mo.x, my = p.y - mo.y, md = mx * mx + my * my;
        if (md < 25600) { x.strokeStyle = 'rgba(129,140,248,' + (1 - md / 25600) * .45 * k + ')'; x.beginPath(); x.moveTo(p.x, p.y); x.lineTo(mo.x, mo.y); x.stroke(); }
      }
      if (!reduce) raf = requestAnimationFrame(draw);
    }
    size(); draw();
    window.addEventListener('resize', function () { size(); if (reduce) draw(); });
    window.addEventListener('pointermove', function (e) { mo.x = e.clientX; mo.y = e.clientY; }, { passive: true });
    document.addEventListener('visibilitychange', function () { if (document.hidden) cancelAnimationFrame(raf); else if (!reduce) draw(); });
  }
})();

/* contact form success message (Netlify Forms redirects with ?sent=true) */
(function () { var s = document.getElementById('sent'); if (s && /[?&]sent=true/.test(location.search)) s.hidden = false; })();

/* ===== Embedded AI assistant (no external services) ===== */
(function () {
  var WA = document.body.getAttribute('data-wa');
  var ASK = 'Project pricing depends entirely on your exact features, scope, and technical requirements. Could you please share a brief description of your project requirements?';
  var THANKS = "Thank you! I have recorded your requirements. Let's connect directly on WhatsApp so Mujahid can review your scope and provide a tailored quote.";
  var PRICE = /(pric|cost|quot|budget|how much|\brates?\b|charg|\bfees?\b|estimat|afford)/i;
  var KB = [
    { k: /\b(hi|hello|hey|salam|assalam)\b/i, a: "Hello! I'm Mujahid's assistant. Ask me about his skills, projects, services or pricing." },
    { k: /(skill|tech|stack|technolog|language|tools?)/i, a: '<b>AI and automation:</b> n8n, Zapier, Make, Cursor IDE, Claude Code, GitHub Copilot, OpenAI APIs.<br><b>Web and mobile:</b> Flutter, Dart, Firebase, PHP, Laravel, MySQL, REST APIs, JavaScript.<br><b>CMS and cloud:</b> WordPress, Elementor Pro, WooCommerce, cPanel, SSL, 90+ PageSpeed optimization.' },
    { k: /(n8n|zapier|make\.com|automat|workflow|llm|openai|agent|chatbot|\bai\b)/i, a: 'Mujahid builds AI solutions and automations: OpenAI and LLM integrations, AI web agents, and n8n, Zapier and Make workflows that connect your CRM, email, forms and databases. See <a href="services.html#ai">AI services</a>.' },
    { k: /(flutter|dart|mobile|android|ios)/i, a: 'He builds cross-platform Android and iOS apps with Flutter, Dart and Firebase from a single codebase. See <a href="services.html#mobile">Flutter services</a>.' },
    { k: /(laravel|php|mysql|saas|backend|\bapis?\b|web app)/i, a: 'He builds secure Laravel and PHP web apps and SaaS platforms with MySQL and clean REST APIs. See <a href="services.html#web">web app services</a>.' },
    { k: /(wordpress|woocommerce|elementor|cpanel|ssl|speed|ecommerce|store)/i, a: 'He builds Elementor Pro sites and WooCommerce stores, with cPanel hosting, SSL and page speed optimization toward 90+ scores.' },
    { k: /(project|portfolio|work|case stud|example|client)/i, a: 'Recent projects include Al Malitha Trading &amp; Contracting, CasaMeds, ICSST, AR Academy Nishat, Orhan Contracting and Grand Arab. See all on the <a href="projects.html">Projects page</a>.' },
    { k: /(experience|years|background|who|about|certif)/i, a: 'Mujahid Abbas is a Full-Stack Developer and AI Solutions Specialist with 3+ years of experience and a Web Development certificate from NPXSoft Engineering Group (January 2026). More on the <a href="about.html">About page</a>.' },
    { k: /(where|location|based|country|time ?zone|remote|london|dubai|new york|riyadh|\buk\b|\busa?\b|uae|saudi|gulf)/i, a: 'Mujahid is based in Rawalpindi / Islamabad, Pakistan and works remotely with clients in the US, UK and Gulf (GCC), including New York, London, Dubai and Riyadh.' },
    { k: /(contact|email|phone|call|whatsapp|reach|hire|availab)/i, a: 'Mujahid is available for freelance and remote work.<br>Email: mujahidabbas.offical@gmail.com<br>WhatsApp: +92 321 9153891<br>Or use the <a href="contact.html">Contact page</a>.' }
  ];
  var st = 'idle', lead = '';

  var fab = document.createElement('button');
  fab.className = 'cb-fab'; fab.type = 'button'; fab.setAttribute('aria-label', 'Open AI assistant chat'); fab.setAttribute('aria-expanded', 'false');
  fab.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="4" y="7" width="16" height="12" rx="4"/><path d="M12 3v4M9 13h.01M15 13h.01M9.5 16.2c1.5 1 3.5 1 5 0"/></svg>';
  var box = document.createElement('div');
  box.className = 'cb'; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', 'AI assistant chat');
  box.innerHTML = '<div class="cb-h"><span class="cb-av">MA</span><div><b>Mujahid\'s AI assistant</b><small>Online</small></div><button class="cb-x" type="button" aria-label="Close chat">&times;</button></div>' +
    '<div class="cb-log" role="log" aria-live="polite"></div>' +
    '<div class="cb-q"><button type="button">Skills</button><button type="button">Projects</button><button type="button">Pricing</button><button type="button">Contact</button></div>' +
    '<form class="cb-f"><input type="text" aria-label="Type your message" placeholder="Ask about skills, projects, pricing..." maxlength="600" autocomplete="off"><button type="submit">Send</button></form>';
  document.body.appendChild(box); document.body.appendChild(fab);
  var log = box.querySelector('.cb-log'), inp = box.querySelector('input'), form = box.querySelector('form'), opened = false;

  function add(cls, html, isText) {
    var d = document.createElement('div'); d.className = 'cb-m ' + cls;
    if (isText) d.textContent = html; else d.innerHTML = html;
    log.appendChild(d); log.scrollTop = log.scrollHeight; return d;
  }
  function reply(html) {
    var t = add('b', '<span class="cb-dots"><i></i><i></i><i></i></span>');
    setTimeout(function () { t.innerHTML = html; log.scrollTop = log.scrollHeight; }, 450);
  }
  function waUrl(txt) { return 'https://wa.me/' + WA + '?text=Hi%20Mujahid,%20here%20are%20my%20project%20requirements:%20' + encodeURIComponent(txt); }
  function handle(text) {
    add('u', text, true);
    if (st === 'lead') {
      if (text.length < 10) return reply('Could you add a little more detail (features, platforms, deadline) so Mujahid can quote accurately?');
      st = 'idle'; lead = text; var url = waUrl(lead);
      add('b', THANKS + '<br><a class="btn l" href="' + url + '" target="_blank" rel="noopener">Continue on WhatsApp</a>');
      window.open(url, '_blank', 'noopener');
      return;
    }
    if (PRICE.test(text)) { st = 'lead'; return reply(ASK); }
    for (var i = 0; i < KB.length; i++) if (KB[i].k.test(text)) return reply(KB[i].a);
    reply('I can help with Mujahid\'s skills, projects, services and pricing. For anything else, message him directly on <a href="https://wa.me/' + WA + '" target="_blank" rel="noopener">WhatsApp</a>.');
  }
  function toggle(open) {
    box.classList.toggle('open', open); fab.setAttribute('aria-expanded', open);
    if (open) { if (!opened) { opened = true; reply("Hi! I'm Mujahid's AI assistant. I can answer questions about his skills, projects and services, or help you get a quote."); } inp.focus(); } else fab.focus();
  }
  fab.addEventListener('click', function () { toggle(!box.classList.contains('open')); });
  box.querySelector('.cb-x').addEventListener('click', function () { toggle(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && box.classList.contains('open')) toggle(false); });
  box.querySelectorAll('.cb-q button').forEach(function (b) { b.addEventListener('click', function () { handle(b.textContent === 'Pricing' ? 'What is your pricing?' : b.textContent); }); });
  form.addEventListener('submit', function (e) { e.preventDefault(); var v = inp.value.trim(); if (!v) return; inp.value = ''; handle(v); });
})();
