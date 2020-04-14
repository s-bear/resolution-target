# Resolution Test Patterns

Various resolution targets for photography with PDF, SVG, and source files.

## radial-sharp-*
Siemens star patterns with the given number of spokes and sharp boundaries between lines.
- These patterns are easier to print than the sinusoidal version.
- The center of the star is covered by a target to make measuring the distance from the center easier.
- These files are entirely vector graphics. The DPI listed is what would give ~10 dots per cycle at the edge of the central 5 mm target. Printing at this DPI should give reasonable quality, but higher will of course be better.

## radial-sine-*
Sinusoidal star patterns with the given number of spokes and a sinusoidal profile
- The sinusoidal pattern is more difficult to print because of the shading
- Converts directly to spatial frequency response unlike the sharp version.
- The center of the star is covered by a target to make measuring the distance from the center easier.
- The images are embedded in the PDFs, but only linked in the SVG files, so be careful.
- To keep file sizes smaller, the full DPI image is only included at the center of the pattern. Lower resolution copies are used for the outer regions, with interpolation to keep things smooth. Many PDF viewers will show artefacts at the boundaries between the regions until you zoom in to the full resolution.
