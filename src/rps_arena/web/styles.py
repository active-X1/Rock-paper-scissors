"""All CSS for the web UI, kept in one place."""

CSS = """
:root {
  --bg-1: #080b1c; --bg-2: #160f3a; --bg-3: #07243b; --bg-4: #230a35;
  --text: #f3f5ff; --muted: #8e97cc;
  --glass: rgba(255,255,255,0.06); --glass-border: rgba(255,255,255,0.12);
  --rock: #f59e0b; --paper: #22d3ee; --scissors: #f472b6;
  --win: #34d399; --lose: #fb7185; --draw: #a5b4fc;
  --font: Inter, "SF Pro Display", "Segoe UI Variable", "Segoe UI", system-ui, -apple-system, Roboto, "Helvetica Neue", sans-serif;
}

html, body, .q-layout, .q-page, .q-page-container {
  background: transparent !important; color: var(--text); font-family: var(--font);
}
body {
  min-height: 100vh;
  background: linear-gradient(-45deg, var(--bg-1), var(--bg-2), var(--bg-3), var(--bg-4)) !important;
  background-size: 400% 400% !important;
  animation: rps-drift 22s ease infinite;
}
body::before, body::after {
  content: ""; position: fixed; z-index: -1; border-radius: 50%; filter: blur(90px);
  pointer-events: none; opacity: .45;
}
body::before { width: 46vmax; height: 46vmax; top: -14vmax; left: -12vmax;
  background: radial-gradient(circle, #7c3aed, transparent 65%); animation: rps-float-a 26s ease-in-out infinite; }
body::after { width: 42vmax; height: 42vmax; bottom: -16vmax; right: -12vmax;
  background: radial-gradient(circle, #06b6d4, transparent 65%); animation: rps-float-b 30s ease-in-out infinite; }

.nicegui-content { padding: 0 !important; align-items: center; }

.rps-shell { width: 100%; max-width: 760px; margin: 0 auto; padding: 36px 18px 48px;
  display: flex; flex-direction: column; gap: 22px; box-sizing: border-box; }

.rps-header { text-align: center; }
.rps-title { font-size: clamp(2rem, 6vw, 3rem); font-weight: 800; letter-spacing: -0.02em; line-height: 1.05;
  background: linear-gradient(90deg, #c4b5fd, #67e8f9, #f9a8d4); -webkit-background-clip: text; background-clip: text;
  color: transparent; }
.rps-sub { margin-top: 8px; color: var(--muted); font-size: 1rem; }

.glass { background: var(--glass); border: 1px solid var(--glass-border); border-radius: 22px;
  backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); box-shadow: 0 10px 40px rgba(0,0,0,.28); }

.rps-scoreboard { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.rps-score { padding: 14px 10px; text-align: center; }
.rps-score .num { font-size: 2.2rem; font-weight: 800; line-height: 1; font-variant-numeric: tabular-nums; }
.rps-score .cap { margin-top: 6px; font-size: .72rem; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
.rps-score.you .num { color: var(--win); }
.rps-score.cpu .num { color: var(--lose); }
.rps-score.tie .num { color: var(--draw); }

.rps-arena { padding: 22px 14px; display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 8px; }
.rps-panel { display: flex; flex-direction: column; align-items: center; gap: 10px; }
.rps-panel .who { font-size: .75rem; letter-spacing: .16em; text-transform: uppercase; color: var(--muted); }
.rps-panel .what { font-weight: 700; min-height: 1.4em; }
.rps-icon { width: clamp(92px, 24vw, 150px); height: clamp(92px, 24vw, 150px); object-fit: contain;
  filter: drop-shadow(0 8px 18px rgba(0,0,0,.4)); }
.rps-icon.pop { animation: rps-pop .42s cubic-bezier(.2,1.4,.4,1) both; }
.rps-icon.shake { animation: rps-shake .5s ease-in-out infinite; }
.rps-icon.idle { opacity: .85; }
.rps-vs { font-weight: 800; font-size: 1.1rem; color: var(--muted); padding: 0 6px; }

.rps-banner { text-align: center; font-weight: 800; font-size: 1.5rem; padding: 14px; border-radius: 16px;
  animation: rps-rise .35s ease both; }
.rps-banner.win  { color: var(--win);  background: rgba(52,211,153,.12);  border: 1px solid rgba(52,211,153,.4); }
.rps-banner.lose { color: var(--lose); background: rgba(251,113,133,.12); border: 1px solid rgba(251,113,133,.4); }
.rps-banner.draw { color: var(--draw); background: rgba(165,180,252,.12); border: 1px solid rgba(165,180,252,.4); }
.rps-banner.wait { color: var(--muted); background: var(--glass); border: 1px solid var(--glass-border); font-size: 1.05rem; font-weight: 600; }

.rps-picks { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.rps-pick { cursor: pointer; padding: 16px 8px 12px; color: var(--text); font: inherit;
  display: flex; flex-direction: column; align-items: center; gap: 6px;
  transition: transform .18s ease, border-color .18s ease, box-shadow .18s ease, background .18s ease; }
.rps-pick img { width: clamp(56px, 14vw, 84px); height: clamp(56px, 14vw, 84px); object-fit: contain; }
.rps-pick .name { font-weight: 700; }
.rps-pick .key { font-size: .7rem; color: var(--muted); letter-spacing: .1em; }
.rps-pick:hover:not(:disabled) { transform: translateY(-5px); background: rgba(255,255,255,.1); }
.rps-pick:active:not(:disabled) { transform: translateY(-1px) scale(.98); }
.rps-pick:disabled { cursor: wait; opacity: .55; }
.rps-pick.rock:hover:not(:disabled) { border-color: var(--rock); box-shadow: 0 12px 34px rgba(245,158,11,.3); }
.rps-pick.paper:hover:not(:disabled) { border-color: var(--paper); box-shadow: 0 12px 34px rgba(34,211,238,.3); }
.rps-pick.scissors:hover:not(:disabled) { border-color: var(--scissors); box-shadow: 0 12px 34px rgba(244,114,182,.3); }
.rps-pick:focus-visible { outline: 2px solid #a78bfa; outline-offset: 3px; }

.rps-meta { display: flex; justify-content: space-between; align-items: center; gap: 12px; flex-wrap: wrap;
  color: var(--muted); font-size: .9rem; }
.rps-trail { display: flex; gap: 6px; align-items: center; }
.rps-dot { width: 12px; height: 12px; border-radius: 50%; }
.rps-dot.win { background: var(--win); } .rps-dot.lose { background: var(--lose); } .rps-dot.draw { background: var(--draw); }
.rps-reset { cursor: pointer; background: transparent; color: var(--muted); font: inherit;
  border: 1px solid var(--glass-border); border-radius: 999px; padding: 7px 16px; transition: all .18s ease; }
.rps-reset:hover { color: var(--text); border-color: rgba(255,255,255,.4); background: var(--glass); }

.rps-footer { text-align: center; color: var(--muted); font-size: .8rem; opacity: .8; }

@keyframes rps-drift { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }
@keyframes rps-float-a { 0%,100% { transform: translate(0,0); } 50% { transform: translate(8vmax, 6vmax); } }
@keyframes rps-float-b { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-7vmax, -8vmax); } }
@keyframes rps-pop { from { transform: scale(.4) rotate(-12deg); opacity: 0; } to { transform: scale(1) rotate(0); opacity: 1; } }
@keyframes rps-shake { 0%,100% { transform: translateX(0) rotate(0); } 25% { transform: translateX(-7px) rotate(-5deg); } 75% { transform: translateX(7px) rotate(5deg); } }
@keyframes rps-rise { from { transform: translateY(10px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }

@media (prefers-reduced-motion: reduce) {
  body, body::before, body::after, .rps-icon.shake, .rps-icon.pop, .rps-banner { animation: none !important; }
}
"""
