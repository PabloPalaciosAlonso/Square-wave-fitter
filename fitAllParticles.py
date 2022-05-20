import TVD
import scientificPlot as splt
import utils as u
import numpy as np
import os
import matplotlib.pyplot as plt
def askFolder():
    folder = input("Where do you want to get the file?\n")
    return folder

jumpWeight = 5000
folder = askFolder()
files = os.listdir(folder)
os.makedirs(folder+"Fits", exist_ok=True)
paramsFile = open(folder+"Fits/fittedParams.txt",'w')
intensities = []
onTimes = []
for file in files:
    if ".txt" in file and "particle_" in file:
        print(file)
        params, intensity = TVD.fitParticle(folder, file, jumpWeight)
        time, particle, background = TVD.readData(folder, file = file)
        ax = None
        ax = splt.plot(time/1000, particle, label = "Particle")
        ax = splt.plot(time/1000, intensity, ax, label = "Fit")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Intensity (A. U.)")
        ax.legend()
        nameFig = file.replace("txt","")
        splt.saveFig(nameFig, folder = folder+"Fits")
        plt.close()
        paramsFile.write(" ".join(u.ntos(params))+"\n")
        if len(params)>1:
            intensities+=[params[1]-params[0]]
            for i in range(1,round(len(params)/2)):
                if params[i]==0:
                    continue
                if 2*i+1==len(params):
                    continue
                onTimes+=[params[2*i+1]]
paramsFile.close()
plt.figure(99)
plt.hist(intensities, bins = 15)
plt.show()
