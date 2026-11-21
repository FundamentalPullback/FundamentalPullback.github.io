'use strict';
const {price,book,scenarios}=require('./fp-axs-full.json');
function calculate(p,{startBook=p.book,re=p.re,term=p.term,year1ROE}={}){
  if(re<=p.g || term<p.g)throw new Error('Terminal growth/discount not coherent');
  const combined=p.attr+p.cat+p.res;
  const uw=p.earned*(1-combined);
  const preTax=uw+p.invest+p.other-p.corp-p.interest-p.amort;
  const netCommon=preTax*(1-p.tax)-p.pref;
  const openingROE=year1ROE??netCommon/book.reportedCommonEquityBn;
  let b=startBook, pvDistributions=0,pvResidual=0;
  const path=[0,...p.fade].map((fade,i)=>{
    const roe=openingROE+(term-openingROE)*fade;
    const earnings=roe*b, payout=p.payout*earnings, ri=(roe-re)*b, year=i+1,beginning=b;
    b+=earnings-payout;
    pvDistributions+=payout/(1+re)**year;
    pvResidual+=ri/(1+re)**year;
    return {year,roe,beginning,earnings,payout,ri,ending:b};
  });
  const fv=pvDistributions+b*(term-p.g)/(re-p.g)/(1+re)**5;
  const riFV=startBook+pvResidual+b*(term-re)/(re-p.g)/(1+re)**5;
  if(Math.abs(fv-riFV)>1e-9)throw new Error('Dividend and RI discrepancy');
  return {combined,uw,preTax,netCommon,openingROE,path,fv,riFV,terminalPayout:1-p.g/term};
}
function findROE(p, target=price){let a=Math.max(p.g,.04),b=.25; for(let i=0;i<70;i++){const m=(a+b)/2;if(calculate(p,{term:m}).fv<target)a=m;else b=m;}return b;}
if(require.main===module){console.log(JSON.stringify(scenarios.map(p=>({key:p.key,...calculate(p),impliedTerminalROE:findROE(p),exAOCISensitivity:calculate(p,{startBook:book.exAOCI}).fv})),null,2));}
module.exports={calculate,findROE};

