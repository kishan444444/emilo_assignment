from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from project.app.schemas import QueryRequest, QueryResponse
from project.app.recommender import recommend_by_occasion

app = FastAPI(title="Recommendation API")


# =============================
# HTML UI
# =============================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Occasion Recommender</title>
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:       #0e0e0f;
      --surface:  #18181b;
      --border:   #2a2a2f;
      --accent:   #c8a96e;
      --accent2:  #e8c98a;
      --text:     #f0ede8;
      --muted:    #888;
      --tag-bg:   #25241f;
      --card-bg:  #1c1c20;
      --radius:   14px;
      --transition: 0.28s cubic-bezier(.4,0,.2,1);
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* HERO */
    .hero {
      position: relative;
      padding: 72px 24px 56px;
      text-align: center;
      overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute;
      inset: 0;
      background:
        radial-gradient(ellipse 70% 55% at 50% -10%, rgba(200,169,110,.18) 0%, transparent 70%),
        radial-gradient(ellipse 40% 30% at 80% 100%, rgba(200,169,110,.07) 0%, transparent 60%);
      pointer-events: none;
    }
    .hero-eyebrow {
      display: inline-block;
      font-size: 11px;
      font-weight: 500;
      letter-spacing: .2em;
      text-transform: uppercase;
      color: var(--accent);
      border: 1px solid rgba(200,169,110,.3);
      border-radius: 999px;
      padding: 6px 18px;
      margin-bottom: 24px;
    }
    .hero h1 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2.2rem, 6vw, 3.8rem);
      font-weight: 700;
      line-height: 1.1;
      color: var(--text);
      margin-bottom: 14px;
    }
    .hero h1 em { font-style: italic; color: var(--accent); }
    .hero p {
      color: var(--muted);
      font-size: 1rem;
      font-weight: 300;
      max-width: 420px;
      margin: 0 auto;
      line-height: 1.6;
    }

    /* SEARCH */
    .search-wrap {
      max-width: 680px;
      margin: 44px auto 0;
      padding: 0 20px;
    }
    .search-label {
      display: block;
      font-size: 12px;
      font-weight: 500;
      letter-spacing: .12em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 12px;
    }
    .search-box {
      display: flex;
      align-items: center;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 6px 6px 6px 20px;
      gap: 10px;
      transition: border-color var(--transition), box-shadow var(--transition);
    }
    .search-box:focus-within {
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(200,169,110,.12);
    }
    .search-box input {
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      font-size: 1rem;
      padding: 10px 0;
    }
    .search-box input::placeholder { color: var(--muted); }
    .search-btn {
      background: var(--accent);
      color: #0e0c08;
      border: none;
      border-radius: 10px;
      padding: 12px 28px;
      font-family: 'DM Sans', sans-serif;
      font-size: 14px;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 8px;
      transition: background var(--transition), transform var(--transition);
    }
    .search-btn:hover { background: var(--accent2); transform: translateY(-1px); }
    .search-btn:active { transform: translateY(0); }

    /* PILLS */
    .pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
      margin-top: 18px;
    }
    .pill {
      background: var(--tag-bg);
      border: 1px solid var(--border);
      border-radius: 999px;
      padding: 6px 16px;
      font-size: 13px;
      color: var(--muted);
      cursor: pointer;
      transition: all var(--transition);
      user-select: none;
    }
    .pill:hover { border-color: var(--accent); color: var(--accent); background: rgba(200,169,110,.07); }

    /* DIVIDER */
    .divider {
      max-width: 900px;
      margin: 44px auto 0;
      height: 1px;
      background: linear-gradient(90deg, transparent, var(--border), transparent);
    }

    /* RESULTS */
    .results-section {
      max-width: 900px;
      margin: 0 auto;
      padding: 40px 20px 80px;
    }
    .status-bar {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 28px;
      min-height: 28px;
    }
    .status-text { font-size: 13px; color: var(--muted); }
    .status-text strong { color: var(--accent); font-weight: 500; }

    .loader { display: none; align-items: center; gap: 10px; color: var(--muted); font-size: 13px; }
    .loader.active { display: flex; }
    .spinner {
      width: 18px; height: 18px;
      border: 2px solid var(--border);
      border-top-color: var(--accent);
      border-radius: 50%;
      animation: spin .8s linear infinite;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* GRID */
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(270px, 1fr));
      gap: 18px;
    }

    /* CARD */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow: hidden;
      display: flex;
      flex-direction: column;
      opacity: 0;
      transform: translateY(14px);
      animation: fadeUp .4s forwards;
      transition: transform var(--transition), border-color var(--transition), box-shadow var(--transition);
    }
    .card:hover {
      transform: translateY(-3px);
      border-color: rgba(200,169,110,.35);
      box-shadow: 0 12px 32px rgba(0,0,0,.35);
    }
    @keyframes fadeUp { to { opacity: 1; transform: translateY(0); } }

    /* IMAGE */
    .card-img-wrap {
      position: relative;
      height: 200px;
      overflow: hidden;
      background: #111;
    }
    .card-img-wrap img {
      width: 100%; height: 100%;
      object-fit: cover;
      transition: transform .5s ease;
    }
    .card:hover .card-img-wrap img { transform: scale(1.05); }

    /* CARD BODY — labeled rows */
    .card-body {
      padding: 18px;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 0;
    }

    .field {
      display: flex;
      flex-direction: column;
      gap: 3px;
      padding: 10px 0;
      border-bottom: 1px solid var(--border);
    }
    .field:last-child { border-bottom: none; padding-bottom: 0; }
    .field:first-child { padding-top: 0; }

    .field-label {
      font-size: 9px;
      font-weight: 600;
      letter-spacing: .18em;
      text-transform: uppercase;
      color: var(--accent);
    }

    .field-value {
      font-size: 13px;
      color: var(--text);
      line-height: 1.5;
    }

    /* Title uses serif */
    .field-value.title {
      font-family: 'Playfair Display', serif;
      font-size: 1.05rem;
      font-weight: 500;
    }

    /* Description muted */
    .field-value.desc {
      color: var(--muted);
      font-weight: 300;
      font-size: 12.5px;
    }

    /* Score row */
    .field-value.score {
      font-weight: 600;
      color: var(--accent2);
      font-size: 14px;
    }

    /* Match chip inline */
    .match-chip {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      font-size: 11px;
      font-weight: 500;
      padding: 3px 12px;
      border-radius: 999px;
      width: fit-content;
    }
    .match-chip.excellent { background: rgba(100,200,120,.12); color: #7ddc99; }
    .match-chip.good      { background: rgba(200,169,110,.12); color: var(--accent); }
    .match-chip.fair      { background: rgba(140,140,160,.12); color: #aaa; }
    .match-chip::before   { content: ''; width: 6px; height: 6px; border-radius: 50%; background: currentColor; }

    /* Reason */
    .field-value.reason {
      font-style: italic;
      color: rgba(240,237,232,.65);
      font-size: 12px;
      line-height: 1.55;
    }

    /* EMPTY STATE */
    .empty-state { display: none; flex-direction: column; align-items: center; justify-content: center; padding: 80px 20px; text-align: center; gap: 16px; }
    .empty-state.visible { display: flex; }
    .empty-icon { font-size: 48px; opacity: .5; }
    .empty-state h3 { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 500; color: var(--text); }
    .empty-state p { font-size: 14px; color: var(--muted); max-width: 300px; line-height: 1.6; }

    /* RESPONSIVE */
    @media (max-width: 600px) {
      .hero { padding: 52px 20px 40px; }
      .grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>

  <header class="hero">
    <span class="hero-eyebrow">✦ Curated Finds</span>
    <h1>Find the perfect gift<br>for <em>every occasion</em></h1>
    <p>Tell us the moment — we'll surface what fits. Birthdays, anniversaries, festivals, and more.</p>

    <div class="search-wrap">
      <label class="search-label" for="occasion-input">What's the occasion?</label>
      <div class="search-box">
        <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="none" viewBox="0 0 24 24" stroke="#888" stroke-width="2">
          <circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/>
        </svg>
        <input id="occasion-input" type="text" placeholder="e.g. birthday, anniversary, Diwali…" autocomplete="off"/>
        <button class="search-btn" onclick="search()">
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
            <circle cx="11" cy="11" r="8"/><path stroke-linecap="round" d="M21 21l-4.35-4.35"/>
          </svg>
          Search
        </button>
      </div>
      <div class="pills">
        <span class="pill" onclick="quickSearch('Birthday')">🎂 Birthday</span>
        <span class="pill" onclick="quickSearch('Anniversary')">💍 Anniversary</span>
        <span class="pill" onclick="quickSearch('Diwali')">🪔 Diwali</span>
        <span class="pill" onclick="quickSearch('Baby shower')">🍼 Baby Shower</span>
        <span class="pill" onclick="quickSearch('Graduation')">🎓 Graduation</span>
        <span class="pill" onclick="quickSearch('Wedding')">💐 Wedding</span>
      </div>
    </div>
  </header>

  <div class="divider"></div>

  <section class="results-section">
    <div class="status-bar">
      <span class="status-text" id="status-text"></span>
      <div class="loader" id="loader">
        <div class="spinner"></div>
        Finding the best matches…
      </div>
    </div>
    <div class="grid" id="results-grid"></div>
    <div class="empty-state" id="empty-state">
      <div class="empty-icon">🎁</div>
      <h3>No matches found</h3>
      <p>We couldn't find products for that occasion. Try "birthday", "Diwali", or "anniversary".</p>
    </div>
  </section>

  <script>
    const input  = document.getElementById('occasion-input');
    const grid   = document.getElementById('results-grid');
    const empty  = document.getElementById('empty-state');
    const loader = document.getElementById('loader');
    const status = document.getElementById('status-text');

    input.addEventListener('keydown', e => { if (e.key === 'Enter') search(); });
    function quickSearch(term) { input.value = term; search(); }

    function matchClass(label = '') {
      const l = label.toLowerCase();
      if (l.includes('excel') || l.includes('perfect')) return 'excellent';
      if (l.includes('good') || l.includes('great'))   return 'good';
      return 'fair';
    }

    function setLoading(on) {
      loader.classList.toggle('active', on);
      if (on) status.innerHTML = '';
    }

    function escHtml(str) {
      return String(str ?? '')
        .replace(/&/g, '&amp;').replace(/</g, '&lt;')
        .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    async function search() {
      const query = input.value.trim();
      if (!query) return;

      grid.innerHTML = '';
      empty.classList.remove('visible');
      setLoading(true);

      try {
        const res = await fetch('/recommend', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query, top_k: 9 })
        });
        if (!res.ok) throw new Error('Server error');
        const data = await res.json();
        const items = data.results || [];

        setLoading(false);

        if (!items.length) {
          empty.classList.add('visible');
          status.innerHTML = `No results for <strong>"${escHtml(query)}"</strong>`;
          return;
        }

        status.innerHTML = `Showing <strong>${items.length}</strong> picks for <strong>"${escHtml(query)}"</strong>`;

        items.forEach((item, i) => {
          const card = document.createElement('div');
          card.className = 'card';
          card.style.animationDelay = `${i * 55}ms`;
          const cls = matchClass(item.match);

          card.innerHTML = `
            <div class="card-img-wrap">
              <img src="${escHtml(item.image)}" alt="${escHtml(item.title)}" loading="lazy"
                   onerror="this.src='https://placehold.co/400x260/1c1c20/888?text=No+Image'"/>
            </div>
            <div class="card-body">

              <div class="field">
                <span class="field-label">Title</span>
                <span class="field-value title">${escHtml(item.title)}</span>
              </div>

              <div class="field">
                <span class="field-label">Category</span>
                <span class="field-value">${escHtml(item.category)}</span>
              </div>

              <div class="field">
                <span class="field-label">Description</span>
                <span class="field-value desc">${escHtml(item.description)}</span>
              </div>

              <div class="field">
                <span class="field-label">Score</span>
                <span class="field-value score">${item.score}</span>
              </div>

              <div class="field">
                <span class="field-label">Match</span>
                <span class="match-chip ${cls}">${escHtml(item.match)}</span>
              </div>

              <div class="field">
                <span class="field-label">Reason</span>
                <span class="field-value reason">${escHtml(item.reason)}</span>
              </div>

            </div>`;

          grid.appendChild(card);
        });

      } catch (err) {
        setLoading(false);
        status.innerHTML = '<span style="color:#e07070">Something went wrong. Please try again.</span>';
        console.error(err);
      }
    }
  </script>
</body>
</html>
"""


# =============================
# API ENDPOINT
# =============================
@app.post("/recommend", response_model=QueryResponse)
def recommend(req: QueryRequest):
    results = recommend_by_occasion(req.query, req.top_k)
    return {"results": results}