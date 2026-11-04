#!/usr/bin/env python3
"""Prove two-file rebuild in an isolated temporary folder, denying networking/external reads."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
P=pathlib.Path(__file__).resolve().parent
NAMES=['history.json','history.csv','ledger.csv','source_index.csv','qa_flags.csv','validation_checks.csv','conflicts.csv','qa.txt','checksums.txt']
expected={n:hashlib.sha256((P/n).read_bytes()).hexdigest() for n in NAMES}
child=r'''
import calendar,csv,hashlib,json,pathlib,os,sys,io,socket
P=pathlib.Path.cwd().resolve()
code=compile((P/'rebuild_history.py').read_text(),str(P/'rebuild_history.py'),'exec')
opened=[]
def gate(event,args):
    if event in ['socket.connect','socket.__new__','urllib.Request']:raise RuntimeError('Network disabled for verification')
    if event=='open':
        name=args[0]
        if isinstance(name,(str,bytes,os.PathLike)):
            fp=pathlib.Path(os.fsdecode(name)).resolve()
            if fp.parent!=P:raise RuntimeError('External file access blocked: '+str(fp))
            opened.append(fp.name)
sys.addaudithook(gate)
exec(code,{'__file__':str(P/'rebuild_history.py'),'__name__':'__main__'})
(P/'access_audit.json').write_text(json.dumps(sorted(set(opened))))
'''
with tempfile.TemporaryDirectory(prefix='pwr_history_offline_') as td:
 T=pathlib.Path(td)
 for n in ['numeric_inputs.json','rebuild_history.py']:shutil.copyfile(P/n,T/n)
 initial=sorted(x.name for x in T.iterdir())
 result=subprocess.run([sys.executable,'-I','-S','-c',child],cwd=T,capture_output=True,text=True,timeout=45)
 if result.returncode:raise RuntimeError(result.stderr)
 actual={n:hashlib.sha256((T/n).read_bytes()).hexdigest() for n in NAMES}
 assert actual==expected,'Rebuilt output differs'
 accessed=json.loads((T/'access_audit.json').read_text())
 proof={'status':'PASS','starting_files':initial,'network':'Denied by Python audit hook','external_file_access':'Denied by Python audit hook after interpreter/module initialization','original_filings_or_companyfacts':'Not copied, read or required','outputs_verified_byte_for_byte':actual,'accessed_filenames':accessed,'checks':(T/'qa.txt').read_text().splitlines()[-3:]}
(P/'offline_reproduction.json').write_text(json.dumps(proof,indent=2)+'\n')
print('PASS: isolated two-file rebuild, no network or outside-file reads, identical '+str(len(NAMES))+' outputs.')
