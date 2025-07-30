from ROOT import (RDataFrame, EnableImplicitMT, TFile, TLegend, gPad, TCanvas, gROOT)
from ROOT import kBlue, kYellow, kRed
from math import acos
from sys import exit
import sys
import re

gROOT.SetBatch(True)

EnableImplicitMT()

def canvas_prep():

    c1 = TCanvas("c1","The Muon Beam Simulation",10,10,1200,700)

    c1.Divide(1, 2) # 1 column, 2 rows

    pad1 = c1.cd(1) # Activate the first pad (top row)
    pad1.Divide(2, 1) # Divide the first pad into 3 columns, 1 row

    pad2 = c1.cd(2) # Activate the second pad (bottom row)
    pad2.Divide(3, 1) # Divide the second pad into 2 columns, 1 row

    p11 = pad1.cd(1)
    p12 = pad1.cd(2)
    p21 = pad2.cd(1)
    p22 = pad2.cd(2)
    p23 = pad2.cd(3)

    return c1, p11, p12, p21, p22, p23


def display_plots(hists):

    c1, p11, p12, p21, p22, p23 = canvas_prep()

    p22.cd()
    hpids.Draw()
    hpids.SetXTitle("Particle ID")
    p22.SetLogy()
    particle_hists[current_key][0].Draw("same")

    legend1 = TLegend(0.75, 0.80, 0.875, 0.865)  # (x1, y1, x2, y2)
    legend1.AddEntry(particle_hists[current_key][0].GetName(), "%s" % (particle_hists[current_key][0].GetName()), "f")
    legend1.Draw()

    p23.cd()
    hVzs.Draw()
    hVzs.SetXTitle("Particle's track z position [cm]")
    p23.SetLogy()
    particle_hists[current_key][1].Draw("same")

    legend2 = TLegend(0.75, 0.80, 0.875, 0.865)  # (x1, y1, x2, y2)
    legend2.AddEntry(particle_hists[current_key][1].GetName(), "%s" % (particle_hists[current_key][1].GetName()), "f")
    legend2.Draw()

    p11.cd()
    particle_hists[current_key][2].Draw("surf2z")
    particle_hists[current_key][2].SetXTitle("Vx")
    particle_hists[current_key][2].SetYTitle("Vy")
    particle_hists[current_key][2].SetStats(0)

    p12.cd()
    particle_hists[current_key][3].Draw("colz")
    particle_hists[current_key][3].SetXTitle("Energy [GeV]")
    particle_hists[current_key][3].SetYTitle("Scattering Angle [deg]")
    particle_hists[current_key][3].SetStats(0)

    p21.cd()
    particle_hists[current_key][4].Draw()
    particle_hists[current_key][4].SetXTitle("Total Energy [GeV]")
    particle_hists[current_key][4].SetStats(0)
    p21.SetLogy()


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
sampling_plane_z = 7400
sampling_plane_zwindow = 400


pids = [10, 11, 5, 6, 27, 28, 8, 7]
particles = ['\\mu^+', '\\mu^-', '\\nu_e', '\\bar{\\nu}_e', '\\nu_{\\mu}', '\\bar{\\nu}_{\\mu}', 'n', '\\gamma']

particle_ids = dict(zip(particles, pids))
events_df = RDataFrame("Events", datafile)
events_df = events_df.Define('theta', 'acos(Cz) * 180/3.1415926535')
events_df = events_df.Filter("abs(Vz-%s)<=%s" % (sampling_plane_z, sampling_plane_zwindow))
hpids = events_df.Histo1D(("pids", "Particle IDs In Simulation", 31, 0., 31), "ParticleID")
hpids.SetStats(0)
hVzs = events_df.Histo1D(("hVzs","Vertex Location along Beam Direction (Vz)",250, 6800, 7800), "Vz")
hVzs.SetStats(0)

particle_dfs = {}
particle_hists = {}
for pname, pid in particle_ids.items():
    particle_dfs[pname] = events_df.Filter("ParticleID==%s" % (pid))
    particle_hists[pname] = [particle_dfs[pname].Histo1D(("%s" % (pname), "Particle IDs", 31, 0., 31), "ParticleID")]
    particle_hists[pname][0].SetFillColor(kBlue)
    particle_hists[pname].append(particle_dfs[pname].Histo1D(("%s" % (pname), "Vz",250, 6800, 7800), "Vz"))
    particle_hists[pname][1].SetFillColor(kRed)
    particle_hists[pname].append(particle_dfs[pname].Histo2D(("%s" % (pname), "Vx vs. Vy", 400, -100, 100, 400, -100, 100), "Vx", "Vy"))
    particle_hists[pname].append(particle_dfs[pname].Histo2D(("%s" % (pname), "Energy vs. Scaterring Angle", 200, 0, 10, 180, 0, 30), "ETot", "theta"))
    particle_hists[pname].append(particle_dfs[pname].Histo1D(("%s" % (pname), "Particle Energy",200, 0, 11), "ETot"))


outfile = datafile.replace(".root", "_plots.root")
fout = TFile(outfile,"RECREATE")
fout.cd()

for current_key in particle_ids.keys():

    c1, p11, p12, p21, p22, p23 = canvas_prep()

    p22.cd()

    hpids.Draw()
    hpids.SetXTitle("Particle ID")
    p22.SetLogy()
    particle_hists[current_key][0].Draw("same")

    legend1 = TLegend(0.75, 0.80, 0.875, 0.865)  # (x1, y1, x2, y2)
    legend1.AddEntry(particle_hists[current_key][0].GetName(), "%s" % (particle_hists[current_key][0].GetName()), "f")

    legend1.Draw()

    p23.cd()
    hVzs.Draw()
    hVzs.SetXTitle("Particle's track z position [cm]")
    p23.SetLogy()
    particle_hists[current_key][1].Draw("same")

    legend2 = TLegend(0.75, 0.80, 0.875, 0.865)  # (x1, y1, x2, y2)
    legend2.AddEntry(particle_hists[current_key][1].GetName(), "%s" % (particle_hists[current_key][1].GetName()), "f")

    legend2.Draw()

    p11.cd()
    particle_hists[current_key][2].Draw("surf2z")
    particle_hists[current_key][2].SetXTitle("Vx")
    particle_hists[current_key][2].SetYTitle("Vy")
    particle_hists[current_key][2].SetStats(0)


    p12.cd()
    particle_hists[current_key][3].Draw("colz")
    particle_hists[current_key][3].SetXTitle("Energy [GeV]")
    particle_hists[current_key][3].SetYTitle("Scattering Angle [deg]")
    particle_hists[current_key][3].SetStats(0)


    p21.cd()
    particle_hists[current_key][4].Draw()
    particle_hists[current_key][4].SetXTitle("Total Energy [GeV]")
    particle_hists[current_key][4].SetStats(0)
    p21.SetLogy()

    fname = datafile.split('.root')[0]
    current_key_pm = re.sub('-', 'minus', current_key)
    current_key_no_specials = re.sub(r'[^a-zA-Z0-9]', '', current_key_pm)
    c1.SaveAs("%s_%s.png" % (fname, current_key_no_specials))

    # Uncomment lines below to enable checking the plots out...
    ans = input("Press y to proceed, n to quit...")
    if ans == 'n':
        exit()
    del c1

    fout.mkdir(current_key_no_specials)
    fout.cd(current_key_no_specials)

    for hist in particle_hists[current_key]:
        hist.Write()

fout.Close()
