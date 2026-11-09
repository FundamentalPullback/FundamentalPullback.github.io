const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const ctx = {window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'data/plan.js'),'utf8'),ctx);
const plan = ctx.window.FP_PLAN;
assert.equal(plan.meta.date,'2026-11-09');
assert.equal(plan.meta.pdf,'data/plan/Plan_Completo_2026-11-09.pdf');
assert.ok(fs.existsSync(path.join(root,plan.meta.pdf)), 'Current PDF must ship with the rule change');
for (const lang of ['es','en']) {
  const get = id => plan[lang].sections.find(s=>s.id===id);
  const a=get('s35a'), b=get('s35b'), c=get('s35c');
  assert.ok(a.blocks[4][1][1][1].includes('2%'), 'Preserve path A first entry');
  assert.ok(a.blocks[1][1].includes('10%') && a.blocks[1][1].includes('15%'), 'Preserve capital limits');
  assert.ok(a.blocks[2][1].includes('1%'), 'Preserve campaign risk');
  assert.ok(a.blocks[4][1][2][1].includes('75%'), 'Usual B/C entry is 75%');
  assert.ok(a.blocks[4][1][2][1].includes('25%'), 'Retain optional remainder/reduced starter');
  assert.ok(b.blocks.at(-1)[1].includes(lang==='es'?'opcional':'optional'), 'No automatic completion');
  assert.ok(c.blocks[3][1].includes(lang==='es'?'peor precio permitido':'worst allowed price'));
  assert.ok(c.blocks[3][1].includes(lang==='es'?'redondeado hacia abajo':'rounded down'));
  assert.ok(c.blocks[8][1].includes('126'), 'Updated worked example');
}
function size(P,E,S,reserve=50) {
  assert.ok(E>S);
  const full=Math.floor(Math.min(.10*P/E,(.01*P-reserve)/(E-S)));
  return {full, initial:Math.floor(.75*full), remaining:full-Math.floor(.75*full)};
}
assert.deepEqual(size(100000,59,53.5),{full:169,initial:126,remaining:43});
assert.deepEqual(size(100000,125,115),{full:80,initial:60,remaining:20});
assert.deepEqual(size(100000,200,180),{full:47,initial:35,remaining:12});
assert.equal(126*59,7434);
assert.equal(126*(59-53.5)+50,743);
console.log('PASS: ES/EN 75/25 entry policy, unchanged capital/risk/path-A limits, optional adds, and sizing examples.');
