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

// A person with kept topics (Duarte here; Rita and Tomás have two answers, specs/two-answers.md):
// photo -> response -> another subject, with the original log still present.
show('duarte', 'start', [option('photo'), option('duarte'), option('pen')]);
click('photo'); show('duarte', 'photo', [option(null)]);
assert.deepEqual(choices(), ['duarte', 'pen']);
assert.equal($('talk-log').children.length, 2);
click('duarte'); show('duarte', 'duarte', [option('warned')]);
assert.deepEqual(choices(), ['warned', 'pen']);
const length = $('talk-log').children.length;
show('duarte', 'start', [option('photo'), option('duarte'), option('pen')]);
assert.equal($('talk-log').children.length, length); // no repeated greeting

// Rita: only the two answers of each line, nothing kept (specs/two-answers.md).
show('rita', 'start', [option('pen'), option('upset')]);
click('pen'); show('rita', 'pen', [option('photo'), option('upset')]);
assert.deepEqual(choices(), ['photo', 'upset']);

// Tomás: every line offers exactly its own two answers, a right one and a wrong one, in the order
// kind -> who -> password; no topic is kept from an earlier line (specs/two-answers.md).
show('tomas', 'start', [option('kind'), option('hard', 5)]);
click('kind'); show('tomas', 'kind', [option('who'), option('hard', 5)]);
assert.deepEqual(choices(), ['who', 'hard']);
click('who'); show('tomas', 'who', [option('password'), option('hard', 5)]);
assert.deepEqual(choices(), ['password', 'hard']);
click('password'); assert.equal(ctx.requested.node, 'password');
show('tomas', 'password', [option(null)]);
assert.deepEqual(choices(), []);
// After an apology, the right answer is offered again even if it was chosen before.
show('tomas', 'calm', [option('kind'), option('closed', 5)]);
assert.deepEqual(choices(), ['kind', 'closed']);
// On his claim line the right answer makes him give in: it is shown to the server as its card.
show('tomas', 'slides', [{ label: 'remind', next: 'slides', crack: 'files' }, option('convinced')]);
click('remind'); assert.deepEqual(ctx.confronted, { npc: 'tomas', card: 'files', said: true });

// Leonor: continue, retain the time penalty, discard context-specific reactions.
show('leonor', 'start', [option('sure'), option('soft'), option('harsh', 5)]);
click('harsh'); assert.equal(ctx.cost, 5);
show('leonor', 'harsh', [option('soft'), option('closed', 5)]);
click('soft'); show('leonor', 'soft', [option('messages')]);
assert.ok(choices().includes('sure') && choices().includes('messages'));
assert.ok(!choices().includes('closed')); // no stale "Insist" after apologising
show('leonor', 'closed', [option(null)], 'Conversation over', [{ id: 'accuse', label: 'Accuse' }]);
assert.deepEqual(choices(), []);

// Computer 12 never inherits another person's subjects.
show('computer12', 'start', [option(null)]);
assert.deepEqual(choices(), []);

// Following a story action, new server-authorised topics remain available afterwards.
show('duarte', 'start', [option('photo')]);
click('photo'); show('duarte', 'result', [option('photo'), option('chat')]);
assert.deepEqual(choices(), ['chat']);
// Leonor before she decides (changed by specs/leonor-two-answers.md, was: her decisions show once they can be taken).
const decisions = allowed => [
  { id: 'ask_for_help', label: 'Ask for help', decision: true, allowed },
  { id: 'accuse', label: 'Accuse', decision: true, allowed }];
const shownActions = () => $('talk-options').children.filter(child => child.children.length)
  .flatMap(group => group.children.map(button => button.dataset.action));
show('leonor', 'start', [option('sure'), option('soft'), option('harsh', 5)], 'start', decisions(false));
assert.deepEqual(shownActions(), []);
assert.deepEqual(choices(), ['soft', 'harsh']);   // one right and one wrong answer
assert.equal($('talk-evidence').hidden, true);   // no evidence before the right answer
click('soft'); show('leonor', 'soft', [option('messages')], 'soft', decisions(true));
assert.deepEqual(shownActions(), []);   // no decision buttons: the photo is shown with "Show evidence"
assert.deepEqual(choices(), []);
assert.equal($('talk-evidence').hidden, false);   // after the right answer

// The clerk offers the copy only after she mentions the original order.
const copy = [{ id: 'request_copy', label: 'Ask for a copy', allowed: true }];
show('amelia', 'start', [option('order'), option('visitor')], 'start', copy);
assert.deepEqual(shownActions(), []);
click('order'); show('amelia', 'order', [option(null)], 'order', copy);
assert.deepEqual(shownActions(), ['request_copy']);
assert.ok(choices().includes('visitor'));   // her other question is still there
const replies = $('talk-options').children;
assert.equal(replies[replies.length - 1].children[0].textContent, 'Ask for a copy');   // after the questions, with no ▶
console.log('Continuous conversation interaction checks passed.');
