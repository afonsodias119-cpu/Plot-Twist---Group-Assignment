// The torn photo of the print shop: a jigsaw puzzle (specs/torn-photo.md).
// This file only DRAWS the photo, cuts it into torn pieces and lets the player move and turn them.
// It does not know the solution: when the frame is full it asks play.js, which asks the server.
(function () {
  "use strict";
  const W = 1000, H = 620;              // the size of the board (SVG units); the screen scales it
  const PW = 540, PH = 360;             // the size of the photo
  const CW = PW / 3, CH = PH / 3;       // the size of one piece (3 x 3 pieces)
  const FX = (W - PW) / 2, FY = (H - PH) / 2;   // where the frame is on the board

  // Which part of the photo each piece shows: [row, column]. (The server keeps which place is right.)
  const PIECES = { q: [0, 0], w: [0, 1], a: [0, 2], f: [1, 0], k: [1, 1], s: [1, 2], d: [2, 0], n: [2, 1], h: [2, 2] };
  // Where the pieces lie on the counter when the window opens: piece, x, y (top left), rotation.
  // Pieces turned on their side are taller, so they lie on the left and right; the upright ones above and below.
  const START = [["a", 25, 40, 90], ["h", 25, 250, 270], ["f", 25, 460, 90], ["k", 795, 40, 270], ["q", 795, 250, 90],
                 ["n", 795, 460, 270], ["s", 300, 3, 180], ["d", 520, 3, 0], ["w", 410, 497, 180]];

  // ---------- the photo: the four of you in front of the campus, by the sea, with the date stamp ----------
  function person(x, { hair, top, legs, skin = "#e8b48c", extra = "" }) {
    return `<g transform="translate(${x} 0)">` +
      `<rect x="-17" y="250" width="14" height="78" rx="5" fill="${legs}"/><rect x="3" y="250" width="14" height="78" rx="5" fill="${legs}"/>` +
      `<rect x="-24" y="326" width="22" height="9" rx="4" fill="#2b2b2b"/><rect x="2" y="326" width="22" height="9" rx="4" fill="#2b2b2b"/>` +
      `<rect x="-38" y="168" width="14" height="70" rx="7" fill="${top}"/><rect x="24" y="168" width="14" height="70" rx="7" fill="${top}"/>` +
      `<rect x="-28" y="160" width="56" height="98" rx="16" fill="${top}"/>` +
      `<rect x="-6" y="140" width="12" height="22" fill="${skin}"/><circle cx="0" cy="118" r="27" fill="${skin}"/>` +
      `${hair}<circle cx="-9" cy="118" r="2.6" fill="#2a1d14"/><circle cx="9" cy="118" r="2.6" fill="#2a1d14"/>` +
      `<path d="M-8 130 Q 0 137 8 130" fill="none" stroke="#7a3b2a" stroke-width="2.5" stroke-linecap="round"/>${extra}</g>`;
  }
  function art() {
    const sea = `<rect x="0" y="0" width="${PW}" height="150" fill="url(#sky)"/><rect x="0" y="150" width="${PW}" height="70" fill="#3f7fa8"/>` +
      [...Array(7)].map((_, i) => `<path d="M${i * 80 + 10} ${168 + (i % 3) * 14} q 14 -6 28 0" fill="none" stroke="#ffffff66" stroke-width="2"/>`).join("") +
      `<rect x="0" y="220" width="${PW}" height="${PH - 220}" fill="#d9c8a8"/>` +
      `<rect x="330" y="40" width="210" height="125" fill="#f2f0eb"/>` +
      [...Array(10)].map((_, i) => `<rect x="${342 + (i % 5) * 40}" y="${54 + Math.floor(i / 5) * 44}" width="28" height="30" fill="#5a6b7c"/>`).join("") +
      `<text x="352" y="158" font-family="Inter, sans-serif" font-weight="700" font-size="15" fill="#1f3b5c">NOVA SBE</text>` +
      `<circle cx="70" cy="50" r="22" fill="#fff4c4" opacity="0.9"/>`;
    const people =
      person(95, { top: "#c0392b", legs: "#2f4a7a", hair: `<path d="M-30 120 Q -32 82 0 84 Q 32 82 30 120 L 34 170 L 18 170 L 20 112 L -20 112 L -18 170 L -34 170 Z" fill="#4a2c1a"/>` }) +
      person(215, { top: "#2e8b57", legs: "#222", hair: `<path d="M-27 112 Q -26 86 0 86 Q 26 86 27 112 L 22 104 L -22 104 Z" fill="#e2c26a"/><circle cx="0" cy="82" r="11" fill="#e2c26a"/>` }) +
      person(330, { top: "#c9a36b", legs: "#3a3a3a", hair: `<path d="M-28 108 Q -28 80 0 80 Q 28 80 28 108 Z" fill="#e8b45c"/><rect x="-29" y="102" width="58" height="9" rx="4" fill="#d79b38"/>`,
                    extra: `<rect x="-24" y="152" width="48" height="12" rx="6" fill="#8a2f2f"/><rect x="8" y="160" width="10" height="34" rx="4" fill="#8a2f2f"/>` }) +
      person(445, { top: "#2251a8", legs: "#6b7178", hair: `<path d="M-27 112 Q -28 88 0 88 Q 28 88 27 112 L 24 100 L -24 100 Z" fill="#1d1d1d"/>`,
                    extra: `<circle cx="-9" cy="118" r="8" fill="none" stroke="#1d1d1d" stroke-width="2.5"/><circle cx="9" cy="118" r="8" fill="none" stroke="#1d1d1d" stroke-width="2.5"/><path d="M-1 118 L 1 118" stroke="#1d1d1d" stroke-width="2.5"/>` });
    const stamp = `<text x="${PW - 18}" y="${PH - 16}" text-anchor="end" font-family="'Courier New', monospace" font-weight="700" font-size="24" fill="#ff8a1f" stroke="#ff8a1f55" stroke-width="3" paint-order="stroke">17.10.2026</text>`;
    return `<g id="photo-art">${sea}${people}${stamp}<rect x="3" y="3" width="${PW - 6}" height="${PH - 6}" fill="none" stroke="#f6f3ec" stroke-width="7"/></g>`;
  }

  // ---------- the torn edges: the same jagged line is shared by the two pieces on each side ----------
  let seed = 11;
  const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
  const STEP = 12;
  const hEdge = [1, 2].map(row => [...Array(PW / STEP + 1)].map((_, i) => {   // across the photo, at y = row * CH
    const x = i * STEP; return [x, row * CH + (x % CW === 0 ? 0 : (rnd() - 0.5) * 12)];
  }));
  const vEdge = [1, 2].map(col => [...Array(PH / STEP + 1)].map((_, i) => {   // down the photo, at x = col * CW
    const y = i * STEP; return [col * CW + (y % CH === 0 ? 0 : (rnd() - 0.5) * 12), y];
  }));
  function outline(row, col) {   // the torn outline of one piece, in its own units (0,0 = its top left corner)
    const x0 = col * CW, y0 = row * CH, x1 = x0 + CW, y1 = y0 + CH;
    const across = (r, from, to) => r === 0 || r === 3 ? [[from, r * CH], [to, r * CH]]
      : hEdge[r - 1].filter(([x]) => x >= Math.min(from, to) && x <= Math.max(from, to)).sort((a, b) => from < to ? a[0] - b[0] : b[0] - a[0]);
    const down = (c, from, to) => c === 0 || c === 3 ? [[c * CW, from], [c * CW, to]]
      : vEdge[c - 1].filter(([, y]) => y >= Math.min(from, to) && y <= Math.max(from, to)).sort((a, b) => from < to ? a[1] - b[1] : b[1] - a[1]);
    const points = [...across(row, x0, x1), ...down(col + 1, y0, y1), ...across(row + 1, x1, x0), ...down(col, y1, y0)];
    return points.map(([x, y]) => `${(x - x0).toFixed(1)},${(y - y0).toFixed(1)}`).join(" ");
  }

  function drawing() {
    const clips = Object.entries(PIECES).map(([id, [row, col]]) =>
      `<clipPath id="piece-${id}"><polygon points="${outline(row, col)}"/></clipPath>`).join("");
    const cells = [...Array(9)].map((_, i) =>
      `<rect x="${FX + (i % 3) * CW}" y="${FY + Math.floor(i / 3) * CH}" width="${CW}" height="${CH}" fill="none" stroke="#e8b45c55" stroke-dasharray="6 6"/>`).join("");
    const pieces = Object.entries(PIECES).map(([id, [row, col]]) =>
      `<g class="photo-piece" data-piece="${id}"><g clip-path="url(#piece-${id})"><use href="#photo-art" x="${-col * CW}" y="${-row * CH}"/></g>` +
      `<polygon points="${outline(row, col)}" fill="none" stroke="#f6f3ec" stroke-width="2"/></g>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img"><defs>` +
      `<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fb9df"/><stop offset="1" stop-color="#f1d9b8"/></linearGradient>` +
      `${art()}${clips}</defs><rect width="${W}" height="${H}" fill="#6b4b33"/>` +
      `<rect class="photo-frame" x="${FX - 10}" y="${FY - 10}" width="${PW + 20}" height="${PH + 20}" rx="6" fill="#20160f" stroke="#e8b45c" stroke-width="2"/>` +
      `${cells}<g class="photo-pieces">${pieces}</g></svg>`;
  }

  // ---------- the window ----------
  const placed = new Map();   // piece id -> {x, y, rot, cell}: how the player left the pieces, while the page is open
  let card = null, options = null, busy = false, drag = null;

  function build() {
    card = document.createElement("section");
    card.id = "photo-card"; card.className = "table-card photo-card"; card.hidden = true;
    card.setAttribute("role", "dialog"); card.setAttribute("aria-labelledby", "photo-title");
    card.innerHTML = `<header><div><h3 id="photo-title"></h3><p id="photo-hint" class="muted"></p></div>
      <button id="photo-close" class="secondary"></button></header><div class="table-view"></div>`;
    (document.getElementById("investigation") || document.body).append(card);
    card.querySelector("#photo-close").addEventListener("click", close);
    const view = card.querySelector(".table-view");
    view.addEventListener("pointerdown", down);
    view.addEventListener("pointermove", move);
    view.addEventListener("pointerup", up);
    view.addEventListener("pointercancel", () => { drag = null; });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && card && !card.hidden) close(); });
  }

  const pieceEl = id => card.querySelector(`.photo-piece[data-piece="${id}"]`);
  function show(id) {   // put one piece where `placed` says, turned around its own centre
    const { x, y, rot } = placed.get(id);
    pieceEl(id).setAttribute("transform", `translate(${x} ${y}) rotate(${rot} ${CW / 2} ${CH / 2})`);
  }
  function toBoard(event) {
    const svg = card.querySelector(".table-view svg");
    return new DOMPoint(event.clientX, event.clientY).matrixTransform(svg.getScreenCTM().inverse());
  }

  // Press and release without moving = turn the piece 90°. Press and move = drag it; near a free place
  // of the frame it snaps there.
  function down(event) {
    const el = event.target.closest(".photo-piece");
    if (!el || busy) return;
    const id = el.dataset.piece, here = placed.get(id), point = toBoard(event);
    drag = { id, sx: event.clientX, sy: event.clientY, px: point.x, py: point.y, ox: here.x, oy: here.y, moving: false };
    try { event.currentTarget.setPointerCapture(event.pointerId); } catch (error) { /* keep going without it */ }
    event.preventDefault();
  }
  function move(event) {
    if (!drag) return;
    if (!drag.moving && Math.hypot(event.clientX - drag.sx, event.clientY - drag.sy) < 6) return;
    const here = placed.get(drag.id);
    if (!drag.moving) { drag.moving = true; here.cell = null; pieceEl(drag.id).parentNode.append(pieceEl(drag.id)); }   // lifted: on top
    const point = toBoard(event);
    here.x = Math.max(-CW / 2, Math.min(W - CW / 2, drag.ox + point.x - drag.px));
    here.y = Math.max(-CH / 2, Math.min(H - CH / 2, drag.oy + point.y - drag.py));
    show(drag.id);
  }
  function up() {
    const was = drag;
    drag = null;
    if (!was) return;
    const here = placed.get(was.id);
    if (!was.moving) {   // a tap: turn it
      here.rot = (here.rot + 90) % 360;
      show(was.id);
    } else {             // a drop: snap into the nearest free place of the frame, if it is close
      const taken = new Set([...placed.values()].map(p => p.cell).filter(c => c !== null));
      let best = null, bestDistance = 50;
      for (let cell = 0; cell < 9; cell++) {
        const distance = Math.hypot(here.x - (FX + (cell % 3) * CW), here.y - (FY + Math.floor(cell / 3) * CH));
        if (!taken.has(cell) && distance < bestDistance) { best = cell; bestDistance = distance; }
      }
      if (best !== null) { here.cell = best; here.x = FX + (best % 3) * CW; here.y = FY + Math.floor(best / 3) * CH; show(was.id); }
    }
    checkFull();
  }

  async function checkFull() {
    const byCell = [...placed.entries()].filter(([, p]) => p.cell !== null).sort((a, b) => a[1].cell - b[1].cell);
    if (byCell.length !== 9) return;
    busy = true;
    try {
      const result = await options.submit(byCell.map(([id, p]) => [id, p.rot]));   // "done", "wrong", or nothing
      if (result === "done") {
        card.querySelector(".photo-frame").classList.add("done");
        setTimeout(close, 2200);
      } else if (result === "wrong") {
        const frame = card.querySelector(".photo-frame");
        frame.classList.remove("wrong"); void frame.getBBox(); frame.classList.add("wrong");   // a short red flash
      }
    } finally { busy = false; }
  }

  function open(opts) {
    options = opts;
    if (!card) build();
    card.querySelector("#photo-title").textContent = opts.title;
    card.querySelector("#photo-hint").textContent = opts.hint;
    card.querySelector("#photo-close").textContent = opts.close;
    card.querySelector(".table-view").innerHTML = drawing();
    if (!placed.size) START.forEach(([id, x, y, rot]) => placed.set(id, { x, y, rot, cell: null }));
    placed.forEach((_, id) => show(id));
    card.hidden = false;
    card.querySelector("#photo-close").focus({ preventScroll: true });
  }

  function close() {
    if (!card || card.hidden) return;
    card.hidden = true;
    drag = null;
    if (options && options.onClose) options.onClose();
  }

  // reset: a new game puts the pieces back on the counter
  window.campusPhoto = { open, close, reset: () => placed.clear(), isOpen: () => Boolean(card && !card.hidden), drawing };
})();
