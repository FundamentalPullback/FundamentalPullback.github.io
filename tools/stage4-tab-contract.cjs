// Exact additive UI successor. All report records and financial data remain unchanged.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert/strict');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function priorHtml(root,html){const c=JSON.parse(fs.readFileSync(root+'/tools/stage4-tab-ui-contract.json'));assert.equal(sha(html),c.afterSha256,'Reviewed Stage4 tab UI');for(const p of c.replacements.slice().reverse()){assert.equal(html.split(p.after).length,2,'Unique reviewed Stage4 UI hunk');html=html.replace(p.after,()=>p.before);}assert.equal(sha(html),c.beforeSha256,'Exact predecessor UI');return html;}
module.exports={priorHtml};
