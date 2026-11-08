/* Search is derived from the published records, never from a separate ticker snapshot.
   Reports may declare profiles:[{ticker,kind:'complete'|'review'|'partial'|'management',completedAt}].
   This optional metadata is useful for standalone reports with no Decisiones row. */
(function (root) {
  'use strict';
  function day(v) {
    var s = String(v || '').trim(), m = /^(\d{4}-\d{2}-\d{2})(?:$|[ T])/.exec(s);
    if (!m) return null;
    var d = new Date(m[1] + 'T00:00:00Z');
    return isFinite(d.getTime()) && d.toISOString().slice(0,10) === m[1] ? m[1] : null;
  }
  function ticker(v) { return String(v || '').trim().toUpperCase(); }
  function norm(v) { return String(v || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,' ').trim(); }
  function completed(depth) { return /^Stage 3 completo(?:\s|$)/i.test(depth || '') || /^Stage 3 revisado(?:\s|$)/i.test(depth || ''); }
  function cmp(a,b) { return String(b.date || '').localeCompare(String(a.date || '')) || String(b.id || '').localeCompare(String(a.id || ''),undefined,{numeric:true}); }
  function isProspectiveStudy(report,meta) {
    return !!(report&&meta&&report.schema==='fp.prospective-stage35.v1'&&report.type==='prospective-stage35-study'&&meta.kind==='prospective'&&ticker(meta.ticker)&&meta.historicalModelReference&&meta.stage3Complete===false&&meta.latestCompletedEligible===false&&meta.stage35Complete===false&&meta.entryApproved===false&&meta.approvedQuantity===0&&meta.signal===null&&meta.entryPrice===null&&meta.quantity===null&&meta.maximumConditioned===null&&meta.operativeStop===null&&!meta.valuation);
  }
  // Dated price reviews do not recertify or supersede their preserved valuation.
  function isCurrentPriceReview(report,meta) {
    var q=meta&&meta.contextQuote;
    return !!(report&&meta&&report.schema==='fp.current-price-review.v1'&&report.type==='current-price-review'&&meta.kind==='current-price-review'&&ticker(meta.ticker)&&meta.historicalModelReference&&meta.valuationChanged===false&&meta.stage3Complete===false&&meta.latestCompletedEligible===false&&meta.stage35Complete===false&&meta.entryApproved===false&&meta.approvedQuantity===0&&meta.signal===null&&meta.entryPrice===null&&meta.quantity===null&&meta.maximumConditioned===null&&meta.operativeStop===null&&!meta.valuation&&q&&q.type==='dated-intraday-not-executable'&&typeof q.price==='number'&&isFinite(q.price)&&q.price>0&&typeof q.at==='string'&&isFinite(Date.parse(q.at))&&day(q.at)===day(report.date)&&typeof meta.summary==='string'&&meta.summary.trim()&&typeof meta.summaryEn==='string'&&meta.summaryEn.trim());
  }
  function build(data) {
    var by = Object.create(null), reports = data.reports || [], reportBy = Object.create(null);
    function get(tk, name) {
      tk = ticker(tk); if (!/^[A-Z0-9][A-Z0-9.-]{0,11}$/.test(tk)) return null;
      var p = by[tk] || (by[tk] = {ticker:tk,company:'',scans:[],decisions:[],management:[],reports:[],completed:[],analyses:[],mentions:[]});
      if (name && (!p.company || String(name).length > p.company.length)) p.company = String(name);
      if ((data.names || {})[tk]) p.company = data.names[tk];
      return p;
    }
    reports.forEach(function(r) { reportBy[r.id] = r; });
    (data.scans || []).forEach(function(r) { var p=get(r.ticker,r.company); if(p) p.scans.push(r); });
    (data.decisions || []).forEach(function(r) { var p=get(r.ticker,r.company); if(p) p.decisions.push(r); });
    (data.management || []).forEach(function(r) { var p=get(r.ticker); if(p) p.management.push(r); });
    (data.operations || []).forEach(function(r) { get(r.ticker); });
    function addReport(p,id,relation) {
      var r=reportBy[id]; if (!p || !r) return;
      var old=p.reports.find(function(x){return x.id===id;});
      if (old) { if(relation==='source') old.relation=relation; return; }
      p.reports.push({id:id,report:r,date:day(r.date),relation:relation});
    }
    function addComplete(p,r,report,id,date,kind,dateSource) {
      var old=p.completed.find(function(x){return x.id===id && x.date===date;});
      if(!old) p.completed.push({id:id,date:date,row:r||null,report:report||null,kind:kind,dateSource:dateSource});
    }
    // Audited legacy rows carried old models into newer daily lists. These source
    // annotations correct provenance only; they do not rewrite any decisions.
    var carried={ 'J|A098':'A080', 'TTEK|A098':'A080', 'WDAY|A098':'A058' };
    var completionDates={A058:'2026-10-17',A064:'2026-10-17'};
    Object.keys(by).forEach(function(tk) {
      var p=by[tk];
      p.decisions.forEach(function(r,i) {
        addReport(p,r.rep,'source'); addReport(p,r.vrep,'source');
        var extracted=String(r.calc||'').match(/\b[Ii]nforme\s+(A\d{2,4})\b/);
        if(extracted) addReport(p,extracted[1],'source');
        var explicit=(reportBy[r.rep] && Array.isArray(reportBy[r.rep].profiles)) ? reportBy[r.rep].profiles.find(function(m){return ticker(m.ticker)===tk;}) : null;
        var id=(explicit && r.rep) || r.vrep || (extracted && extracted[1]) || carried[tk+'|'+r.rep] || r.rep || '';
        var report=reportBy[id], isFull=explicit ? (explicit.kind==='complete'||explicit.kind==='review') : completed(r.depth), kind=(explicit&&explicit.label)||r.depth;
        if(id==='A037') isFull=false; // This source explicitly withdraws retrospective full certification.
        if(id==='A064') kind='Revisión de decisión completada · certificación incompleta';
        var vd=day(r.vdate), rd=report && day(report.date);
        var date=(explicit && day(explicit.completedAt)) || completionDates[id] || vd || rd || (!report ? day(r.adate) : null);
        if(/^Stage 3 (?:completo|revisado|rápido|bloqueado)(?:\s|$)/i.test(r.depth||'')) {
          if(explicit && explicit.kind!=='management' || !report || report.cat==='Selección y valoración' || id==='A058') {
            if(!p.analyses.some(function(x){return x.id===(id||'review-'+i)&&x.date===date;}))p.analyses.push({id:id||'review-'+i,date:date,row:r,report:report||null,kind:kind,isComplete:isFull});
          }
        }
        if(!isFull) return;
        if(report && /^(Gestión de posiciones|Ampliaciones|Entrada y seguimiento)$/.test(report.cat) && !r.vrep && !extracted && id!=='A058' && !explicit) return;
        addComplete(p,r,report,id || 'row-'+i,date,kind,completionDates[id]?'explicit':(vd?'valuation':(rd?'report':(!report&&date?'decision':'unknown'))));
      });
      p.management.forEach(function(r) { addReport(p,r.rep,'management'); });
    });
    // Migration annotation for a verified standalone report absent from Decisiones.
    // Future reports can carry the same structured profiles metadata themselves.
    var legacy={A036:[{ticker:'GOOG',kind:'complete',completedAt:'2026-10-13'}],A122:[{ticker:'FA',kind:'review',completedAt:'2026-10-30',label:'Revisión completada · modelo anterior conservado'},{ticker:'P',kind:'review',completedAt:'2026-10-30',label:'Revisión completada · modelo anterior conservado'},{ticker:'ACN',kind:'partial',completedAt:'2026-10-30',label:'Revisión de evidencia · modelo anterior conservado'}],A146:[{ticker:'NTNX',kind:'complete',completedAt:'2026-11-03'}]};
    reports.forEach(function(r) {
      var entries=Array.isArray(r.profiles)?r.profiles:(legacy[r.id]||[]);
      entries.forEach(function(meta) {
        var p=get(meta.ticker,meta.company); if(!p)return;
        addReport(p,r.id,meta.kind==='management'?'management':'source');
        if(meta.kind==='complete'||meta.kind==='review') addComplete(p,null,r,r.id,day(meta.completedAt)||day(r.date),meta.label||'standalone',day(meta.completedAt)?'explicit':'report');
        // Prospective entry studies are separate from fundamental analysis and completion.
        if(meta.kind!=='management'&&!isProspectiveStudy(r,meta)&&!isCurrentPriceReview(r,meta)) p.analyses.push({id:r.id,date:day(meta.completedAt)||day(r.date),row:null,report:r,kind:meta.label||'standalone',isComplete:meta.kind==='complete'||meta.kind==='review'});
      });
      // A ticker explicitly written in a title is a subject link, never proof of completion.
      var titleTokens=String(r.title||'').match(/\b[A-Z][A-Z0-9.-]{0,10}\b/g)||[];
      titleTokens.forEach(function(tk) { if(by[tk] && (tk.length>1 || new RegExp('(?:^|\\()'+tk+'(?:\\)|\\s*[—·:])').test(r.title))) addReport(by[tk],r.id,'subject'); });
    });
    // Audited issuer-only provenance correction. Original library and decision records
    // remain untouched. A037 withdraws A036 price ceilings, not historical delivery.
    var withdrawal=reportBy.A037;
    if(withdrawal && String(withdrawal.text||'').indexOf('Quedan retiradas.')>=0 && String(withdrawal.text||'').indexOf('no constituye aprobación de compra ni certificación retrospectiva de Stage 3 completo')>=0) {
      ['GOOG','GOOGL'].forEach(function(tk) {
        var p=get(tk); if(!p)return;
        p.issuerResearch={schema:'fp.issuer-research-provenance.v1',appliedOn:'2026-11-08',issuerKey:'CIK0001652044',issuer:'Alphabet Inc.',shareClass:tk==='GOOG'?'C':'A',scope:'historical-issuer-research-only',statusAsOf:'2026-11-08',appliesToReportIds:['A036','A037','A057'],historicalWorkDelivered:true,currentStage3Certified:false,latestCompletedEligible:false,approvedValue:null,approvedEntry:null,entryApproved:false,priceCeilingsWithdrawnBy:'A037',reports:[]};
        ['A036','A037','A057'].forEach(function(id) {
          var report=reportBy[id];if(!report)return;
          addReport(p,id,'issuer-reference');
          p.issuerResearch.reports.push({id:id,historicalWorkDelivered:true,currentStage3Certified:false,referenceOnly:id==='A057'});
          // Override only the audited historical sources, never later research.
          p.completed=p.completed.filter(function(x){return x.id!==id;});
          var prior=p.analyses.find(function(x){return x.id===id;});
          p.analyses=p.analyses.filter(function(x){return x.id!==id;});
          if(id!=='A057')p.analyses.push({id:id,date:day(report.date),row:prior&&prior.row||null,report:report,kind:id==='A037'?'Revisión parcial de valoración; sin certificación Stage 3':'Investigación histórica parcial; límites retirados por A037',isComplete:false,scope:'issuer-research-only',historicalWorkDelivered:true,currentStage3Certified:false});
        });
      });
    }
    // Mentions are searchable source material, explicitly separate from subject analysis.
    reports.forEach(function(r) {
      var seen=Object.create(null), tokens=String(r.text||'').match(/\b[A-Z][A-Z0-9.-]{0,10}\b/g)||[];
      tokens.forEach(function(tk) { if(by[tk]&&!seen[tk]) { seen[tk]=true; if(!by[tk].reports.some(function(x){return x.id===r.id;})) by[tk].mentions.push({id:r.id,date:day(r.date),report:r}); } });
    });
    return Object.keys(by).map(function(tk) {
      var p=by[tk], dates=Array.from(new Set(p.scans.map(function(r){return day(r.date);}).filter(Boolean))).sort();
      p.scanDates=dates; p.firstScan=dates[0]||null; p.lastScan=dates[dates.length-1]||null;
      p.completed.sort(cmp); p.latestCompleted=p.completed.find(function(x){return x.date;})||p.completed[0]||null;
      p.completed.forEach(function(x) { if(!p.analyses.some(function(y){return y.id===x.id && y.date===x.date;}))p.analyses.push(Object.assign({isComplete:true},x)); });
      p.analyses.sort(cmp); p.latestAnalysis=p.analyses.find(function(x){return x.date;})||p.analyses[0]||null;
      p.reports.sort(cmp); p.mentions.sort(cmp);
      p.decisions.sort(function(a,b){return String(day(b.adate)||'').localeCompare(String(day(a.adate)||''))||String(day(b.date)||'').localeCompare(String(day(a.date)||''));});
      p.latestReview=p.decisions[0]||null;
      p.management.sort(function(a,b){return String(day(b.date)||'').localeCompare(String(day(a.date)||''));});
      p.latestManagement=p.management[0]||null;
      p.hasResearch=!!p.decisions.length || p.reports.some(function(x){return (x.relation==='source'||x.relation==='issuer-reference') && x.report.cat==='Selección y valoración';});
      p.search=norm(tk+' '+p.company);
      return p;
    }).sort(function(a,b){return a.ticker.localeCompare(b.ticker);});
  }
  function search(profiles,q) {
    var words=norm(String(q||'').replace(/^\$/,'')).split(' ').filter(Boolean), exact=ticker(q).replace(/^\$/,'');
    var exactProfile=profiles.find(function(p){return p.ticker===exact;});
    if(exactProfile)return [exactProfile];
    return profiles.filter(function(p){return words.every(function(w){return p.search.indexOf(w)>=0;});}).sort(function(a,b){return (b.ticker===exact?1:0)-(a.ticker===exact?1:0)||a.ticker.localeCompare(b.ticker);});
  }

  // Pros/cons are evidence selections, never inferred from price, status or word sentiment.
  // Fingerprints are for change detection, not authentication. Every item also has an exact
  // evidence span in the same report. A correction invalidates the whole migrated summary.
  function balanceFingerprint(text) {
    text=String(text||''); var h=2166136261;
    for(var i=0;i<text.length;i++){h^=text.charCodeAt(i);h=Math.imul(h,16777619);}
    return text.length+':'+(h>>>0).toString(16);
  }
  function balanceItems(items,report) {
    if(!Array.isArray(items)||items.length>3)return null;
    var out=[];
    for(var i=0;i<items.length;i++) {
      var x=items[i],text=x&&String(x.text||'').trim(),en=x&&String(x.textEn||'').trim(),ev=x&&String(x.evidence||'');
      if(!x||!text||text.length>320||ev.length<15||String(report.text||'').indexOf(ev)<0)return null;
      if(en&&en.length>360)return null;
      var url=String(x.sourceUrl||'');
      if(url&&(!/^https:\/\/[^\s<>"']+$/.test(url)||String(report.text||'').indexOf(url)<0))return null;
      out.push({text:text,textEn:en||'',evidence:ev,sourceUrl:url});
    }
    return out;
  }
  function balanceStructured(record,report,tk,date,mode) {
    if(!record||record.schema!=='fp.research-balance.v1'||record.ticker!==tk||record.reportId!==report.id||day(record.asOf)!==date)return null;
    if(record.sourceFingerprint!==balanceFingerprint(report.text))return null;
    var pros=balanceItems(record.pros,report),cons=balanceItems(record.cons,report);
    if(!pros||!cons||(!pros.length&&!cons.length))return null;
    return {status:'ready',sourceId:report.id,date:date,pros:pros,cons:cons,mode:mode,report:report};
  }
  function balanceExplicit(report,tk,date) {
    // Only an exact ticker-scoped, polarity-labelled section is machine extractable.
    // Business/quality/thesis/risk discussions are deliberately NOT classified by regex.
    var lines=String(report.text||'').split(/\r?\n/),side='',pros=[],cons=[],seen={pros:0,cons:0};
    lines.forEach(function(line){
      var heading=/^#{1,6}\s+(Pros|Cons|Puntos a favor|Riesgos)\s*[·:]\s*([A-Z0-9.-]+)\s*$/i.exec(line);
      if(heading){side=heading[2].toUpperCase()===tk?(/^(pros|puntos a favor)$/i.test(heading[1])?'pros':'cons'):'';if(side)seen[side]++;return;}
      if(/^#{1,6}\s/.test(line)){side='';return;}
      var bullet=/^[-*]\s+(.+)$/.exec(line);
      if(side&&bullet&&bullet[1].length>=15&&bullet[1].length<=320){var item={text:bullet[1],textEn:'',evidence:bullet[1],sourceUrl:''};(side==='pros'?pros:cons).push(item);}
    });
    if(seen.pros!==1||seen.cons!==1||!pros.length||!cons.length||pros.length>3||cons.length>3)return null;
    return {status:'ready',sourceId:report.id,date:date,pros:pros,cons:cons,mode:'explicit-sections',report:report};
  }
  function researchBalance(p) {
    var a=p&&p.latestCompleted,latest=p&&p.latestAnalysis;
    if(!a||!a.report||!day(a.date))return {status:'no-analysis',pros:[],cons:[]};
    // A later incomplete/withdrawn source must not leave an older positive box looking current.
    if(latest&&!latest.isComplete&&(String(latest.date||'')>String(a.date||'')||(latest.date===a.date&&latest.id!==a.id&&String(latest.id).localeCompare(String(a.id),undefined,{numeric:true})>0)))return {status:'newer-analysis',sourceId:latest.id,date:latest.date,pros:[],cons:[],report:latest.report};
    var report=a.report,meta=(report.profiles||[]).find(function(x){return ticker(x.ticker)===p.ticker;}),record=meta&&meta.prosCons;
    if(record) {
      // Author metadata is bound to the reviewed whole report, including later corrections.
      var direct=Object.assign({},record,{ticker:p.ticker,reportId:report.id});
      var valid=balanceStructured(direct,report,p.ticker,a.date,'structured-report');
      return valid||{status:'stale',sourceId:a.id,date:a.date,pros:[],cons:[],report:report};
    }
    var explicit=meta&&meta.prosConsSectionsFingerprint===balanceFingerprint(report.text)&&balanceExplicit(report,p.ticker,a.date);if(explicit)return explicit;
    var unavailable=meta&&meta.prosConsUnavailable;
    if(unavailable) {
      if(unavailable.schema==='fp.research-balance-unavailable.v1'&&day(unavailable.asOf)===a.date&&unavailable.sourceFingerprint===balanceFingerprint(report.text)&&typeof unavailable.reason==='string'&&unavailable.reason.trim().length>=12&&unavailable.reason.length<=320)return {status:'unavailable',sourceId:a.id,date:a.date,pros:[],cons:[],report:report,reason:unavailable.reason,reasonEn:unavailable.reasonEn||''};
      return {status:'stale',sourceId:a.id,date:a.date,pros:[],cons:[],report:report};
    }
    var records=root.FP_RESEARCH_BALANCE&&root.FP_RESEARCH_BALANCE.records||[],old=records.find(function(x){return x.ticker===p.ticker&&x.reportId===a.id;});
    var migrated=balanceStructured(old,report,p.ticker,a.date,'verified-migration');
    return migrated||{status:old?'stale':'pending',sourceId:a.id,date:a.date,pros:[],cons:[],report:report};
  }

  root.FP_PROFILE_ENGINE={isProspectiveStudy:isProspectiveStudy,isCurrentPriceReview:isCurrentPriceReview,build:build,search:search,day:day,completed:completed,researchBalance:researchBalance,balanceFingerprint:balanceFingerprint,balanceStructured:balanceStructured,balanceExplicit:balanceExplicit};
})(typeof window==='undefined'?globalThis:window);

