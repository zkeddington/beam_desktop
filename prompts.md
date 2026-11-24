# Request log

## 2026-11-24
- Asked: Update `spec.md` to describe a Python desktop app using Tkinter; do not build anything.
- Changed: Updated the specification to identify Python/Tkinter as the desktop platform, describe the interface and canvas diagrams, and keep calculations separate from presentation. No application was built.
- Worked: Yes. The specification now describes the requested app.

## 2026-11-24
- Asked: Resolve the PowerShell `pip` not recognized error and install NumPy and Matplotlib.
- Changed: Added `requirements.txt`; installed/confirmed NumPy and Matplotlib for the available Python 3.15. Use `py -m pip install -r requirements.txt` because `pip` is not on PATH.
- Worked: Yes. Both packages import from the installed interpreter. Project-local virtual environment creation was blocked by a Windows temp-directory permission error.
