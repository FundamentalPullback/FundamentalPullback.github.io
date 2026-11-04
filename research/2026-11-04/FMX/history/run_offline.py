"""Rebuild deterministic history and exKOF comparison from compact inputs only."""
import runpy,pathlib
P=pathlib.Path(__file__).resolve().parent
runpy.run_path(str(P/'build_history.py'),run_name='__main__')
runpy.run_path(str(P/'build_ex_kof_comparison.py'),run_name='__main__')
