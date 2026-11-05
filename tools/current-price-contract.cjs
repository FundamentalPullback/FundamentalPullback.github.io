// Pinned, explicit publication successor. No general allowance for future records.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto');
const sha=b=>crypto.createHash('sha256').update(b).digest('hex');
function validate(root,loaded){
 const c=JSON.parse(fs.readFileSync(path.join(root,'tools/current-price-contract.json')));
 assert.deepEqual(c.ids,['A283','A284','A285']);
 assert.equal(sha(fs.readFileSync(root+'/data/entry-observation-followups.js')),c.observationFollowupSha256,'Exact audited observation registry');
 for(const [file,h] of Object.entries(c.observationSourceHashes))assert.equal(sha(fs.readFileSync(root+'/'+file)),h,'Exact observation source '+file);
 assert.equal(sha(fs.readFileSync(root+'/index.html')),c.indexSha256,'Exact reviewed application successor');
 assert.equal(sha(fs.readFileSync(root+'/data/stock-profiles.js')),c.engineSha256,'Exact separate-review engine');
 assert.equal(sha(fs.readFileSync(root+'/data/lib-current-price-reviews.js')),c.librarySha256,'Exact new source chunk');
 assert.equal(loaded.reports.length,Object.keys(c.historicalReportHashes).length+3,'Only three new records');
 assert.equal(new Set(loaded.reports.map(r=>r.id)).size,loaded.reports.length,'Unique report IDs');
 for(const [id,h] of Object.entries({...c.historicalReportHashes,...c.newReportHashes})){const r=loaded.reports.find(r=>r.id===id);assert(r,'Required '+id);assert.equal(sha(JSON.stringify(r)),h,'Exact historical or newly audited report '+id);}
 return c;
}
function legacy(root,loaded){
 const c=validate(root,loaded);delete loaded.c.window.FP_ENTRY_OBSERVATION_FOLLOWUPS;delete loaded.c.window.FP_MANIFEST.entryObservationFollowupFile;loaded.c.window.FP_MANIFEST.libraryFiles=loaded.c.window.FP_MANIFEST.libraryFiles.filter(f=>f!=='data/entry-observation-followups.js');loaded.reports=loaded.reports.filter(r=>!c.ids.includes(r.id));loaded.t.S.lib=loaded.reports;loaded.profiles=loaded.t.profiles();return loaded;
}
module.exports={validate,legacy};
