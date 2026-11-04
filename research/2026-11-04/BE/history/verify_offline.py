#!/usr/bin/env python3
"""Prove the numerical package rebuilds from only its two portable inputs."""
import pathlib,tempfile,shutil,subprocess,sys,json,hashlib
P=pathlib.Path(__file__).resolve().parent
names=['history.json','history.csv','ledger.csv','validation_checks.csv','conflicts.csv','source_index.csv','qa_flags.csv','qa.txt','checksums.txt']
with tempfile.TemporaryDirectory(prefix='bloom_history_') as tmp:
 t=pathlib.Path(tmp)
 for f in ['numeric_inputs.json','rebuild_history.py']:shutil.copy2(P/f,t/f)
 subprocess.run([sys.executable,'-I',str(t/'rebuild_history.py')],cwd='/',check=True,capture_output=True)
 checks={f:hashlib.sha256((P/f).read_bytes()).hexdigest()==hashlib.sha256((t/f).read_bytes()).hexdigest() for f in names}
 result=dict(pass_all=all(checks.values()),files_identical=checks,dependencies='Python standard library only',inputs=['numeric_inputs.json','rebuild_history.py'],network_required=False,filings_required=False,companyfacts_required=False,cwd_independent=True)
 (P/'offline_reproduction.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert result['pass_all']
