import ROOT
from ROOT import RDataFrame
import sys

ROOT.EnableImplicitMT()

if len(sys.argv) < 2:
    print(f"Usage: python3 {sys.argv[0]} <your_root_file.root>")
    sys.exit(1)

filename = sys.argv[1]
real_electrons = 2.8313712e21  # Electrons on target in 30-week run with 50% eff

# Get total EOT from RunSummary 
run_df = RDataFrame("RunSummary", filename)
EOT = run_df.Sum("TotEvents").GetValue()
print(f"Total electron primaries (EOT): {EOT:,}")

# Get total weighted muons 
events_df = RDataFrame("Events", filename)
muons_df = events_df.Filter("ParticleID == 10 || ParticleID == 11")
muon_sum = muons_df.Sum("Weight1").GetValue()
print(f"Total weighted muons (μ⁺ + μ⁻): {muon_sum:.4f}")

# Calculate muons per EOT 
muons_per_eot = muon_sum / EOT
print(f"Muons per EOT: {muons_per_eot:.6e}")

# JLAB electrons
print(f"EOT in a 30-week run with 50% efficiency:{real_electrons:.6e}")

# Scale to JLAB
real_muons = muons_per_eot * real_electrons
print(f"Estimated muons in 30-week run with 50% efficiency: {real_muons:.6e}")

# Scale to /s
muons_sec = real_muons / 9072000
print(f"Estimated muons per second: {muons_sec:.6e}")