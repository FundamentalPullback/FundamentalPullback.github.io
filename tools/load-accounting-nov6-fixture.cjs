// Public, hash-pinned historical inputs. Never used by application code.
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto'),vm=require('vm');
module.exports=function(){
 const raw=fs.readFileSync(path.join(__dirname,'accounting-nov6-fixture.json'));
 assert.equal(crypto.createHash('sha256').update(raw).digest('hex'),'a1981f9b3bc38f859ce833cc5e66c0e3c910fdb96abdbf794a12e6aa71a7f9ff','Historical fixture immutable');
 const f=JSON.parse(raw),c={window:{FP:{}}};c.FP=c.window.FP;vm.createContext(c);
 for(const file of ['data/acct.js','data/hist.js'])vm.runInContext(f.files[file],c);
 return {...c.FP,sourceFiles:f.files};
};
