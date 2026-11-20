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
      <div class="bar-tools"><span id="save-status" role="status"></span><button id="view-toggle" class="secondary"></button></div></header>
    <section class="scene-panel" aria-labelledby="scene-heading">
      <div class="scene-top"><span id="scene-label" class="label"></span><span id="player-label" class="muted"></span></div>
      <h2 id="scene-heading" tabindex="-1"></h2><p id="feedback" role="status"></p>
      <div id="scene-paragraphs"></div><div id="action-groups"></div>
      <details id="notebook"><summary id="notebook-label"></summary><p id="notebook-hint" class="muted"></p><div id="notes"></div></details>
      <section aria-labelledby="inventory-label" class="inventory"><h3 id="inventory-label"></h3><ul id="inventory-list"></ul></section>
      <footer class="panel-foot"><button id="restart" class="secondary"></button><span id="controls" class="muted"></span></footer>
    </section>
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
    updateLabels();
  }
  window.addEventListener("campus-renderer-failed", fallback);
  if (window.campusRenderFailed) fallback();
  setTimeout(fallback, 12000);
  updateLabels();

  function setBusy(busy) {
    window.campusBusy = busy;
    shell.querySelectorAll("button").forEach(b => b.disabled = busy);
    $("accept").disabled = busy;
    $("back").disabled = busy;
    dialog.querySelectorAll("button").forEach(b => b.disabled = busy);
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
      if (current) { $("feedback").className = "error"; $("feedback").hidden = false; }
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
    if (roomChanged) {
      $("scene-heading").focus({ preventScroll: true });
      document.querySelector(".scene-panel").scrollTop = 0;
    }
  }

  window.campusStart = async () => {
    if (!await send("open")) return;
    $("intro").classList.add("gone");
    $("intro").style.display = "none";
    shell.hidden = false;
    window.playing = true;
    window.dispatchEvent(new Event("start-game"));
    $("scene-heading").focus({ preventScroll: true });
  };
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
    updateLabels();
  });
})();
