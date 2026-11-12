// Reviewed daily-market refresh: prior history and account configuration stay immutable.
const fs=require('fs'),cp=require('child_process'),assert=require('assert/strict'),path=require('path');
const root=path.resolve(__dirname,'..'),base='36a01fc52c03745d7634ce954e1d224ea36cd4ef';
const parse=s=>JSON.parse(s.toString().slice(s.toString().indexOf('FP.')+3).split('=').slice(1).join('=').trim().replace(/;$/,''));
const old=n=>parse(cp.execFileSync('git',['show',base+':data/'+n+'.js'],{cwd:root}));
const cur=n=>parse(fs.readFileSync(root+'/data/'+n+'.js'));
const h=cur('hist'),o=old('hist');assert.deepEqual(h.slice(0,o.length),o,'Every prior history row exact');assert(h.length>=o.length+1,'Nov10 retained; later verified sessions may append');const nov10=cur('hist')[o.length];assert.equal(nov10[0],'46336,67','Nov10 row retained at original position');
const a=cur('acct'),b=old('acct');assert.equal(a.length,b.length);for(let i=0;i<a.length;i++){assert.equal(a[i][0],b[i][0]);if(a[i][0]!=='SPY actual')assert.deepEqual(a[i].slice(0,3),b[i].slice(0,3),'Nonmarket account fields unchanged');}
const source=JSON.parse(fs.readFileSync(root+'/data/market-closes-2026-11-10.json'));assert.deepEqual(source.sessions['2026-11-10'],{SPY:749.92,ASO:70.39,DOCU:77.66,EXLS:44.30,ULTA:664.41,CTSH:65,JXN:138.01});
for(const [ticker,price] of Object.entries(source.sessions['2026-11-10'])){const col=h[0].indexOf(ticker);assert(col>=0);assert.equal(Number(String(nov10[col+1]).replace(',','.')),price,ticker+' immutable Nov10 close');}
const page=fs.readFileSync(root+'/research/accounting-update.html','utf8'),priorPage=cp.execFileSync('git',['show',base+':research/accounting-update.html'],{cwd:root,encoding:'utf8'});assert.equal(page.replace(/<section id="close-2026-11-(?:10|11)">[\s\S]*?<\/section>/g,''),priorPage,'Prior reconciliation page unchanged');
require('./test-account-close-current.cjs');console.log('PASS Nov10 reviewed close source; all prior history rows and nonmarket account fields immutable.');
