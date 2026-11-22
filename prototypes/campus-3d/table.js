// The close-up of the study room table: a hidden-object search for the USB stick (specs/hidden-object-table.md).
// This file only DRAWS the table and says which kind of object was clicked. The rules (is it the stick?
// how much time does a wrong click cost?) are in play.js and on the server (campus_search.py).
(function () {
  "use strict";
  const W = 1000, H = 620;   // the size of the drawing (SVG units); the screen scales it
  const LENS_R = 95, LENS_ZOOM = 2.5;   // the magnifier: its radius and how much bigger it shows things

  // ---------- how each kind of object is drawn, seen from above, centred on (0, 0) ----------
  const r = (x, y, w, h, fill, extra = "") => `<rect x="${x}" y="${y}" width="${w}" height="${h}" fill="${fill}" ${extra}/>`;
  const c = (x, y, radius, fill, extra = "") => `<circle cx="${x}" cy="${y}" r="${radius}" fill="${fill}" ${extra}/>`;
  const p = (d, fill, extra = "") => `<path d="${d}" fill="${fill}" ${extra}/>`;
  const line = "stroke=\"#00000022\" stroke-width=\"1\"";
  const SHAPES = {
    papers: () => r(-75, -100, 150, 200, "#f4f2ec", line) +
      [...Array(11)].map((_, i) => r(-58, -78 + i * 15, i % 4 === 3 ? 70 : 116, 3, "#b9bcc4")).join(""),
    notebook: () => r(-80, -105, 160, 210, "#26456e", "rx=\"6\"") + r(-62, -88, 128, 176, "#2d5283", "rx=\"4\"") +
      [...Array(9)].map((_, i) => c(-72, -90 + i * 22, 4, "#c9ccd2")).join("") + r(-20, -40, 60, 16, "#e9e3d0"),
    pizza_box: () => r(-135, -130, 270, 260, "#c49a6c", "rx=\"4\" " + line) + r(-118, -113, 236, 226, "#d8b48a") +
      c(-30, 20, 34, "#b98a55", "opacity=\"0.5\"") + c(55, -40, 22, "#b98a55", "opacity=\"0.45\"") +
      p("M-90 70 q 30 -14 60 0", "none", "stroke=\"#a8662b\" stroke-width=\"10\" stroke-linecap=\"round\"") +
      p("M40 80 q 25 10 50 -6", "none", "stroke=\"#a8662b\" stroke-width=\"9\" stroke-linecap=\"round\""),
    pizza_slice: () => p("M0 -70 L 48 60 Q 0 80 -48 60 Z", "#f2c14e") +
      p("M-48 60 Q 0 80 48 60", "none", "stroke=\"#b8742f\" stroke-width=\"12\" stroke-linecap=\"round\"") +
      c(-8, 5, 9, "#b8322a") + c(14, 32, 8, "#b8322a") + c(-18, 40, 7, "#b8322a") + c(4, -28, 6, "#b8322a"),
    napkin: () => p("M-62 -40 L -20 -58 L 30 -50 L 64 -20 L 58 30 L 20 56 L -34 50 L -64 18 Z", "#f7f5f0", line) +
      p("M-40 -20 L 0 -36 L 38 -14 L 30 22 L -8 36 L -42 14 Z", "#ecebe6") +
      c(18, 8, 13, "#c0392b", "opacity=\"0.55\"") + c(-14, -6, 7, "#c0392b", "opacity=\"0.4\""),
    can: () => c(0, 0, 33, "#c62828") + c(0, 0, 27, "#d8d8d8") + c(0, 0, 22, "#bdbdbd") +
      r(-8, -16, 16, 22, "#9e9e9e", "rx=\"6\"") + c(0, -12, 4, "#757575"),
    mug: () => p("M30 -14 q 26 0 26 14 q 0 14 -26 14", "none", "stroke=\"#ece8df\" stroke-width=\"9\"") +
      c(0, 0, 36, "#ece8df") + c(0, 0, 29, "#4a2c1a") + c(-8, -8, 7, "#6b4430", "opacity=\"0.7\""),
    crisps: () => p("M-60 -85 L 60 -85 L 66 85 L -66 85 Z", "#f0a020") +
      r(-62, -92, 124, 12, "#d88a14") + r(-66, 80, 132, 12, "#d88a14") + c(0, -5, 34, "#fcd46a") +
      c(-30, 110, 4, "#e7b85a") + c(26, 104, 3, "#e7b85a") + c(48, 118, 3, "#e7b85a"),
    cable: () => p("M-140 0 C -100 -60 -60 60 -20 0 S 60 -60 100 0 S 150 40 160 10", "none",
      "stroke=\"#22262b\" stroke-width=\"6\" stroke-linecap=\"round\"") + r(156, 2, 22, 14, "#d9dde2", "rx=\"2\""),
    sticky_notes: () => r(-38, -38, 76, 76, "#ffe066", line) + [...Array(4)].map((_, i) => r(-26, -22 + i * 14, 50, 3, "#c9a800")).join(""),
    pen: () => r(-90, -6, 160, 12, "#2251a8", "rx=\"5\"") + p("M70 -6 L 92 0 L 70 6 Z", "#cfd3d8") + r(-60, -8, 6, 16, "#163a7a"),
    highlighter: () => r(-70, -13, 110, 26, "#f5e100", "rx=\"8\"") + r(40, -12, 34, 24, "#3c3c3c", "rx=\"6\""),
    headphones: () => p("M-70 10 C -70 -90 70 -90 70 10", "none", "stroke=\"#30343a\" stroke-width=\"14\"") +
      c(-70, 26, 28, "#30343a") + c(70, 26, 28, "#30343a") + c(-70, 26, 16, "#4a5059") + c(70, 26, 16, "#4a5059"),
    keys: () => c(0, 0, 16, "none", "stroke=\"#b0b4ba\" stroke-width=\"5\"") +
      p("M10 10 L 60 32 L 56 40 L 50 37 L 47 44 L 41 41 L 8 18 Z", "#c9a94a") +
      p("M-8 12 L -30 64 L -22 66 L -20 60 L -14 62 L 2 18 Z", "#b9bcc2") + r(-30, -36, 26, 18, "#1d6fb8", "rx=\"4\""),
    calculator: () => r(-60, -90, 120, 180, "#2b2f36", "rx=\"10\"") + r(-46, -76, 92, 30, "#a9b8a0", "rx=\"3\"") +
      [...Array(16)].map((_, i) => r(-44 + (i % 4) * 23, -34 + Math.floor(i / 4) * 28, 17, 20, i % 4 === 3 ? "#d27a2c" : "#4a505a", "rx=\"3\"")).join(""),
    // student life (specs/more-to-find.md, point 1). None looks like the stick: the card is twice its size,
    // white, with a photo and the NOVA stripe; the other two are paper.
    student_card: () => r(-48, -30, 96, 60, "#fbfbf8", "rx=\"5\" " + line) + r(-48, -30, 96, 13, "#0b2a5b", "rx=\"5\"") +
      `<text x="-40" y="-20" font-size="9" font-weight="700" fill="#ffffff">NOVA</text>` +
      r(-40, -11, 26, 33, "#cbb9a4", "rx=\"2\"") + c(-27, -1, 7, "#8a6a50") + p("M-37 22 q 10 -14 20 0", "#8a6a50") +
      [...Array(4)].map((_, i) => r(-6, -7 + i * 8, i === 3 ? 26 : 44, 3, "#b9bcc4")).join(""),
    timetable: () => r(-72, -96, 144, 192, "#fbfaf5", line) + r(-60, -84, 90, 6, "#3c3c3c") +
      [...Array(9)].map((_, i) => r(-60, -64 + i * 17, 120, 1.5, "#c9ccd2")).join("") +
      [...Array(4)].map((_, i) => r(-60 + i * 40, -64, 1.5, 136, "#c9ccd2")).join("") +
      [...Array(3)].map((_, i) => `<ellipse cx="0" cy="-4" rx="${26 + i * 3}" ry="${11 + i * 2}" fill="none" stroke="#d0342c" stroke-width="2.5"/>`).join("") +
      c(42, -4, 7, "#3c3c3c") + c(39.5, -5, 1.8, "#fbfaf5") + c(44.5, -5, 1.8, "#fbfaf5") + r(39, 2, 6, 4, "#3c3c3c"),
    receipt: () => p("M-28 -84 L 28 -84 L 28 76 L 21 84 L 14 76 L 7 84 L 0 76 L -7 84 L -14 76 L -21 84 L -28 76 Z", "#fdfcf6", line) +
      r(-18, -72, 36, 5, "#5f656c") + [...Array(7)].map((_, i) => r(-20, -56 + i * 13, i % 3 === 2 ? 22 : 40, 3, "#9ea3aa")).join("") +
      r(-20, 42, 40, 2, "#5f656c") + r(4, 52, 16, 5, "#5f656c"),
    // the USB stick: a dark body, a metal end with two small squares, and a hole for a key ring
    usb_stick: () => r(-24, -8, 40, 16, "#2a2e33", "rx=\"4\"") + r(16, -6, 13, 12, "#c3c8ce", "rx=\"1\"") +
      r(20, -3, 3, 2, "#5f656c") + r(24, -3, 3, 2, "#5f656c") + c(-18, 0, 2.5, "#15181b"),
  };

  // ---------- the mess: kind, x, y, rotation (degrees), size. Later objects lie on top of earlier ones ----------
  const ITEMS = [
    ["pizza_box", 175, 165, -8, 1], ["papers", 410, 110, 14, 1], ["papers", 470, 150, -9, 1], ["papers", 560, 95, 28, 1],
    ["pizza_box", 850, 150, 17, 0.85], ["notebook", 650, 190, -16, 1], ["papers", 330, 330, -32, 1], ["papers", 720, 330, 6, 1],
    ["papers", 90, 470, 78, 1], ["crisps", 540, 330, 22, 0.9], ["calculator", 150, 470, -12, 0.95],
    ["pizza_slice", 140, 150, 35, 1], ["pizza_slice", 220, 205, -120, 1], ["pizza_slice", 780, 470, 160, 0.95],
    ["napkin", 300, 215, 20, 1], ["napkin", 640, 70, -10, 0.8], ["napkin", 430, 520, 45, 0.9], ["napkin", 905, 330, 70, 0.85],
    ["cable", 790, 260, 12, 1], ["cable", 300, 580, -6, 0.9], ["headphones", 360, 440, -25, 1],
    ["notebook", 940, 560, 72, 0.9], ["sticky_notes", 520, 210, 12, 1], ["sticky_notes", 250, 380, -20, 0.9],
    ["sticky_notes", 700, 560, 35, 0.9], ["sticky_notes", 880, 60, -8, 0.8], ["sticky_notes", 600, 420, 60, 0.75],
    ["can", 900, 150, 0, 1], ["can", 420, 280, 0, 0.95], ["can", 960, 440, 0, 1], ["mug", 255, 300, 0, 1], ["mug", 820, 400, 0, 0.95],
    ["pen", 470, 250, -38, 1], ["pen", 760, 120, 64, 0.9], ["pen", 220, 560, 8, 0.9], ["pen", 640, 510, -70, 0.85],
    ["highlighter", 580, 280, 140, 0.9], ["highlighter", 60, 300, 85, 0.9], ["keys", 285, 500, 25, 1],
    ["crisps", 980, 250, -40, 0.7],
    ["timetable", 240, 95, -14, 0.95], ["student_card", 700, 250, 18, 1], ["receipt", 375, 590, 78, 0.95],   // far from the stick
    ["usb_stick", 588, 492, 23, 1],
    ["napkin", 618, 470, -15, 0.7],   // lies over half of the USB stick
    ["pizza_slice", 470, 600, -200, 0.8], ["cable", 120, 60, 170, 0.8],
  ];

  // crumbs and grease stains: part of the table, not objects (clicking them does nothing)
  function tableTop() {
    let seed = 7;
    const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
    const grain = [...Array(26)].map((_, i) => `<path d="M0 ${12 + i * 24} Q ${250 + rnd() * 120} ${4 + i * 24 + rnd() * 18} 500 ${12 + i * 24} T 1000 ${12 + i * 24}" fill="none" stroke="#8a5a32" stroke-opacity="0.25" stroke-width="${1 + rnd() * 2}"/>`).join("");
    const crumbs = [...Array(140)].map(() => c((rnd() * W).toFixed(1), (rnd() * H).toFixed(1), (1 + rnd() * 3).toFixed(1), rnd() < 0.6 ? "#d9a35f" : "#8c6239")).join("");
    const stains = [...Array(9)].map(() => c((rnd() * W).toFixed(0), (rnd() * H).toFixed(0), (14 + rnd() * 26).toFixed(0), "#5a3417", "opacity=\"0.18\"")).join("");
    return r(0, 0, W, H, "#a87346") + grain + stains + crumbs;
  }

  // where each object is: it starts as in ITEMS and changes when the player drags it
  const transformOf = item => `translate(${item.dataset.x} ${item.dataset.y}) rotate(${item.dataset.r}) scale(${item.dataset.s})`;

  function drawing() {
    const items = ITEMS.map(([kind, x, y, angle, size], i) =>
      `<g class="table-item" data-kind="${kind}" data-index="${i}" data-x="${x}" data-y="${y}" data-r="${angle}" data-s="${size}" ` +
      `transform="translate(${x} ${y}) rotate(${angle}) scale(${size})">${SHAPES[kind]()}</g>`).join("");
    // The magnifier: a bigger copy of the table, cut in a circle, with a ring and a handle the player drags.
    // Only the ring and the handle take the mouse: a click through the glass reaches the object below.
    const lens = `<g class="table-lens"><g clip-path="url(#lens-clip)" pointer-events="none"><use href="#table-content" class="lens-view"/></g>` +
      `<g class="lens-grab"><title>${LENS_TITLE}</title><circle class="lens-ring" r="${LENS_R}" fill="none" stroke="#e8b45c" stroke-width="12" pointer-events="stroke"/>` +
      `<rect class="lens-handle" x="${LENS_R - 6}" y="-11" width="78" height="22" rx="9" fill="#5a3b1f" stroke="#e8b45c" stroke-width="3"/></g></g>`;
    // the clip path cuts what sticks out of the table (the edges of the drawing)
    return `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg" role="img"><defs><clipPath id="table-edge"><rect width="${W}" height="${H}"/></clipPath>` +
      `<clipPath id="lens-clip"><circle class="lens-hole" r="${LENS_R}"/></clipPath></defs>` +
      `<g clip-path="url(#table-edge)"><g id="table-content">${tableTop()}<g class="table-items">${items}</g><g class="table-tags"></g></g>${lens}</g></svg>`;
  }

  // ---------- the window over the game ----------
  const checked = new Set();   // kinds already clicked and wrong, while the page is open
  const moved = new Map();     // objects the player dragged: index -> {x, y}, in the order they were moved
  let card = null, busy = false, options = null;
  let LENS_TITLE = "";

  function build() {
    card = document.createElement("section");
    card.id = "table-card"; card.className = "table-card"; card.hidden = true;
    card.setAttribute("role", "dialog"); card.setAttribute("aria-labelledby", "table-title");
    card.innerHTML = `<header><div><h3 id="table-title"></h3><p id="table-hint" class="muted"></p></div>
      <button id="table-close" class="secondary"></button></header><div class="table-view"></div>`;
    (document.getElementById("investigation") || document.body).append(card);
    card.querySelector("#table-close").addEventListener("click", close);
    const view = card.querySelector(".table-view");
    view.addEventListener("pointerdown", down);
    view.addEventListener("pointermove", move);
    view.addEventListener("pointerup", up);
    view.addEventListener("pointercancel", () => { drag = null; });
    document.addEventListener("keydown", e => { if (e.key === "Escape" && card && !card.hidden) close(); });
  }

  // from the screen (mouse or finger) to the drawing's own units
  function toDrawing(event) {
    const svg = card.querySelector(".table-view svg");
    return new DOMPoint(event.clientX, event.clientY).matrixTransform(svg.getScreenCTM().inverse());
  }

  // ---------- the magnifier: it starts in a corner of the table and stays where the player leaves it ----------
  const lensAt = { x: 870, y: 480 };
  function placeLens() {
    const { x, y } = lensAt;
    card.querySelector(".lens-hole").setAttribute("cx", x);
    card.querySelector(".lens-hole").setAttribute("cy", y);
    card.querySelector(".lens-grab").setAttribute("transform", `translate(${x} ${y}) rotate(40)`);   // ring and handle
    // bigger around the centre of the glass: the point under the centre stays where it is
    card.querySelector(".lens-view").setAttribute("transform", `translate(${x} ${y}) scale(${LENS_ZOOM}) translate(${-x} ${-y})`);
  }

  // ---------- dragging and clicking ----------
  // Press and release without moving = a click (the object is checked). Press and move = drag it (free).
  let drag = null;
  function down(event) {
    if (busy) return;
    const point = toDrawing(event);
    if (event.target.closest(".lens-grab")) {
      drag = { lens: true, dx: lensAt.x - point.x, dy: lensAt.y - point.y };
    } else {
      const item = event.target.closest(".table-item");
      if (!item) return;
      drag = { item, sx: event.clientX, sy: event.clientY, px: point.x, py: point.y,
               ox: Number(item.dataset.x), oy: Number(item.dataset.y), moving: false };
    }
    try { event.currentTarget.setPointerCapture(event.pointerId); } catch (error) { /* keep going without it */ }   // keep the drag even if the mouse leaves the object
    event.preventDefault();
  }
  function move(event) {
    if (!drag) return;
    const point = toDrawing(event);
    if (drag.lens) {
      lensAt.x = Math.max(0, Math.min(W, point.x + drag.dx));
      lensAt.y = Math.max(0, Math.min(H, point.y + drag.dy));
      return placeLens();
    }
    if (!drag.moving && Math.hypot(event.clientX - drag.sx, event.clientY - drag.sy) < 6) return;   // still a click
    if (!drag.moving) { drag.moving = true; drag.item.parentNode.append(drag.item); }   // lifted: it goes on top
    const x = Math.max(0, Math.min(W, drag.ox + point.x - drag.px)), y = Math.max(0, Math.min(H, drag.oy + point.y - drag.py));
    moveItem(drag.item, x, y);
    moved.delete(drag.item.dataset.index);
    moved.set(drag.item.dataset.index, { x, y });
  }
  function up() {
    const was = drag;
    drag = null;
    if (was && was.item && !was.moving) pick(was.item);
  }
  function moveItem(item, x, y) {
    item.dataset.x = x; item.dataset.y = y;
    item.setAttribute("transform", transformOf(item));
    const label = card.querySelector(`.table-tags [data-for="${item.dataset.index}"]`);   // its ✗ label goes with it
    if (label) label.setAttribute("transform", `translate(${x - Number(label.dataset.w) / 2} ${y - 11})`);
  }

  function tag(item, text) {   // a small label on an object: "✗ Eraser"
    const x = Number(item.dataset.x), y = Number(item.dataset.y);
    const width = 16 + text.length * 7.2;
    card.querySelector(".table-tags").insertAdjacentHTML("beforeend",
      `<g data-for="${item.dataset.index}" data-w="${width}" transform="translate(${x - width / 2} ${y - 11})"><rect width="${width}" height="22" rx="11" fill="#0b1b29e6"/>` +
      `<text x="${width / 2}" y="15" text-anchor="middle" font-size="12.5" fill="#f3efe6">${text.replace(/</g, "&lt;")}</text></g>`);
  }

  function markChecked(kind) {
    checked.add(kind);
    card.querySelectorAll(`.table-item[data-kind="${kind}"]`).forEach(item => {
      if (item.classList.contains("checked")) return;
      item.classList.add("checked");
      tag(item, `✗ ${options.labels[kind] || kind}`);
    });
  }

  async function pick(item) {
    if (busy || item.classList.contains("checked")) return;
    const kind = item.dataset.kind;
    busy = true;
    try {
      const result = await options.pick(kind);   // "found", "wrong", or nothing (nothing happened)
      if (result === "wrong") markChecked(kind);
      if (result === "found") {
        item.classList.add("found");
        tag(item, options.labels[kind] || kind);
        setTimeout(close, 1600);
      }
    } finally { busy = false; }
  }

  function open(opts) {
    options = opts;
    LENS_TITLE = (opts.lens || "").replace(/</g, "&lt;");
    if (!card) build();
    card.querySelector("#table-title").textContent = opts.title;
    card.querySelector("#table-hint").textContent = opts.hint;
    card.querySelector("#table-close").textContent = opts.close;
    card.querySelector(".table-view").innerHTML = drawing();
    // the table as the player left it: dragged objects where they were put, on top, in the same order
    const list = card.querySelector(".table-items");
    moved.forEach(({ x, y }, index) => {
      const item = list.querySelector(`[data-index="${index}"]`);
      list.append(item);
      moveItem(item, x, y);
    });
    checked.forEach(kind => markChecked(kind));
    placeLens();
    card.hidden = false;
    card.querySelector("#table-close").focus({ preventScroll: true });
  }

  function close() {
    if (!card || card.hidden) return;
    card.hidden = true;
    drag = null;
    if (options && options.onClose) options.onClose();
  }

  // reset: a new game puts the table back as it was
  window.campusTable = { open, close, reset: () => { checked.clear(); moved.clear(); }, isOpen: () => Boolean(card && !card.hidden), drawing };
})();
