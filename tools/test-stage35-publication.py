#!/usr/bin/env python3
import copy, importlib.util, json, tempfile, unittest
from pathlib import Path
spec=importlib.util.spec_from_file_location('guard',Path(__file__).with_name('stage35-publication.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
class ContractTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.r=Path(self.tmp.name);(self.r/'data').mkdir();(self.r/'research').mkdir()
  self.h=['Ticker','Informe (ID)','Fecha análisis','Decisión','Profundidad','Ejecución','Ejecución (EN)','Máximo condicionado','untouched']
  self.rows=[self.h,['FUTURE.X','NEW987','2027-02-03','En observación','Stage 3 completo','','','','keep']]
  self.t={'ticker':'FUTURE.X','stage':'Stage 3.5','as_of_utc':'2027-02-03T09:00:00Z','trade_authorized':False,'approved_quantity':0,'publication':{'eligibility':'ready','execution':'suspended'},**{f:None for f in ('operative_M','operative_stop_S','fundamental_buy_max','technical_buy_max','buy_signal')}}
  self.reg={'schemaVersion':1,'assessments':[{'ticker':'FUTURE.X','reportId':'NEW987','analysisDate':'2027-02-03','assessedAt':self.t['as_of_utc'],'ticket':'research/future-ticket.json','publication':copy.deepcopy(self.t['publication'])}]};self.save()
 def save(self):
  (self.r/'research/future-ticket.json').write_text(json.dumps(self.t));(self.r/'data/stage35-assessments.json').write_text(json.dumps(self.reg));(self.r/'data/dec.js').write_text('window.FP=window.FP||{};FP.dec='+json.dumps(self.rows)+';')
 def test_future_symbol_projects_status_only(self):
  rows=g.project(self.r,self.rows);self.assertEqual(rows[1][3],'Apta para Stage 3.5');self.assertTrue(rows[1][5].startswith('Suspendida'));self.assertEqual(rows[1][8],'keep');self.assertEqual(self.rows[1][3],'En observación');self.assertEqual(g.project(self.r,rows),rows)
 def test_mismatch_blocks(self):
  self.t['publication']['eligibility']='watch';self.save()
  with self.assertRaises(ValueError):g.project(self.r,self.rows)
 def test_duplicate_blocks(self):
  self.rows.append(self.rows[1][:])
  with self.assertRaises(ValueError):g.project(self.r,self.rows)
 def test_stale_blocks(self):
  self.rows.append(['FUTURE.X','NEW988','2027-02-04','En observación','','','','',''])
  with self.assertRaises(ValueError):g.project(self.r,self.rows)
 def test_held_blocks_and_does_not_mutate(self):
  self.rows[1][3]='En cartera';before=copy.deepcopy(self.rows)
  with self.assertRaises(ValueError):g.project(self.r,self.rows)
  self.assertEqual(self.rows,before)
 def test_execution_and_levels_block(self):
  for field,value in [('approved_quantity',1),('trade_authorized',True),('operative_stop_S',10),('fundamental_buy_max',15),('buy_signal','trigger')]:
   original=self.t[field];self.t[field]=value;self.save()
   with self.assertRaises(ValueError):g.project(self.r,self.rows)
   self.t[field]=original
 def test_unregistered_ticket_blocks(self):
  self.reg['assessments']=[];self.save()
  with self.assertRaises(ValueError):g.project(self.r,self.rows)
 def test_row_mapping_and_minimal_payload(self):
  projected=g.project(self.r,self.rows);snapshot={'sheetId':77,'startRowIndex':102,'contiguous':True,'values':[self.h,['OTHER','Z','2027-01-01','','','','','',''],self.rows[1]]};p=g.sheet_plan(self.r,snapshot,projected)
  self.assertEqual(len(p['requests']),4)
  for q in p['requests']:
   u=q['updateCells'];self.assertEqual(u['range']['startRowIndex'],104);self.assertEqual(u['fields'],'userEnteredValue');self.assertEqual(len(u['rows'][0]['values']),1)
  snapshot['values']=[self.h,projected[1]];self.assertEqual(g.sheet_plan(self.r,snapshot,projected)['requests'],[])
 def test_readback_required_and_actual_agreement(self):
  self.rows=g.project(self.r,self.rows);self.save()
  with self.assertRaises(ValueError):g.validate(self.r,None)
  readback={'source':'google-sheets-readback','capturedAt':'2027-02-03T09:01:00Z','values':copy.deepcopy(self.rows)};self.assertTrue(g.validate(self.r,readback))
  readback['values'][1][3]='En observación'
  with self.assertRaises(ValueError):g.validate(self.r,readback)
 def test_readback_predates_assessment(self):
  self.rows=g.project(self.r,self.rows);self.save()
  with self.assertRaises(ValueError):g.validate(self.r,{'source':'google-sheets-readback','capturedAt':'2027-02-03T08:00:00Z','values':self.rows})
 def test_later_eligibility_demotion(self):
  self.t['publication']['eligibility']='watch';self.reg['assessments'][0]['publication']=copy.deepcopy(self.t['publication']);self.save();self.assertEqual(g.project(self.r,self.rows)[1][3],'En observación')
 def test_path_escape_blocks(self):
  self.reg['assessments'][0]['ticket']='../escape.json';self.save()
  with self.assertRaises(ValueError):g.project(self.r,self.rows)
 def test_serial_date_lossless_matching_and_readback(self):
  self.assertEqual(g.analysis_date(46330),'2026-11-04')
  serial=(__import__('datetime').date(2027,2,3)-__import__('datetime').date(1899,12,30)).days
  self.rows[1][2]=serial
  projected=g.project(self.r,self.rows);self.assertEqual(projected[1][2],serial)
  self.rows=projected;self.save()
  self.assertTrue(g.validate(self.r,{'source':'google-sheets-readback','capturedAt':'2027-02-03T09:01:00Z','values':self.rows}))
  for bad in [serial+0.5,float('nan'),True,'02/03/2027']:
   with self.assertRaises(ValueError):g.analysis_date(bad)
 def test_serial_stale_checks(self):
  serial=(__import__('datetime').date(2027,2,4)-__import__('datetime').date(1899,12,30)).days
  rows=self.rows+[['FUTURE.X','NEXT',serial,'En observación','','','','','']]
  with self.assertRaises(ValueError):g.project(self.r,rows)
  with self.assertRaises(ValueError):g.sheet_plan(self.r,{'sheetId':77,'contiguous':True,'startRowIndex':0,'values':rows},g.project(self.r,self.rows))
 def test_contiguous_empty_rows_keep_offsets(self):
  plan=g.sheet_plan(self.r,{'sheetId':77,'contiguous':True,'startRowIndex':0,'values':[self.h,[],self.rows[1]]},g.project(self.r,self.rows))
  self.assertTrue(all(r['updateCells']['range']['startRowIndex']==2 for r in plan['requests']))
 def test_sparse_mapping_requires_actual_indices(self):
  projected=g.project(self.r,self.rows)
  ambiguous={'sheetId':77,'startRowIndex':0,'values':self.rows}
  with self.assertRaises(ValueError):g.sheet_plan(self.r,ambiguous,projected)
  sparse={'sheetId':77,'rowIndices':[0,675],'values':self.rows}
  plan=g.sheet_plan(self.r,sparse,projected)
  self.assertTrue(plan['requests'])
  for request in plan['requests']:self.assertEqual(request['updateCells']['range']['startRowIndex'],675)
  self.assertTrue(all(c['rowIndex']==675 for c in plan['verification']))
  for bad in [[0],[0,0],[0,675.5]]:
   sparse['rowIndices']=bad
   with self.assertRaises(ValueError):g.sheet_plan(self.r,sparse,projected)
  sparse['rowIndices']=[0,675];sparse['startRowIndex']=0
  with self.assertRaises(ValueError):g.sheet_plan(self.r,sparse,projected)
if __name__=='__main__':unittest.main()
