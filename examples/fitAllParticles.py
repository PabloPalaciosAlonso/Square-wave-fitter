import sys
sys.path.insert(0, '../src')
import squareWaveFit as SWF
import scientificPlot as splt
import utils as u
import numpy as np
import os
import matplotlib.pyplot as plt

def askFolder():
    folder = input("Where do you want to get the file(s)?\n")
    return folder

# Read input parameter
inputs = u.readInputFile("data.main", inputs = ["jumpWeight", "minJump"],
                       optionalInputs = ["plotFits", "nPointsSmooth"])

jumpWeight = inputs["jumpWeight"]
minJump = inputs["minJump"]
plotFits = True
nPoitnsSmooth = -1
if "plotFits" in inputs.keys():
    plotFits = bool(inputs["plotFits"])
if "nPointsSmooth" in inputs.keys():
    nPointsSmooth = inputs["nPointsSmooth"]
    
# Ask for a folder where search for the files
folder = askFolder()
files = os.listdir(folder)

# Create a folder where save the fits and the fitting parameters
os.makedirs(folder+"Fits", exist_ok=True)
paramsFile = open(folder+"Fits/fittedParams.txt",'w')
intensities = []
onTimes = []
for file in files:
    # Change the conditional depending on the format of the input files
    if ".txt" in file and "particle_" in file:
        print(file)

        # Fit the intensity of the file
        params, intensity = SWF.fitParticle(folder, filename = file, jumpWeight = jumpWeight, minJump = minJump)

        #Write the parameters to a file
        paramsFile.write(" ".join(u.ntos(params))+"\n")

        #Plot the fit
        if plotFits:
            time, particle, background = SWF.readData(folder, file = file)
            ax = None
            ax = splt.plot(time/1000, SWF.smoothIntensity(particle,3), label = "Particle")
            ax = splt.plot(time/1000, intensity, ax, label = "Fit")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Intensity (A. U.)")
            ax.legend()
            nameFig = file.replace("txt","")
            splt.saveFig(nameFig, folder = folder+"Fits")
            plt.close()
paramsFile.close()

