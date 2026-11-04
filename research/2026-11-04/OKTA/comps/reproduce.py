import pathlib,json,subprocess
P=pathlib.Path(__file__).parent
subprocess.run(['python',str(P/'security_context/reproduce.py')],check=True)
f=json.loads((P/'ftnt_inputs.json').read_text());f['company_fcf']=f['cfo']-f['ppe']-f['escrow'];f['fcf_less_sbc_sensitivity']=f['company_fcf']-f['sbc'];f['margin']=f['ebit']/f['revenue']
(P/'ftnt_context.json').write_text(json.dumps(f,indent=2)+'\n')
