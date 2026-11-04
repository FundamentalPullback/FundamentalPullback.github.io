#!/usr/bin/env python3
import tempfile,pathlib,shutil,runpy,socket,os,json,hashlib
P=pathlib.Path(__file__).resolve().parent
names=['history.json','history.csv','ledger.csv','conflicts.csv','validation_checks.csv','source_index.csv','qa.txt']
def deny(*a,**k):raise RuntimeError('Network disabled for offline reproduction')
socket.create_connection=deny;socket.socket.connect=deny
with tempfile.TemporaryDirectory(prefix='hurn_offline_') as t:
 q=pathlib.Path(t)
 for n in ['numeric_inputs.json','rebuild_history.py']:shutil.copyfile(P/n,q/n)
 os.chdir('/')
 runpy.run_path(str(q/'rebuild_history.py'),run_name='__main__')
 checks={n:(q/n).read_bytes()==(P/n).read_bytes() for n in names}
 assert all(checks.values()),checks
 result=dict(status='PASS',network='socket.connect and create_connection disabled',input_files=['numeric_inputs.json','rebuild_history.py'],working_directory='/',reproduced=checks)
(P/'offline_reproduction.json').write_text(json.dumps(result,indent=2)+'\n');print('All 7 outputs byte-identical from isolated inputs; network disabled.')
