import composite
import Plotting
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import sys
import time
#import bootstrap
"""
Here's the main function that anyone can use to run some analysis.

It iterates through a loop based on how many queries were entered
Each one gets its data saved and the composite spectrum returned
Then all of the composites that were created get plotted

The next section sets up the plots to be used, and then plots using Plotting.py
Right now it doesn't work all the time...but it will

More can be added as our programs evolve

There are a few parameters you should set beforehand.
plot_name is where the plot showing both composite spectra together will be saved.
wmin and wmax define the boundary of the plot.
"""
queries = int(sys.argv[1])

#Now the file name of the plot is labeled by time of creation, but you can personalize it if you want.
#Or rename it once it's been saved.
plot_name = str(queries) + '_composite_comparison, ' + (time.strftime("%H,%M,%S"))
wmin = 3000
wmax = 10000

d={}
for n in range(queries):
    if len(sys.argv) == queries+3:
        d["composite{0}".format(n+1)] = composite.main(sys.argv[n+2], sys.argv[queries+2])
    if len(sys.argv) == queries+4:
        d["composite{0}".format(n+1)] = composite.main(sys.argv[n+2], sys.argv[queries+2], sys.argv[queries+3])
    if len(sys.argv) == queries+5:
        d["composite{0}".format(n+1)] = composite.main(sys.argv[n+2], sys.argv[queries+2], sys.argv[queries+3], sys.argv[queries+4])
    else:
        d["composite{0}".format(n+1)] = composite.main(sys.argv[n+2])

#This makes, shows, and saves a quick comparison plot...we can probably get rid of this when plotting.main works.
lowindex  = np.where(d["composite1"].wavelength == composite.find_nearest(d["composite1"].wavelength, wmin))
highindex = np.where(d["composite1"].wavelength == composite.find_nearest(d["composite1"].wavelength, wmax))
#for n in range(queries):
#    plt.plot(d["composite{0}".format(n+1)].wavelength[lowindex[0]:highindex[0]], d["composite{0}".format(n+1)].flux[lowindex[0]:highindex[0]])
#plt.savefig('../plots/' + plot_name + '.png')
#print 'Plot saved as: ' + plot_name
#plt.show()

#Read whatever you sasved the table as, iterates over however many composites you used.
#This is how you have to address things if you want to iterate over queries.
#The n+1 makes the first item composite1, not composite0.
for n in range(queries):
    d["data{0}".format(n+1)]         = Table.read(d["composite{0}".format(n+1)].savedname, format='ascii')
    d["wavelengths{0}".format(n+1)]  = np.array([d["data{0}".format(n+1)]["Wavelength"]])
    d["fluxes{0}".format(n+1)]       = np.array([d["data{0}".format(n+1)]["Flux"]])
    d["variances{0}".format(n+1)]    = np.array([d["data{0}".format(n+1)]["Variance"]])
    

# From now on, list the data you want to plot as [ Xdata, Ydata, Xdata_2, Ydata_2]
#This chunk will create an array that's the right length for however many queries you used.
plot_array     = []
name_array     = []
residual_array = []
variance_array = []
for n in range(queries):
    plot_array.append(d["wavelengths{0}".format(n+1)])
    plot_array.append(d["fluxes{0}".format(n+1)])
    residual_array.append(d["wavelengths{0}".format(n+1)])
    residual_list = abs(np.array([d["fluxes{0}".format(n+1)]-d["fluxes1"]]))
    residual_array.append(residual_list)
    variance_array.append(d["wavelengths{0}".format(n+1)])
    variance_array.append(d["variances{0}".format(n+1)])
    name_array.append("composite{0}".format(n+1))
    name_array.append(" ")
  
#print residual_array # this array has zeros for values on the xaxis (wavelength)?    
##################
#If you want to use custom names for your composites,
#fill out and uncomment this next line
#name_array = ["composite1name", " ", "composite2name", " ", etc]
##################

Relative_Flux   = plot_array #plots all given composites
#Technically, the variances are not the residuals. Plotting them is useful, but it's mislabeled here.
## Do you want to plot the variance or the residual? The residual is something else that can be plotted. (4/13)
###We should be able to plot both. I've created two separate arrays, and they both print just fine on this end. (also 4/13)
Variance        = []
Residuals       = residual_array # This is giving nan values when it's normalized, I'm not sure why
Spectra_Bin     = [] 
Age             = [] 
Delta           = [] 
Redshift        = []
# Can name_array puhttp://cosmo2014.uchicago.edu/t an empty "  " space between each associated data name
# yes
#Names           = ["Carbon Positive", "","Carbon Negative",""] # the names corresponding to each composite go here
## If you want custom names ^^^, uncomment and use line 83, for consistency.
##Otherwise it'll default to just labeling composites in order.
Names           = name_array
Show_Data       = [Relative_Flux,Variance,Residuals,Spectra_Bin,Age,Delta,Redshift]

## Available Plots:  Relative Flux, Residuals, Spectra/Bin, Age, Delta, Redshift, Variance
##                   0              1          2            3    4      5         6
# the plots you want to create 
Plots        = [0] 

image_title  = "../plots/" + str(sys.argv[1]) + "_composites.png"
print "Plot saved as: " + image_title
title        = "Composite Spectra Comparison"	
# The following line will plot the data
#<<<<<<< HEAD
#It's commented out until it works...
"""
Plotting.main(Show_Data , Plots, image_title , title)
=======
Plotting.main(Show_Data , Plots , image_title , title, Names)
>>>>>>> 9381a6f916691e8b782228e862e14a86c711f45d
"""