from pathlib import Path
import runpy
p=Path(__file__).parent
runpy.run_path(str(p/'model.py'))
runpy.run_path(str(p/'extend_model.py'))
