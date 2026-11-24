# Request log

## 2026-11-24
- Asked: Update `spec.md` to describe a Python desktop app using Tkinter; do not build anything.
- Changed: Updated the specification to identify Python/Tkinter as the desktop platform, describe the interface and canvas diagrams, and keep calculations separate from presentation. No application was built.
- Worked: Yes. The specification now describes the requested app.

## 2026-11-24
- Asked: Resolve the PowerShell `pip` not recognized error and install NumPy and Matplotlib.
- Changed: Added `requirements.txt`; installed/confirmed NumPy and Matplotlib for the available Python 3.15. Use `py -m pip install -r requirements.txt` because `pip` is not on PATH.
- Worked: Yes. Both packages import from the installed interpreter. Project-local virtual environment creation was blocked by a Windows temp-directory permission error.

## 2026-11-24
- Asked: Read `spec.md` and build its Tkinter desktop app, using `index.html` as a behavior reference.
- Changed: Added `beam_designer.py` with separate beam analysis, example-loaded Tkinter controls, load inputs, screening results, and canvas beam/response/section drawings.
- Worked: Yes. Python import succeeded and the specified 20 ft benchmark produced 50.0 kip-ft, 0.609 in deflection, and 17.964 ksi bending stress.

## 2026-11-24
- Asked: Fix the app because `py beam_designer.py` exits without opening a window.
- Changed: Added the `__main__` entry point to instantiate the Tkinter app and enter its event loop.
- Worked: The module compiles and the script now enters the Tkinter main loop when launched; GUI display could not be interactively confirmed in this session.

## 2026-11-24
- Asked: Prevent shear/moment label overlap, correct the cross-section drawing, and show distributed loads on the beam.
- Changed: Allocated separate vertical rows for response diagrams, drew entered distributed and point loads above the beam, and rendered steel W-shapes or rectangular lumber with scaled dimensions.
- Worked: Yes. Python compilation and the 20 ft benchmark check succeeded.

## 2026-11-24
- Asked: Add File > Save/Open for beam support, span, section, deflection limit, and loads; remove saving designs from spec out of scope.
- Changed: Added Save/Open commands backed by JSON design files and moved design saving into the specification scope.
- Worked: Yes. Python compilation and a JSON data round-trip check succeeded.

## 2026-11-24
- Asked: Add a button to export x, shear, moment, and deflection along the beam to an Excel-compatible CSV.
- Changed: Added an Export results to CSV button and UTF-8 BOM CSV output with unit-labeled columns; updated the specification.
- Worked: Yes. Python compilation and CSV header validation succeeded.

## 2026-11-24
- Asked: Add a calculation sheet button that saves inputs, diagrams, and checks as a hand-in-ready PDF.
- Changed: Added a PDF export button, a printable calculation summary with inputs and check results, and sampled beam response values; documented PDF output in the specification.
- Worked: Python compilation succeeded. Export is a one-page printable PDF using built-in fonts.

## 2026-11-24
- Asked: Write a short README explaining the app, packages to install, and startup command.
- Changed: Added `README.md` with the app summary, dependency installation, and launch commands.
- Worked: Yes. README content matches the current requirements and app entry point.
