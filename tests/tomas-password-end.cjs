// Run with node tests/continuous-conversations.cjs. No browser or npm packages needed.
const fs = require('node:fs');
const vm = require('node:vm');
const assert = require('node:assert/strict');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../prototypes/campus-3d/play.js'), 'utf8');
const elements = new Map();
function element(text = '') {
  return { textContent: text, children: [], dataset: {}, classList: { toggle() {} },
    append(...children) { this.children.push(...children); },
    replaceChildren(...children) { this.children = children; },
    querySelector() { return null; }, setAttribute() {},
    addEventListener(event, callback) { this[event] = callback; } };
}
const $ = id => { if (!elements.has(id)) elements.set(id, element()); return elements.get(id); };
const ctx = vm.createContext({ $, make: (tag, text) => element(text), ui: () => ({}),
  current: { player: 'test' }, window: {}, talking: null, asked: new Set(), topics: new Map(),
  applyInside() {}, saveDiary() {}, updateNear() {}, sound: { talk() {} },
  speak(text) { ctx.spoken = text; },
  addSaid(text) { $('talk-log').append(element(text)); }, addBubble() {},
  penalize(cost) { ctx.cost = cost; }, talkStep(npc, node) { ctx.requested = { npc, node }; },
  talkAction() {}, askCode() {},
  confrontWith(line, card, said) { ctx.confronted = { npc: line.npc, card: card.id, said }; } });
const start = source.indexOf('  function showLine(line) {');
vm.runInContext(source.slice(start, source.indexOf('  // The player chose to do something', start)), ctx);
const option = (next, cost) => ({ label: next, next, ...(cost ? { cost } : {}) });
const show = (npc, node, options, text = node, actions = []) => ctx.showLine({ npc, node, name: npc, options, text, actions });
const choices = () => $('talk-options').children.map(button => button.textContent);
function click(label) { const button = $('talk-options').children.find(b => b.textContent === label); assert.ok(button, label); button.click(); }

// The final hint keeps its text, but no replies/actions or evidence tray.
for (const text of ['A password é o dia e o mês.', 'The password is the day and month.']) {
  show('tomas', 'start', [option('kind'), option('hard')]);
  show('tomas', 'password', [option('slides'), option('photo'), option('hard')], text,
       [{id: 'extra', label: 'Extra action', allowed: true}]);
  assert.deepEqual(choices(), []);
  assert.equal($('talk-options').hidden, true);
  assert.equal($('talk-evidence').hidden, true);
  assert.equal($('talk-log').children.at(-1).textContent, text);
}
// Other people and Tomás's later evidence discussion keep their answers.
show('rita', 'photo', [option('five'), option('upset')]);
assert.deepEqual(choices(), ['five', 'upset']);
show('tomas', 'slides', [option('convinced')]);
assert.deepEqual(choices(), ['convinced']);

// Exercise the real request handler: only an opening with file evidence goes to slides.
Object.assign(ctx, { setBusy() {}, catchUp: async () => true, showTyping() {},
  request: async input => { ctx.lastRequest = input; return {npc: input.npc, node: input.node}; },
  showLine() {}, screenLine: null });
const handlerStart = source.indexOf('  async function talkStep(');
vm.runInContext(source.slice(handlerStart, source.indexOf('  // ---------- walking up', handlerStart)), ctx);
(async () => {
  ctx.current.evidence = [];
  await ctx.talkStep('tomas', 'start');
  assert.equal(ctx.lastRequest.node, 'start');
  ctx.current.evidence = [{ id: 'files' }];
  await ctx.talkStep('tomas', 'start');
  assert.equal(ctx.lastRequest.node, 'slides');
  await ctx.talkStep('tomas', 'password');
  assert.equal(ctx.lastRequest.node, 'password');
  await ctx.talkStep('rita', 'start');
  assert.equal(ctx.lastRequest.node, 'start');
  console.log('Tomás password ending checks passed.');
})().catch(error => { console.error(error); process.exitCode = 1; });
