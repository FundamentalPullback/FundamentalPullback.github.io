from pathlib import Path
import subprocess
P=Path(__file__).parent
header='<style>'+ (P/'style.css').read_text()+'</style>'
(P/'html_header.html').write_text(header)
subprocess.run(['pandoc',str(P/'report.md'),'-s','--metadata','title=CTSH | Investigación condicional','--include-in-header',str(P/'html_header.html'),'-o',str(P/'report.html')],check=True)
print('HTML rendered; live visual check still required by publisher')
