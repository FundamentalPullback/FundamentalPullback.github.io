import pathlib,hashlib,zipfile
P=pathlib.Path(__file__).parent
files=[P/x for x in ['build_analysis.py','analysis.json','report.py','report.md','report.html','prepare.py','publication.json','english_evidence.md','qa.py','qa.json','package.py','README.md']]
files+=list((P/'facts').glob('*.txt'))
files += [P/'history'/x for x in ['numeric_facts.json','reproduce.py','normalized_history.json','normalized_history.csv','README.md']]
files += [P/'merger'/x for x in ['terms_note.md','numeric_inputs.json','lite_target_context.md','lite_target_inputs.json']]
(P/'manifest.sha256').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+str(p.relative_to(P))+'\n' for p in sorted(files)))
with zipfile.ZipFile(P/'support.zip','w',zipfile.ZIP_DEFLATED) as z:
 for p in files+[P/'manifest.sha256']:z.write(p,str(p.relative_to(P)))
for x in ['report.md','analysis.json','publication.json','support.zip']:print(x,hashlib.sha256((P/x).read_bytes()).hexdigest())
