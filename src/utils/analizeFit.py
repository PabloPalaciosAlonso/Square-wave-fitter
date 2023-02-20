import sys
sys.path.insert(0, '../fitSquareWave')
import scientificPlot as splt
import utils as u
import numpy as np
import os
import matplotlib.pyplot as plt
import argparse

def readFlags():
    p = argparse.ArgumentParser()
    p.add_argument('-saveFigs', type = str, default = "True")
    p.add_argument('-density', type = str, default = "True")
    p.add_argument('-path', type = str, default = "")
    p.add_argument('-folder', type = str, default = "")
    p.add_argument('-filename', type = str, default = "fittedParams.txt")
    p.add_argument('-plotInfo', type = str, default = "")
    ops = p.parse_args()
    if len(ops.path)>0:
        if len(ops.folder)>0:
            ops.folder = ops.path + "/" + ops.folder
    if len(ops.plotInfo)>0:
        if len(ops.folder)>0:
                ops.plotInfo = ops.folder + "/" + ops.plotInfo
        elif len(ops.path)>0:
            ops.plotInfo = ops.path + "/" + ops.plotInfo
    if ops.saveFigs == "False" or ops.saveFigs == "false": #Argparse doesn't like bool
        saveFigs = False
    else:
        saveFigs = True
    if ops.density == "False" or ops.density == "false": #Argparse doesn't like bool
        density = False
    else:
        density = True
    return ops.folder, ops.filename, saveFigs, density, ops.plotInfo


def readPlotInfo(folder, filename):
    optionalInputs = ["nbinsBaseLine", "nbinsdI", "nbinsTimeOnAll",
                      "nbinsTimeOnNL", "nbinsTimeOff",
                      "minJump", "maxJump", "minTimeOn", "maxTimeOn", "minTimeOff",
                      "maxTimeOff"]
    default = [15, 50, 50, 50, 50, 0, -1, 0, -1, 0, -1]
    if len(filename)==0:
        info = dict(zip(optionalInputs, default))
    else:
        info = u.readInputFile(filename, optionalInputs = optionalInputs, default = default)
    return info

def askFolder():
    folder = input("Where are the fitting parameters?\n")
    return folder

def removeOutOfRange(data, validRange):
    data = data[np.where(data>validRange[0])]
    if validRange[1]>0:
        data = data[np.where(data<validRange[1])]
    return data
    
def readFittedParams(folder, filename, maxJump = 1e15):
    baseline = []
    dI = []
    timeOnAll = []
    timeOff = []
    timeOnNotLast = []
    numberJumps = []
    timeAfter = []
    if len(folder)>0:
        file = open(folder+"/"+filename, "r")
    else:
        file = open(filename, 'r')
    for line in file:
        data = line.strip().split(" ")
        baseline += [float(data[0])]
        nJumps = int((len(data)-2)/2)
        numberJumps += [nJumps]
        if nJumps>0: #More than one jump
            dI_i = float(data[1])
            if dI_i>maxJump:
                continue
            for i in range(nJumps-1):
                timeOnAll += [float(data[2+i*2+1])]
                timeOnNotLast += [float(data[2+i*2+1])]
                timeOff_i = float(data[2+2*i+2])-(float(data[2+2*i])+float(data[2+2*i+1]))
                timeOff += [timeOff_i]
            dI += [float(data[1])]
            timeOnAll+=[float(data[nJumps*2+1])]
            timeAfter +=[3.3416000e+04-float(data[nJumps*2+1])-float(data[nJumps*2])]
    return np.array(baseline), np.array(dI), np.array(timeOnAll), np.array(timeOnNotLast), np.array(timeOff), np.array(timeAfter), np.array(numberJumps)

def plotBaseline(saveFig, folder, baseline, bins, density):
    fig, ax = splt.initializeFigure()
    ax.hist(baseline, edgecolor = "k",
            bins = bins, linewidth=2,
            density = density)
    ax.set_xlabel("Base Intensity (A. U.)")
    if density:
        ax.set_ylabel("Frequency")
    else:
        ax.set_ylabel("Repetitions")
    if saveFig:
        splt.saveFig(name = "baseline", folder = folder)
    else:
        plt.tight_layout()
        plt.show()

        
def plotdI(saveFig, folder, dI, dIRange, bins, density):
    fig, ax = splt.initializeFigure()
    ax.hist(dI, edgecolor = "k",
            bins = bins, linewidth=2,
            density = density)
    ax.set_xlabel("$\Delta I$ (A. U.)")
    if density:
        ax.set_ylabel("Frequency")
    else:
        ax.set_ylabel("Repetitions")
    if saveFig:
        splt.saveFig(name = "jumpSize", folder = folder)
    else:
        plt.tight_layout()
        plt.show()

