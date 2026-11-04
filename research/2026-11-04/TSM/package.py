import pathlib,hashlib,zipfile,subprocess,json
P=pathlib.Path(__file__).parent
subprocess.run(['pandoc',str(P/'report.md'),'-s','--metadata','title=TSM — revisión fundamental parcial','-o',str(P/'report.html')],check=True)
files=['README.md','report.md','report.html','report.py','analysis.json','build_analysis.py','prepare.py','publication.json','english_evidence.md','qa.py','qa.json','package.py','history/history.json','history/source_inputs.json','history/build_history.py','history/SOURCES.md','comps/build_peer_fundamentals.py','comps/peer_fundamentals.json','comps/peer_notes.md']
lines=[hashlib.sha256((P/f).read_bytes()).hexdigest()+'  '+f for f in files];(P/'checksums.txt').write_text('\n'.join(lines)+'\n')
with zipfile.ZipFile(P/'TSM_support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for f in files+['checksums.txt']:z.write(P/f,f)
manifest={f:hashlib.sha256((P/f).read_bytes()).hexdigest() for f in ['report.md','analysis.json','publication.json','TSM_support.zip']};(P/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');print(json.dumps(manifest))
