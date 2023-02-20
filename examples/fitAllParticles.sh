#Example of how to use the program fitIntensity.py.
#The options that can be provided to the program are:
#    - folder: Folder where all the files are stored, by default it will take the current folder
#    - particle: The particle to fit, use 'All' to fit all the particles in the folder
#    -datamain: Name of the file with the data, by default data.main
#    -path: Path to the folder where is contained the data.main file and the folder with the measurements
#    -showfit: (True or False) specify if you want to show the fit while the program is running. 

#The data.main file must contain:
#    -jumpWeight: Paramter that 
#    -minJump: Min jump intensity in units of the standard deviation of the background
#    -plotFits: (True or False). Plotting the fits is very time consuming
#    -minDuration: Minimum duration in frames of the jump
#    -nPointsSmooth: Not tested, better to use 1

python ../src/utils/fitIntensity.py -folder measurements -particle All -datamain data.main