def plotTimeOnAll(saveFig, folder, timeOn, timeOnRange, bins, density):
    fig, ax = splt.initializeFigure()
    ax.hist(timeOn, edgecolor = "k",
            bins = bins, linewidth=2,
            density = density)
    ax.set_xlabel("Time On All(ms)")
    #ax.set_yscale("log")
    if density:
        ax.set_ylabel("Frequency")
    else:
        ax.set_ylabel("Repetitions")
    if saveFig:
        splt.saveFig(name = "Time_On_All", folder = folder)
    else:
        plt.tight_layout()
        plt.show()

def plotTimeOnNotLast(saveFig, folder, timeOn, timeOnRange, bins, density):
    fig, ax = splt.initializeFigure()
    ax.hist(timeOn, edgecolor = "k",
            bins = bins, linewidth=2,
            density = density)
    ax.set_xlabel("Time On Not Last(ms)")
    #ax.set_yscale("log")
    if density:
        ax.set_ylabel("Frequency")
    else:
        ax.set_ylabel("Repetitions")
    if saveFig:
        splt.saveFig(name = "Time_On_Not_Last", folder = folder)
    else:
        plt.tight_layout()
        plt.show()

def plotTimeOff(saveFig, folder, timeOff, timeOffRange, bins, density):
    fig, ax = splt.initializeFigure()
    ax.hist(timeOff, edgecolor = "k",
            bins = bins, linewidth=2,
            density = density)
    #ax.set_yscale("log")
    ax.set_xlabel("Time Off(ms)")
    if density:
        ax.set_ylabel("Frequency")
    else:
        ax.set_ylabel("Repetitions")
    if saveFig:
        splt.saveFig(name = "Time_Off", folder = folder)
    else:
        plt.tight_layout()
        plt.show()

def plotNumberJumps(saveFig, folder, numberJumps, density):
    bins = range(1,max(numberJumps)+2)
    fig, ax = splt.initializeFigure()
    ax.hist(numberJumps, edgecolor = "k",
            bins = bins, linewidth=2,
            density = density, align='left')
    ax.set_xlabel("Number jumps")
    if density:
        ax.set_ylabel("Frequency")
    else:
        ax.set_ylabel("Repetitions")
    if saveFig:
        splt.saveFig(name = "NumberJumps", folder = folder)
    else:
        plt.tight_layout()
        plt.show()

def writeResumeFitting(folder, baseline, dI, timeOnAll, timeOnNL, timeOff):
    filename = "ProcessedData.txt"
    if len(folder)>0:
        filename = folder + "/" + filename
    file = open(filename, "w")
    file.write("Mean baseline: "+ str(np.mean(baseline))+"\n")
    file.write("Standard deviation baseline: "+ str(np.std(baseline))+"\n")
    file.write("Mean dI: "+ str(np.mean(dI))+"\n")
    file.write("Standard deviation dI: "+ str(np.std(dI))+"\n")
    file.write("Mean time on all: "+ str(np.mean(timeOnAll))+" ms\n")
    file.write("Standard deviation time on all: "+ str(np.std(timeOnAll))+" ms\n")
    file.write("Mean time on not last: "+ str(np.mean(timeOnNL))+" ms\n")
    file.write("Standard deviation time on not last: "+ str(np.std(timeOnNL))+" ms\n")
    file.write("Mean time off: "+ str(np.mean(timeOff))+"\n")
    file.write("Standard deviation time off: "+ str(np.std(timeOff))+"\n")

if __name__ == "__main__":
    splt.setFormatPlot()
    folder, filename, saveFigs, density, filePlotInfo = readFlags()
    plotInfo = readPlotInfo(folder, filePlotInfo)
    dIRange = (plotInfo["minJump"], plotInfo["maxJump"])
    timeOnRange = (plotInfo["minTimeOn"], plotInfo["maxTimeOn"])
    timeOffRange = (plotInfo["minTimeOff"], plotInfo["maxTimeOff"])
    if len(folder) == 0:
        folder = askFolder()
    baseline, dI, timeOnAll, timeOnNL, timeOff, numberJumps = readFittedParams(folder, filename)
    dI = removeOutOfRange(dI, dIRange)
    timeOnRange = (0,2000)
    timeOnNLRange = (0,2000)
    timeOnAll = removeOutOfRange(timeOnAll, timeOnRange)
    timeOnNL = removeOutOfRange(timeOnNL, timeOnRange)
    timeOff = removeOutOfRange(timeOff, timeOffRange)
    plotBaseline(saveFigs, folder, baseline, int(plotInfo["nbinsBaseLine"]), density)
    plotdI(saveFigs, folder, dI, dIRange, int(plotInfo["nbinsdI"]), density)
    plotTimeOnAll(saveFigs, folder, timeOnAll, timeOnRange, int(plotInfo["nbinsTimeOnAll"]), density)
    plotTimeOnNotLast(saveFigs, folder, timeOnNL, timeOnRange, int(plotInfo["nbinsTimeOnNL"]), density)
    plotTimeOff(saveFigs, folder, timeOff, timeOffRange, int(plotInfo["nbinsTimeOff"]), density)
    plotNumberJumps(saveFigs, folder, numberJumps, density)
    writeResumeFitting(folder, baseline, dI, timeOnAll, timeOnNL, timeOff)
