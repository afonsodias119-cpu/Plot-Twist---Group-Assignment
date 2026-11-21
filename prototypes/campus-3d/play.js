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
  // One emoji for each ending (the collection and the share card). It is defined here because the first screen uses it at start-up.
  const ENDING_EMOJI = { full_case: "🏆", impostor: "🔍", stolen_credits: "💸", fifth_element: "👁️" };
  document.body.classList.add("playable");

  const nameBox = make("div", undefined, "name-box");
  const nameLabel = make("label"); nameLabel.htmlFor = "detective-name";
  const name = make("input"); name.id = "detective-name"; name.maxLength = 20;
  name.autocomplete = "nickname";
  const nameHint = make("p", undefined, "muted");
  const startError = make("p", "", "error"); startError.setAttribute("role", "alert");
  const collection = make("p", undefined, "muted collection");   // the endings found so far, kept in this browser
  nameBox.append(nameLabel, name, nameHint, collection, startError);
  $("mission").after(nameBox);

  const shell = make("main"); shell.id = "investigation"; shell.hidden = true;
  shell.innerHTML = `
    <header class="case-bar"><div><p id="case-eyebrow" class="label"></p><h1 id="game-title"></h1></div>
      <div class="bar-tools"><span id="clock" class="clock"></span><span id="save-status" role="status"></span>
        <div class="tool-row"><button id="howto-open" class="secondary icon-btn">ℹ️</button><button id="voice-toggle" class="secondary icon-btn"></button><button id="torch-toggle" class="secondary icon-btn"></button><button id="sound-toggle" class="secondary"></button><button id="phone-open" class="secondary"></button></div></div></header>
    <section class="scene-panel" aria-labelledby="scene-heading">
      <div class="scene-top"><span id="scene-label" class="label"></span><span id="player-label" class="muted"></span></div>
      <h2 id="scene-heading" tabindex="-1"></h2><p id="feedback" role="status"></p>
      <div id="scene-paragraphs"></div><div id="action-groups"></div>
      <details id="notebook"><summary id="notebook-label"></summary><p id="notebook-hint" class="muted"></p><div id="notes"></div></details>
      <section aria-labelledby="inventory-label" class="inventory"><h3 id="inventory-label"></h3><ul id="inventory-list"></ul></section>
      <footer class="panel-foot"><button id="restart" class="secondary"></button><span id="controls" class="muted"></span></footer>
    </section>
    <div id="toast" role="status" aria-live="polite" hidden></div>
    <button id="sms" class="sms" hidden><span id="sms-from" class="sms-from"></span><span id="sms-text"></span></button>
    <div id="confetti" class="confetti" aria-hidden="true" hidden></div>
    <section id="chat-card" class="chat-card" role="dialog" aria-labelledby="chat-title" hidden>
      <header><h3 id="chat-title"></h3><button id="chat-close" class="secondary"></button></header>
      <p id="chat-intro" class="muted"></p><ol id="chat-messages"></ol></section>
    <section id="ending-card" class="ending-card" role="dialog" aria-labelledby="ending-title" hidden>
      <p id="ending-stamp" class="stamp"></p><p id="ending-label" class="label"></p><h2 id="ending-title"></h2><div id="ending-text"></div>
      <p id="ending-collection" class="collection"></p>
      <div class="share"><pre id="share-text"></pre><button id="share-copy" class="secondary"></button></div>
      <div class="ending-actions"><button id="ending-again"></button><button id="ending-hide" class="secondary"></button></div></section>
    <button id="panel-toggle" class="panel-tab" aria-expanded="true"></button>
    <div id="hud-bottom" class="hud-bottom">
      <button id="near-hint" class="near-hint" hidden></button>
      <div id="action-bar" class="action-bar" hidden><p id="outside-hint" class="muted" hidden></p><div id="bar-actions" class="actions investigate"></div></div>
    </div>
    <section id="talk" class="talk-card" role="dialog" aria-labelledby="talk-name" aria-live="polite" hidden>
      <header><h3 id="talk-name"></h3><span id="talk-trust" class="trust"></span><button id="talk-close" class="secondary"></button></header>
      <p id="talk-text"></p><div id="talk-options"></div></section>
    <p id="renderer-status" class="renderer-status"></p>`;
  document.body.append(shell);
  const dialog = make("dialog"); dialog.id = "restart-dialog";
  dialog.setAttribute("aria-labelledby", "restart-question");
  dialog.innerHTML = '<h2 id="restart-question"></h2><div class="dialog-actions"><button id="cancel-restart" class="secondary"></button><button id="confirm-restart"></button></div>';
  document.body.append(dialog);
  let current = null, textMode = false, uncertain = false, talking = null;   // talking: the person being talked to
  // ---------- sound: everything is generated in the browser, there are no sound files ----------
  const sound = (() => {
    let ctx = null, master = null, seaGain = null, muted = false, lastStep = 0;
    try { muted = localStorage.getItem("plot-twist-sound") === "off"; } catch (error) { /* no storage */ }
    function start() {
      if (ctx) { if (ctx.state === "suspended") ctx.resume(); return; }
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) return;
      try {
        ctx = new AudioContextClass();
        master = ctx.createGain(); master.gain.value = muted ? 0 : 0.5; master.connect(ctx.destination);
        // the sea: soft noise through a low-pass filter whose cut-off swells like waves
        const length = ctx.sampleRate * 4, buffer = ctx.createBuffer(1, length, ctx.sampleRate), data = buffer.getChannelData(0);
        let last = 0;
        for (let i = 0; i < length; i++) { last = (last + 0.02 * (Math.random() * 2 - 1)) / 1.02; data[i] = last * 3.5; }
        const sea = ctx.createBufferSource(); sea.buffer = buffer; sea.loop = true;
        const filter = ctx.createBiquadFilter(); filter.type = "lowpass"; filter.frequency.value = 500;
        const swell = ctx.createOscillator(); swell.frequency.value = 0.12;
        const swellDepth = ctx.createGain(); swellDepth.gain.value = 130;
        swell.connect(swellDepth); swellDepth.connect(filter.frequency); swell.start();
        seaGain = ctx.createGain(); seaGain.gain.value = 0;
        sea.connect(filter); filter.connect(seaGain); seaGain.connect(master); sea.start();
        startMusic();
      } catch (error) { ctx = null; }
    }
    function tone(freq, seconds, type, volume, slideTo) {
      if (!ctx || muted) return;
      const now = ctx.currentTime, osc = ctx.createOscillator(), gain = ctx.createGain();
      osc.type = type; osc.frequency.setValueAtTime(freq, now);
      if (slideTo) osc.frequency.exponentialRampToValueAtTime(slideTo, now + seconds);
      gain.gain.setValueAtTime(volume, now); gain.gain.exponentialRampToValueAtTime(0.0001, now + seconds);
      osc.connect(gain); gain.connect(master); osc.start(now); osc.stop(now + seconds + 0.02);
    }
    function step() {
      if (!ctx || muted) return;
      const now = ctx.currentTime, osc = ctx.createOscillator(), gain = ctx.createGain();
      osc.type = "triangle"; osc.frequency.setValueAtTime(110 + Math.random() * 30, now); osc.frequency.exponentialRampToValueAtTime(55, now + 0.09);
      gain.gain.setValueAtTime(0.07, now); gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.1);
      osc.connect(gain); gain.connect(master); osc.start(now); osc.stop(now + 0.12);
    }
    // music: a low drone and a pulse that get faster and darker as the night goes on (tension 0..1)
    let tension = 0, droneGain = null, droneFilter = null, musicOn = false, beatCount = 0;
    const NOTES = [110, 130.8, 164.8, 196, 220];   // A minor
    function startMusic() {
      if (musicOn || !ctx) return;
      musicOn = true;
      droneFilter = ctx.createBiquadFilter(); droneFilter.type = "lowpass"; droneFilter.frequency.value = 200;
      droneGain = ctx.createGain(); droneGain.gain.value = 0;
      for (const detune of [0, 8]) {
        const osc = ctx.createOscillator(); osc.type = "sawtooth"; osc.frequency.value = 55; osc.detune.value = detune;
        osc.connect(droneFilter); osc.start();
      }
      droneFilter.connect(droneGain); droneGain.connect(master);
      beat();
    }
    function beat() {
      if (ctx && !muted && window.campusState && !window.campusState.ending) {
        const now = ctx.currentTime, osc = ctx.createOscillator(), gain = ctx.createGain();   // the pulse: a soft thump
        osc.type = "sine"; osc.frequency.setValueAtTime(72, now); osc.frequency.exponentialRampToValueAtTime(38, now + 0.16);
        gain.gain.setValueAtTime(0.05 + 0.07 * tension, now); gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.2);
        osc.connect(gain); gain.connect(master); osc.start(now); osc.stop(now + 0.22);
        if (beatCount++ % 2 === 1) tone(NOTES[Math.floor(Math.random() * NOTES.length)] * (tension > 0.6 ? 2 : 1), 0.7, "triangle", 0.012 + 0.02 * tension);
      }
      setTimeout(beat, 60000 / (52 + 78 * tension));   // from 52 to 130 beats a minute
    }
    // every 120 ms: footsteps while the character walks, and the sea louder outside than inside a room
    setInterval(() => {
      if (!ctx || muted) return;
      const outside = window.campusInside === false;
      seaGain.gain.setTargetAtTime(outside ? 0.3 : 0.07, ctx.currentTime, 0.5);
      if (droneGain) {
        const playing = Boolean(window.campusState) && !window.campusState.ending;
        droneGain.gain.setTargetAtTime(playing ? 0.02 + 0.035 * tension : 0, ctx.currentTime, 0.8);
        droneFilter.frequency.setTargetAtTime(160 + 520 * tension, ctx.currentTime, 0.8);
      }
      if (window.campusMoving && window.playing && ctx.currentTime - lastStep > 0.34) { lastStep = ctx.currentTime; step(); }
    }, 120);
    return {
      start,
      isMuted: () => muted,
      toggle() {
        muted = !muted;
        try { localStorage.setItem("plot-twist-sound", muted ? "off" : "on"); } catch (error) { /* no storage */ }
        if (master) master.gain.value = muted ? 0 : 0.5;
        if (!muted) start();
      },
      click: () => tone(620, 0.05, "square", 0.025),
      chime() { tone(660, 0.18, "sine", 0.1); setTimeout(() => tone(990, 0.3, "sine", 0.09), 110); },
      refuse: () => tone(150, 0.28, "sawtooth", 0.06, 90),
      talk: () => tone(340 + Math.random() * 60, 0.07, "triangle", 0.05),
      buzz() { tone(110, 0.13, "square", 0.07); setTimeout(() => tone(110, 0.13, "square", 0.07), 180); },   // the phone
      setTension(value) { tension = Math.max(0, Math.min(1, value)); },
    };
  })();
  // The torch of the 3D scene and the voices of the people; both are remembered in this browser.
  let torchOn = true, voiceOn = true;
  try { torchOn = localStorage.getItem("plot-twist-torch") !== "off"; voiceOn = localStorage.getItem("plot-twist-voice") !== "off"; } catch (error) { /* no storage */ }
  window.campusTorchOn = torchOn;
  const canSpeak = "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;
  // Who speaks: [gender, pitch, speed]. Computer 12 has no voice and stays silent.
  // Only what the people SAY is read aloud (the text between quotation marks), never the description of what they do.
  const VOICES = { rita: ["f", 1.08, 1.0], amelia: ["f", 0.95, 0.92], leonor: ["f", 1.0, 1.0],
                   tomas: ["m", 1.06, 1.05], professor: ["m", 0.88, 0.9], duarte: ["m", 0.94, 0.95], narrator: ["f", 1, 0.95] };
  const FEMALE = /raquel|fernanda|francisca|helia|heloisa|maria|joana|catarina|sonia|libby|maisie|hazel|susan|zira|emily|female|feminina/i;
  const MALE = /duarte|antonio|daniel|ricardo|hugo|ryan|thomas|george|mark|david|james|male|masculino/i;
  // The natural (neural, online) voices of the browser sound far more human than the old robotic ones.
  const voiceQuality = voice => (/natural|online/i.test(voice.name) ? 3 : /neural|premium|enhanced/i.test(voice.name) ? 2 : /google/i.test(voice.name) ? 1 : 0);
  function pickVoice(who, lang) {
    const normal = voice => voice.lang.toLowerCase().replace("_", "-");
    const all = speechSynthesis.getVoices().filter(voice => normal(voice).startsWith(lang.slice(0, 2).toLowerCase()));
    if (!all.length) return null;
    const region = all.filter(voice => normal(voice) === lang.toLowerCase());   // pt-PT and en-GB when there are such voices
    const pool = region.length ? region : all;
    const ofGender = pool.filter(voice => (VOICES[who][0] === "f" ? FEMALE : MALE).test(voice.name));
    const ranked = (ofGender.length ? ofGender : pool).slice().sort((a, b) => voiceQuality(b) - voiceQuality(a));
    const best = ranked.filter(voice => voiceQuality(voice) === voiceQuality(ranked[0]));
    return best[Object.keys(VOICES).indexOf(who) % best.length];   // the different people get different voices when there are several
  }
  const quotesOf = text => [...text.matchAll(/"([^"]+)"|«([^»]+)»|“([^”]+)”/g)].map(match => (match[1] || match[2] || match[3]).trim());
  function stopSpeaking() { if (canSpeak) speechSynthesis.cancel(); }
  // pairs: [line, who]. Each sentence is spoken on its own, so there are natural pauses and long lines are not cut off.
  function say(pairs) {
    const lang = (window.lang || "pt") === "pt" ? "pt-PT" : "en-GB";
    for (const [line, who] of pairs) {
      const [, pitch, rate] = VOICES[who];
      for (const sentence of line.split(/(?<=[.!?…])\s+/)) {
        const utterance = new SpeechSynthesisUtterance(sentence);
        utterance.lang = lang;
        utterance.voice = pickVoice(who, lang);
        utterance.pitch = pitch;
        utterance.rate = rate * (0.97 + Math.random() * 0.06);   // a tiny change from sentence to sentence, like a real voice
        speechSynthesis.speak(utterance);
      }
    }
  }
  function speak(text, who) {
    if (!canSpeak || !voiceOn || !VOICES[who]) return;
    stopSpeaking();
    say(quotesOf(text).map(line => [line, who]));
  }
  function speakEnding(ending) {
    if (!canSpeak || !voiceOn) return;
    stopSpeaking();
    const speakers = (ui().ending_voices || {})[ending.id] || [];
    say(quotesOf(ending.text).map((line, i) => [line, VOICES[speakers[i]] ? speakers[i] : "narrator"]));
  }
  if (canSpeak) speechSynthesis.getVoices();   // some browsers only load the list after the first call
  document.addEventListener("pointerdown", () => sound.start());
  document.addEventListener("click", e => { if (e.target.closest("button:not(:disabled)")) sound.click(); });


  function updateLabels() {
    const t = ui();
    document.documentElement.lang = window.lang || "pt";
    nameLabel.textContent = t.name_label;
    nameHint.textContent = t.continue_hint;
    collection.textContent = collectionText();
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
    paintPanelTab();
    $("talk-close").textContent = t.talk_close;
    $("howto-open").setAttribute("aria-label", t.howto_open); $("howto-open").title = t.howto_open;
    $("voice-toggle").hidden = !canSpeak;
    $("voice-toggle").textContent = voiceOn ? "🗣️" : "🤐"; $("voice-toggle").setAttribute("aria-label", voiceOn ? t.voice_on : t.voice_off); $("voice-toggle").title = voiceOn ? t.voice_on : t.voice_off;
    $("torch-toggle").textContent = torchOn ? "🔦" : "🌑"; $("torch-toggle").setAttribute("aria-label", torchOn ? t.torch_on : t.torch_off); $("torch-toggle").title = torchOn ? t.torch_on : t.torch_off;
    $("sound-toggle").textContent = sound.isMuted() ? "🔇" : "🔊";
    $("sound-toggle").setAttribute("aria-label", sound.isMuted() ? t.sound_off : t.sound_on);
    $("restart-question").textContent = t.confirm_question;
    $("cancel-restart").textContent = t.confirm_cancel;
    $("confirm-restart").textContent = t.confirm_yes;
    updateNear();
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
    shell.querySelectorAll("#chat-messages li.flagged button").forEach(b => { b.disabled = true; });   // a flag cannot be undone
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

  async function request(payload) {
    if (window.campusBridge) return window.campusBridge.call(payload);   // inside Streamlit (app_3d.py)
    const response = await fetch("/api/command", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload), signal: AbortSignal.timeout(12000),
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || ui().network_error);
    return result;
  }

  async function send(operation, extra = {}) {
    if (window.campusBusy) return;
    if (location.protocol === "file:") { startError.textContent = ui().local_only; return; }
    setBusy(true);
    try {
      const result = await request({ operation, player: current?.player || name.value,
        language: window.lang || "pt", ...extra });
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
    const gotItem = current && state.inventory.length > current.inventory.length;
    current = state;
    window.campusState = state;
    window.lang = state.language;
    window.dispatchEvent(new Event("language"));
    window.dispatchEvent(new Event("campus-state"));
    const t = ui();
    $("scene-heading").textContent = state.ending ? state.ending.title : state.title;
    $("scene-label").textContent = state.ending ? t.the_end : t.scene;
    $("player-label").textContent = `${t.player} · ${state.player}`;
    $("clock").textContent = `🕘 ${state.clock}`;
    $("clock").setAttribute("aria-label", `${t.clock}: ${state.clock}`);
    $("feedback").textContent = state.message;
    $("feedback").className = state.accepted ? "success" : "error";
    $("feedback").hidden = !state.message;
    $("scene-paragraphs").replaceChildren(...(state.ending ? [state.ending.text] : state.texts).map(p => make("p", p)));
    $("action-groups").replaceChildren();
    let bar = [];   // the investigation buttons shown over the picture
    if (!state.ending) {
      if (state.people.length) {   // the people in this room; reuses the investigate rules (talking only reads the saved game)
        const group = make("section", undefined, "actions people");   // not "investigate": talking works from outside the room too
        group.append(make("h3", t.people));
        for (const person of state.people) {
          const box = make("div", undefined, "action-row");
          const button = make("button", person.object ? `🖥️ ${t.use} ${person.name}` : `💬 ${t.talk_to} ${person.name}`);
          button.dataset.talk = person.id;
          button.addEventListener("click", () => talkStep(person.id, "start"));
          box.append(button); group.append(box);
        }
        $("action-groups").append(group);
      }
      const actionRow = action => {
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
        return box;
      };
      const travel = state.actions.filter(a => a.kind === "travel");
      if (travel.length) {
        const group = make("section", undefined, "actions travel");
        group.append(make("h3", t.travel), ...travel.map(actionRow));
        $("action-groups").append(group);
      }
      bar = state.actions.filter(a => a.kind === "investigate" && !a.person).map(actionRow);
    }
    $("bar-actions").replaceChildren(...bar);
    $("action-bar").hidden = !bar.length;
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
    if (!state.accepted && state.message) { toast(state.message); sound.refuse(); }   // a refusal also shows as a note over the picture
    else if (gotItem) sound.chime();
    showEnding(state.ending);
    showChat(state.chat);
    checkNotices(state);
    sound.setTension(state.ending ? 0 : tensionOf(state));
    if (roomChanged) closeTalk();
    if (roomChanged) {
      $("scene-heading").focus({ preventScroll: true });
      document.querySelector(".scene-panel").scrollTop = 0;
    }
  }

  // ---------- computer 12: the group chat is read and flagged on a screen over the picture ----------
  function showChat(chat) {
    const card = $("chat-card"), t = ui();
    const wasOpen = !card.hidden;
    $("hud-bottom").classList.toggle("chatting", Boolean(chat));
    if (!chat) {
      card.hidden = true;
      if (wasOpen && !talking && !phone.open && !dialog.open) window.playing = true;
      return;
    }
    window.playing = false;   // the character stands at the computer
    $("chat-title").textContent = t.chat_title;
    $("chat-close").textContent = t.chat_close;
    $("chat-intro").textContent = chat.intro;
    $("chat-messages").replaceChildren(...chat.messages.map(message => {
      const row = make("li", undefined, message.flagged ? "flagged" : "");
      const button = make("button", message.flagged ? t.chat_flagged : t.chat_flag, message.flagged ? "secondary" : "");
      button.disabled = message.flagged;
      button.dataset.action = message.action;
      button.addEventListener("click", () => send("play", { action: message.action }));
      row.append(make("p", message.text), button);
      return row;
    }));
    card.hidden = false;
    if (!wasOpen) $("chat-messages").querySelector("button:not(:disabled)")?.focus({ preventScroll: true });
  }
  $("chat-close").addEventListener("click", () => send("play", { action: "go_computer_lab" }));
  document.addEventListener("keydown", e => { if (e.key === "Escape" && !$("chat-card").hidden && !dialog.open) $("chat-close").click(); });

  // ---------- the ending: a screen over the picture, with a stamp and confetti ----------
  const CONFETTI = { full_case: ["#e8b45c", "#f4e3b0", "#7fd6a0"], impostor: ["#7fd6a0", "#e8b45c", "#cfe8d8"],
                     fifth_element: ["#b79cff", "#ffffff", "#6a4cff"], stolen_credits: ["#ff8c7a", "#9aa4ad"] };
  function showEnding(ending) {
    const card = $("ending-card"), t = ui();
    if (!ending) { delete card.dataset.id; card.hidden = true; $("confetti").hidden = true; $("confetti").replaceChildren(); return; }
    if (card.dataset.id !== ending.id) {   // a new ending: build the screen once
      card.dataset.id = ending.id;
      card.className = `ending-card ending-${ending.id}`;
      $("ending-stamp").textContent = (t.stamps || {})[ending.id] || "";
      $("ending-label").textContent = t.the_end;
      $("ending-title").textContent = ending.title;
      $("ending-text").replaceChildren(make("p", ending.text));
      $("ending-again").textContent = t.play_again;
      $("ending-hide").textContent = t.see_scene;
      rememberEnding(ending.id);
      speakEnding(ending);
      $("ending-collection").textContent = collectionText();
      $("share-text").textContent = shareText(ending);
      $("share-copy").textContent = t.share_copy;
      const colors = CONFETTI[ending.id] || CONFETTI.full_case;
      $("confetti").replaceChildren(...Array.from({ length: 48 }, () => {
        const piece = make("span");
        piece.style.setProperty("--x", `${Math.random() * 100}%`);
        piece.style.setProperty("--delay", `${(Math.random() * 6).toFixed(2)}s`);
        piece.style.setProperty("--dur", `${(4 + Math.random() * 4).toFixed(2)}s`);
        piece.style.setProperty("--c", colors[Math.floor(Math.random() * colors.length)]);
        return piece;
      }));
    }
    card.hidden = false; $("confetti").hidden = false;
    $("ending-again").focus({ preventScroll: true });
  }
  $("ending-again").addEventListener("click", () => $("restart").click());
  $("ending-hide").addEventListener("click", () => { $("ending-card").hidden = true; $("confetti").hidden = true; });

  // ---------- hide the side panel ----------
  function paintPanelTab() {
    const hidden = document.body.classList.contains("panel-hidden");
    $("panel-toggle").textContent = hidden ? "‹" : "›";
    $("panel-toggle").setAttribute("aria-label", hidden ? ui().show_panel : ui().hide_panel);
    $("panel-toggle").setAttribute("aria-expanded", String(!hidden));
  }
  function setPanelHidden(hidden, remember = false) {
    document.body.classList.toggle("panel-hidden", hidden);
    paintPanelTab();
    if (remember) { try { localStorage.setItem("plot-twist-panel", hidden ? "closed" : "open"); } catch (error) { /* no storage */ } }
    window.dispatchEvent(new Event("resize"));   // the 3D picture takes the new width
  }
  $("sound-toggle").addEventListener("click", () => { sound.toggle(); updateLabels(); });
  $("panel-toggle").addEventListener("click", () => setPanelHidden(!document.body.classList.contains("panel-hidden"), true));
  try { if (localStorage.getItem("plot-twist-panel") === "closed") setPanelHidden(true); } catch (error) { /* no storage */ }

  // ---------- a note over the 3D picture: it stays visible even when the panel is hidden ----------
  let toastTimer;
  function toast(text) {
    $("toast").textContent = text;
    $("toast").hidden = false;
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => { $("toast").hidden = true; }, 8000);
  }


  // ---------- conversations ----------
  function closeTalk() {
    const was = talking;
    talking = null;
    stopSpeaking();
    $("talk").hidden = true;
    updateNear();
    if (was && !phone.open && !dialog.open) window.playing = true;
  }
  function showLine(line) {
    const t = ui();
    talking = line.npc;
    window.playing = false;   // the character stands still while talking
    $("talk-name").textContent = line.name;
    $("talk-text").textContent = line.text;
    const hearts = line.trust === null || line.trust === undefined ? "" : "♥".repeat(line.trust) + "♡".repeat(3 - line.trust);
    $("talk-trust").textContent = hearts;
    $("talk-trust").setAttribute("aria-label", hearts ? `${t.trust}: ${line.trust}/3` : "");
    $("talk-trust").className = `trust trust-${line.trust === null || line.trust === undefined ? "none" : line.trust}`;
    const answers = line.options.map(option => {
      const button = make("button", option.label, "answer");
      button.addEventListener("click", () => option.next === null ? closeTalk() : talkStep(line.npc, option.next));
      return button;
    });
    // What can be done by talking to this person (ask for the copy, take the decision...): choices inside the conversation.
    const doing = make("div", undefined, "actions investigate talk-actions");
    for (const action of line.actions || []) {
      const row = make("div", undefined, "talk-action");
      const button = make("button", `▶ ${action.label}`, action.allowed ? "" : "locked");
      button.dataset.action = action.id;
      button.addEventListener("click", () => talkAction(line, action));
      row.append(button);
      if (action.decision) row.append(make("p", t.decision, "action-hint"));
      doing.append(row);
    }
    if (doing.children.length && window.campusInside === false) doing.append(make("p", t.outside_hint, "muted"));
    $("talk-options").replaceChildren(...(doing.children.length ? [doing] : []), ...answers);
    applyInside();
    if (line.note) saveDiary(line.name, line.note);
    $("talk").hidden = false;
    updateNear();
    sound.talk();
    speak(line.text, line.npc);
    $("talk-options").querySelector("button")?.focus({ preventScroll: true });
  }
  // The player chose to do something by talking: the story's own action runs, and the person answers with its result.
  async function talkAction(line, action) {
    if (window.campusBusy || !current) return;
    const scene = current.scene;
    if (!await send("play", { action: action.id })) return;
    if (!talking || current.scene !== scene) return;   // the scene changed (for example the chat opened): the conversation is over
    showLine({ npc: line.npc, name: line.name, text: current.message, trust: null, note: "", actions: [],
               options: [{ label: ui().talk_continue, next: "start" }, { label: ui().talk_bye, next: null }] });
  }
  async function talkStep(npc, node) {
    if (window.campusBusy || !current) return;
    setBusy(true);
    try {
      showLine(await request({ operation: "talk", player: current.player, language: window.lang || "pt", npc, node }));
    } catch (error) {
      closeTalk();
      toast(error.name === "Error" ? error.message : ui().network_error);
    } finally { setBusy(false); }
  }
  // ---------- walking up to a person: a note says which key starts the conversation ----------
  // The 3D scene sets window.campusNear (the id of the person close enough, or null).
  function updateNear() {
    $("hud-bottom").classList.toggle("talking", Boolean(talking));
    const person = window.campusNear && current?.people.find(p => p.id === window.campusNear);
    $("near-hint").hidden = !person || Boolean(talking);
    if (!person) return;
    const key = make("kbd", "K");
    const sentence = person.object ? ui().press_use.replace("{name}", person.name.toLowerCase()) : ui().press_talk.replace("{name}", person.name);
    $("near-hint").replaceChildren(key, document.createTextNode(" " + sentence));
  }
  window.addEventListener("campus-near", updateNear);
  $("near-hint").addEventListener("click", () => { if (window.campusNear) talkStep(window.campusNear, "start"); });
  document.addEventListener("keydown", e => {
    if (e.key.toLowerCase() !== "k" || e.repeat || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest("input, textarea, dialog") || !window.campusNear || talking || !window.playing || window.campusBusy) return;
    e.preventDefault();
    talkStep(window.campusNear, "start");
  });
  $("talk-close").addEventListener("click", closeTalk);
  document.addEventListener("keydown", e => { if (e.key === "Escape" && talking && !phone.open && !dialog.open) closeTalk(); });

  // ---------- the share card, the collection of endings and the tension of the night ----------
  function loadEndings() {
    try { const found = JSON.parse(localStorage.getItem("plot-twist-endings") || "[]"); return Array.isArray(found) ? found : []; } catch (error) { return []; }
  }
  function rememberEnding(id) {
    const found = loadEndings();
    if (found.includes(id)) return;
    found.push(id);
    try { localStorage.setItem("plot-twist-endings", JSON.stringify(found)); } catch (error) { /* no storage */ }
  }
  function collectionCount() {
    const all = data[window.lang || "pt"].endings, found = loadEndings();
    return `${ui().collection}: ${all.filter(e => found.includes(e.id)).length}/${all.length}`;
  }
  function collectionText() {
    const all = data[window.lang || "pt"].endings, found = loadEndings();
    return `${collectionCount()}   ${all.map(e => found.includes(e.id) ? ENDING_EMOJI[e.id] || "✔" : "🔒").join(" ")}`;
  }
  function shareText(ending) {
    const t = ui(), clues = current?.clues || [], done = clues.filter(c => c.done).length;
    const squares = clues.map(c => (c.done ? "🟩" : "⬛")).join("") + (current?.flagged ? "🟨" : "⬛");
    return [`${t.share_title} 🕵️`, `${ENDING_EMOJI[ending.id] || "🕵️"} ${ending.title}`,
            `${squares} · ${done}/${clues.length} ${t.share_clues}`, `🕘 ${current?.clock || ""} · ${collectionCount()}`].join("\n");
  }
  $("share-copy").addEventListener("click", async () => {
    const t = ui(), box = $("share-text");
    try {
      await navigator.clipboard.writeText(box.textContent);
      $("share-copy").textContent = t.share_copied;
    } catch (error) {   // the page may not be allowed to use the clipboard: select the text so Ctrl+C works
      const range = document.createRange(); range.selectNodeContents(box);
      const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
      $("share-copy").textContent = t.share_select;
    }
    setTimeout(() => { $("share-copy").textContent = ui().share_copy; }, 3000);
  });
  // How far the night has gone, from 0 (22:15) to 1 (after one in the morning): it drives the music.
  function tensionOf(state) {
    const [h, m] = String(state.clock || "22:15").split(":").map(Number);
    return Math.min(1, ((h * 60 + m - (22 * 60 + 15) + 1440) % 1440) / 185);
  }

  // ---------- messages from an unknown number: they arrive as the case moves forward ----------
  const msgKey = player => `plot-twist-msgs:${player}`;
  function loadMsgs(player) {
    try {
      const saved = JSON.parse(localStorage.getItem(msgKey(player)) || "{}");
      return { sent: saved.sent || [], list: saved.list || [], read: saved.read || 0 };
    } catch (error) { return { sent: [], list: [], read: 0 }; }
  }
  function saveMsgs(player, store) {
    try { localStorage.setItem(msgKey(player), JSON.stringify(store)); } catch (error) { /* no storage */ }
  }
  const unreadMsgs = () => { const store = loadMsgs(current?.player || ""); return Math.max(0, store.list.length - store.read); };
  let smsTimer;
  function showSms(text) {
    const banner = $("sms");
    $("sms-from").textContent = `📱 ${ui().notice_from}`;
    $("sms-text").textContent = text;
    banner.hidden = false;
    banner.classList.remove("buzz"); void banner.offsetWidth; banner.classList.add("buzz");   // restart the shaking
    clearTimeout(smsTimer);
    smsTimer = setTimeout(() => { banner.hidden = true; }, 9000);
  }
  $("sms").addEventListener("click", () => { $("sms").hidden = true; openPhone("msgs"); });
  // One message for each clue found (the first three build up, the fourth says what the player found),
  // and one when the first chat message is flagged. Only the newest pops up; all of them stay in the phone.
  function checkNotices(state) {
    if (state.ending) { $("sms").hidden = true; return; }
    const t = ui(), done = (state.clues || []).filter(c => c.done).length, store = loadMsgs(state.player);
    const due = [];
    for (let i = 1; i <= Math.min(done, t.notices.length); i++) if (!store.sent.includes(`c${i}`)) due.push([`c${i}`, t.notices[i - 1]]);
    if (state.flagged > 0 && !store.sent.includes("chat")) due.push(["chat", t.notice_chat]);
    if (!due.length) return;
    for (const [id, text] of due) { store.sent.push(id); store.list.push({ text, clock: state.clock }); }
    saveMsgs(state.player, store);
    showSms(due[due.length - 1][1]);
    sound.buzz();
  }
  function drawMsgs(screen, t) {
    const store = loadMsgs(current?.player || "");
    if (!store.list.length) screen.append(make("p", t.msgs_empty, "muted"));
    for (const message of store.list.slice().reverse()) {
      const row = make("article", undefined, "sms-row");
      row.append(make("h4", `${t.notice_from} · ${message.clock}`), make("p", message.text));
      screen.append(row);
    }
    store.read = store.list.length;
    saveMsgs(current?.player || "", store);
  }

  // ---------- the buttons for the torch, the voices and "How it was made" ----------
  $("torch-toggle").addEventListener("click", () => toggleTorch());
  $("voice-toggle").addEventListener("click", () => {
    voiceOn = !voiceOn;
    try { localStorage.setItem("plot-twist-voice", voiceOn ? "on" : "off"); } catch (error) { /* no storage */ }
    if (!voiceOn) stopSpeaking();
    updateLabels();
  });
  function toggleTorch() {
    torchOn = !torchOn;
    window.campusTorchOn = torchOn;
    try { localStorage.setItem("plot-twist-torch", torchOn ? "on" : "off"); } catch (error) { /* no storage */ }
    updateLabels();
  }
  document.addEventListener("keydown", e => {
    if (e.key.toLowerCase() !== "f" || e.repeat || e.ctrlKey || e.metaKey || e.altKey) return;
    if (e.target.closest("input, textarea, dialog") || !current) return;
    toggleTorch();
  });

  const howto = make("dialog", undefined, "howto-dialog"); howto.id = "howto";
  howto.setAttribute("aria-labelledby", "howto-title");
  howto.innerHTML = '<h2 id="howto-title"></h2><p id="howto-intro" class="muted"></p><ul id="howto-list"></ul><p id="howto-run" class="muted"></p><div class="dialog-actions"><button id="howto-close"></button></div>';
  document.body.append(howto);
  function openHowto() {
    if (howto.open) return;
    const t = ui();
    $("howto-title").textContent = t.howto_title;
    $("howto-intro").textContent = t.howto_intro;
    $("howto-run").textContent = t.howto_run;
    $("howto-close").textContent = t.howto_close;
    $("howto-list").replaceChildren(...t.howto_items.map(([title, file, detail]) => {
      const item = make("li");
      item.append(make("strong", title), document.createTextNode(" "), make("code", file), make("p", detail));
      return item;
    }));
    window.playing = false;
    howto.showModal();
    $("howto-close").focus();
  }
  $("howto-open").addEventListener("click", openHowto);
  $("howto-close").addEventListener("click", () => howto.close());
  howto.addEventListener("close", () => { window.playing = !talking && $("chat-card").hidden && !phone.open; });

  // ---------- the phone: a map, the to-do list of clues and the diary ----------
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
      screen.append(make("p", t.map_no_3d, "muted"), make("p", `${t.map_where}: ${titles[current.room].title}`, "map-where"));
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

  // The diary: the evidence the server knows, and what people told the player (kept in this browser only).
  const diaryKey = () => `plot-twist-diary:${current?.player || ""}`;
  function loadDiary() {
    try { const list = JSON.parse(localStorage.getItem(diaryKey()) || "[]"); return Array.isArray(list) ? list : []; } catch (error) { return []; }
  }
  function saveDiary(name, text) {
    const list = loadDiary();
    if (list.some(entry => entry.text === text)) return;
    list.push({ name, text });
    try { localStorage.setItem(diaryKey(), JSON.stringify(list.slice(-40))); } catch (error) { /* no storage: the diary just forgets */ }
  }
  function drawDiary(screen, t) {
    const sections = [[t.diary_evidence, (current?.notebook || []).map(n => [n.title, n.text])],
                      [t.diary_people, loadDiary().map(n => [n.name, n.text])]];
    for (const [heading, entries] of sections) {
      screen.append(make("h3", heading, "diary-heading"));
      if (!entries.length) screen.append(make("p", t.diary_empty, "muted"));
      for (const [title, text] of entries) {
        const note = make("article", undefined, "diary-note");
        note.append(make("h4", title), make("p", text));
        screen.append(note);
      }
    }
  }

  function showPhone(view) {
    const t = ui(), screen = $("phone-screen");
    $("phone-back").hidden = view === "home";
    $("phone-back").textContent = `‹ ${t.phone_home}`;
    $("phone-close").setAttribute("aria-label", t.phone_close);
    $("phone-title").textContent = view === "map" ? t.map_title : view === "todo" ? t.todo_title : view === "diary" ? t.diary_title : view === "msgs" ? t.msgs_title : t.phone;
    screen.replaceChildren();
    if (view === "home") {
      const { done, total } = clueCount();
      const grid = make("div", undefined, "app-grid");
      for (const [id, icon, label, badge] of [["map", "📍", t.app_map, ""], ["todo", "✅", t.app_todo, `${done}/${total}`],
                                              ["diary", "📔", t.app_diary, String((current?.notebook || []).length + loadDiary().length)],
                                              ["msgs", "💬", t.app_msgs, unreadMsgs() ? String(unreadMsgs()) : ""]]) {
        const app = make("button", undefined, "app-icon");
        app.dataset.app = id;
        app.append(make("span", icon, "app-glyph"), make("span", label, "app-name"));
        if (badge) app.append(make("span", badge, "app-badge"));
        app.addEventListener("click", () => showPhone(id));
        grid.append(app);
      }
      screen.append(grid);
    } else if (view === "map") drawMap(screen, t);
    else if (view === "diary") drawDiary(screen, t);
    else if (view === "msgs") drawMsgs(screen, t);
    else drawTodo(screen, t);
    (view === "home" ? screen.querySelector("button") : $("phone-back")).focus();
  }
  function openPhone(view = "home") {
    if (!current || window.campusBusy || phone.open) return;
    window.playing = false;   // the character stands still while the phone is out
    showPhone(view);
    phone.showModal();
  }
  function closePhone() {
    phone.close();
    window.playing = !talking;
    $("phone-open").focus();
  }
  $("phone-open").addEventListener("click", () => openPhone());
  $("phone-close").addEventListener("click", closePhone);
  $("phone-back").addEventListener("click", () => showPhone("home"));
  phone.addEventListener("cancel", e => { e.preventDefault(); closePhone(); });

  window.campusStart = async () => {
    sound.start();
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
      stopSpeaking();
      window.dispatchEvent(new Event("campus-restarted"));
      try { localStorage.removeItem(msgKey(current.player)); localStorage.removeItem(diaryKey()); } catch (error) { /* no storage */ }
    }
  });
})();
