#! /usr/bin/env python



from ROOT import (TFile, TTree, TH1F, TH2F, TH3F, TCanvas, TPad, gDirectory, gStyle, gPad, kBlue, kYellow, kWhite, kBlack, TLatex, TArrayD)
import sys
from math import acos, pi

gStyle.SetOptStat(0)

def process_events(events, pid, pname, surface_pos, dsurf):
    hETot = TH1F("hETot","Total Energy",200, 0, 11)
    hPID = TH1F("hPID","Particle ID",30, 0, 30)
    hPIDpart = TH1F("hPIDpart","Particle ID",30, 0, 30)
    hVxVy = TH2F("hVxVy","Vx vs. Vy", 400, -100, 100, 400, -100, 100)
    hETotTheta = TH2F("hETotTheta","ETot vs. Scaterring Angle", 200, 0, 10, 180, 0, 30,)
    
    c1 = TCanvas("c1","The Muon Beam Simulation",200,10,1400,1400)

    p1 = TPad('p1','This is pad1',0.02,0.48,0.48,0.94,0)
    p2 = TPad('p2','This is pad2',0.52,0.48,0.98,0.94,0)
    p3 = TPad('p3','This is pad3',0.02,0.02,0.48,0.48,0)
    p4 = TPad('p4','This is pad4',0.52,0.02,0.98,0.48,0)

    p1.Draw()
    p2.Draw()
    p3.Draw()
    p4.Draw()
    p1.cd()

    for i, entry in enumerate(events):
        PID = entry.ParticleID
        zpos = entry.Vz
        hPID.Fill(PID)
        if pid == PID:
            # Uncomment the line below to zero in on a specific sampling surface
            # if abs(zpos-surface_pos) <= dsurf: 
            hPIDpart.Fill(PID)
            hETot.Fill(events.ETot)
            hVxVy.Fill(entry.Vx, entry.Vy)
            theta = acos(entry.Cz)*180/pi
            hETotTheta.Fill(entry.ETot, theta)

# Uncomment these lines to speed up execution when running checks and such...
          #  if i > 1000:
           #    break

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

    p4.cd()
    hPID.Draw()
    hPIDpart.Draw("same")
    hPIDpart.SetFillColor(kBlue)
    p4.SetLogy()
    hPID.SetXTitle("Particle ID")

    if PID == 7:
        label = TLatex(pid+0.635, 2*hPIDpart.GetMaximum(), pname)
        label.SetTextColor(kBlack)
    else:
        label = TLatex(pid+0.635, 1.5*hPIDpart.GetMinimum(), pname)
        label.SetTextColor(kYellow)
        label.SetTextSize(0.032)
        label.SetTextFont(42)
        label.SetTextAngle(90)
        label.Draw()

    gPad.Update()
    c1.Update()
    
    c1.cd()
    from ROOT import TPaveText
    import os
    filename = os.path.splitext(os.path.basename(datafile))[0]
    flabel = filename.replace('_', ' ')
    title_text = f"Beam Analysis: {flabel}"
    title = TPaveText(0.2, 0.94, 0.8, 0.99, "NDC")
    title.AddText(title_text)
    title.SetTextAlign(22)
    title.SetTextSize(0.04)
    title.SetFillColor(0)
    title.SetBorderSize(0)
    title.Draw()
    
    c1.Modified()
    c1.Update()

    c1.SaveAs("Simulation_Plot_%s.png" % (pname))

    input("Press enter to quit...")

    return hETot, hVxVy, hETotTheta, hPID, hPIDpart

if __name__ == "__main__":
    try:
        datafile  = sys.argv[1]
    except IndexError:
        print('WARNING: arguments are missing')
        print('USAGE: python3 %s <imput_file>' % (sys.argv[0].split('/')[-1]) )
        sys.exit()

    except IOError or ValueError:
        print('WARNING: input file missing')
        print('cannot open file: %s', sys.argv[1])
        print('USAGE: python3 %s <input_file>' % (sys.argv[0].split('/')[-1]) )
        sys.exit()

    fin = TFile(datafile, "READ")
    evnts = fin.Get("Events")

    outfile = datafile.replace(".root", "_plots.root")
    fout = TFile(outfile,"RECREATE")
    fout.cd()

    pids = [5, 6, 7, 8, 10, 11, 27, 28]
    particles = ['neutrino_e', 'anti_neutrino_e', 'photon', 'neutron', 'muon+', 'muon-', 'nueutrino_m', 'anti_neutrino_m']
    particle_ids = dict(zip(pids, particles))

    for pid, particle in particle_ids.items():
        hETot, hVxVy, hETotTheta, hPID, hPIDpart = process_events(evnts, pid, particle, 7450, 100)
        fout.mkdir(particle)
        fout.cd(particle)
       
        hETot.Write()
        hVxVy.Write()
        hETotTheta.Write()
        hPID.Write()
        hPIDpart.Write()
        
        del hETot, hVxVy, hETotTheta, hPID, hPIDpart
        
    fout.Close()
    fin.Close()