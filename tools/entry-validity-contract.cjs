// Exact reviewed display-only successor. Canonical records and economics are unchanged.
const fs=require('fs'),crypto=require('crypto'),assert=require('assert/strict');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function priorHtml(root,html){html=require('./stage4-tab-contract.cjs').priorHtml(root,html);const c=JSON.parse(fs.readFileSync(root+'/tools/entry-validity-ui-contract.json'));assert.equal(sha(html),c.afterSha256,'Reviewed entry-validity UI');for(const p of c.replacements){assert.equal(html.split(p.after).length,2,'Unique reviewed UI hunk');html=html.replace(p.after,p.before);}assert.equal(sha(html),c.beforeSha256,'Exact predecessor UI');return html;}
module.exports={priorHtml};
