"""
Deprecated wrapper. Use: python tools/update_stars.py
This file now delegates to the new tool location.
"""

from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent
TOOL = ROOT / "tools" / "update_stars.py"

if not TOOL.exists():
    print("Error: tools/update_stars.py not found")
    sys.exit(1)

runpy.run_path(str(TOOL))
