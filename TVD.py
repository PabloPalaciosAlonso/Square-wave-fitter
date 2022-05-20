from TVDCondat2013 import TVD
import scientificPlot as splt
import matplotlib.pyplot as plt
import utils as u
from scipy import optimize
import numpy as np

time = []
particleIntensity = []
backgroundIntensity = []
denoisedIntensity = []
fitDenoisedIntensity = []

#Ask for which particle the user wants to fit
def askParticle():
    particleId = int(input("Which particle do you want to fit?\n"))
    return particleId

# Import intensities of a particle and correct the background
def readData(folder, file = None, particleId = None):
    filename = file
    if filename is None:
        if particleId is None:
            particleId = askParticle()
        filename = "particle_"+str(particleId)+".txt"
    data = u.readMatrix(filename, folder = folder, remove = 3, delimiter = "   ")
    time = data[:,1]
    particle = data[:,2]
    background = data[:,3]
    fit = u.least_squares(time,background)
    background-=time*fit[0]+fit[1]
    particle-=time*fit[0]+fit[1]
    return time, particle, background

#Square wave function with arbitrary number of steps
def squareWave(params, nFrames):
    """
    params[0] = basline
    params[1] = dI
    params[2*n (n>0)] = start of the n on state
    params[2*n+1 (n>0)] = duration of the n on state
    """
    sw = np.ones(nFrames)*params[0]
    for i in range(1,int(len(params)/2)):
        if (2*i+1)<(len(params)):
            sw[round(params[2*i]):round(params[2*i]+params[2*i+1])] = params[1]
        else:
            sw[round(params[2*i]):] = params[1]
    return sw 

# Given a set of intensities a baseline and an excitation energy returns a fit of the intensities such that
# if the distance between intensity[i] and the baseline is smaller than the distance between intensity[i] and
# dI, fitIntensity[i] = baseline, and if not fitIntensity[i] = dI
def squareWaveDistance(intensity, baseline, dI):
    fitIntensity = np.ones(len(intensity))*baseline
    diff = (intensity-dI)**2-(intensity-baseline)**2
    fitIntensity[np.where(diff<0)] = dI
    return fitIntensity

# Computes error[i] = min((intensity-baseline)^2, (intensity-dI)^2)
def errorFunctionFilteredIntensities(params):
    errorUpDown = np.zeros((2,len(particleIntensity)))
    errorUpDown[0,:] = (denoisedIntensity-params[0])**2
    errorUpDown[1,:] = (denoisedIntensity-params[1])**2
    error = np.min(errorUpDown, axis = 0)
    return error

# Computes the distance for each point between a set of intensities and a square wave
def dist_SquareWave_ParticleIntensities(params):
    return squareWave(params, len(particleIntensity))-particleIntensity

# Given a set of intensities forming a square wave returns the parameters of the square wave
def getParamsOfSquareWave(intensities, baseline, dI):
    params = []
    params+=[baseline, dI]
    lastInt = baseline
    for i in range(len(intensities)):
        newInt = intensities[i]
        if newInt>lastInt: # New jump
            params+=[i]
        elif newInt<lastInt:
            params+=[i-params[-1]]
        lastInt = newInt
    return params

"""
Principal function, reads the intensity of a particle and fit it in three steps:
   First: Denoise the intensities using the TVD algorithm
   Second: Fit the denoised intensity to a square wave 
   Third: From the square wave obtained in step 2 uses the lm algorithm to fit the square wave
          that best fits the intensity of the particle
"""
def fitParticle(folder, particleId=None, filename = None, jumpWeight = 5000):
    global time, particleIntensity, background, denoisedIntensity
    time, particleIntensity, background = readData(folder, particleId)
    denoisedIntensity = TVD(particleIntensity, jumpWeight)
    fit1 = optimize.root(errorFunctionFilteredIntensities, [min(denoisedIntensity), max(denoisedIntensity)], method = 'lm')
    [baselineFit1, dIFit1] = fit1.x
    fitDenoisedIntensity = squareWaveDistance(denoisedIntensity, baselineFit1, dIFit1)
    params = getParamsOfSquareWave(fitDenoisedIntensity, baselineFit1, dIFit1)
    fit2 = optimize.least_squares(dist_SquareWave_ParticleIntensities, params, method = "lm")
    fittedParams = fit2.x
    if fit2.x[1]<np.std(particleIntensity):
        fittedParams = [np.mean(particleIntensity)]
    return fittedParams, squareWave(fittedParams, len(particleIntensity))
