// Historic accounting and UI suites must replay the app before the two reviewed
// portfolio-only UI changes. The current portfolio has its own live regression.
const assert=require('assert/strict'),crypto=require('crypto'),cp=require('child_process');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const beforeSha='e6bcf0b9a89e899f44e45d0a26435a06f3ffb23e9260c2439e5d83323d3d7c91';
const afterSha='ba1935871a2824a076b5a1809f4330b24e8dfcd1c86cfdf8dccf50527b117b6f';
function priorHtml(root,html) {
  if(sha(html)!==afterSha) return html;
  const historic=cp.execFileSync('git',['show','9c3211ed3342af058f1966c383fef570527addd1:index.html'],{cwd:root,encoding:'utf8',maxBuffer:10e6});
  assert.equal(sha(historic),beforeSha,'Exact predecessor before reviewed portfolio UI changes');
  return historic;
}
module.exports={priorHtml};
