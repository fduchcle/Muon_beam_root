from ROOT import (TFile, TTree, TH1F, TH2F, TH3F, TCanvas, TPad, gDirectory, gStyle, gPad)
import sys
from math import acos, pi


hETot = TH1F("hETot","Total Energy",200, 0, 11)
hPID = TH1F("hPID","Particle ID",30, 0, 31)
hVxVy = TH2F("hVxVy","Vx vs. Vy", 400, -100, 100, 400, -100, 100)
hETotTheta = TH2F("hETotTheta","ETot vs. Scaterring Angle", 200, 0, 10, 180, 0, 30,)

c1 = TCanvas("c1","The FillRandom example",200,10,1400,1400)

p1 = TPad('p1','This is pad1',0.02,0.48,0.48,0.94,0)
p2 = TPad('p2','This is pad2',0.52,0.48,0.98,0.94,0)
p3 = TPad('p3','This is pad3',0.02,0.02,0.48,0.48,0)
p4 = TPad('p4','This is pad4',0.52,0.02,0.98,0.48,0)

p1.Draw()
p2.Draw()
p3.Draw()
p4.Draw()
p1.cd()

gStyle.SetOptStat(0) 


if __name__ == "__main__":

    try:
        datafile  = sys.argv[1]
        particle_id = int(sys.argv[2])
    except IndexError:
        print('WARNING: arguments are missing')
        print('USAGE: python3 %s <imput_file PID>' % (sys.argv[0].split('/')[-1]) )
        sys.exit()
    except IOError or ValueError:
        print('WARNING: input file missing')
        print('cannot open file: %s', sys.argv[1])
        print('USAGE: python3 %s <input_file PID>' % (sys.argv[0].split('/')[-1]) )
        sys.exit()

    fin = TFile(datafile, "READ")
    evnts = fin.Get("Events")

    if not isinstance(evnts, TTree):
        print("ERROR: 'Events' tree not found in the file or not a TTree object.")
        fin.ls()
        sys.exit(1)

    for i in range(evnts.GetEntries()):
        evnts.GetEntry(i)
        entry = evnts
        PID = entry.ParticleID
        hPID.Fill(PID)
        if particle_id == PID:
            hETot.Fill(evnts.ETot)
            hVxVy.Fill(entry.Vx, entry.Vy)
            theta = acos(entry.Cz)*180/pi
            hETotTheta.Fill(entry.ETot, theta)

# Uncomment these lines to speed up execution when running checks and such...
            # if i > 1000:
            #     break

    p1.cd()
    hETot.Draw()
    hETot.SetXTitle("Total Energy [GeV]")
    p1.SetLogy()
    
    p2.cd()
    hVxVy.Draw("surf2z")
    hVxVy.SetXTitle("Vx")
    hVxVy.SetYTitle("Vy")

    p3.cd()
    hETotTheta.Draw("colz")
    hETotTheta.SetXTitle("Energy [GeV]")
    hETotTheta.SetYTitle("Scattering Angle [deg]")
    from ROOT import TLine

    # Horizontal dotted line at y = 5
    line = TLine(hETotTheta.GetXaxis().GetXmin(), 5,
                 hETotTheta.GetXaxis().GetXmax(), 5)
    line.SetLineStyle(2)   
    line.SetLineColor(1)   
    line.SetLineWidth(2)
    line.Draw("same")

    p4.cd()
    hPID.Draw()
    p4.SetLogy()
    hPID.SetXTitle("Particle ID")
    
    gPad.Update()
    c1.Update()
    
    gPad.Update()
    c1.Update()

    # Add dynamic title
    c1.cd()
    from ROOT import TPaveText
    import os
    filename = os.path.splitext(os.path.basename(datafile))[0]
    flabel = filename.replace('_', ' ')
    title_text = f"Muon Beam Analysis: {flabel}"
    title = TPaveText(0.2, 0.94, 0.8, 0.99, "NDC")
    title.AddText(title_text)
    title.SetTextAlign(22)
    title.SetTextSize(0.04)
    title.SetFillColor(0)
    title.SetBorderSize(0)
    title.Draw()

    c1.Modified()
    c1.Update()
    
    c1.SaveAs("Plot1_%s.png" % (filename))  
    
    fin.Close()
    
    outfile = datafile.replace("Sim_muon_beam", "muon_beam_plots")
    outfile = outfile.replace(".0.", "."+str(particle_id)+".")
  
    input("Press enter to quit...")