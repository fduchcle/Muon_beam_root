These 4 python script are used to plot and analyze data from a root file generated using FLUKA, a monte carlo simulation. The purpose of the simulation was to test the 
feasability of constructing a muon beamline using the decay from the beam dump of Jefferson Lab CEBAF electron beam.  

The first file, beam_plots1.py, creates 4 plots on one canvas. The total energy generated (hETot), the particle ID in the .root file (hPID), the energy distribution 
and its cattering angle (hETotTheta), and a 3D plot of the Vx and Vy bins along the Vz axis (hVxVy). 

The second file, beam_plots2.py, is similar to the first, but it replaces the 3D plot with a simpler Vx vs Vy plot at a specific point on the Vz axis.

The thrid file, beam_plots3.py, takes a max of 4 .root file (can be easily edited to be more or less) and plots their total energy on the same plot.
