# Request log

## 2026-11-24
- Asked: Resolve the PowerShell `pip` not recognized error and install NumPy and Matplotlib.
- Changed: Added `requirements.txt`; installed/confirmed NumPy and Matplotlib for the available Python 3.15. Use `py -m pip install -r requirements.txt` because `pip` is not on PATH.
- Worked: Yes. Both packages import from the installed interpreter. Project-local virtual environment creation was blocked by a Windows temp-directory permission error.
