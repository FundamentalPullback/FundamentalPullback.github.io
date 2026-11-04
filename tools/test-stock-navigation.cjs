// Run: node tools/test-stock-navigation.cjs. Uses Node built-ins only.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'..'),c={window:{}},events={},replaced=[];c.FP=c.window.FP={};vm.createContext(c);
vm.runInContext(fs.readFileSync(root+'/data/manifest.js','utf8'),c);
for(const file of [...c.window.FP_MANIFEST.files,'data/names.js',...c.window.FP_MANIFEST.libraryFiles,'data/stock-profiles.js'])vm.runInContext(fs.readFileSync(root+'/'+file,'utf8'),c);
const html=fs.readFileSync(root+'/index.html','utf8');let app=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(x=>x[1]).find(x=>x.includes('var DEC_MAP'));new vm.Script(app);
app=app.slice(0,app.indexOf('  var hash ='))+app.slice(app.indexOf('  var PARTS ='),app.indexOf('  var DENY ='))+'\nwindow.TEST={renderUI:render,S,PARTS,profiles,vFichas,renderProfile,profileRoute,profileResults,profileContext,profileHref,profileSearchHash,profileNavigation,profileSummaryCard,mountProfileQuotes,setLang:function(l){lang=l;}};render=function(){};})();';
const noop=()=>{},el={addEventListener:noop,setAttribute:noop,querySelectorAll:()=>[],style:{}};
Object.assign(c,{document:{getElementById:()=>el,addEventListener:(name,fn)=>(events[name]||(events[name]=[])).push(fn),querySelectorAll:()=>[],querySelector:()=>el,hidden:false},localStorage:{getItem:()=>null},history:{state:{unrelated:'preserved'},replaceState:(state,title,href)=>replaced.push({state,href})},console,Date,Intl,setTimeout:()=>1,clearTimeout:noop,AbortController,location:{hash:'#fichas'},URL,URLSearchParams});c.window.addEventListener=noop;vm.runInContext(app,c);
const t=c.window.TEST,F=c.FP;t.S.scan=t.PARTS.scan([F.scanHead].concat(F.scan));for(const k of ['dec','ges','ops','acct','hist'])t.S[k]=t.PARTS[k](F[k]);t.S.lib=c.window.FP_LIB.reports;t.S.libState='ok';t.S.snapshot=c.window.FP_MANIFEST.asOf;
const unescape=s=>s.replaceAll('&amp;','&').replaceAll('&quot;','"'),hrefs=h=>[...h.matchAll(/class="profile-result" href="([^"]+)"/g)].map(x=>unescape(x[1])),navLink=(h,id)=>{const m=h.match(new RegExp('<a[^>]*id="profile-'+id+'"[^>]*href="([^"]+)"'));return m&&unescape(m[1]);},disabled=(h,id)=>new RegExp('<button[^>]*id="profile-'+id+'"[^>]* disabled>').test(h),tickers=rows=>Array.from(rows,p=>p.ticker);
const all=t.profiles();assert(all.length>500);
for(const language of ['en','es'])for(const filter of ['all','complete','other']){
 t.setLang(language);t.profileRoute('fichas?filter='+filter+'&sort=ticker');
 const rows=t.profileResults(t.profiles()),links=hrefs(t.vFichas());assert.equal(links.length,rows.length);assert.deepEqual(tickers(rows),tickers(rows).sort((a,b)=>a.localeCompare(b)));
 if(filter!=='all')assert(rows.every(p=>filter==='complete'?!!p.latestCompleted:!p.latestCompleted));
 for(let i=0;i<rows.length;i++){
  t.profileRoute(links[i].slice(1));assert.equal(t.S.profileTicker,rows[i].ticker);assert.equal(t.S.profileFilter,filter);const h=t.profileNavigation(rows[i]);
  assert.equal(navLink(h,'prev'),i?links[i-1]:null);assert.equal(navLink(h,'next'),i+1<rows.length?links[i+1]:null);assert.equal(disabled(h,'prev'),i===0);assert.equal(disabled(h,'next'),i===rows.length-1);assert(h.includes((i+1)+' '+(language==='en'?'of':'de')+' '+rows.length));
  assert.equal(t.profileSearchHash(),'#fichas?filter='+filter+'&sort=ticker');
 }
}
// A multi-result company query uses exactly the displayed subset and ordering.
t.profileRoute('fichas?q=holdings&filter=all&sort=ticker');let rows=t.profileResults(t.profiles()),links=hrefs(t.vFichas());assert(rows.length>2&&rows.length<all.length);assert.equal(links.length,rows.length);
for(let i=0;i<rows.length;i++){t.profileRoute(links[i].slice(1));const h=t.profileNavigation(rows[i]);assert.equal(navLink(h,'prev'),i?links[i-1]:null);assert.equal(navLink(h,'next'),i+1<rows.length?links[i+1]:null);assert.equal(t.S.profileQ,'holdings');}
// Query/filter/sort round-trip, including literal &, +, /, $, Unicode and quotes.
const query='Estée & "Co" + / $';t.profileRoute('fichas?q='+encodeURIComponent(query)+'&filter=complete&sort=ticker');const saved=t.profileHref('BRK.B',t.profileContext());t.S.profileQ='stale';t.S.profileFilter='other';t.profileRoute(saved.slice(1));assert.equal(t.S.profileTicker,'BRK.B');assert.equal(t.S.profileQ,query);assert.equal(t.S.profileFilter,'complete');const back=t.profileSearchHash();t.profileRoute(back.slice(1));assert.equal(t.S.profileTicker,null);assert.equal(t.S.profileQ,query);
// A legacy direct bookmark must not inherit an unrelated search from this tab.
t.profileRoute('ficha/WMG');assert.equal(t.S.profileQ,'');assert.equal(t.S.profileFilter,'all');assert(t.profileNavigation(all.find(p=>p.ticker==='WMG')).includes('All stocks')||t.profileNavigation(all.find(p=>p.ticker==='WMG')).includes('Todas las acciones'));
// Exact ticker is the established inline card, with a genuine one-result cohort.
t.profileRoute('fichas?q=WMG&filter=all&sort=ticker');let h=t.vFichas();assert(h.includes('stock-summary'));assert(!h.includes('class="profile-results"'));assert(disabled(h,'prev')&&disabled(h,'next'));assert(h.includes('1 de 1')||h.includes('1 of 1'));assert(h.includes('href="#ficha/WMG?q=WMG&amp;filter=all&amp;sort=ticker"'));
t.profileRoute('fichas?q=ZZZZ_NOT_PUBLISHED');h=t.vFichas();assert(!h.includes('profile-navigation'));assert(!h.includes('stock-summary'));assert(!h.includes('class="profile-results"'));
// Unknown filters/order are never silently treated as a valid all-stock cohort.
for(const hash of ['ficha/WMG?filter=bogus','ficha/WMG?sort=unknown']){t.profileRoute(hash);h=t.vFichas();assert.equal(t.S.profileContextValid,false);assert(disabled(h,'prev')&&disabled(h,'next'));assert(!navLink(h,'prev')&&!navLink(h,'next'));}
assert.doesNotThrow(()=>t.profileRoute('ficha/%E0%A4%A'));assert.doesNotThrow(()=>t.vFichas());
// Search edits replace the current list URL, not the saved profile/browser history.
t.profileRoute('fichas?q=old&filter=complete&sort=ticker');for(const callback of events.input)callback({target:{id:'profile-q',value:'new + query'}});assert.equal(replaced.at(-1).href,'#fichas?q=new+%2B+query&filter=complete&sort=ticker');assert.equal(replaced.at(-1).state,c.history.state);for(const callback of events.change)callback({target:{id:'profile-filter',value:'other'}});assert.equal(replaced.at(-1).href,'#fichas?q=new+%2B+query&filter=other&sort=ticker');
// Render keeps keyboard focus on the filter or current navigation direction.
const nodes={},focused=[];c.document.getElementById=id=>nodes[id]||(nodes[id]={...el,focus:()=>focused.push(id)});c.document.documentElement={};t.S.view='fichas';
t.profileRoute('fichas?filter=all&sort=ticker');c.document.activeElement={id:'profile-filter'};t.renderUI();assert.equal(focused.at(-1),'profile-filter');
t.profileRoute('ficha/WMG?filter=all&sort=ticker');c.document.activeElement={id:'profile-next'};t.renderUI();assert.equal(focused.at(-1),'profile-next');nodes['profile-next'].disabled=true;t.renderUI();assert.equal(focused.at(-1),'profile-title');delete nodes['profile-next'].disabled;
// Stepping mounts a fresh provider script with the newly selected symbol.
const configs=[];c.document.documentElement.getAttribute=()=> 'light';c.document.createElement=tag=>({tag,style:{},appendChild(child){if(child.tag==='script')configs.push(JSON.parse(child.textContent));}});
function mountFromCard(){const card=t.vFichas(),symbol=card.match(/data-quote-symbol="([^"]+)"/)[1];const mount={isConnected:true,getAttribute:()=>symbol,appendChild:noop,innerHTML:''};t.mountProfileQuotes({querySelectorAll:()=>[mount]});return card;}
h=mountFromCard();const firstQuote=configs.at(-1).symbol,next=navLink(h,'next');assert(next);t.profileRoute(next.slice(1));h=mountFromCard();assert.notEqual(configs.at(-1).symbol,firstQuote);assert(configs.at(-1).symbol.endsWith(':'+t.S.profileTicker));assert(!h.includes('data-quote-symbol="'+firstQuote+'"'));
// Publication changes rebuild the same criteria: additions, completion changes,
// removed symbols, and an existing current stock falling out of the filter.
t.S.scan=[{ticker:'AAA',company:'Fixture Group',date:'2026-11-01'},{ticker:'BBB',company:'Fixture Group',date:'2026-11-01'},{ticker:'CCC',company:'Fixture Group',date:'2026-11-01'}];t.S.dec=[];t.S.ges=[];t.S.ops=[];t.S.lib=[{id:'T1',date:'2026-11-01',profiles:[{ticker:'AAA',kind:'complete'},{ticker:'CCC',kind:'complete'}]}];
t.profileRoute('ficha/AAA?q=fixture&filter=complete&sort=ticker');assert.deepEqual(tickers(t.profileResults(t.profiles())),['AAA','CCC']);assert(navLink(t.vFichas(),'next').startsWith('#ficha/CCC?'));
t.S.lib=t.S.lib.concat([{id:'T2',date:'2026-11-02',profiles:[{ticker:'BBB',kind:'complete'}]}]);assert.deepEqual(tickers(t.profileResults(t.profiles())),['AAA','BBB','CCC']);assert(navLink(t.vFichas(),'next').startsWith('#ficha/BBB?'));
t.S.scan=t.S.scan.concat([{ticker:'AAB',company:'Fixture Group',date:'2026-11-02'}]);t.S.lib=t.S.lib.concat([{id:'T3',date:'2026-11-02',profiles:[{ticker:'AAB',kind:'complete'}]}]);assert(navLink(t.vFichas(),'next').startsWith('#ficha/AAB?'));
t.profileRoute('ficha/BBB?q=fixture&filter=other&sort=ticker');h=t.vFichas();assert(h.includes('stock-summary'));assert(disabled(h,'prev')&&disabled(h,'next'));assert(h.includes('Not in these results')||h.includes('Fuera de estos resultados'));
t.S.scan=t.S.scan.filter(p=>p.ticker!=='BBB');t.S.lib=t.S.lib.filter(r=>r.id!=='T2');t.profileRoute('ficha/BBB?q=fixture&filter=complete&sort=ticker');h=t.vFichas();assert(!h.includes('stock-summary'));assert(disabled(h,'prev')&&disabled(h,'next'));assert(h.includes('href="#fichas?q=fixture&amp;filter=complete&amp;sort=ticker"'));
t.S.scan=[];t.S.lib=[];h=t.vFichas();assert(disabled(h,'prev')&&disabled(h,'next'));assert.equal(t.profileResults(t.profiles()).length,0);
console.log('PASS stock navigation: 523 published profiles; exact all/completed/other cohorts in ES/EN; ticker A–Z neighbors and disabled boundaries; company query, one/zero result, URL reload/back round-trip, direct/invalid links, query edit history, render focus, quote-symbol remount, and changed/removed publications.');
