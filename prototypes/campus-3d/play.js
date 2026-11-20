/* The screen sends commands; Python alone decides and saves their effects. */
(() => {
  "use strict";
  const data = JSON.parse(document.getElementById("data").textContent);
  const $ = id => document.getElementById(id);
  const make = (tag, text, cls) => {
    const el = document.createElement(tag);
    if (text !== undefined) el.textContent = text;
    if (cls) el.className = cls;
    return el;
  };
  const ui = () => data[window.lang || "pt"].play_ui;
  document.body.classList.add("playable");

  const nameBox = make("div", undefined, "name-box");
  const nameLabel = make("label"); nameLabel.htmlFor = "detective-name";
  const name = make("input"); name.id = "detective-name"; name.maxLength = 20;
  name.autocomplete = "nickname";
  const nameHint = make("p", undefined, "muted");
  const startError = make("p", "", "error"); startError.setAttribute("role", "alert");
  nameBox.append(nameLabel, name, nameHint, startError);
  $("mission").after(nameBox);

  const shell = make("main"); shell.id = "investigation"; shell.hidden = true;
  shell.innerHTML = `
    <header class="case-bar"><div><p id="case-eyebrow" class="label"></p><h1 id="game-title"></h1></div>
      <div class="bar-tools"><span id="save-status" role="status"></span>
        <div class="tool-row"><button id="phone-open" class="secondary"></button><button id="panel-toggle" class="secondary" aria-expanded="true"></button><button id="view-toggle" class="secondary"></button></div></div></header>
    <section class="scene-panel" aria-labelledby="scene-heading">
      <div class="scene-top"><span id="scene-label" class="label"></span><span id="player-label" class="muted"></span></div>
      <h2 id="scene-heading" tabindex="-1"></h2><p id="feedback" role="status"></p>
      <div id="scene-paragraphs"></div><p id="outside-hint" class="muted" hidden></p><div id="action-groups"></div>
      <details id="notebook"><summary id="notebook-label"></summary><p id="notebook-hint" class="muted"></p><div id="notes"></div></details>
      <section aria-labelledby="inventory-label" class="inventory"><h3 id="inventory-label"></h3><ul id="inventory-list"></ul></section>
      <footer class="panel-foot"><button id="restart" class="secondary"></button><span id="controls" class="muted"></span></footer>
    </section>
    <div id="toast" role="status" aria-live="polite" hidden></div>
    <p id="renderer-status" class="renderer-status"></p>`;
  document.body.append(shell);
  const dialog = make("dialog"); dialog.id = "restart-dialog";
  dialog.setAttribute("aria-labelledby", "restart-question");
  dialog.innerHTML = '<h2 id="restart-question"></h2><div class="dialog-actions"><button id="cancel-restart" class="secondary"></button><button id="confirm-restart"></button></div>';
  document.body.append(dialog);
  let current = null, textMode = false, uncertain = false;

  function updateLabels() {
    const t = ui();
    document.documentElement.lang = window.lang || "pt";
    nameLabel.textContent = t.name_label;
    nameHint.textContent = t.continue_hint;
    $("accept").textContent = t.start;
    $("case-eyebrow").textContent = t.case;
    $("game-title").textContent = t.title;
    $("scene-label").textContent = current?.ending ? t.the_end : t.scene;
    $("inventory-label").textContent = t.inventory;
    $("notebook-label").textContent = t.notebook;
    $("notebook-hint").textContent = t.notebook_hint;
    $("restart").textContent = t.new_game;
    $("controls").textContent = t.controls;
    $("outside-hint").textContent = t.outside_hint;
    $("phone-open").textContent = `📱 ${t.phone}`;
    $("phone-open").setAttribute("aria-label", t.phone_open);
    $("panel-toggle").textContent = document.body.classList.contains("panel-hidden") ? t.show_panel : t.hide_panel;
    $("restart-question").textContent = t.confirm_question;
    $("cancel-restart").textContent = t.confirm_cancel;
    $("confirm-restart").textContent = t.confirm_yes;
    $("view-toggle").textContent = textMode ? t.world_mode : t.text_mode;
    $("renderer-status").textContent = window.campus3dReady ? t.render_ready : t.render_loading;
  }
  window.addEventListener("language", () => { queueMicrotask(updateLabels); startError.textContent = ""; });
  window.addEventListener("campus-renderer-ready", updateLabels);
  function fallback() {
    if (window.campus3dReady) return;
    textMode = true;
    document.body.classList.add("text-mode");
    setPanelHidden(false);   // in text mode the panel is the whole game
    updateLabels();
  }
  window.addEventListener("campus-renderer-failed", fallback);
  if (window.campusRenderFailed) fallback();
  setTimeout(fallback, 12000);
  updateLabels();

  // Investigating needs the character inside the room of the saved scene. Travel buttons always work.
  function applyInside() {
    const outside = window.campusInside === false && !current?.ending;
    $("outside-hint").hidden = !outside;
    shell.querySelectorAll(".actions.investigate button").forEach(b => { b.disabled = outside || Boolean(window.campusBusy); });
  }
  window.addEventListener("campus-inside", applyInside);

  function setBusy(busy) {
    window.campusBusy = busy;
    shell.querySelectorAll("button").forEach(b => b.disabled = busy);
    $("accept").disabled = busy;
    $("back").disabled = busy;
    dialog.querySelectorAll("button").forEach(b => b.disabled = busy);
    applyInside();
    $("save-status").textContent = busy ? ui().saving : (uncertain ? "" : ui().saved);
  }

  async function send(operation, extra = {}) {
    if (window.campusBusy) return;
    if (location.protocol === "file:") { startError.textContent = ui().local_only; return; }
    setBusy(true);
    try {
      const response = await fetch("/api/command", {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ operation, player: current?.player || name.value,
          language: window.lang || "pt", ...extra }),
        signal: AbortSignal.timeout(12000),
      });
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || ui().network_error);
      uncertain = false;
      render(result);
      return true;
    } catch (error) {
      uncertain = true;
      const message = error.name === "Error" ? error.message : ui().network_error;
      (current ? $("feedback") : startError).textContent = message;
      if (current) { $("feedback").className = "error"; $("feedback").hidden = false; toast(message); }
      return false;
    } finally { setBusy(false); }
  }

  function render(state) {
    const roomChanged = !current || current.scene !== state.scene || Boolean(current.ending) !== Boolean(state.ending);
    current = state;
    window.campusState = state;
    window.lang = state.language;
    window.dispatchEvent(new Event("language"));
    window.dispatchEvent(new Event("campus-state"));
    const t = ui();
    $("scene-heading").textContent = state.ending ? state.ending.title : state.title;
    $("scene-label").textContent = state.ending ? t.the_end : t.scene;
    $("player-label").textContent = `${t.player} · ${state.player}`;
    $("feedback").textContent = state.message;
    $("feedback").className = state.accepted ? "success" : "error";
    $("feedback").hidden = !state.message;
    $("scene-paragraphs").replaceChildren(...(state.ending ? [state.ending.text] : state.texts).map(p => make("p", p)));
    $("action-groups").replaceChildren();
    if (!state.ending) {
      for (const kind of ["investigate", "travel"]) {
        const group = make("section", undefined, `actions ${kind}`);
        group.append(make("h3", t[kind]));
        const actions = state.actions.filter(a => a.kind === kind);
        if (!actions.length && kind === "travel") continue;
        if (!actions.length) group.append(make("p", t.no_actions, "muted"));
        for (const action of actions) {
          const box = make("div", undefined, "action-row");
          const button = make("button", action.label, action.allowed ? "" : "locked");
          button.dataset.action = action.id;
          button.addEventListener("click", () => send("play", { action: action.id }));
          box.append(button);
          // A blocked button still explains the rule if clicked; it never moves or saves.
          if (action.blocked_text || action.decision) {
            const hint = make("p", action.allowed ? t.decision : `${t.locked}: ${action.blocked_text}`, "action-hint");
            hint.id = `hint-${action.id}`;
            button.setAttribute("aria-describedby", hint.id);
            box.append(hint);
          }
          group.append(box);
        }
        $("action-groups").append(group);
      }
    }
    $("inventory-list").replaceChildren(...(state.inventory.length
      ? state.inventory.map(item => make("li", item.label)) : [make("li", t.inventory_empty, "muted")]));
    $("notes").replaceChildren();
    if (!state.notebook.length) $("notes").append(make("p", t.empty_notes, "muted"));
    state.notebook.forEach((note, i) => {
      const article = make("article", undefined, "note");
      article.append(make("h3", `${String(i + 1).padStart(2, "0")} · ${note.title}`), make("p", note.text));
      $("notes").append(article);
    });
    shell.classList.toggle("ended", Boolean(state.ending));
    applyInside();
    if (state.ending) setPanelHidden(false);                 // the ending text lives in the panel
    if (!state.accepted && state.message) toast(state.message);   // a refusal also shows as a note over the picture
    if (roomChanged) {
      $("scene-heading").focus({ preventScroll: true });
      document.querySelector(".scene-panel").scrollTop = 0;
    }
  }

  // ---------- hide the side panel ----------
  function setPanelHidden(hidden) {
    document.body.classList.toggle("panel-hidden", hidden);
    $("panel-toggle").textContent = hidden ? ui().show_panel : ui().hide_panel;
    $("panel-toggle").setAttribute("aria-expanded", String(!hidden));
    window.dispatchEvent(new Event("resize"));   // the 3D picture takes the new width
  }
  $("panel-toggle").addEventListener("click", () => setPanelHidden(!document.body.classList.contains("panel-hidden")));

  // ---------- a note over the 3D picture: it stays visible even when the panel is hidden ----------
  let toastTimer;
  function toast(text) {
    $("toast").textContent = text;
    $("toast").hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { $("toast").hidden = true; }, 8000);
  }

  // ---------- the phone: a map and the to-do list of clues ----------
  const phone = make("dialog", undefined, "phone-dialog"); phone.id = "phone";
  phone.setAttribute("aria-labelledby", "phone-title");
  phone.innerHTML = `<div class="phone"><div class="phone-notch"></div>
    <header class="phone-bar"><button id="phone-back" class="phone-btn" hidden></button><h2 id="phone-title"></h2><button id="phone-close" class="phone-btn">✕</button></header>
    <section id="phone-screen"></section></div>`;
  document.body.append(phone);

  const SVG_NS = "http://www.w3.org/2000/svg";
  function svg(tag, attrs, text) {
    const el = document.createElementNS(SVG_NS, tag);
    for (const [name, value] of Object.entries(attrs || {})) el.setAttribute(name, value);
    if (text !== undefined) el.textContent = text;
    return el;
  }
  const clueCount = () => {
    const clues = current?.clues || [];
    return { done: clues.filter(c => c.done).length, total: clues.length };
  };
  const titleLines = text => {   // a long room name goes on two lines
    const words = text.split(" ");
    if (words.length < 2) return [text];
    const half = Math.ceil(words.length / 2);
    return [words.slice(0, half).join(" "), words.slice(half).join(" ")];
  };

  function drawTodo(screen, t) {
    const { done, total } = clueCount();
    screen.append(make("p", `${done} / ${total} ${t.todo_progress}`, "todo-count"));
    const bar = make("div", undefined, "todo-bar"), fill = make("span");
    fill.style.width = `${total ? (100 * done) / total : 0}%`;
    bar.append(fill);
    const list = make("ul", undefined, "todo-list");
    for (const clue of current?.clues || []) {
      const item = make("li", undefined, clue.done ? "done" : "");
      const box = make("span", clue.done ? "✔" : "○", "todo-box");
      box.setAttribute("aria-label", clue.done ? t.todo_done : t.todo_open);
      const text = make("span", undefined, "todo-text");
      text.append(make("strong", clue.label), make("small", `${t.todo_where}: ${clue.room}`));
      item.append(box, text);
      list.append(item);
    }
    screen.append(bar, list, make("p", t.todo_hint, "muted todo-hint"));
  }

  function drawMap(screen, t) {
    const titles = data[window.lang || "pt"].scenes;
    const map = window.campusMap && window.campusMap();
    if (!map) {   // the 3D scenery did not load: only say where the character is
      screen.append(make("p", t.map_no_3d, "muted"), make("p", `${t.map_where}: ${titles[current.scene].title}`, "map-where"));
      return;
    }
    const ready = (current?.clues || []).every(c => c.done);
    const X0 = -30, Z0 = -13, K = 10, W = 44 * K, H = 26 * K;   // the map shows x from -30 to 14 and z from -13 to 13
    const sx = x => (x - X0) * K, sy = z => (z - Z0) * K;
    const board = svg("svg", { viewBox: `0 0 ${W} ${H}`, class: "map-svg", role: "img", "aria-label": t.map_title });
    board.append(
      svg("rect", { x: 0, y: 0, width: W, height: H, class: "map-plaza" }),
      svg("text", { x: sx(-22.5), y: sy(10), class: "map-label small" }, t.map_outside),
      svg("rect", { x: sx(-29.5), y: sy(-3.7), width: 5 * K, height: 10, rx: 3, class: "map-sign" }),
      svg("text", { x: sx(-27), y: sy(-3.2) + 3.5, class: "map-label sign-text" }, "NOVA"),
      svg("rect", { x: sx(-13), y: sy(-3), width: 26 * K, height: 6 * K, class: "map-corridor" }),
      svg("text", { x: sx(0), y: sy(0) + 4, class: "map-label small" }, t.map_corridor),
    );
    for (const room of map.rooms) {
      const mine = map.here === room.id, locked = room.id === "auditorium" && !ready;
      const cx = sx((room.minX + room.maxX) / 2), cy = sy((room.minZ + room.maxZ) / 2);
      board.append(
        svg("rect", { x: sx(room.minX), y: sy(room.minZ), width: (room.maxX - room.minX) * K, height: (room.maxZ - room.minZ) * K,
                      class: `map-room${mine ? " here" : ""}${locked ? " locked" : ""}` }),
        svg("text", { x: cx, y: cy - 8, class: "map-icon" }, `${room.icon}${locked ? "🔒" : ""}`),
      );
      titleLines(titles[room.id].title).forEach((line, i) => board.append(svg("text", { x: cx, y: cy + 10 + i * 15, class: "map-label" }, line)));
    }
    board.append(svg("rect", { x: sx(-13) - 3, y: sy(-1.3), width: 6, height: 2.6 * K, class: "map-door" }));
    // you: shown where the character stands at the moment the map is opened
    const px = Math.max(10, Math.min(W - 10, sx(map.player.x))), py = Math.max(10, Math.min(H - 10, sy(map.player.z)));
    board.append(
      svg("circle", { cx: px, cy: py, r: 13, class: "map-pulse" }),
      svg("circle", { cx: px, cy: py, r: 6, class: "map-you" }),
      // the label goes below the dot (above it near the bottom edge), clear of the room names
      svg("text", { x: Math.max(40, Math.min(W - 40, px)), y: py > H - 40 ? py - 17 : py + 28, class: "map-you-label" }, t.map_you),
    );
    const place = map.here === "outside" ? t.map_outside : map.here ? titles[map.here].title : t.map_corridor;
    screen.append(board, make("p", `${t.map_where}: ${place}`, "map-where"));
    if (!ready) screen.append(make("p", `🔒 ${titles.auditorium.title}: ${t.map_locked}`, "muted map-lock"));
  }

  function showPhone(view) {
    const t = ui(), screen = $("phone-screen");
    $("phone-back").hidden = view === "home";
    $("phone-back").textContent = `‹ ${t.phone_home}`;
    $("phone-close").setAttribute("aria-label", t.phone_close);
    $("phone-title").textContent = view === "map" ? t.map_title : view === "todo" ? t.todo_title : t.phone;
    screen.replaceChildren();
    if (view === "home") {
      const { done, total } = clueCount();
      const grid = make("div", undefined, "app-grid");
      for (const [id, icon, label, badge] of [["map", "📍", t.app_map, ""], ["todo", "✅", t.app_todo, `${done}/${total}`]]) {
        const app = make("button", undefined, "app-icon");
        app.dataset.app = id;
        app.append(make("span", icon, "app-glyph"), make("span", label, "app-name"));
        if (badge) app.append(make("span", badge, "app-badge"));
        app.addEventListener("click", () => showPhone(id));
        grid.append(app);
      }
      screen.append(grid);
    } else if (view === "map") drawMap(screen, t);
    else drawTodo(screen, t);
    (view === "home" ? screen.querySelector("button") : $("phone-back")).focus();
  }
  function openPhone() {
    if (!current || window.campusBusy || phone.open) return;
    window.playing = false;   // the character stands still while the phone is out
    showPhone("home");
    phone.showModal();
  }
  function closePhone() {
    phone.close();
    window.playing = true;
    $("phone-open").focus();
  }
  $("phone-open").addEventListener("click", openPhone);
  $("phone-close").addEventListener("click", closePhone);
  $("phone-back").addEventListener("click", () => showPhone("home"));
  phone.addEventListener("cancel", e => { e.preventDefault(); closePhone(); });

  window.campusStart = async () => {
    if (!await send("open")) return;
    $("intro").classList.add("gone");
    $("intro").style.display = "none";
    shell.hidden = false;
    window.playing = true;
    window.dispatchEvent(new Event("start-game"));
    $("scene-heading").focus({ preventScroll: true });
  };
  // The 3D scene calls this when the character walks through a door into another room.
  window.campusEnter = room => send("enter", { room });
  name.addEventListener("keydown", e => {
    if (e.key === "Enter" && $("accept").classList.contains("ready")) window.campusStart();
  });
  $("restart").addEventListener("click", () => {
    window.playing = false;
    dialog.showModal();
    $("cancel-restart").focus();
  });
  const closeDialog = () => { dialog.close(); window.playing = true; $("restart").focus(); };
  $("cancel-restart").addEventListener("click", closeDialog);
  dialog.addEventListener("cancel", e => { e.preventDefault(); closeDialog(); });
  $("confirm-restart").addEventListener("click", async () => {
    if (await send("restart", { confirmed: true })) {
      dialog.close(); window.playing = true; $("scene-heading").focus();
    }
  });
  $("view-toggle").addEventListener("click", () => {
    textMode = !textMode;
    document.body.classList.toggle("text-mode", textMode);
    if (textMode) setPanelHidden(false);
    updateLabels();
  });
})();
