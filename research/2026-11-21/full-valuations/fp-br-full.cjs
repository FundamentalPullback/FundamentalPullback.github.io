const start={recurring:4983.6,event:301.7,distribution:2270.7,stock:181.41,shares:114,carryingDebt:3347.1,reportedCash:284.1,regulatedCash:76.1,excessCash:150,otherAssets:0,acquisitionPayables:59.3,ebit:1285.3,stockComp:101.6};
const scen={
bear:{wacc:.097,tax:.245,rg:[.05,.045,.04,.035,.035],eg:.005,dg:.01,margin:[.167,.167,.169,.17,.17],termMargin:.169,tg:.019,roic:.125,physical:.012,software:.009,conversion:.024,ip:.027,wc:.12},
base:{wacc:.084,tax:.23,rg:[.074,.07,.065,.062,.06],eg:.025,dg:.024,margin:[.174,.179,.184,.187,.19],termMargin:.188,tg:.025,roic:.17,physical:.01,software:.007,conversion:.021,ip:.026,wc:.09},
bull:{wacc:.076,tax:.22,rg:[.088,.085,.08,.075,.07],eg:.045,dg:.032,margin:[.178,.187,.196,.202,.207],termMargin:.205,tg:.029,roic:.22,physical:.009,software:.007,conversion:.019,ip:.024,wc:.06}
};
const total=s=>s.recurring+s.event+s.distribution;
const interp=(a,b,w)=>a+(b-a)*w;
const terminalRatio=(p)=>p.termMargin*(1-p.tax)*p.tg/p.roic;
// 5y forecast; fade revenues and margins through year 10, and phase extra strategic investment to steady state.
// Recurring growth, event growth and distribution growth all fade to same terminal growth for stable mix.
function model(p,startInput=start) {
 let out=[], prev={...startInput,revenue:total(startInput)};
 for(let y=1;y<=10;y++){
  const w=y<=5?0:(y-5)/5;
  const rg=y<=5?p.rg[y-1]:interp(p.rg[4],p.tg,w), eg=interp(p.eg,p.tg,w),dg=interp(p.dg,p.tg,w);
  const recurring=prev.recurring*(1+rg), event=prev.event*(1+eg), distribution=prev.distribution*(1+dg);
  const revenue=recurring+event+distribution, growth=revenue/prev.revenue-1;
  const margin=y<=5?p.margin[y-1]:interp(p.margin[4],p.termMargin,w), ebit=margin*revenue, nopat=ebit*(1-p.tax);
  const da=.0668*revenue, physical=p.physical*revenue, software=p.software*revenue, conversion=p.conversion*revenue, ip=p.ip*revenue;
  const wc=p.wc*(revenue-prev.revenue);
  const rawReinvestment=physical+software+conversion+ip+wc-da;
  const capitalFloor=Math.max(0,-rawReinvestment);
  const targetReinvestmentRate=terminalRatio(p);
  const fadeSpend=w*(targetReinvestmentRate*revenue-(rawReinvestment+capitalFloor));
  const reinvestment=rawReinvestment+capitalFloor+fadeSpend, fcff=nopat-reinvestment, pv=fcff/(1+p.wacc)**y;
  prev={year:y,recurring,event,distribution,revenue,growth,margin,ebit,nopat,da,physical,software,conversion,ip,wc,rawReinvestment,capitalFloor,fadeSpend,reinvestment,fcff,pv};
  out.push(prev);
 }
 const termNopat=prev.revenue*(1+p.tg)*p.termMargin*(1-p.tax), termReinvestment=termNopat*p.tg/p.roic, terminalFCFF=termNopat-termReinvestment;
 const tv=terminalFCFF/(p.wacc-p.tg), pvTV=tv/(1+p.wacc)**10, pvFCFF=out.reduce((s,x)=>s+x.pv,0);
 const ev=pvTV+pvFCFF, equity=ev-startInput.carryingDebt-startInput.acquisitionPayables+startInput.excessCash+startInput.otherAssets, value=equity/startInput.shares;
 return {value, upside:value/startInput.stock-1, mos20:value*.8, ev,equity,pvTV,pvFCFF,termNopat,termReinvestment,terminalFCFF,tv,termShare:pvTV/ev,years:out};
}
function solve(f,target){
 let a=-.5,b=.5;const increasing=f(b)>f(a);
 for(let i=0;i<80;i++){let m=(a+b)/2; if((f(m)<target)===increasing)a=m;else b=m;}
 return (a+b)/2;
}
const base=scen.base;
const currentGrowthShift=solve(h=>model({...base,rg:base.rg.map(x=>x+h)}).value,start.stock);
const currentMarginShift=solve(h=>model({...base,margin:base.margin.map(x=>x+h),termMargin:base.termMargin+h}).value,start.stock);
function rootOn(f,target,a,b){const inc=f(b)>f(a); for(let i=0;i<80;i++){let m=(a+b)/2;if((f(m)<target)===inc)a=m;else b=m;}return(a+b)/2;}
const waccImplied=rootOn(w=>model({...base,wacc:w}).value,start.stock,.04,.2);
const safetyShift=solve(h=>model({...base,rg:base.rg.map(x=>x+h)}).value,start.stock/.8);
const results=Object.fromEntries(Object.entries(scen).map(([k,p])=>[k,model(p)]));
const sensitivity=Object.fromEntries([.074,.079,.084,.089,.094].map(wacc=>[wacc,Object.fromEntries([.02,.025,.03].map(tg=>[tg,model({...base,wacc,tg}).value]))]));
const summary={start,scen,results,sensitivity,reverse:{price:start.stock,mktCap:start.shares*start.stock,impliedEV:start.stock*start.shares+start.carryingDebt+start.acquisitionPayables-start.excessCash,growthShift:currentGrowthShift,impliedRecurringGrowth:base.rg.map(x=>x+currentGrowthShift),marginShift:currentMarginShift,impliedYear5Margin:base.margin[4]+currentMarginShift,impliedTerminalMargin:base.termMargin+currentMarginShift,waccImplied,safetyShift,safetyRequiredValue:start.stock/.8}};
console.log(JSON.stringify(summary,null,2));
