These 4 python script are used to plot and analyze data from a root file generated using FLUKA, a monte carlo simulation. The purpose of the simulation was to test the 
feasability of constructing a muon beamline using the decay from the beam dump of Jefferson Lab CEBAF electron beam.  

beam_plots1.py, creates 4 plots on one canvas. The total energy generated (hETot), the particle ID's in the .root file and the count generated (hPID), the energy distribution 
and its scattering angle with a horizontal line at preassigned angle (hETotTheta), and a 3D plot of the Vx and Vy bins along the Vz axis (hVxVy). 
run it with: python3 beam_plots1.py simulation_name.root PID

beam_plots2.py, is similar to the first, but it replaces the 3D plot with a simpler Vx vs Vy plot at a specific point along the Vz axis.
run it with: python3 beam_plots2.py simulation_name.root PID

beam_plots3.py, creates the same plots as plots1 but does so for each predefined particle, prompting you after each canvas creation with "Press enter to continue..."
run with: python3 beam_plots3.py simulation_name.root

particle_plots.py, is similar to the plots3 except it doesn't show you the canvas, just saves each set of particle plots as .png. There is also an additional plot showing the count of the particle along the z-axis at the important detection points. 
run it with: python particle_plots.py simulation_name.root

tot_energy_plots.py, takes a max of 4 .root file (can be easily modified to be more or less) and plots their total energy on the same plot.
run it with: python3 tot_energy_plots.py simulation1_name.root simulation2_name.root " " PID 

The muon_yield_calc.py file prints out the total electron primaries from the TotEvents plot. The total weighted muons from Weight1 in the TTree. 
And calculates how many muons will be generated in 30 weeks with a beamline efficiency of 50% with a preset EOT number of 2.8314E+21. 
