import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'fitSquareWave'))
import squareWaveFit as SWF
import scientificPlot as splt
import utils as u
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse

def readFlags():
    p = argparse.ArgumentParser()
    p.add_argument('-path', type = str, default = "")
    p.add_argument('-folder', type = str, default = "")
    p.add_argument('-datamain', type = str, default = "data.main")
    p.add_argument('-particle', type = str, default = "All")
    p.add_argument('-showFit', type = str, default = "False")
    options = p.parse_args()
    showFit = False
    if (len(options.path)>0):
        options.folder = options.path + "/" + options.folder
        options.datamain = options.path + "/" + options.datamain
    if options.showFit == 'True' or options.showFit == 'true':
        showFit = True
    return options.folder, options.datamain, options.particle, showFit

# Ask for a folder where search for the files
def askFolder():
    folder = input("Where do you want to get the file(s)?\n")
    return folder

# Read input parameter
def readInputs(filename = "data.main"):
    inputs = u.readInputFile(filename, inputs = ["jumpWeight", "minJump", "minDuration"],
                             optionalInputs = ["plotFits", "nPointsSmooth"])

    jumpWeight = inputs["jumpWeight"]
    minJump = inputs["minJump"]
    minDuration = inputs["minDuration"]
    plotFits = True
    nPoitnsSmooth = -1
    if "plotFits" in inputs.keys():
        plotFits = bool(inputs["plotFits"])
    if "nPointsSmooth" in inputs.keys():
        nPointsSmooth = inputs["nPointsSmooth"]
    return jumpWeight, minJump, minDuration, plotFits, nPointsSmooth

def runFitting(folder, particle, jumpWeight, minJump, minDuration, plotFits, nPointsSmooth, showFits):
    if particle == "All":
        paramsFile = open(folder+"Fits/fittedParams_"+str(jumpWeight)+".txt",'w')
        files = os.listdir(folder)
        for file in files:
            # Change the conditional depending on the format of the input files
            if ".txt" in file and "particle_" in file and "#" not in file and "~" not in file:
                #print(file)
                # Fit the intensity of the file
                params, intensity = SWF.fitParticle(folder, filename = file,
                                                    jumpWeight = jumpWeight, minJump = minJump,
                                                    npointsSmooth = nPointsSmooth, minDuration = minDuration)

                #Write the parameters to a file
                paramsFile.write(" ".join(u.ntos(params))+"\n")

                #Plot the fit
                if plotFits:
                    time, particle, background = SWF.readData(folder, file = file)
                    ax = None
                    ax = splt.plot(time/1000, SWF.smoothIntensity(particle,1), label = "Particle")
                    ax = splt.plot(time/1000, intensity, ax, label = "Fit")
                    ax.set_xlabel("Time (s)")
                    ax.set_ylabel("Intensity (A. U.)")
                    ax.legend()
                    nameFig = file.replace("txt","")
                    splt.saveFig(nameFig, folder = folder+"Fits")
                    if showFits:
                        splt.show()
                    plt.close()
        paramsFile.close()

    else:
        if particle.isnumeric():
            file = "particle_"+particle+".txt"
        else:
            file = particle
        paramsFile = open(folder+"Fits/fittedParams_"+file,'w')
        params, intensity = SWF.fitParticle(folder, filename = file,
                                            jumpWeight = jumpWeight, minJump = minJump,
                                            npointsSmooth = nPointsSmooth, minDuration = minDuration)

        #Write the parameters to a file
        paramsFile.write(" ".join(u.ntos(params))+"\n")

        #Plot the fit
        if plotFits:
            time, particleIntensity, background = SWF.readData(folder, file = file)
            ax = None
            ax = splt.plot(time/1000, SWF.smoothIntensity(particleIntensity,1), label = "Particle")
            ax = splt.plot(time/1000, intensity, ax, label = "Fit")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Intensity (A. U.)")
            ax.legend()
            nameFig = file.replace("txt","")
            splt.saveFig(nameFig, folder = folder+"Fits")
            if showFits:
                splt.show()
            plt.close()
        paramsFile.close()
    


        
if __name__ == "__main__":
    folder, datamain, particle, showFit = readFlags()
    if len(folder) == 0:
        folder = askFolder()
    jumpWeight, minJump, minDuration, plotFits, nPointsSmooth = readInputs(datamain)
    # Create a folder where saving the fits and the fitting parameters
    os.makedirs(folder+"Fits", exist_ok=True)
    runFitting(folder, particle, jumpWeight, minJump, minDuration, plotFits, nPointsSmooth, showFit)



