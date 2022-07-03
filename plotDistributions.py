import utils as u
#import scientificPlot as splt
import matplotlib.pyplot as plt
import numpy as np

def askFolder():
    folder = input("Where do you want to get the file(s)?\n")
    return folder

filename = "allParams.txt"
folder = askFolder()
file = open(filename)
intensities = []
times_all = []
times_0 = [] #Times without 0

for line in file:
    params = u.stof(line.strip().split(" "))
    if len(params) == 1:
        continue
    intensities+=[params[1]-params[0]]
    for i in range(1,int(len(params)/2)):
        times_all+=[params[2*i+1]]
        if params[2*i]>0:
            times_0+=[params[2*i+1]]
fileTime = open("allTimes.data", "w")
fileTime_0 = open("allTimes_sin0.data", "w")
fileIntensity = open("allIntensities.data", "w")

for dI in intensities:
    fileIntensity.write(str(dI)+"\n")

for ton in times_all:
    fileTime.write(str(ton)+"\n")

for ton in times_0:
    fileTime_0.write(str(ton)+"\n")

times_all = np.array(times_all)
times_0 = np.array(times_0)
#print("Mean time with 0: "+str(np.mean(times_all[np.where(times_all<3000)]))+ " ms")
#print("Mean time without 0: "+str(np.mean(times_0[np.where(times_0<3000)]))+ " ms")
print("Mean time with 0: "+str(np.mean(times_all))+ " ms")
print("Mean time without 0: "+str(np.mean(times_0))+ " ms")
print("Mean Intensity: "+str(np.mean(intensities)))

plt.figure(1)
plt.hist(intensities, bins = 20)
plt.title("Intensities")
plt.ylabel("Number of ocurrences")
plt.xlabel("Intensity (A. U.)")
plt.figure(2)
plt.hist(times_all[np.where(times_all<3000)], bins = 15)
plt.title("All times")
plt.ylabel("Number of ocurrences")
plt.xlabel(r"$\tau_{on}$ (ms)")
plt.figure(3)
plt.hist(times_0[np.where(times_0<3000)], bins = 15)
plt.title("Times without 0")
plt.ylabel("Number of ocurrences")
plt.xlabel(r"$\tau_{on}$ (ms)")

plt.show()
