const fs=require('fs'),assert=require('assert/strict'),crypto=require('crypto');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function legacy(root,a){
 if(!a.reports.some(r=>r.id==='A300'))return a;
 const c=JSON.parse(fs.readFileSync(root+'/tools/continuation-nov7-prior.json'));
 for(const [id,h] of Object.entries(c.reportHashes)){const r=a.reports.find(x=>x.id===id);assert(r,'Preserved report '+id);assert.equal(sha(JSON.stringify(r)),h,'Exact historical report '+id);}
 const extra=a.reports.filter(r=>!Object.hasOwn(c.reportHashes,r.id));assert.equal(JSON.stringify(extra.map(r=>r.id)),JSON.stringify(['A300','A301','A302','A303','A304','A305','A306','A307','A308','A309','A310','A311','A312','A313','A314','A315','A316','A317','A318','A319','A320','A321','A322','A323','A324','A325','A326','A327','A328','A329','A330','A331','A332','A333','A334','A335','A336']));
 a.reports=a.reports.filter(r=>Object.hasOwn(c.reportHashes,r.id));a.t.S.lib=a.reports;a.c.window.FP_LIB.reports=a.reports;a.profiles=a.t.profiles();return a;
}
module.exports={legacy};
