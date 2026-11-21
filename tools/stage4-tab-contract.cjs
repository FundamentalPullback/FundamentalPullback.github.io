// Exact additive UI successor. All report records and financial data remain unchanged.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert/strict');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function priorHtml(root,html){
  html=require('./portfolio-ui-contract.cjs').priorHtml(root,html);
  // Remove only the exact reviewed scanner coverage extension before validating the unchanged Stage 4 predecessor.
  const scanner=JSON.parse(fs.readFileSync(root+'/tools/scanner-nov17-ui-contract.json'));
  if(sha(html)===scanner.afterSha256){
    for(const p of scanner.replacements.slice().reverse()){assert.equal(html.split(p.after).length,2,'Unique reviewed Nov17 scanner UI hunk');html=html.replace(p.after,()=>p.before);}
    assert.equal(sha(html),scanner.beforeSha256,'Exact predecessor before Nov17 scanner UI');
  }
  const c=JSON.parse(fs.readFileSync(root+'/tools/stage4-tab-ui-contract.json'));assert.equal(sha(html),c.afterSha256,'Reviewed Stage4 tab UI');for(const p of c.replacements.slice().reverse()){assert.equal(html.split(p.after).length,2,'Unique reviewed Stage4 UI hunk');html=html.replace(p.after,()=>p.before);}assert.equal(sha(html),c.beforeSha256,'Exact predecessor UI');return html;}
module.exports={priorHtml};
