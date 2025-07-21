from ROOT import TFile, TH1F, TCanvas, gPad, TLegend
import sys
from math import acos, pi

#Create histograms
hETot1 = TH1F("hETot1", "Total Energy (File 1)", 200, 0, 11)
hETot2 = TH1F("hETot2", "Total Energy (File 2)", 200, 0, 11)
hETot3 = TH1F("hETot3", "Total Energy (File 3)", 200, 0, 11)
hETot4 = TH1F("hETot4", "Total Energy (File 4)", 200, 0, 11)

#Fill histograms from ROOT files
def fill_histogram(filename, pid, hist):
    file = TFile.Open(filename, "READ")
    if not file or file.IsZombie():
        print(f"Error opening file: {filename}")
        return

    tree = file.Get("Events")
    if not tree or not tree.InheritsFrom("TTree"):
        print(f"Tree 'Events' not found in: {filename}")
        file.Close()
        return

    for entry in tree:
        if entry.ParticleID == pid:
            hist.Fill(entry.ETot)

    file.Close()  

#Handle arguments
if len(sys.argv) < 4:
    print("Usage: python3 script.py file1.root file2.root file3.root file4.root PID")
    sys.exit()

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
file4 = sys.argv[4]
pid = int(sys.argv[5])

#Fill histograms
fill_histogram(file1, pid, hETot1)
fill_histogram(file2, pid, hETot2)
fill_histogram(file3, pid, hETot3)
fill_histogram(file4, pid, hETot4)

#Plotting
canvas = TCanvas("canvas", "Total Energy Comparison", 800, 600)
gPad.SetLogy()

hETot1.SetLineColor(1)  # Black 
hETot2.SetLineColor(2)  # Red
hETot3.SetLineColor(4)  # Blue
hETot4.SetLineColor(3)   # Green

hETot1.Draw("hist")
hETot2.Draw("hist same")
hETot3.Draw("hist same")
hETot4.Draw("hist same")

hETot1.SetTitle("Total Energy Comparison")
hETot1.GetXaxis().SetTitle("Total Energy [GeV]")

legend = TLegend(0.6, 0.75, 0.88, 0.88)
legend.AddEntry(hETot1, "NO Pipe", "l")
legend.AddEntry(hETot2, "Pipe 4.56 in", "l")
legend.AddEntry(hETot3, "Pipe 18.24 in", "l")
legend.AddEntry(hETot4, "Thru Pipe", "l")
legend.Draw()

gPad.Update()

#Save comparison to NEW file
outfile_name = f"compare_ETot_pid{pid}.root"
fout = TFile(outfile_name, "RECREATE")
hETot1.Write()
hETot2.Write()
fout.Close()

input("Press enter to quit...")