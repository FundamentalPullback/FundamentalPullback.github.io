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
        if(meta.kind!=='management') p.analyses.push({id:r.id,date:day(meta.completedAt)||day(r.date),row:null,report:r,kind:meta.label||'standalone',isComplete:meta.kind==='complete'||meta.kind==='review'});
      });
      // A ticker explicitly written in a title is a subject link, never proof of completion.
      var titleTokens=String(r.title||'').match(/\b[A-Z][A-Z0-9.-]{0,10}\b/g)||[];
      titleTokens.forEach(function(tk) { if(by[tk] && (tk.length>1 || new RegExp('(?:^|\\()'+tk+'(?:\\)|\\s*[—·:])').test(r.title))) addReport(by[tk],r.id,'subject'); });
    });
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
      p.hasResearch=!!p.decisions.length || p.reports.some(function(x){return x.relation==='source' && x.report.cat==='Selección y valoración';});
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
  root.FP_PROFILE_ENGINE={build:build,search:search,day:day,completed:completed};
})(typeof window==='undefined'?globalThis:window);
