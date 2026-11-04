// Run: node tools/test-floating-navigation.cjs. Browser geometry/touch QA supplements this suite.
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict'),path=require('node:path');
const html=fs.readFileSync(path.join(__dirname,'../index.html'),'utf8');
assert(html.includes('.profile-navigation .profile-nav-step { position:fixed; z-index:7;'));
assert(html.includes('padding-left:max(84px, calc(env(safe-area-inset-left, 0px) + 72px))'));
assert(html.includes('@media(max-width:899px), (max-height:599px)'));
assert(html.includes('.profile-navigation .profile-nav-step { position:static; transform:none;'));
assert(!html.includes('id="page-scroll"'));assert(!html.includes('body:has(.profile-navigation)::after'));
assert(html.includes('Swipe left for the next stock or right for the previous one.'));
assert(html.includes('Desliza a la izquierda para la siguiente acción'));
assert(html.includes('target.style.scrollMarginTop='));
const events={},state={mobile:true,selection:'',blocked:false,inProfile:true,nav:true,edge:390,horiz:false,disabled:false,href:'#ficha/CTSH?filter=complete&status=decision%3AEn+observaci%C3%B3n&sort=ticker&scans=1'};
const boundary={id:'v-fichas'},target={parentElement:boundary,clientWidth:200,get scrollWidth(){return state.horiz?400:200},closest(q){if(q==='#v-fichas')return state.inProfile?boundary:null;return state.blocked?{}:null;}};
const c={S:{view:'fichas'},window:{matchMedia:()=>({matches:state.mobile}),getSelection:()=>state.selection,get innerWidth(){return state.edge}},document:{getElementById:id=>state.nav?{disabled:state.disabled,getAttribute:()=>state.href}:null,addEventListener:(name,fn,options)=>{events[name]=fn;assert(options.passive);}},getComputedStyle:()=>({overflowX:'auto'}),location:{hash:'original'},Math,String};
const start=html.indexOf('  var profileSwipe=null;'),end=html.indexOf('  document.addEventListener("click", function (e) {',start);vm.runInNewContext(html.slice(start,end),c);
function touch(x,y,id=1){return {clientX:x,clientY:y,identifier:id};}
function gesture({x=300,y=200,dx=-160,dy=10,duration=250,move=true,id=1,otherId=1,multi=false}={}){c.location.hash='original';const a=touch(x,y,id),b=touch(x+dx,y+dy,otherId);events.touchstart({target,timeStamp:100,touches:multi?[a,touch(200,200,2)]:[a]});if(move)events.touchmove({target,timeStamp:200,touches:[b]});events.touchend({target,timeStamp:100+duration,touches:[],changedTouches:[b]});return c.location.hash;}
assert.equal(gesture(),state.href);let requested=[];c.document.getElementById=id=>{requested.push(id);return {disabled:state.disabled,getAttribute:()=>state.href};};gesture({x:80,dx:170});assert.equal(requested.at(-1),'profile-prev');gesture();assert.equal(requested.at(-1),'profile-next');
for(const changes of [{dx:-20},{dx:-160,dy:80},{dx:-80,dy:30},{duration:40},{duration:1200},{x:5},{x:385,dx:-100},{multi:true},{otherId:2}])assert.equal(gesture(changes),'original',JSON.stringify(changes));
for(const [key,value] of [['mobile',false],['blocked',true],['inProfile',false],['selection','selected text'],['horiz',true],['disabled',true]]){const old=state[key];state[key]=value;assert.equal(gesture(),'original',key);state[key]=old;}
c.S.view='revision';assert.equal(gesture(),'original');c.S.view='fichas';
events.touchstart({target,timeStamp:100,touches:[touch(300,200)]});events.touchmove({touches:[touch(290,225)]});events.touchend({timeStamp:300,touches:[],changedTouches:[touch(120,225)]});assert.equal(c.location.hash,'original');
events.touchstart({target,timeStamp:100,touches:[touch(300,200)]});events.touchcancel({});events.touchend({timeStamp:300,touches:[],changedTouches:[touch(120,200)]});assert.equal(c.location.hash,'original');
events.touchstart({target,timeStamp:100,touches:[touch(300,200)]});state.selection='new selection';events.touchend({timeStamp:300,touches:[],changedTouches:[touch(120,200)]});assert.equal(c.location.hash,'original');state.selection='';
for(const href of ['',null,'#revision','javascript:alert(1)']){state.href=href;assert.equal(gesture(),'original');}
console.log('PASS floating/swipe navigation: reserved desktop gutters; compact inline accessible links and ES/EN hint; passive deliberate left/right gestures; exact existing cohort URLs; no vertical/short/diagonal/fast/slow/edge/multitouch/cancel/selection/interactive/horizontal-widget/disabled-boundary navigation; no fixed phone overlay.');

state.href='#ficha/NEXT?filter=complete&scans=5';
for(const change of [()=>c.location.hash='#ficha/DIFFERENT',()=>state.mobile=false,()=>c.S.view='revision']){c.location.hash='original';state.mobile=true;c.S.view='fichas';events.touchstart({target,timeStamp:100,touches:[touch(300,200)]});change();const expected=c.location.hash;events.touchend({timeStamp:300,touches:[],changedTouches:[touch(120,200)]});assert.equal(c.location.hash,expected);}
console.log('PASS in-flight gesture invalidation after route, view or viewport changes.');
