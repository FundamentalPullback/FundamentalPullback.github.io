// Execute every immutable public November 9 sales assertion against the current app.
// Only the explicitly dated pre-adoption protection scenario projects management.
// No portfolio or account fixture data is embedded here.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto'),Module=require('module');
const root=path.resolve(__dirname,'..'),filename=path.join(__dirname,'test-sales-nov9.cjs');
const original=fs.readFileSync(filename,'utf8'),contract=JSON.parse(fs.readFileSync(path.join(__dirname,'stage4-nov9-prior.json')));
assert.equal(crypto.createHash('sha256').update(original).digest('hex'),contract.preservedSources['tools/test-sales-nov9.cjs'],'Immutable public sales test; never republish a replacement fixture');
const start='// Protection state remains explicit: proposed JXN level is not a stop.',end='// Unknown fee keeps all net totals unavailable.';
assert.equal(original.split(start).length,2);assert.equal(original.split(end).length,2);assert(original.indexOf(start)<original.indexOf(end));
const projected=original.replace(start,"const stage4CurrentGes=t.S.ges;try{t.S.ges=stage4CurrentGes.filter(r=>r.rep!=='A494');\n"+start).replace(end,"}finally{t.S.ges=stage4CurrentGes;}\n"+end);
const m=new Module(filename,module);m.filename=filename;m.paths=Module._nodeModulePaths(__dirname);m._compile(projected,filename);
console.log('PASS immutable sales suite on current code; only dated pre-adoption protection uses explicit management projection. Current adoption is tested by test-stage4-nov9.cjs.');
