import pathlib,json,hashlib,zipfile,subprocess
P=pathlib.Path(__file__).parent
subprocess.run(['pandoc',str(P/'report.md'),'-s','--metadata','title=VLO — ciclo y capital','-o',str(P/'report.html')],check=True)
files=['README.md','model.py','model.json','peers.py','peers.json','report.py','report.md','report.html','prepare.py','publication.json','english_evidence.md','qa.py','qa.json','package.py']
for sub in ['history/portable','comps/mpc','facts']:files += [str(f.relative_to(P)) for f in sorted((P/sub).glob('*')) if f.is_file() and f.suffix in ['.py','.json','.txt','.md']]
(P/'checksums.txt').write_text('\n'.join(hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in files)+'\n')
with zipfile.ZipFile(P/'VLO_support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+['checksums.txt']:z.write(P/f,f)
manifest={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['report.md','model.json','publication.json','VLO_support.zip']};(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
