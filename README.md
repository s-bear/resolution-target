# Resolution Test Patterns

Various resolution targets for photography with PDF, SVG, and source files. With some tweaking, the image files could also be used for testing image interpolation or compression algorithms.

These are close to a standard ISO 12233 target, but I haven't purchased the standard so it's certainly not compliant!

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

## Using the targets
These targets can be used to test a variety of imaging systems... printers, scanners, cameras, eyeballs, etc. The typical use case is for a camera or scanner:
1) Print the pattern using a high-quality printer with at least the DPI specified on the pattern.
2) Inspect your print (likely with magnification) to make sure the pattern is clear up to the center of the chart. Use calipers or another high-precision measuring device to ensure that the target printed uniformly. Each of the squares around the periphery should be the same size.
3) Image the chart with your device-under-test. Ensure reasonable exposure, uniform lighting, the focal plane is parallel to the chart, etc.
4) Inspect your image. The resolution is given by measuring from the center of the image of the chart to the radius where you can distinguish the lines.
    - The resolution is {cycles}/(2 π {radius}). {cycles} is given by which chart you use. {radius} should be in the units of your image (e.g. pixels). If you know the physical size of your pixels, you can scale {radius} to that.
    - The resolution may be different in different directions. That's the whole point of using a radial chart like this.
    - **The scale is given by the size of the _image_, not the size of the chart.** Unless you're using a 1:1 imaging device (like a scanner or macro camera), **you should not use the cm scale on the chart**. The cm scale is only for making sure that the chart printed correctly.
    
