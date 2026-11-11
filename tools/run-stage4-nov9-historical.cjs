// Execute the immutable November 9 Stage 4 assertions with only the validated later management projected out.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto'),Module=require('module');
const root=path.resolve(__dirname,'..'),filename=path.join(__dirname,'test-stage4-nov9.cjs'),original=fs.readFileSync(filename,'utf8'),p=JSON.parse(fs.readFileSync(path.join(__dirname,'stage4-nov10-prior.json')));
assert.equal(crypto.createHash('sha256').update(original).digest('hex'),p.preservedSources['tools/test-stage4-nov9.cjs']);
const needle='const a=m.exports(root),';assert.equal(original.split(needle).length,2);
const projected=original.replace(needle,"const a=require('./stage4-nov10-contract.cjs').legacy(root,m.exports(root)),");
const m=new Module(filename,module);m.filename=filename;m.paths=Module._nodeModulePaths(__dirname);m._compile(projected,filename);
console.log('PASS immutable Nov 9 Stage 4 suite with explicit Nov 10 management-only projection.');
