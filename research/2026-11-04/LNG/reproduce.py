from pathlib import Path
import subprocess,sys
P=Path(__file__).resolve().parent
for path in ['history/build_history.py','history_review/reproduce.py','capital_review/waterfall.py','comparables/reproduce.py','analyze.py','normalize.py','build_report.py','build_summary.py','qa.py']:
 subprocess.run([sys.executable,str(P/path)],cwd=P,check=True)
print('Nine offline stdlib steps passed. No certified total valuation, owner FCF or entry.')
