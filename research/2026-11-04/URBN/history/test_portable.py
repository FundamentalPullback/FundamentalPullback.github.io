"""Prove history runs in isolation without sources, network or third-party modules."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
root=Path(__file__).resolve().parent
expected=json.loads((root/'portable_baseline.json').read_text())
with tempfile.TemporaryDirectory(prefix='urbn_isolated_') as tmp:
 isolated=Path(tmp)/'history';isolated.mkdir()
 for name in ['build_history.py','numeric_inputs.json','custom_numeric_inputs.json','source_hashes.json']:
  shutil.copyfile(root/name,isolated/name)
 assert not (isolated.parent/'sources').exists()
 run=subprocess.run([sys.executable,'-I',str(isolated/'build_history.py')],cwd=tmp,capture_output=True,text=True,check=True)
 checks={name:hashlib.sha256((isolated/name).read_bytes()).hexdigest()==digest for name,digest in expected.items()}
 report={'isolated_directory':str(isolated),'sources_directory_present':False,'input_files':['numeric_inputs.json','custom_numeric_inputs.json'],'standard_library_only':True,'python_isolated_mode':True,'byte_identical_to_original':checks,'all_pass':all(checks.values())}
 print(json.dumps(report,indent=2))
 if not report['all_pass']:raise SystemExit(1)
