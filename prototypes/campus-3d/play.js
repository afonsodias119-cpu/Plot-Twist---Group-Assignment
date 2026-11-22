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
  // No count of endings here: the player should not know how many endings there are before playing
  // (specs/no-endings-on-start.md). The ending screen still shows the endings found.
  nameBox.append(nameLabel, name, nameHint, startError);
  // The last name used in this browser is filled in again: if the page reloads (for example after an
  // update of the app), continuing the game is one click (specs/chat-dialogues.md).
  const LAST_NAME_KEY = "plot-twist-last-name";
  try { name.value = localStorage.getItem(LAST_NAME_KEY) || ""; } catch (error) { /* no storage */ }
  // ---------- the character creator: boy or girl, clothes, colours (kept in this browser, for each name) ----------
  // It only changes how the detective looks; the server never sees it (specs/rules-and-character.md).
  const OUTFITS = ["tee", "jacket", "hoodie", "suit", "trench", "dress"];
  const OUTFIT_COLORS = ["#b3895a", "#c2566b", "#3b6a8c", "#2f7a5a", "#7a5cc2", "#d9a441", "#2a2b33", "#8a1f24"];
  const HAIR_COLORS = ["#1c1410", "#5a2a12", "#d9b36a", "#9a3a1c", "#b8b8b8"];
  const SKIN_COLORS = ["#f0c8a8", "#e2b08a", "#c68863", "#8d5a3b"];
  const DEFAULT_LOOK = { body: "m", outfit: "trench", color: 0, hair: 1, skin: 1, hat: true };
  const LAST_LOOK_KEY = "plot-twist-look";
  const lookKey = who => `plot-twist-look:${String(who).trim().toLowerCase()}`;
  const hexToInt = hex => parseInt(hex.slice(1), 16);
  // Whatever is read from the browser is checked: a damaged note can only give the default look.
  function cleanLook(raw) {
    const clean = { ...DEFAULT_LOOK };
    if (!raw || typeof raw !== "object") return clean;
    if (raw.body === "m" || raw.body === "f") clean.body = raw.body;
    if (OUTFITS.includes(raw.outfit)) clean.outfit = raw.outfit;
    if (Number.isInteger(raw.color) && raw.color >= 0 && raw.color < OUTFIT_COLORS.length) clean.color = raw.color;
    if (Number.isInteger(raw.hair) && raw.hair >= 0 && raw.hair < HAIR_COLORS.length) clean.hair = raw.hair;
    if (Number.isInteger(raw.skin) && raw.skin >= 0 && raw.skin < SKIN_COLORS.length) clean.skin = raw.skin;
    if (typeof raw.hat === "boolean") clean.hat = raw.hat;
    if (clean.outfit === "dress" && clean.body !== "f") clean.outfit = "trench";   // the dress is for the girl
    return clean;
  }
  function readLook(key) {
    try { return cleanLook(JSON.parse(localStorage.getItem(key) || "null")); } catch (error) { return { ...DEFAULT_LOOK }; }
  }
  let look = readLook(LAST_LOOK_KEY);
  const resolvedLook = value => ({ body: value.body, outfit: value.outfit, topColor: hexToInt(OUTFIT_COLORS[value.color]),
    hairColor: hexToInt(HAIR_COLORS[value.hair]), skin: hexToInt(SKIN_COLORS[value.skin]), hat: value.hat });
  function saveLook(who) {
    try {
      localStorage.setItem(LAST_LOOK_KEY, JSON.stringify(look));
      if (who) localStorage.setItem(lookKey(who), JSON.stringify(look));
    } catch (error) { /* no storage */ }
  }

  const creator = make("section", undefined, "creator"); creator.setAttribute("aria-labelledby", "creator-title");
  const creatorTitle = make("h3"); creatorTitle.id = "creator-title";
  const previewCanvas = make("canvas", undefined, "creator-preview"); previewCanvas.width = 240; previewCanvas.height = 320;
  previewCanvas.setAttribute("aria-hidden", "true");
  const creatorBody = make("div", undefined, "creator-controls");
  const creatorParts = [];   // every button: how to say it and when it is pressed, so one function can redraw them all
  function creatorRow(labelOf) {
    const row = make("div", undefined, "creator-row"), label = make("span", undefined, "creator-label"), options = make("div", undefined, "creator-options");
    row.append(label, options);
    creatorParts.push({ label, labelOf });
    creatorBody.append(row);
    return options;
  }
  function creatorButton(options, textOf, pressedOf, patchOf, extra) {
    const button = make("button", undefined, extra || "choice");
    button.type = "button";
    button.addEventListener("click", () => changeLook(patchOf()));
    options.append(button);
    creatorParts.push({ button, textOf, pressedOf });
    return button;
  }
  const bodyOptions = creatorRow(t => t.creator_body);
  for (const body of ["m", "f"]) creatorButton(bodyOptions, t => t[`body_${body}`], () => look.body === body, () => ({ body }));
  const outfitOptions = creatorRow(t => t.creator_outfit);
  const outfitButtons = {};
  for (const outfit of OUTFITS) outfitButtons[outfit] = creatorButton(outfitOptions, t => t.outfits[outfit], () => look.outfit === outfit, () => ({ outfit }));
  const colorOptions = creatorRow(t => t.creator_color);
  OUTFIT_COLORS.forEach((hex, index) => {
    const swatch = creatorButton(colorOptions, t => t.color_names[index], () => look.color === index, () => ({ color: index }), "swatch");
    swatch.style.background = hex;
  });
  const hairOptions = creatorRow(t => t.creator_hair);
  HAIR_COLORS.forEach((hex, index) => {
    const swatch = creatorButton(hairOptions, t => t.hair_names[index], () => look.hair === index, () => ({ hair: index }), "swatch");
    swatch.style.background = hex;
  });
  const skinOptions = creatorRow(t => t.creator_skin);
  SKIN_COLORS.forEach((hex, index) => {
    const swatch = creatorButton(skinOptions, t => t.skin_names[index], () => look.skin === index, () => ({ skin: index }), "swatch");
    swatch.style.background = hex;
  });
  const hatOptions = creatorRow(t => t.creator_hat);
  creatorButton(hatOptions, t => t.hat_on, () => look.hat, () => ({ hat: true }));
  creatorButton(hatOptions, t => t.hat_off, () => !look.hat, () => ({ hat: false }));
  const randomButton = make("button", undefined, "choice random"); randomButton.type = "button";
  randomButton.addEventListener("click", () => {
    const pick = list => list[Math.floor(Math.random() * list.length)];
    const body = pick(["m", "f"]);
    changeLook({ body, outfit: pick(OUTFITS.filter(o => o !== "dress" || body === "f")), color: Math.floor(Math.random() * OUTFIT_COLORS.length),
      hair: Math.floor(Math.random() * HAIR_COLORS.length), skin: Math.floor(Math.random() * SKIN_COLORS.length), hat: Math.random() < 0.5 });
  });
  creatorBody.append(randomButton);
  creator.append(creatorTitle, previewCanvas, creatorBody);

  function paintCreator() {
    const t = ui();
    creatorTitle.textContent = t.creator_title;
    randomButton.textContent = `🎲 ${t.creator_random}`;
    for (const part of creatorParts) {
      if (part.label) { part.label.textContent = part.labelOf(t); continue; }
      const text = part.textOf(t);
      part.button.setAttribute("aria-pressed", String(part.pressedOf()));
      part.button.setAttribute("aria-label", text);
      part.button.title = text;
      if (!part.button.classList.contains("swatch")) part.button.textContent = text;
    }
    outfitButtons.dress.hidden = look.body !== "f";
  }
  let previewShown = false;
  function showPreview() {
    if (!window.campusPreview || document.body.classList.contains("text-mode")) return;
    if (previewShown) window.campusPreview.setLook(resolvedLook(look));
    else { window.campusPreview.show(previewCanvas, resolvedLook(look)); previewShown = true; }
  }
  function changeLook(patchValues) {
    look = cleanLook({ ...look, ...patchValues });
    saveLook(null);
    paintCreator();
    showPreview();
    window.dispatchEvent(new Event("campus-look"));   // the fifth figure of the photo wears the same colour
  }
  // Writing a name that already has a look in this browser shows that look again.
  let lookTimer;
  name.addEventListener("input", () => {
    clearTimeout(lookTimer);
    lookTimer = setTimeout(() => {
      let stored = null;
      try { stored = localStorage.getItem(lookKey(name.value)); } catch (error) { /* no storage */ }
      if (stored) { look = readLook(lookKey(name.value)); paintCreator(); showPreview(); window.dispatchEvent(new Event("campus-look")); }
    }, 250);
  });
  window.addEventListener("campus-renderer-ready", showPreview);
  nameBox.append(creator);
  paintCreator();

  $("mission").after(nameBox);
  // Which night of this name it is, under the name box (specs/earlier-nights.md, point 6). Empty on night 1,
  // so a first player sees only the name field and its hint. It never counts endings. drawNight fills it.
  const nightLine = make("p", "", "night-line");
  nameBox.after(nightLine);

  const shell = make("main"); shell.id = "investigation"; shell.hidden = true;
  shell.innerHTML = `
    <header class="case-bar"><div><p id="case-eyebrow" class="label"></p><h1 id="game-title"></h1></div>
      <div class="bar-tools"><span id="clock" class="clock"></span><span id="save-status" role="status"></span>
        <div class="tool-row"><button id="phone-open" class="secondary"></button>
          <div class="tool-menu"><button id="menu-toggle" class="secondary" aria-expanded="false" aria-controls="menu-list"></button>
            <div id="menu-list" class="menu-list" hidden><button id="howto-open" class="secondary"></button><button id="torch-toggle" class="secondary"></button><button id="sound-toggle" class="secondary"></button></div></div></div></div></header>
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
    <section id="timeup-card" class="ending-card timeup-card" role="alertdialog" aria-labelledby="timeup-title" hidden>
      <p class="stamp">⏳ 22:45</p><h2 id="timeup-title"></h2><div id="timeup-text"></div>
      <div class="ending-actions"><button id="timeup-again"></button></div></section>
    <button id="panel-toggle" class="panel-tab" aria-expanded="true"></button>
    <div id="hud-bottom" class="hud-bottom">
      <button id="near-hint" class="near-hint" hidden></button>
      <div id="action-bar" class="action-bar" hidden><p id="outside-hint" class="muted" hidden></p><div id="bar-actions" class="actions investigate"></div></div>
    </div>
    <section id="talk" class="talk-card" role="dialog" aria-labelledby="talk-name" hidden>
      <header class="talk-head"><span id="talk-avatar" class="avatar" aria-hidden="true"></span>
        <div class="talk-who"><h3 id="talk-name"></h3></div>
        <button id="talk-close" class="secondary"></button></header>
      <div id="talk-log" class="chat-log" aria-live="polite"></div><div id="talk-evidence" class="talk-evidence" hidden></div><div id="talk-options" class="chat-replies"></div></section>
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
  let torchOn = true;
  try { torchOn = localStorage.getItem("plot-twist-torch") !== "off"; } catch (error) { /* no storage */ }
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
  // A line is split into what the person SAYS (between quotation marks) and what HAPPENS (the rest).
  // The voices read only what is said; the conversation shows what is said in speech bubbles and the
  // rest as a short narration line outside the bubbles (specs/chat-dialogues.md).
  function partsOf(text) {
    const parts = [];
    let last = 0, narration = "";
    for (const match of text.matchAll(/"([^"]+)"|«([^»]+)»|“([^”]+)”/g)) {
      const said = (match[1] || match[2] || match[3]).trim();
      narration += text.slice(last, match.index);
      last = match.index + match[0].length;
      // A short quote without a full stop is a name or a title (someone added "Duarte" to the
      // report), not a line someone says: it stays in the narration, with its quotation marks.
      if (said.split(/\s+/).length <= 3 && !/[.!?…]/.test(said)) { narration += match[0]; continue; }
      if (narration.trim()) parts.push({ kind: "narration", text: narration.trim() });
      narration = "";
      parts.push({ kind: "speech", text: said });
    }
    narration += text.slice(last);
    if (narration.trim()) parts.push({ kind: "narration", text: narration.trim() });
    return parts;
  }
  const quotesOf = text => partsOf(text).filter(part => part.kind === "speech").map(part => part.text);
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
    if (!canSpeak || sound.isMuted() || !VOICES[who]) return;
    stopSpeaking();
    say(quotesOf(text).map(line => [line, who]));
  }
  function speakEnding(ending, reply) {
    if (!canSpeak || sound.isMuted()) return;
    stopSpeaking();
    // An ending that is not one of the story's four brings its own voices (specs/earlier-nights.md, point 9).
    const speakers = ending.voices || (ui().ending_voices || {})[ending.id] || [];
    // After a hearing: first its last reply in its speaker's voice, then the professor's verdict.
    // The ending's own quotes keep their voices (specs/evidence-and-hearing.md, point 11).
    const before = [];
    if (reply && VOICES[reply.who]) before.push(...quotesOf(reply.text).map(line => [line, reply.who]));
    if (ending.verdict) before.push(...quotesOf(ending.verdict).map(line => [line, "professor"]));
    say([...before, ...quotesOf(ending.text).map((line, i) => [line, VOICES[speakers[i]] ? speakers[i] : "narrator"])]);
  }
  if (canSpeak) speechSynthesis.getVoices();   // some browsers only load the list after the first call
  document.addEventListener("pointerdown", () => sound.start());
  document.addEventListener("click", e => { if (e.target.closest("button:not(:disabled)")) sound.click(); });


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
    // The top bar has words, not emojis: the phone, and a menu with the other tools.
    $("phone-open").textContent = t.phone;
    $("phone-open").setAttribute("aria-label", t.phone_open);
    $("menu-toggle").textContent = t.menu;
    paintPanelTab();
    $("talk-close").textContent = t.talk_close;
    paintCreator();
    // Each menu item is one word; the dot beside Torch and Sound says if it is on (aria-pressed, drawn by the stylesheet).
    $("howto-open").textContent = t.howto_open;
    $("torch-toggle").textContent = t.torch_on;
    $("torch-toggle").setAttribute("aria-pressed", String(torchOn));
    $("sound-toggle").textContent = t.sound_on;
    $("sound-toggle").setAttribute("aria-pressed", String(!sound.isMuted()));
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
    // Before a command the server hears the page's own minute (specs/night-schedule.md, point 4). The
    // command is for the person of the open card: it is not sent if the report shows that person gone.
    if (!["open", "restart", "time"].includes(operation) && !await catchUp(talking)) return false;
    setBusy(true);
    try {
      const result = await request({ operation, player: current?.player || name.value,
        language: window.lang || "pt", ...extra });
      uncertain = false;
      render(result, operation);
      if (operation !== "confront") endGoneTalk();   // confrontWith draws the rebuff first, then this
      return true;
    } catch (error) {
      uncertain = true;
      const message = error.name === "Error" ? error.message : ui().network_error;
      (current ? $("feedback") : startError).textContent = message;
      if (current) { $("feedback").className = "error"; $("feedback").hidden = false; toast(message); }
      return false;
    } finally { setBusy(false); }
  }

  function render(state, operation) {   // operation: the command this snapshot answers
    const roomChanged = !current || current.scene !== state.scene || Boolean(current.ending) !== Boolean(state.ending);
    const gotItem = current && state.inventory.length > current.inventory.length;
    current = state;
    window.campusState = state;
    window.lang = state.language;
    window.dispatchEvent(new Event("language"));
    window.dispatchEvent(new Event("campus-state"));
    rememberNight(state.memory);   // before showEnding: the ★ of the collection reads it
    const t = ui();
    $("scene-heading").textContent = state.ending ? state.ending.title : state.title;
    $("scene-label").textContent = state.ending ? t.the_end : t.scene;
    $("player-label").textContent = `${t.player} · ${state.player}`;
    startCountdown(state);   // the countdown replaces the clock of the server (specs/harder-campus.md)
    applyNight(state, operation);   // ...and now follows the server's campus minute (specs/night-schedule.md, point 4)
    tick();
    $("feedback").textContent = state.message;
    $("feedback").className = state.accepted ? "success" : "error";
    $("feedback").hidden = !state.message;
    $("scene-paragraphs").replaceChildren(...(state.ending ? [state.ending.text] : state.texts).map(p => make("p", p)));
    if (state.ending && state.ending.verdict) $("scene-paragraphs").prepend(make("p", state.ending.verdict, "verdict"));   // the text mode's panel too
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
      // Searching the study room for the USB stick (specs/hidden-object-table.md): the button opens the
      // close-up of the messy table (in 3D, clicking the table does the same).
      if (state.scene === "study_room" && !state.inventory.some(item => item.id === "usb_stick")) {
        // No title or hint: saying where the stick is would give the solution away.
        const group = make("section", undefined, "actions search investigate");
        const box = make("div", undefined, "action-row");
        const button = make("button", t.table_open);
        button.id = "table-open";
        button.addEventListener("click", () => window.campusOpenTable());
        box.append(button); group.append(box);
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
    if (!state.accepted && state.message) {   // a refusal also shows as a note over the picture
      // A catch is refused and charged: Duarte's line and "−3 min" (design-notes/texts-2-schedule.md, C).
      toast(state.night?.charged > 0 ? `${state.message} (${chargedNote(state)})` : state.message);
      sound.refuse();
    }
    else if (gotItem) sound.chime();
    // Close the old conversation before the ending card starts speaking: closing stops every voice.
    if (roomChanged) closeTalk();
    // The person of the open card has left (by the schedule, or Leonor after being accused): that
    // conversation ends in place, with the reply's message or the room's notice (specs/night-schedule.md, point 5).
    // A catch changes the scene, so closeTalk above has already closed the card (point 8).
    // Once per conversation: the later snapshots, while that ended card stays open, add nothing.
    goneLine = talking && !state.ending && talking !== endedTalk && !state.people.some(person => person.id === talking)
      ? state.message || (state.night ? state.night.notice : "") || null : null;   // an empty text is nothing to draw
    showNotice(state);
    showEnding(state.ending);
    showChat(state.chat);
    checkNotices(state);
    sound.setTension(state.ending ? 0 : tensionOf(state));
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
                     fifth_element: ["#b79cff", "#ffffff", "#6a4cff"], stolen_credits: ["#ff8c7a", "#9aa4ad"],
                     extra: ["#ffb38a", "#ffe2a8", "#f2d089"] };
  function showEnding(ending) {
    const card = $("ending-card"), t = ui();
    if (!ending) { delete card.dataset.id; card.hidden = true; $("confetti").hidden = true; $("confetti").replaceChildren(); return; }
    if (card.dataset.id !== ending.id) {   // a new ending: build the screen once
      card.dataset.id = ending.id;
      // An ending that carries its own stamp is not one of the story's four: the page does not name it,
      // it gets the neutral class `ending-extra` and uses the stamp, emoji and voices it brings
      // (specs/earlier-nights.md, point 9).
      const kind = ending.stamp ? "extra" : ending.id;
      card.className = `ending-card ending-${kind}`;
      $("ending-stamp").textContent = ending.stamp || (t.stamps || {})[ending.id] || "";
      $("ending-label").textContent = t.the_end;
      $("ending-title").textContent = ending.title;
      $("ending-text").replaceChildren(make("p", ending.text));
      // After a hearing, above the text: the reply to the third answer, with its speaker's name,
      // then the professor's verdict when there is one (specs/evidence-and-hearing.md, point 11).
      const reply = lastReply();
      if (ending.verdict) $("ending-text").prepend(make("p", ending.verdict, "verdict"));
      if (reply) {
        const said = make("p", undefined, "hearing-reply");
        said.append(make("strong", `${reply.name}: `), document.createTextNode(reply.text));
        $("ending-text").prepend(said);
      }
      $("ending-again").textContent = t.play_again;
      $("ending-hide").textContent = t.see_scene;
      rememberEnding(ending.id);
      speakEnding(ending, reply);
      $("ending-collection").textContent = collectionText();
      $("share-text").textContent = shareText(ending);
      $("share-copy").textContent = t.share_copy;
      const colors = CONFETTI[kind] || CONFETTI.full_case;
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
  $("sound-toggle").addEventListener("click", () => { sound.toggle(); if (sound.isMuted()) stopSpeaking(); updateLabels(); });   // the voices follow the sound
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


  // ---------- conversations (specs/chat-dialogues.md) ----------
  // The conversation is drawn like a messaging app: a log of bubbles (the person on the left,
  // the player's choices on the right) and the possible answers as reply buttons underneath.
  // The log lives only on the screen: closing the conversation empties it.
  function addBubble(text, who) {   // who: "them" (the person) or "me" (the player)
    $("talk-log").querySelector(".typing")?.remove();
    const bubble = make("div", undefined, `bubble ${who}`);
    bubble.append(make("p", text), make("time", campusTime()));
    $("talk-log").append(bubble);
    $("talk-log").scrollTop = $("talk-log").scrollHeight;   // always show the newest message
  }
  function addSaid(text) {   // a line of the person: speech bubbles for what is said, narration for the rest
    $("talk-log").querySelector(".typing")?.remove();
    for (const part of partsOf(text)) {
      if (part.kind === "speech") { addBubble(part.text, "them"); continue; }
      const narration = make("div", undefined, "narration");
      narration.append(make("p", part.text));
      $("talk-log").append(narration);
    }
    $("talk-log").scrollTop = $("talk-log").scrollHeight;
  }
  function showTyping() {   // three dots while the answer is on its way
    const bubble = make("div", undefined, "bubble them typing");
    bubble.setAttribute("aria-label", "…");
    bubble.append(make("span"), make("span"), make("span"));
    $("talk-log").append(bubble);
    $("talk-log").scrollTop = $("talk-log").scrollHeight;
  }
  const topics = new Map();   // unasked subjects learned from this conversation
  const asked = new Set();   // the questions (node ids) already chosen in the open conversation
  // The last line the server gave by "talk": "Show evidence" sends its node (specs/evidence-and-hearing.md, point 5).
  let screenLine = null;
  function closeTalk() {
    const was = talking;
    talking = null;
    endedTalk = null;
    screenLine = null;
    asked.clear();
    topics.clear();
    stopSpeaking();
    $("talk").hidden = true;
    $("talk-log").replaceChildren();   // the next conversation starts empty
    updateNear();
    if (was && !phone.open && !dialog.open) window.playing = true;
  }
  // The last line of a conversation whose person has left (render sets goneLine; specs/night-schedule.md,
  // point 5). It is a "closed" line: no answers, no actions, and the kept topics are emptied.
  let goneLine = null;
  let endedTalk = null;   // the person whose conversation has had its last line (closeTalk forgets it)
  function endGoneTalk() {
    if (goneLine === null || !talking) return;
    const text = goneLine;
    goneLine = null;
    endedTalk = talking;
    window.campusPhoto?.close();   // the clerk has gone: the pieces of the photo stay on the counter
    showLine({ npc: talking, name: $("talk-name").textContent, node: "closed", text, trust: null, note: "", actions: [], options: [] });
  }
  function showLine(line) {
    const t = ui();
    if (talking !== line.npc) { $("talk-log").replaceChildren(); asked.clear(); topics.clear(); }   // a different person: a new conversation
    talking = line.npc;
    window.playing = false;   // the character stands still while talking
    $("talk-name").textContent = line.name;
    $("talk-avatar").textContent = line.name.charAt(0);
    const firstLine = $("talk-log").children.length === 0;
    // Returning to the menu keeps the messages already on screen, without another greeting.
    const sayLine = line.node !== "start" || firstLine;
    if (sayLine) addSaid(line.text);
    if (line.npc !== "computer12") {
      if (line.node === "closed") {
        topics.clear();
        line = { ...line, actions: [] };
      } else {
        // Root subjects, Tomás's factual leads and Rita's question about the photo remain useful after choosing a sibling.
        // Reactions such as "Apologise" belong only to the current exchange.
        if (line.node === "start" || line.node === "result" || (line.npc === "tomas" && line.node === "kind") || (line.npc === "rita" && line.node === "photo")) {
          // A memory answer (↺) is something said on arriving: it is never kept as a topic, and it is
          // offered only with the greeting, the first line of a conversation (specs/earlier-nights.md, point 5).
          for (const option of line.options) {
            if (option.next && option.next !== "start" && !option.memory) topics.set(option.next, option);
          }
        }
        const available = new Map();
        for (const option of [...line.options, ...topics.values()]) {
          if (option.next !== "start" && (firstLine || !option.memory)) available.set(option.next, option);
        }
        line = { ...line, options: [...available.values()] };
      }
    }
    // No trust hearts on screen: the player reads the mood in what the person says (specs/cleaner-interface.md).
    // The server still sends `trust`, and a person with trust 0 still ends the conversation.
    // "Goodbye" (an answer that ends the talk) is not shown: the header has "End conversation".
    // A question already chosen in this conversation is not offered again.
    // When a decision can be taken, it is the moment of the choice: only the decisions are offered (specs/actions-when-they-make-sense.md).
    const deciding = (line.actions || []).some(action => action.decision && action.allowed);
    const answers = deciding ? [] : line.options.filter(option => option.next !== null && !asked.has(option.next)).map(option => {
      // A memory answer has a small ↺ in front; screen readers hear "You have heard this before" instead.
      const button = make("button", option.memory ? `↺ ${option.label}` : option.label, "answer");
      if (option.memory) {
        button.title = t.memory_answer;
        button.setAttribute("aria-label", `${t.memory_answer}: ${option.label}`);
      }
      button.addEventListener("click", () => {
        asked.add(option.next);
        addBubble(option.label, "me");   // the player's answer goes on the right, like a sent message
        if (option.cost) penalize(option.cost);   // a rude answer: minutes off the countdown
        talkStep(line.npc, option.next);
      });
      return button;
    });
    // What can be done by talking to this person (ask for the copy, take the decision...): choices inside the conversation.
    // They look like any other answer and come after the questions (specs/actions-when-they-make-sense.md).
    const doing = make("div", undefined, "actions investigate talk-actions");
    for (const action of line.actions || []) {
      if (action.id === "open_drawer") continue;   // the USB stick has to be found in the room (specs/pen-and-code.md)
      if (action.decision && !action.allowed) continue;   // a decision shows only when it can be taken
      if (action.id === "request_copy" && !asked.has("order")) continue;   // the copy only after the clerk mentions the original order
      if (action.id === "present_evidence") continue;   // the hearing button below replaces it (specs/evidence-and-hearing.md, point 9)
      const isCode = action.id === "view_files";   // computer 12 asks for its code first
      const isPhoto = action.id === "request_copy";   // the original photo has to be put together (specs/torn-photo.md)
      const button = make("button", isCode ? t.code_enter : action.label, "answer");
      button.dataset.action = action.id;
      button.addEventListener("click", () => isCode ? askCode(line) : isPhoto ? openPhoto(line, action) : talkAction(line, action));
      doing.append(button);
    }
    // The professor's story button starts the hearing instead of ending the game at once (point 9).
    // It has the story's own label and looks like any other answer (specs/actions-when-they-make-sense.md);
    // a short line under it says the hearing cannot be left. The hearing is played in this same card (showHearing).
    const present = (line.actions || []).find(action => action.id === "present_evidence");
    if (present) {
      const button = make("button", present.label, "answer");
      button.dataset.action = "hearing";
      button.addEventListener("click", () => startHearing(present));
      doing.append(button, make("p", t.hearing_hint, "muted"));
    }
    // "📁 Show evidence", in its own row between the log and the answers, on every line of a person
    // (not computer 12, not a closed line, not during the hearing: specs/evidence-and-hearing.md, point 5).
    const showsEvidence = line.npc !== "computer12" && line.node !== "closed" && !(current && current.hearing);
    const evidenceButton = make("button", t.evidence_show, "secondary evidence-show");
    evidenceButton.addEventListener("click", () => askEvidence(line));
    $("talk-evidence").replaceChildren(...(showsEvidence ? [evidenceButton] : []));
    $("talk-evidence").hidden = !showsEvidence;
    if (doing.children.length && window.campusInside === false) doing.append(make("p", t.outside_hint, "muted"));
    $("talk-options").replaceChildren(...answers, ...(doing.children.length ? [doing] : []));
    $("talk-options").hidden = !doing.children.length && !answers.length;
    $("talk-close").classList.toggle("only-way", !doing.children.length && !answers.length);   // the way out stands out
    applyInside();
    if (line.note) saveDiary(line.name, line.note);
    $("talk").hidden = false;
    updateNear();
    sound.talk();
    if (sayLine) speak(line.text, line.npc);
    $("talk-options").querySelector("button")?.focus({ preventScroll: true });
  }
  // The player chose to do something by talking: the story's own action runs, and the person answers with its result.
  async function talkAction(line, action) {
    if (window.campusBusy || !current) return;
    const scene = current.scene;
    addBubble(action.label, "me");
    showTyping();
    if (!await send("play", { action: action.id })) { $("talk-log").querySelector(".typing")?.remove(); return; }
    if (!talking || current.scene !== scene) return;   // the scene changed (for example the chat opened): the conversation is over
    // The person is no longer here (Leonor after `accuse`, or gone by the schedule): send() has already
    // ended the conversation with the reply's message, so the start menu is not asked for again.
    if (!current.people.some(person => person.id === line.npc)) return;
    // Refresh conditions and available actions after changing the story, retaining the log.
    // The computer has its own code/chat flow.
    if (line.npc === "computer12") {
      showLine({ npc: line.npc, name: line.name, text: current.message, trust: null, note: "", actions: [], options: [] });
      return;
    }
    setBusy(true);
    try {
      const menu = await request({ operation: "talk", player: current.player, language: window.lang || "pt", npc: line.npc, node: "start" });
      screenLine = menu;   // a card shown now is shown on the start line (specs/evidence-and-hearing.md, point 5)
      showLine({ ...menu, node: "result", text: current.message });
    } catch (error) {
      closeTalk();
      toast(error.name === "Error" ? error.message : ui().network_error);
    } finally { setBusy(false); }
  }
  // ---------- the code of computer 12 (specs/pen-and-code.md) ----------
  // A small field for 4 digits replaces the answers. The server checks the code; a wrong one costs 1 minute.
  function askCode(line) {
    const t = ui();
    const form = make("form", undefined, "code-form");
    const input = make("input");
    Object.assign(input, { inputMode: "numeric", maxLength: 4, autocomplete: "off", placeholder: "• • • •" });
    input.setAttribute("aria-label", t.code_label);
    const unlock = make("button", t.code_unlock); unlock.type = "submit";
    form.append(input, unlock);   // to give up, "End conversation" in the header
    form.addEventListener("submit", async event => {
      event.preventDefault();
      const code = input.value.trim();
      if (!/^\d{4}$/.test(code) || window.campusBusy) { input.focus(); return; }
      addBubble("••••", "me");
      showTyping();
      const scene = current.scene;
      if (!await send("unlock", { code })) { $("talk-log").querySelector(".typing")?.remove(); return; }
      if (!current.unlocked) {   // wrong code: the computer stays locked, and it costs time
        addSaid(current.message);
        penalize(1, t.time_penalty_code);
        input.value = ""; input.focus();
        return;
      }
      if (!talking || current.scene !== scene) return;
      showLine({ npc: line.npc, name: line.name, text: current.message, trust: null, note: "", actions: [], options: [] });
    });
    $("talk-options").replaceChildren(form);
    $("talk-options").hidden = false;
    $("talk-close").classList.remove("only-way");
    input.focus();
  }
  // ---------- the torn photo of the print shop (specs/torn-photo.md) ----------
  // The clerk finds the original print shredded; photo.js shows the pieces. When the frame is full, the
  // server says if the photo is right (only it knows the solution) and, if so, gives the photo.
  function openPhoto(line, action) {
    if (!window.campusPhoto) return;
    const t = ui();
    addBubble(action.label, "me");   // the player asks for the copy, and hears that it was shredded
    addSaid(t.photo_intro);
    window.campusPhoto.open({
      title: t.photo_title, hint: t.photo_hint, close: t.photo_close,
      submit: async pieces => {
        const scene = current.scene;
        if (!await send("assemble", { pieces })) return;
        if (!current.assembled) { toast(current.message); return "wrong"; }   // it does not fit yet: no time is taken
        if (talking && current.scene === scene) {
          showLine({ npc: line.npc, name: line.name, text: current.message, trust: null, note: "", actions: [], options: [] });
        }
        return "done";
      },
    });
  }
  // ---------- showing evidence (specs/evidence-and-hearing.md, points 5 and 6) ----------
  // Like the code field, the cards held replace the answers. The answers are kept aside, so
  // "Put it away" puts back the very same buttons: nothing is sent and nothing is added to the log.
  function askEvidence(line) {
    const t = ui();
    const kept = [...$("talk-options").children], wasHidden = $("talk-options").hidden;
    const wasOnlyWay = $("talk-close").classList.contains("only-way");
    const tray = make("div", undefined, "evidence-tray");
    tray.append(make("p", t.evidence_title, "evidence-title"));
    const cards = current.evidence || [];
    if (!cards.length) tray.append(make("p", t.evidence_empty, "muted"));
    for (const card of cards) {
      const button = make("button", `📁 ${card.label}`, "answer evidence-card");
      button.addEventListener("click", () => confrontWith(line, card));
      tray.append(button);
    }
    const back = make("button", t.evidence_back, "secondary evidence-back");
    back.addEventListener("click", () => {
      $("talk-options").replaceChildren(...kept);
      $("talk-options").hidden = wasHidden;
      $("talk-close").classList.toggle("only-way", wasOnlyWay);
      $("talk-evidence").hidden = false;
      applyInside();
      $("talk-evidence").querySelector("button")?.focus({ preventScroll: true });
    });
    tray.append(back);
    $("talk-evidence").hidden = true;   // the tray is open: the button that opened it steps aside
    $("talk-options").replaceChildren(tray);
    $("talk-options").hidden = false;
    $("talk-close").classList.remove("only-way");
    tray.querySelector("button").focus({ preventScroll: true });
  }
  // A card is shown on the line on the screen. The server answers with the reveal or the rebuff,
  // drawn as a line of that person with the answers that line had; a rebuff costs minutes, like a rude answer.
  async function confrontWith(line, card) {
    if (window.campusBusy || !current || !screenLine || screenLine.npc !== line.npc) return;
    const t = ui(), node = screenLine.node;
    addBubble(`📁 ${card.label}`, "me");
    showTyping();
    if (!await send("confront", { npc: line.npc, node, evidence: card.id })) { $("talk-log").querySelector(".typing")?.remove(); return; }
    if (!talking || !current.confront) { goneLine = null; return; }   // a catch closed the card: nothing more is drawn
    const reply = current.confront;
    if (reply.cracked) {
      topics.delete(node);   // the claim is broken: its kept answer is not offered again (point 7)
      screenLine = { ...screenLine, node: "start" };
    }
    showLine({ npc: reply.npc, name: reply.name, text: reply.text, trust: reply.trust, note: reply.note,
               options: screenLine.options, actions: current.actions.filter(action => action.person === reply.npc) });
    // The server now charges the card's minutes and they arrive in night.charged (specs/night-schedule.md,
    // point 4): only the note is shown here, so a rebuff is not counted twice.
    if (reply.minutes) {
      toast((reply.npc === "duarte" ? t.time_penalty_duarte : t.time_penalty_card).replace("{n}", reply.minutes));
      sound.refuse();
    }
    endGoneTalk();   // a rebuff whose minutes reach a departure: the rebuff first, then the last line
  }
  // ---------- the hearing, inside the professor's conversation card (specs/evidence-and-hearing.md, points 9 to 11) ----------
  // It is not an ordinary conversation: no kept topics, no start menu. The server sends the whole log
  // (`hearing.said`), and this card is drawn again from it after every answer.
  async function startHearing(action) {
    if (window.campusBusy || !current) return;
    addBubble(action.label, "me");
    showTyping();
    if (!await send("hearing", { answer: "start" })) { $("talk-log").querySelector(".typing")?.remove(); return; }
    $("talk-log").querySelector(".typing")?.remove();
    if (current.heard && current.hearing && !current.ending) showHearing(current.hearing);
  }
  async function answerHearing(answer) {
    if (window.campusBusy || !current) return;
    showTyping();
    if (!await send("hearing", { answer })) { $("talk-log").querySelector(".typing")?.remove(); return; }
    // After the third answer the ending arrives and render() closes this card: the ending card shows the reply.
    if (talking && current.hearing && !current.ending) showHearing(current.hearing);
  }
  function addHeard(entry) {   // one entry of the log: the player on the right, Duarte or the professor with their name
    if (entry.who === "you") { addBubble(entry.text, "me"); return; }
    for (const part of partsOf(entry.text)) {
      if (part.kind === "speech") {
        const bubble = make("div", undefined, `bubble them by-${entry.who}`);
        bubble.append(make("strong", entry.name, "speaker"), make("p", part.text), make("time", campusTime()));
        $("talk-log").append(bubble);
        continue;
      }
      const narration = make("div", undefined, "narration");
      narration.append(make("p", part.text));
      $("talk-log").append(narration);
    }
  }
  function showHearing(hearing) {
    const t = ui();
    const professor = current.people.find(person => person.id === "professor");
    talking = "professor";
    window.playing = false;
    $("talk-log").replaceChildren(); asked.clear(); topics.clear();
    $("talk-name").textContent = professor ? professor.name : "";
    $("talk-avatar").textContent = professor ? professor.name.charAt(0) : "";
    // The professor's trust: three minus the doubts (the server never counts more than three), in words
    // under the claim number. There are no hearts in conversations (specs/cleaner-interface.md).
    const trust = Math.max(0, 3 - hearing.doubts);
    const step = make("p", t.hearing_step.replace("{n}", hearing.step), "hearing-step");
    const doubt = make("p", `${t.hearing_trust}: ${trust}/3`, `hearing-trust trust-${trust}`);
    for (const entry of hearing.said) addHeard(entry);
    $("talk-log").scrollTop = $("talk-log").scrollHeight;
    $("talk-evidence").replaceChildren();
    $("talk-evidence").hidden = true;   // no "Show evidence" and no story actions: the answers are the cards
    const answers = (current.evidence || []).map(card => {
      const button = make("button", `📁 ${card.label}`, "answer evidence-card");
      button.addEventListener("click", () => answerHearing(card.id));
      return button;
    });
    const silent = make("button", t.hearing_concede, "answer");
    silent.addEventListener("click", () => answerHearing("concede"));
    $("talk-options").replaceChildren(step, doubt, ...answers, silent);
    $("talk-options").hidden = false;
    $("talk-close").classList.remove("only-way");
    $("talk").hidden = false;
    updateNear();
    sound.talk();
    speakHeard(hearing.said);
    $("talk-options").querySelector("button")?.focus({ preventScroll: true });
  }
  // The voices read what was said since the player's last answer (the reply and the next claim),
  // each quote in the voice of its speaker.
  function speakHeard(said) {
    if (!canSpeak || sound.isMuted()) return;
    let first = 0;
    said.forEach((entry, i) => { if (entry.who === "you") first = i + 1; });
    stopSpeaking();
    say(said.slice(first).filter(entry => VOICES[entry.who]).flatMap(entry => quotesOf(entry.text).map(line => [line, entry.who])));
  }
  // The reply to the third answer, shown on the ending card; null when the ending came without a hearing.
  function lastReply() {
    const hearing = current && current.hearing;
    if (!hearing || !hearing.said.length) return null;
    return hearing.said[hearing.said.length - 1];   // after the third answer, the last entry is always a reply
  }
  // ---------- searching the study room: the close-up of the table (specs/hidden-object-table.md) ----------
  // Asks the server about one kind of object of the table. Answers "found", "wrong" or nothing.
  window.campusSearch = async spot => {
    if (window.campusBusy || !current || current.ending) return;
    const t = ui();
    if (current.scene !== "study_room" || window.campusInside === false) { toast(t.search_where); return; }
    if (current.inventory.some(item => item.id === "usb_stick")) { toast(t.search_done); return; }
    if (!await send("search", { spot })) return;
    if (current.found) { toast(current.message); return "found"; }
    if (current.message !== t.search_where && current.message !== t.search_done) {
      penalize(1, `${current.message} (${t.time_penalty_search})`);   // a wrong object costs 1 minute
      return "wrong";
    }
  };
  // Opens the close-up (table.js draws it): only inside the study room, before the stick is found.
  window.campusOpenTable = () => {
    if (!current || current.ending || !window.campusTable) return;
    const t = ui();
    if (current.scene !== "study_room" || window.campusInside === false) { toast(t.search_where); return; }
    if (current.inventory.some(item => item.id === "usb_stick")) { toast(t.search_done); return; }
    window.playing = false;   // the character stands still while looking at the table
    window.campusTable.open({
      title: t.table_title, hint: t.table_hint, close: t.table_close, lens: t.table_lens, labels: t.spots,
      pick: kind => window.campusSearch(kind),
      onClose: () => { if (!talking && !phone.open && !dialog.open) window.playing = true; },
    });
  };
  async function talkStep(npc, node) {
    if (window.campusBusy || !current) return;
    // During the hearing, the professor's card shows the hearing where it stopped (specs/evidence-and-hearing.md, point 9).
    // Anyone else cannot be talked to until the hearing ends: a note says so and the hearing card stays open.
    if (current.hearing && !current.ending) {
      if (npc === "professor") showHearing(current.hearing);
      else toast(ui().hearing_locked);
      return;
    }
    // A line asked for is a command: the page reports its minute first when it is ahead, and the line is
    // not asked for when that person has gone meanwhile (specs/night-schedule.md, point 4).
    if (!await catchUp(npc)) return;
    if (talking === npc) showTyping();   // only inside an open conversation (not before the first line)
    setBusy(true);
    try {
      const line = await request({ operation: "talk", player: current.player, language: window.lang || "pt", npc, node });
      screenLine = line;
      showLine(line);
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
    // Still "n/4": the story has four endings. A ★ after it once the night is over (specs/earlier-nights.md, point 9).
    const star = current?.memory?.over ? " ★" : "";
    return `${ui().collection}: ${all.filter(e => found.includes(e.id)).length}/${all.length}${star}`;
  }
  function collectionText() {
    const all = data[window.lang || "pt"].endings, found = loadEndings();
    return `${collectionCount()}   ${all.map(e => found.includes(e.id) ? ENDING_EMOJI[e.id] || "✔" : "🔒").join(" ")}`;
  }
  function shareText(ending) {
    const t = ui(), clues = current?.clues || [], done = clues.filter(c => c.done).length;
    const squares = clues.map(c => (c.done ? "🟩" : "⬛")).join("") + (current?.flagged ? "🟨" : "⬛");
    return [`${t.share_title} 🕵️`, `${ending.emoji || ENDING_EMOJI[ending.id] || "🕵️"} ${ending.title}`,
            `${squares} · ${done}/${clues.length} ${t.share_clues}`, `⏳ ${minutesSeconds(msLeft())} · ${collectionCount()}`].join("\n");
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
  // ---------- countdown: 30 minutes before the faculty closes (specs/harder-campus.md) ----------
  // The time LEFT is kept in this browser, per player, and it only goes down while the game is really
  // being played (the page open and in sight, before an ending). Closing the game pauses it, so a saved
  // game can be continued later with the time it had. Rude answers take 5 minutes off; at 0 the game
  // stops and only "Try again" is left.
  const COUNTDOWN_MINUTES = 30, FULL_TIME = COUNTDOWN_MINUTES * 60000;
  const NIGHT_STARTS = 22 * 60 + 15;   // 22:15, the time on the case file, so the doors close at 22:45
  const timeKey = player => `plot-twist-time-left:${player}`;
  let timeLeft = null;      // milliseconds left for the player of `current` (null until a game is open)
  let timeOwner = null;     // the player `timeLeft` belongs to
  let lastTick = null;      // when the time was last counted
  function loadTime(player) {
    try { const saved = localStorage.getItem(timeKey(player)); return saved === null ? null : Number(saved); }
    catch (error) { return null; }   // no storage: the time is kept only while the page is open
  }
  function saveTime() {
    try { localStorage.setItem(timeKey(timeOwner), String(Math.round(timeLeft))); } catch (error) { /* no storage */ }
  }
  const msLeft = () => (timeLeft === null ? FULL_TIME : timeLeft);
  const minutesSeconds = ms => {
    const seconds = Math.ceil(ms / 1000);
    return `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
  };
  function campusTime() {   // the time on the campus clocks: 22:15 plus the time already used
    const minutes = Math.floor(NIGHT_STARTS + COUNTDOWN_MINUTES - msLeft() / 60000);
    return `${String(Math.floor(minutes / 60) % 24).padStart(2, "0")}:${String(minutes % 60).padStart(2, "0")}`;
  }
  function startCountdown(state) {   // called on every render
    if (timeOwner !== state.player) {   // a game was opened: take its time from this browser
      timeOwner = state.player;
      timeLeft = loadTime(state.player) ?? FULL_TIME;
      lastTick = null;
    }
    if (state.fresh && timeLeft <= 0) timeLeft = FULL_TIME;   // a game that was never played gets 30 new minutes
    saveTime();
  }
  function penalize(minutes, note = ui().time_penalty) {   // a rude answer, a wrong place, a wrong code: less time
    if (!current || current.ending || timeLeft === null) return;
    timeLeft = Math.max(0, timeLeft - minutes * 60000);
    saveTime();
    toast(note.replace("{n}", minutes));
    sound.refuse();
    tick();
  }
  // ---------- the server's campus minute (specs/night-schedule.md, points 3 and 4) ----------
  // The page keeps drawing its own countdown, but the server now knows the minute too: the page
  // follows every snapshot, and tells the server its own minute when it is ahead.
  // The page's own whole minute: the minutes already used, rounded down (from 0 to 30).
  const pageMinute = () => Math.min(COUNTDOWN_MINUTES, Math.max(0, Math.floor((FULL_TIME - msLeft()) / 60000)));
  // After every snapshot: take off what this command cost, once, then never have more time than the
  // server's minute leaves. So a cleared browser or another device no longer gets 30 new minutes.
  function applyNight(state, operation) {
    const night = state.night;
    if (!night || timeLeft === null) return;
    // A fresh game at minute 0, opened or restarted: the server is starting a new night, so the page starts
    // from 30 minutes too (after a restart of the host the browser would otherwise push its old time onto
    // the new night). Only then: the other replies of an untouched game must not give time back.
    const opening = operation === "open" || operation === "restart";
    if (opening && state.fresh && night.minute === 0) timeLeft = FULL_TIME;
    timeLeft = Math.max(0, timeLeft - night.charged * 60000);   // the countdown counts in ms: half a minute is 30 seconds
    timeLeft = Math.min(timeLeft, (COUNTDOWN_MINUTES - night.minute) * 60000);
    saveTime();
    // A refusal shows its own note (render adds the charge to it): only one note at a time.
    if (night.charged > 0 && (state.accepted || !state.message)) toast(chargedNote(state));
  }
  // "−0.5 min" in English, "−0,5 min" in Portuguese
  function chargedNote(state) {
    return ui().time_charged.replace("{n}", state.night.charged.toLocaleString(state.language === "pt" ? "pt-PT" : "en-GB"));
  }
  // Sends the page's own minute with the operation "time". Returns false when a command that was waiting
  // for this report must not be sent: the reply is a catch (not accepted), the night is closed, or
  // `person` (the person the command is for) is no longer in the room (point 4).
  async function reportTime(person = null) {
    if (!await send("time", { minute: pageMinute() })) return false;
    if (current.accepted && current.message) toast(current.message);   // Tomás in the lab door: the round passes
    if (!current.accepted || current.night.closed) return false;
    return !person || current.people.some(p => p.id === person);
  }
  // Before a command: report first, but only when the page is ahead of the server's minute.
  function catchUp(person) {
    if (!current || !current.night || current.ending || pageMinute() <= current.night.minute) return true;
    return reportTime(person);
  }
  // Every second (from the timer under tick): report when the page reaches the next mark of the schedule
  // (`night.report_at`), and when the time is up. It never polls the server otherwise.
  let lastReportTry = 0;
  function reportDue(left) {
    const night = current.night, minute = pageMinute();
    if (!night || night.closed || window.campusBusy || minute <= night.minute) return;
    if (minute < night.report_at && left > 0) return;
    if (Date.now() - lastReportTry < 5000) return;   // a report that failed is tried again a few seconds later
    lastReportTry = Date.now();
    reportTime();
  }
  // The shutter slip and the empty chair (point 5): a notice that is new (the room was just entered,
  // the page was reloaded there, or the person has just left) is kept in the diary under the room's
  // title, so the date on the slip can be read again, and shown as the note over the picture, unless
  // it has just become the last line of the open card.
  let lastNotice = "";
  function showNotice(state) {
    const notice = state.night ? state.night.notice : "";
    if (notice && notice !== lastNotice) {
      saveDiary(state.title, notice);
      if (goneLine !== notice) toast(notice);
    }
    lastNotice = notice;
  }
  function showTimeUp() {
    const t = ui();
    closeTalk();
    stopSpeaking();
    window.playing = false;   // the detective cannot move any more
    $("timeup-title").textContent = t.time_up_title;
    $("timeup-text").replaceChildren(make("p", t.time_up_text));
    $("timeup-again").textContent = t.time_up_again;
    $("timeup-card").hidden = false;
    $("timeup-again").focus();
    sound.refuse();
  }
  function tick() {   // every second: the countdown on the screen, and the end when it reaches 0
    if (!current || timeLeft === null) return;
    const now = Date.now();
    // The time goes down only while the game is on the screen and running.
    const running = !current.ending && !document.hidden && !shell.hidden && $("timeup-card").hidden;
    if (running && lastTick !== null) { timeLeft = Math.max(0, timeLeft - (now - lastTick)); saveTime(); }
    lastTick = now;
    const left = msLeft();
    // The campus time first, then the countdown: "22:27 · ⏳ 17:04" (specs/night-schedule.md, point 4).
    $("clock").textContent = `${campusTime()} · ⏳ ${minutesSeconds(left)}`;
    $("clock").setAttribute("aria-label", `${campusTime()} · ${ui().time_aria}: ${minutesSeconds(left)}`);
    $("clock").classList.toggle("urgent", !current.ending && left < 5 * 60000);
    if (left === 0 && !current.ending && $("timeup-card").hidden) showTimeUp();
    if (!$("timeup-card").hidden) window.playing = false;   // nothing else may let the detective walk again
  }
  // Only the timer reports, never a tick called by render or penalize: a report started there would keep
  // the page busy and stop the command that called it (a rude answer would lose its reply).
  setInterval(() => { tick(); if (current && !current.ending) reportDue(msLeft()); }, 1000);
  $("timeup-again").addEventListener("click", () => $("confirm-restart").click());   // the same confirmed restart as "New game"
  // How far the night has gone, from 0 (30 minutes left) to 1 (the faculty closes): it drives the music.
  function tensionOf() {
    return Math.min(1, Math.max(0, 1 - msLeft() / (COUNTDOWN_MINUTES * 60000)));
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
  let restarting = false;   // true while a confirmed "New game" is on its way (set by the restart button)
  function checkNotices(state) {
    if (state.ending) { $("sms").hidden = true; return; }
    // During a new game the old night's messages are about to be deleted: the restart calls this again
    // once they are gone, so the new night's first message is not wiped (specs/earlier-nights.md, point 7).
    if (restarting) return;
    const t = ui(), done = (state.clues || []).filter(c => c.done).length, store = loadMsgs(state.player);
    const due = [];
    // The unknown number remembers earlier nights: its message as this night starts, each id only once
    // (specs/earlier-nights.md, point 4). It comes first, so a message of the case pops up over it.
    for (const whisper of state.whispers || []) {
      if (!store.sent.includes(whisper.id)) due.push([whisper.id, whisper.text]);
    }
    for (let i = 1; i <= Math.min(done, t.notices.length); i++) if (!store.sent.includes(`c${i}`)) due.push([`c${i}`, t.notices[i - 1]]);
    if (state.flagged > 0 && !store.sent.includes("chat")) due.push(["chat", t.notice_chat]);
    // The unknown number also keeps the time: the warnings and the rounds the server says are due now,
    // each id only once (specs/night-schedule.md, point 7).
    for (const message of (state.night && state.night.messages) || []) {
      if (!store.sent.includes(message.id)) due.push([message.id, message.text]);
    }
    if (!due.length) return;
    for (const [id, text] of due) { store.sent.push(id); store.list.push({ text, clock: campusTime() }); }
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

  // ---------- the buttons for the torch and the Rules window ----------
  $("torch-toggle").addEventListener("click", () => toggleTorch());
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
  howto.innerHTML = '<h2 id="howto-title"></h2><p id="howto-intro" class="muted"></p><ul id="howto-list"></ul><details class="howto-dev"><summary id="howto-dev-title"></summary><p id="howto-dev-intro" class="muted"></p><ul id="howto-dev-list"></ul><p id="howto-run" class="muted"></p></details><div class="dialog-actions"><button id="howto-close"></button></div>';
  document.body.append(howto);
  function openHowto() {
    if (howto.open) return;
    const t = ui();
    $("howto-title").textContent = t.howto_title;
    $("howto-intro").textContent = t.howto_intro;
    $("howto-run").textContent = t.howto_run;
    $("howto-close").textContent = t.howto_close;
    $("howto-dev-title").textContent = t.rules_dev;
    $("howto-dev-intro").textContent = t.dev_intro;
    const entry = ([title, file, detail]) => {
      const item = make("li");
      item.append(make("strong", title));
      if (file) item.append(document.createTextNode(" "), make("code", file));
      item.append(make("p", detail));
      return item;
    };
    $("howto-list").replaceChildren(...t.rules_items.map(entry));
    $("howto-dev-list").replaceChildren(...t.howto_items.map(entry));
    window.playing = false;
    howto.showModal();
    howto.scrollTop = 0;   // the window opens at its top, not at the Close button
    $("howto-title").setAttribute("tabindex", "-1");
    $("howto-title").focus({ preventScroll: true });
  }
  $("howto-open").addEventListener("click", openHowto);
  $("howto-close").addEventListener("click", () => howto.close());
  // ---------- the menu of the top bar: rules, torch, sound (specs/cleaner-interface.md, changed by specs/rules-and-character.md) ----------
  function setMenu(open) {
    $("menu-list").hidden = !open;
    $("menu-toggle").setAttribute("aria-expanded", String(open));
  }
  $("menu-toggle").addEventListener("click", () => setMenu($("menu-list").hidden));
  $("howto-open").addEventListener("click", () => setMenu(false));   // its window opens over the game
  document.addEventListener("click", e => { if (!e.target.closest(".tool-menu")) setMenu(false); });   // a click anywhere else closes it
  document.addEventListener("keydown", e => {
    if (e.key === "Escape" && !$("menu-list").hidden) { setMenu(false); $("menu-toggle").focus(); }
  });
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
      const item = make("li", undefined, clue.done ? "done" : clue.lost ? "lost" : "");
      const box = make("span", clue.done ? "✔" : clue.lost ? "✕" : "○", "todo-box");
      box.setAttribute("aria-label", clue.done ? t.todo_done : clue.lost ? t.todo_lost : t.todo_open);
      const text = make("span", undefined, "todo-text");
      text.append(make("strong", clue.label));   // not where to find it: the player has to look (specs/cleaner-interface.md)
      // When it closes, from the start of the night, and "Too late" once it is lost (specs/night-schedule.md, point 6).
      if (clue.lost) text.append(make("small", t.todo_lost));
      else if (clue.until && !clue.done) text.append(make("small", t.todo_until.replace("{time}", clue.until)));
      item.append(box, text);
      list.append(item);
    }
    screen.append(bar, list, make("p", t.todo_hint, "muted todo-hint"));
    if ((current?.clues || []).some(c => c.lost)) screen.append(make("p", t.todo_hint_lost, "muted todo-hint"));
  }

  function drawMap(screen, t) {
    const titles = data[window.lang || "pt"].scenes;
    const map = window.campusMap && window.campusMap();
    if (!map) {   // the 3D scenery did not load: only say where the character is
      screen.append(make("p", t.map_no_3d, "muted"), make("p", `${t.map_where}: ${titles[current.room].title}`, "map-where"));
      return;
    }
    const ready = (current?.clues || []).every(c => c.done || c.lost);   // a lost clue does not lock it (specs/night-schedule.md, point 6)
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

  // ---------- earlier nights: the fifth figure grows on the case-file photo (specs/earlier-nights.md, point 6) ----------
  // The start screen is drawn before the server knows the player, so it uses a display copy kept in this
  // browser: the night and `over` the server last reported. Only the picture reads it, never the rules.
  const NIGHT_KEY = "plot-twist-night";
  function loadNight() {
    try {
      const saved = JSON.parse(localStorage.getItem(NIGHT_KEY) || "{}");
      const night = Math.floor(Number(saved.night));   // a damaged copy (2.5, "x") must not stop the page
      return { night: night >= 1 ? night : 1, over: saved.over === true };
    } catch (error) { return { night: 1, over: false }; }
  }
  function rememberNight(memory) {   // called by render with the snapshot's `memory`
    if (!memory) return;
    try { localStorage.setItem(NIGHT_KEY, JSON.stringify({ night: memory.night, over: memory.over })); } catch (error) { /* no storage */ }
  }
  // The night shown: the larger of the copy and one more than the story endings in this browser's collection
  // (an ending on screen is still "night 1" for the server until the new game).
  function shownNight() {
    const copy = loadNight(), found = loadEndings();
    const story = data[window.lang || "pt"].endings.filter(ending => found.includes(ending.id)).length;
    return { night: Math.max(copy.night, story + 1), over: copy.over };
  }
  // 1: nothing is added. 2: the fifth silhouette is darker. 3: its long coat has the detective's colour.
  // 4: plus a scarf. 5: plus a hat. 6 (and every later night): the "?" of the red box is the player's initial.
  function nightStage(night) {
    return Math.min(6, Math.max(1, night));
  }
  // The fifth silhouette of assets/cover.jpg in the picture's own pixels (1280 × 720), measured on the file.
  // The shapes use the same viewBox and "slice" as the photo's object-fit: cover, so they lie exactly on it.
  const FIFTH_COAT = "938,247 999,247 1016,335 1012,350 1020,428 924,428 925,350 918,335 926,252";
  // The scarf and the hat of the detective in game3d.html. The coat takes the colour chosen in the
  // character creator (OUTFIT_COLORS[look.color]), so "Yours." on night 3 is true.
  const DETECTIVE = { scarf: "#8a1f24", hat: "#3a2a1e" };
  const PHOTO_PAPER = "#f2d089", PHOTO_FLOOR = "#d9a359";   // the pale yellow behind the people, and the floor
  function silhouette(fill, coat, stroke, width) {   // the head, the long coat and the two legs
    const style = { stroke, "stroke-width": width, "stroke-linejoin": "round" };
    return [svg("circle", { cx: 962, cy: 219, r: 22, fill, ...style }),
            svg("rect", { x: 946, y: 428, width: 25, height: 104, rx: 6, fill, ...style }),
            svg("rect", { x: 977, y: 428, width: 25, height: 104, rx: 6, fill, ...style }),
            svg("polygon", { points: FIFTH_COAT, fill: coat, ...style })];
  }
  const photoBox = document.querySelector("#stepCase .photo"), redBox = photoBox?.querySelector(".target");
  const fifthFigure = svg("svg", { class: "fifth-figure", viewBox: "0 0 1280 720", preserveAspectRatio: "xMidYMid slice", "aria-hidden": "true" });
  if (photoBox) photoBox.insertBefore(fifthFigure, redBox);   // under the red box
  function drawFifthFigure(shown) {
    const stage = nightStage(shown.night), dark = "#03060b";
    fifthFigure.replaceChildren();
    if (shown.over) {
      // After the true ending a patch of the photo's own colours covers the fifth silhouette: four people are left.
      fifthFigure.append(...silhouette(PHOTO_PAPER, PHOTO_PAPER, PHOTO_PAPER, 12),
                         svg("rect", { x: 930, y: 535, width: 90, height: 14, fill: PHOTO_FLOOR }));
    } else if (stage >= 2) {
      fifthFigure.append(...silhouette(dark, stage >= 3 ? OUTFIT_COLORS[look.color] : dark, dark, 5));
      if (stage >= 4) {   // a scarf round the neck, one end hanging
        fifthFigure.append(svg("rect", { x: 938, y: 240, width: 50, height: 13, rx: 5, fill: DETECTIVE.scarf }),
                           svg("rect", { x: 973, y: 246, width: 12, height: 50, rx: 4, fill: DETECTIVE.scarf }));
      }
      if (stage >= 5) {   // a fedora: the crown, then the brim
        fifthFigure.append(svg("rect", { x: 944, y: 174, width: 36, height: 28, rx: 7, fill: DETECTIVE.hat }),
                           svg("ellipse", { cx: 962, cy: 202, rx: 37, ry: 7, fill: DETECTIVE.hat }));
      }
    }
    if (!redBox) return;
    redBox.hidden = shown.over;   // the red box and its "?" go with the fifth person
    const initial = name.value.trim().charAt(0).toUpperCase();
    if (stage >= 6 && initial) redBox.dataset.initial = initial;   // play.css shows it in place of the "?"
    else delete redBox.dataset.initial;
  }
  function drawNight() {
    const shown = shownNight(), t = ui(), stage = nightStage(shown.night);
    drawFifthFigure(shown);
    // night_lines has one line for each of nights 2, 3, 4, 5 and 6-and-later; after the true ending, night_done.
    if (shown.over) nightLine.textContent = t.night_done;
    else nightLine.textContent = stage === 1 ? "" : t.night_lines[stage - 2].replace("{n}", shown.night);
    nightLine.hidden = !nightLine.textContent;
  }
  window.addEventListener("language", () => { if (!current) drawNight(); });   // only the start screen shows it
  name.addEventListener("input", () => { if (!current) drawNight(); });   // the initial follows the name typed
  window.addEventListener("campus-look", () => { if (!current) drawNight(); });   // and the coat follows the look
  drawNight();

  window.campusStart = async () => {
    sound.start();
    if (!await send("open")) return;
    try { localStorage.setItem(LAST_NAME_KEY, current.player); } catch (error) { /* no storage */ }
    saveLook(current.player); saveLook(name.value);
    if (window.campusPreview) window.campusPreview.stop();
    if (window.campusSetLook) window.campusSetLook(resolvedLook(look));
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
    // The new night's snapshot is drawn before the old messages are deleted: `restarting` makes
    // checkNotices wait until they are gone (specs/earlier-nights.md, point 7).
    restarting = true;
    try {
      if (await send("restart", { confirmed: true })) {
        dialog.close(); window.playing = true; $("scene-heading").focus();
        stopSpeaking();
        window.dispatchEvent(new Event("campus-restarted"));
        window.campusTable?.reset();   // a new game: no object of the table is marked as checked
        window.campusPhoto?.reset();   // and the pieces of the photo are back on the counter
        timeLeft = FULL_TIME; timeOwner = current.player; lastTick = null; saveTime();   // a new game: 30 new minutes
        $("timeup-card").hidden = true;
        tick();
        try { localStorage.removeItem(msgKey(current.player)); localStorage.removeItem(diaryKey()); } catch (error) { /* no storage */ }
        restarting = false;
        checkNotices(current);   // now the new night's whisper lands in an empty phone, at 22:15
      }
    } finally { restarting = false; }
  });
})();
