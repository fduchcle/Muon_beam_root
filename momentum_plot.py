from ROOT import TFile, TH1F, TCanvas, gPad, TLegend
import sys
from math import acos, pi

#Create histograms
hP1 = TH1F("hP1", "Total Momentum (File 1)", 200, 0, 11)
hP2 = TH1F("hP2", "Total Momentum (File 2)", 200, 0, 11)
hP3 = TH1F("hP3", "Total Momentum (File 3)", 200, 0, 11)


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
            hist.Fill(entry.P)

    file.Close()  

#Handle arguments
if len(sys.argv) < 4:
    print("Usage: python3 script.py file1.root file2.root file3.root PID")
    sys.exit()

file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]
pid = int(sys.argv[4])

#Fill histograms
fill_histogram(file1, pid, hP1)
fill_histogram(file2, pid, hP2)
fill_histogram(file3, pid, hP3)


#Plotting
canvas = TCanvas("canvas", "Total Momentum Comparison", 800, 600)
gPad.SetLogy()

hP1.SetLineColor(2)  # Red 
hP2.SetLineColor(3)  # Green
hP3.SetLineColor(4)  # Blue

hP1.Draw("hist")
hP2.Draw("hist same")
hP3.Draw("hist same")


hP1.SetTitle("Total Momentum Comparison")
hP1.GetXaxis().SetTitle("Total Momentum [GeV/c]")

legend = TLegend(0.6, 0.75, 0.88, 0.88)
legend.AddEntry(hP1, "NO Pipe", "l")
legend.AddEntry(hP2, "Pipe 4.56 in", "l")
legend.AddEntry(hP3, "Pipe 18.24 in", "l")
legend.Draw()

gPad.Update()

#Save comparison to NEW file
outfile_name = f"compare_p_pid{pid}.root"
fout = TFile(outfile_name, "RECREATE")
hP1.Write()
hP2.Write()
fout.Close()

input("Press enter to quit...")