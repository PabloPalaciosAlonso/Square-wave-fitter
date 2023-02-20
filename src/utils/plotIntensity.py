import utils as u
import scientificPlot as splt
import os
import matplotlib.pyplot as plt
import numpy as np
import argparse

def readFlags():
    p = argparse.ArgumentParser()
    p.add_argument('-path', type = str, default = "")
    p.add_argument('-folder', type = str, default = "")
    p.add_argument('-particle', type = str, default = "All")
    p.add_argument('-simulation', type = str, default = "False")
    options = p.parse_args()
    if (len(options.path)>0):
        options.folder = options.path + "/" + options.folder
    plotSimulation = False
    if options.simulation == "True" or options.simulation == "true":
        plotSimulation = True
    return options.folder, options.particle, plotSimulation


# Ask for a folder where search for the files
def askFolder():
    folder = input("Where do you want to get the file(s)?\n")
    return folder

def plotIntensities(folder, particle, simulation):
    if particle == "All":        
        files = os.listdir(folder)
        for filename in files:
            if ".txt" in filename and "particle_" in filename and "#" not in filename and "~" not in filename:
                print(filename)
                data = u.readMatrix(filename, folder = folder, remove = 3, delimiter = "   ")
                time = data[:,1]
                particleIntensity = data[:,2]
                background = data[:,3]
                fit = u.least_squares(time,background)
                background-=time*fit[0]+fit[1]
                particleIntensity-=time*fit[0]+fit[1]
                ax = splt.plot(time/1000, particleIntensity, label = "Particle")
                ax = splt.plot(time/1000, background, ax, linewidth = 1, label = "background")
                if simulation:
                    denoised = data[:,4]
                    ax = splt.plot(time/1000, denoised, ax, linewidth = 1.5, label = "Denoised")
                ax.legend()
                ax.set_xlabel("Time (s)")
                ax.set_ylabel("Intensity")
                splt.saveFig(ax = ax, name = filename.replace(".txt",""), folder = folder)
                plt.close()
    else:
        if particle.isnumeric():
            filename = "particle_"+particle+".txt"
        else:
            filename = particle
        data = u.readMatrix(filename, folder = folder, remove = 3, delimiter = "   ")
        time = data[:,1]
        particleIntensity = data[:,2]
        background = data[:,3]
        fit = u.least_squares(time,background)
        background-=time*fit[0]+fit[1]
        particleIntensity-=time*fit[0]+fit[1]
        ax = splt.plot(time/1000, particleIntensity, label = "Particle")
        ax = splt.plot(time/1000, background, ax, linewidth = 1, label = "background")
        if simulation:
            denoised = data[:,4]
            ax = splt.plot(time/1000, denoised, ax, linewidth = 1.5, label = "No noise")
        ax.legend()
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Intensity")
        splt.show(ax = ax, name = filename.replace(".txt",""), folder = folder)

        
if __name__ == "__main__":
    folder, particle, simulation = readFlags()
    if len(folder) == 0:
        folder = askFolder()
    plotIntensities(folder, particle, simulation)
