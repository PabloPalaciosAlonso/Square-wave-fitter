"""
Conjunto de funciones que facilitan hacer plots con matplotlib con un formato bonito

Recordatorio para mi yo del futuro: Para poner cosas en latex poner r'codsas $\mathregular{\mu}$'

Uso:

Primero inicializamos la figura
fig, ax = prepareFigure (datax, datay, Parameters) 

Y después pintamos normalmente

ax.plot(datax,datay,Parameters)

Si queremos dibujar más de una curva es necesario utilizar la función addData(datax,datay, majorDistanceX, majorDistanceY)

Los parámetros por defecto son:

   figsize = (7, 5),
   majorDistanceX = 0,
   majorDistanceY = 0,
   fontFamily = 'serif',
   fontSize = 18,
   axisLineWidth = 2,
   labelpad = '10',
   legendLocation = 'best',
   legendFrameOn = False,
   legendFontSize = 16

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from pylab import cm

nPlots = 0
def loadColormap():
     colors = cm.get_cmap('Paired')
     colorDict = {'bluel':colors(0),
                  'blued':colors(1),
                  'greenl':colors(2),
                  'greend':colors(3),
                  'redl':colors(4),
                  'redd':colors(5),
                  'orangel':colors(6),
                  'oranged':colors(7),
                  'purplel':colors(8),
                  'purpled':colors(9),
                  'black':"k",
                  0:colors(1),
                  1:colors(7),
                  2:colors(3),
                  3:colors(5),
                  4:colors(9),
                  5:colors(0),
                  6:colors(6),
                  7:colors(2),
                  8:colors(4),
                  9:colors(8),
                  10:"k"}
     return colorDict
     

def setFormatPlot(fontFamily = 'serif',
                  fontSize = 18,
                  axisLineWidth = 2,
                  labelpad = '10',
                  legendLocation = 'best',
                  legendFrameOn = False,
                  legendFontSize = 16):
     
     mpl.rcParams['font.family'] = fontFamily
     plt.rcParams['font.size'] = fontSize
     plt.rcParams['axes.linewidth'] = axisLineWidth
     plt.rcParams['xtick.major.pad'] = labelpad
     plt.rcParams['ytick.major.pad'] = labelpad
     plt.rcParams['legend.loc'] = legendLocation
     plt.rcParams['legend.frameon'] = legendFrameOn
     plt.rcParams['legend.fontsize'] = legendFontSize     
     
def initializeFigure(figsize = (7, 5)):
     fig = plt.figure(figsize=figsize)
     ax = plt.subplot(111)
     ax.xaxis.set_tick_params(which='major', size=10, width=2, direction='in', top='on')
     ax.xaxis.set_tick_params(which='minor', size=7, width=2, direction='in', top='on')
     ax.yaxis.set_tick_params(which='major', size=10, width=2, direction='in', right='on')
     ax.yaxis.set_tick_params(which='minor', size=7, width=2, direction='in', right='on')
     return fig,ax

def setXticks(ax, nminorticks = -1):
     ticks = ax.get_xticks()
     ticksDistance = ticks[1]-ticks[0]
     nticks = len(ticks)-2
     if nminorticks<0:
          nminorticks = 1
          #if nticks<=4:
               #nminorticks = 4
          if nticks>=7:
               nminorticks = 0
     minorDistance = ticksDistance/(nminorticks+1)
     ax.xaxis.set_minor_locator(mpl.ticker.MultipleLocator(minorDistance))
     xlim = ax.get_xlim()
     minx = xlim[0]
     firstMajor = ticks[1]
     firstMinor = firstMajor-minorDistance 
     """
     if firstMinor>minx: # El primer minor tick está antes del major
          dminor = firstMinor-minx
          if dminor<0.25*minorDistance:
               ax.set_xlim(firstMinor,xlim[1])
     elif firstMajor-minx<0.2*ticksDistance:
          ax.set_xlim(firstMajor,xlim[1])
     
     # Si el último major tick esta cerca del eje, ponemos el eje justo en el major tick
     xlim = ax.get_xlim()
     lastMajor = ticks[-2]
     if xlim[1]-lastMajor<0.2*ticksDistance:
          ax.set_xlim(xlim[0], lastMajor)
     """

def setYticks(ax):
     ticks = ax.get_yticks()
     ticksDistance = ticks[1]-ticks[0]
     nticks = len(ticks)-2
     nminorticks = 1
     #if nticks<=3:
          #nminorticks = 4
     if nticks>=7:
          nminorticks = 0
     minorDistance = ticksDistance/(nminorticks+1)
     ax.yaxis.set_minor_locator(mpl.ticker.MultipleLocator(minorDistance))

     ylim = ax.get_ylim()
     miny = ylim[0]
     firstMajor = ticks[1]
     firstMinor = firstMajor-minorDistance
     ax.set_yticks(ticks)
     """
     if firstMinor>miny: # El primer minor tick está antes del major
          dminor = firstMinor-miny
          if dminor<0.25*minorDistance:
               ax.set_ylim(firstMinor,ylim[1])
     elif firstMajor-miny<0.2*ticksDistance:
          ax.set_ylim(firstMajor,ylim[1])

     # Si el último major tick esta cerca del eje, ponemos el eje justo en el major tick
     ylim = ax.get_ylim()
     lastMajor = ticks[-2]
     if ylim[1]-lastMajor<0.2*ticksDistance:
          ax.set_ylim(ylim[0], lastMajor)
     """
def prepareFigure(x,y,
                  error = None,
                  figsize = (7, 5),
                  majorDistanceX = 0,
                  majorDistanceY = 0,
                  fontFamily = 'serif',
                  fontSize = 18,
                  axisLineWidth = 2,
                  labelpad = '10',
                  legendLocation = 'best',
                  legendFrameOn = False,
                  legendFontSize = 16):
     
     
     setFormatPlot(fontFamily,
                   fontSize,
                   axisLineWidth,
                   labelpad,
                   legendLocation,
                   legendFrameOn,
                   legendFontSize)
     
     fig, ax = initializeFigure(figsize)
     if error is None:
          ax.plot(x, y, linestyle='', color = 'white')
     else:
          ax.errorbar(x,y,error,linestyle='', color = 'white')
     setXticks(ax,majorDistanceX)
     setYticks(ax,majorDistanceY)
     return fig, ax

def addData(x,y,ax,
            error = None,
            majorDistanceX = 0,
            majorDistanceY = 0):
     if error is None:
          ax.plot(x, y, linestyle='', color = 'white')
     else:
          ax.errorbar(x,y,error, linestyle='', color = 'white')
     setXticks(ax, majorDistanceX)
     setYticks(ax, majorDistanceY)
     return ax

def plot(x,y,ax = None, error = None, figsize = (7, 5),
         majorDistanceX = 0,
         majorDistanceY = 0,
         fontFamily = 'serif',
         fontSize = 18,
         axisLineWidth = 2,
         labelpad = '10',
         legendLocation = 'best',
         legendFrameOn = False,
         legendFontSize = 16.,
         marker = '-',
         color = None,
         label = '',
         markersize = 15,
         linewidth = 3,
         capsize = 5
):
     global nPlots
     setFormatPlot(fontFamily,
                   fontSize,
                   axisLineWidth,
                   labelpad,
                   legendLocation,
                   legendFrameOn,
                   legendFontSize)

     
     
     if ax is None:
          nPlots = 0
          fig, ax = initializeFigure(figsize)

     colors = loadColormap()
     if color is None:
          color = colors[nPlots%10]
     if color in colors:
          color = colors[color]
     if error is None:
          ax.plot(x,y,marker, color = color, label = label, markersize = markersize, linewidth = linewidth, zorder = nPlots)
     else:
          ax.errorbar(x,y,error,linestyle='', markersize = markersize, color = color, marker = marker, capsize = capsize, label = label, zorder = nPlots)
     
     #setXticks(ax)
     #setYticks(ax)
     ax.autoscale()
     nPlots+=1
     return ax

def bar(x,y,ax = None, figsize = (7, 5),
        fontFamily = 'serif',
        fontSize = 18,
        axisLineWidth = 2,
        labelpad = '10',
        legendLocation = 'best',
        legendFrameOn = False,
        legendFontSize = 16.,
        color = None,
        edgecolor = "k",
        label = '',
        align = "center",
        width=1):
         
     global nPlots
     setFormatPlot(fontFamily,
                   fontSize,
                   axisLineWidth,
                   labelpad,
                   legendLocation,
                   legendFrameOn,
                   legendFontSize)

     
     
     if ax is None:
          fig, ax = initializeFigure(figsize)

     colors = loadColormap()
     if color is None:
          color = colors[nPlots%10]
     if color in colors:
          color = colors[color]
     ax.bar(x,y,color = color, edgecolor = edgecolor, align = align, width = width)
     setXticks(ax)
     setYticks(ax)
     ax.autoscale()
     return ax

def show(ax = None, tight_layout = True, name = "", dpi = 300, minorXticks = True, minorYticks = True, nminorXticks = -1):
     if (tight_layout):
          plt.tight_layout()
     if ax is not None:
          if minorXticks:
               setXticks(ax, nminorXticks)
          if minorYticks:
               setYticks(ax)
     if len(name)>0:
          plt.savefig(name+".png",dpi = dpi)
     plt.show()

def saveFig(name, folder = "", extension = ".png", ax = None, tight_layout = True, dpi = 300, minorXticks = True, minorYticks = True):
     if ax is not None:
          if minorXticks:
               setXticks(ax)
          if minorYticks:
               setYticks(ax)
     if (tight_layout):
          plt.tight_layout()
     if len(folder)>0:
          name = folder+"/"+name
     plt.savefig(name+extension, dpi = dpi)
