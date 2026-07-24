## Disclaimer
These tools are NOT done being tested. Please mark where the tools are used 
with "fovtool" or "flashtool" depending on the program used. 

Future unit testing is pending and may invalidate some or all of the results.
    -- Leif

## fovtool
Run "fov.py" to use. Used to compare a given CSS pixel area against a nominal area of 341 x 256 px.

NOTE: This tool is ONLY useful at a resolution of 1024 x 768 px, unless the code is modified to fit a different need.

### Use
If a \[CAUTION] result is received, continue on to using flashtool.

### Algorithm
Compares the given area against how much of the "nominal area" it takes up. 
* Since the "nominal area" is defined as `<341 x 256>` internally, it:
  * limits the given dimensions to 341 and 256 respectively, and
  * returns the % of the "nominal area" the limited area covers.

## flashtool
Use fovtool first.

Run "flash.py" to use. Used to compare two colors against the WCAG definitions of "general flash threshold" and "red flash threshold"
