# Beam Designer

## Application platform
- Build the application as a Python desktop program using Tkinter.
- Present the inputs, results, and validation messages in a native desktop
  window. Use Tkinter widgets for controls and a Tkinter canvas for the beam,
  cross-section, and response diagrams.
- Keep calculations independent of the interface so the analysis can be
  validated separately from the desktop presentation.
- This specification describes the intended application; it does not define
  an implementation or prescribe a particular packaging method.

## Purpose
Create shear, moment, and deflection diagrams for a beam and provide
preliminary bending-strength and stiffness checks. This is an educational
screening tool, not a substitute for a complete code-based structural design.

## Initial scope and assumptions
- Imperial units.
- Prismatic, linearly elastic beams with small deflections and constant
  stiffness along the span.
- Supports: simply supported or cantilever.
- Continuous beams and code-compliant member design are out of scope.
- Save and open beam designs, including support type, span, section/member inputs,
  deflection limit, and applied loads.
- Export sampled position, shear, moment, and deflection results to a CSV file
  suitable for opening in spreadsheet software.

## Inputs
- Support condition and span (ft).
- Point loads: magnitude, direction, and position along the span.
- Uniform distributed loads: magnitude, direction, and start/end positions.
- Whether self-weight is included. When included, use the selected section's
  weight per length and show it as part of the applied loading.
- A steel W-shape or a lumber member.

### Member properties
- Steel W-shapes: select a section identifier from the curated list of 20
  common W-shapes. The selection does not auto-load table properties; enter
  and verify overall depth `d`, flange width `bf`, web thickness `tw`, flange
  thickness `tf`, weight per length, strong-axis moment of inertia `Ix`,
  elastic section modulus `Sx`, elastic modulus `E`, yield strength `Fy`, and
  an explicitly supplied allowable bending stress for the screening check.
- Lumber: species and grade, actual rectangular-section width `b` and depth
  `d` (including bending orientation), `E`, `Fb`, and `Fv`. Calculate
  `Ix = b*d^3/12` and `Sx = b*d^2/6`. Identify and explicitly apply any
  specified adjustment factors used to obtain the allowable bending stress;
  do not assume factors that the user has not specified.
- Identify the source of tabulated section/material properties. Allow users to
  inspect or correct the properties used in a calculation.

## Calculations and checks
- Reactions, shear, and moment from statics.
- Elastic deflection using the selected member's `E` and `Ix`.
- Maximum absolute bending stress, `fb = |M|/Sx`, compared with the explicitly
  supplied allowable bending stress.
- Maximum deflection compared with a user-selected limit; default to `L/360`.
- Display shear, moment, and deflection diagrams in the desktop window with
  units and sign conventions.
- Plot shear for analysis, but do not report a shear-strength pass/fail.
- Do not infer code-compliant strength from `Fy` alone. Buckling, lateral
  bracing, local buckling, shear strength, bearing, connections, load
  combinations, and other code checks are not included. Clearly label results
  as preliminary and identify checks not performed.

## Outputs
- A desktop window showing the beam, supports, loads, a dimensioned member
  cross-section, and the three response diagrams.
- Reactions, maximum moment, maximum bending stress, and maximum deflection.
- Pass/fail for bending only when an allowable bending stress is supplied;
  pass/fail for deflection against the selected limit.
- Units, member properties, load/self-weight assumptions, and limitations
  alongside the results.

## Look and feel
Clean and professional, with an example beam loaded when it opens. Draw the
selected member cross-section using a uniform scale based on its entered
dimensions. Use a Christmas palette and subtle seasonal decoration throughout
the interface and diagrams.

## Validation
For a 20 ft simply supported W12x26 with a full-span uniform load of
1 kip/ft, excluding self-weight, the statics benchmark is `Mmax = 50.0 kip-ft`.
For the elastic-deflection benchmark, use `E = 29,000 ksi` and `Ix = 204 in^4`;
the expected maximum deflection is approximately `0.609 in`. With `Sx =
33.4 in^3`, the expected maximum elastic bending stress is approximately `18.0 ksi`. Verify
the section properties against the selected section-data source. This
benchmark does not define a design allowable or imply code compliance.
Check the section sketch's aspect ratio against its entered dimensions for
both a W-shape and rectangular lumber.
