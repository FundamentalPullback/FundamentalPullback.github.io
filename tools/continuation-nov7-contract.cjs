const fs=require('fs'),assert=require('assert/strict'),crypto=require('crypto');
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
function legacy(root,a){
 if(!a.reports.some(r=>r.id==='A300'))return a;
 const c=JSON.parse(fs.readFileSync(root+'/tools/continuation-nov7-prior.json'));
 for(const [id,h] of Object.entries(c.reportHashes)){const r=a.reports.find(x=>x.id===id);assert(r,'Preserved report '+id);assert.equal(sha(JSON.stringify(r)),h,'Exact historical report '+id);}
 const extra=a.reports.filter(r=>!Object.hasOwn(c.reportHashes,r.id));assert.equal(JSON.stringify(extra.map(r=>r.id)),JSON.stringify(['A300','A301','A302','A303','A304','A305','A306','A307','A308','A309','A310','A311','A312','A313','A314','A315','A316','A317','A318','A319','A320','A321','A322','A323','A324','A325','A326','A327','A328','A329','A330','A331','A332','A333','A334','A335','A336','A337','A338','A339','A340','A341','A342','A343','A344','A345','A346','A347','A348','A349','A350','A351','A352','A353','A354','A355','A356','A357','A358','A359','A360','A361','A362','A363','A364','A365','A366','A367','A368','A369','A370','A371','A372','A373','A374','A375','A376','A377','A378','A379','A380','A381','A382','A383','A384','A385','A386','A387','A388','A389','A390','A391','A392','A393','A394','A395','A396','A397','A398','A399','A400','A401','A402']));
 a.reports=a.reports.filter(r=>Object.hasOwn(c.reportHashes,r.id));a.t.S.lib=a.reports;a.c.window.FP_LIB.reports=a.reports;a.profiles=a.t.profiles();return a;
}
module.exports={legacy};
