// Load published source records without a browser or network. Shared publication checks.
const fs=require('fs'),vm=require('vm'),path=require('path');
module.exports=function(root=path.resolve(__dirname,'..')) {
 const c={window:{}};c.FP=c.window.FP={};vm.createContext(c);vm.runInContext(fs.readFileSync(root+'/data/manifest.js','utf8'),c);
 for(const f of [...c.window.FP_MANIFEST.files,'data/names.js',...c.window.FP_MANIFEST.libraryFiles,'data/stock-profiles.js'])vm.runInContext(fs.readFileSync(root+'/'+f,'utf8'),c);
 const html=fs.readFileSync(root+'/index.html','utf8');let app=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('var DEC_MAP'));
 app=app.slice(0,app.indexOf('  var hash ='))+app.slice(app.indexOf('  var PARTS ='),app.indexOf('  var DENY ='))+'\nwindow.TEST={S,PARTS,profiles,profileBalancePanel,profileSummaryCard,profileResults,profileRoute,renderProfile,setLang:function(l){lang=l;}};render=function(){};})();';
 const noop=()=>{},el={addEventListener:noop,setAttribute:noop,querySelectorAll:()=>[],style:{}};
 Object.assign(c,{document:{getElementById:()=>el,addEventListener:noop,querySelectorAll:()=>[],querySelector:()=>el,hidden:false},localStorage:{getItem:()=>null},console,Date,Intl,setTimeout,clearTimeout,AbortController,location:{hash:'#fichas'},URL,URLSearchParams});c.window.addEventListener=noop;vm.runInContext(app,c);
 const t=c.window.TEST,F=c.FP;t.S.scan=t.PARTS.scan([F.scanHead].concat(F.scan));for(const k of ['dec','ges','ops','acct','hist'])t.S[k]=t.PARTS[k](F[k]);t.S.lib=c.window.FP_LIB.reports;t.S.libState='ok';t.S.snapshot=c.window.FP_MANIFEST.asOf;
 return {c,t,engine:c.window.FP_PROFILE_ENGINE,profiles:t.profiles(),reports:t.S.lib,html};
};
