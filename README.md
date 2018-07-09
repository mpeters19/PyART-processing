# PyART Processing

Environment Analytics software written to aid in the processing, analysis, and visualization of radar software through the ARM PyART python package. Functions and documentation were written by Sara Berry in 2015. Software was updated and uploaded to Github by Daniel Hueholt in 2018.

---EnvAn PyART processing toolkit:

colormap: Contains functions controlling colormaps for reflectivity, velocity, differential reflectivity, spectral width, and one-way differential propagation phase.

gen_fun: Miscellaneous functions for tasks such as parsing a list of files or generating an image filename.

Master_plotter.py: Plots and saves Plan Position Indicator (PPI) and/or Range Height Indicator (RHI) images for a given field.

quality_control: Multiple functions, including the dealiasing function.

start_script: "Just set the variables and press PLAY!" -Sara Berry

---MODIFIED Py-ART files

nexrad_level2: Updated to use np.frombuffer instead of np.fromstring, which is now deprecated.
