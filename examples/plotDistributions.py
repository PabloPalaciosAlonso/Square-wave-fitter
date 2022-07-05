import utils as u
#import scientificPlot as splt
import matplotlib.pyplot as plt
import numpy as np

def askFolder():
    folder = input("Where do you want to get the file(s)?\n")
    return folder

filename = "fittedParams.txt"
folder = askFolder()
if len(folder)>0:
    filename = folder+"/"+filename
file = open(filename)

intensities = []
onTimes = []
for line in file:
    params = u.stof(line.strip().split(" "))
    if len(params) == 1: #No excitation detected
        continue
    intensities+=[params[1]-params[0]]
    for i in range(1,int(len(params)/2)):
        if params[2*i]>0:
            onTimes+=[params[2*i+1]]
            
fileTime = open("onTimes.data", "w")
fileIntensity = open("ExcitationIntensities.data", "w")

for dI in intensities:
    fileIntensity.write(str(dI)+"\n")

for ton in onTimes:
    fileTime.write(str(ton)+"\n")

onTimes = np.array(onTimes)

print("Mean on time: "+str(np.mean(onTimes))+ " ms")
print("Mean Intensity: "+str(np.mean(intensities)))

plt.figure(1)
plt.hist(intensities, bins = 25, edgecolor = "k")
plt.title("Intensities")
plt.ylabel("Number of ocurrences")
plt.xlabel("Intensity (A. U.)")

maxTime = 5000
plt.figure(2)
plt.hist(onTimes[np.where(onTimes<maxTime)], bins = 30, edgecolor = "k")
plt.yscale("log")
plt.title("On times")
plt.ylabel("Number of ocurrences")
plt.xlabel(r"$\tau_{on}$ (ms)")
plt.show()
