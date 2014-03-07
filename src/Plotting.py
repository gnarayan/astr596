import numpy as np
import matplotlib as mpl
from matplotlib import rc
import matplotlib.pyplot as plt
import math
from pylab import *
import matplotlib.gridspec as gridspec


###########################################
#             HOW TO USE
## At the top of YOUR code write the following
# import Plotting
# 
## Place the following after you have calculated your data 
## fill in information
# 
#Relative_Flux = [wavelengths, avg_flux_p, names of samples]  # Want to plot 2 spectra on the same figure
#Residuals     = []
#Spectra_Bin   = []
#Age           = []
#Delta         = []
#Redshift      = [] 
#Show_Data     = [Relative_Flux,Residuals]
# image_title  = "WHOA.png"            # Name the image (with location)
# title        = "Image is called this" 
# legend       = ["First","Second","Third","Fouth"]         # Names for the legend
#
#
## The following line will plot the data
#
# Plotting.main(Show_Data , image_title , plot_labels , legend)
#
#
###########################################
def main(Show_Data , Plots , image_title , title , legend_names):

    # Available Plots:  Relative Flux, Residuals, Spectra/Bin, Age, Delta, Redshift, Multiple Spectrum, Stacked Spectrum
    #                   0              1          2            3    4      5         6,                 7
    Height =           [8,             2,         3,           2,   2,     2,        0,                 0]

    #Plots = [0,1] # Plots to generate # Remove me

    h = []

    for m in Plots:
        h.append(Height[m])
        
# re-name variables
    if len(Show_Data[:][0]) > 0 :
	xaxis_1   = Show_Data[:][0][0] 
	yaxis_1   = Show_Data[:][0][1]
	names_1   = Show_Data[:][0][2]
	#err_n_1   = Show_Data[:][0][3] 

	# will work on the legend next
    legend_1  = legend_names[0]
    legend_2  = legend_names[1]
    legend_3  = legend_names[2]
    legend_4  = legend_names[3]

    #f = figure()
    #subplots_adjust(hspace=0.001)

# Changing font parameters. 
    params = {'legend.fontsize': 8, 
              'legend.linewidth': 2,
              'legend.font': 'serif',
              'mathtext.default': 'regular', 
              'xtick.labelsize': 8, 
              'ytick.labelsize': 8} # changes font size in the plot legend

    plt.rcParams.update(params)                             # reset the plot parameters

    font = {'family' : 'serif',
            'color'  : 'black',
            'weight' : 'bold',
            'size'   : 10,
            }
        
    plt.figure(num = 1, dpi = 100, figsize = [8, np.sum(h)], facecolor = 'w')
    plt.title(title)
    gs = gridspec.GridSpec(len(Plots), 1, height_ratios = h, hspace = 0.001)
    p = 0

    import scipy.optimize as optimize        
        
    def residual(comp, data):
        return comp - data

    source = (np.array(yaxis_1)).T
    guess = yaxis_1[0]
    comp_data = []
    sbins = []

    for m in range(len(source)):
        comp, cov = optimize.leastsq(residual, guess[m], args = (source[m]), full_output = False)
        comp_data.append(comp[0])
        sbins.append(len(source[m]))

    delta_data = []     # difference from the mean value

    for m in range(len(yaxis_1)):   # finds difference between composite data and interpolated data sets
        delta_data.append(comp_data-yaxis_1[m]) 

    rms_data = np.sqrt(np.mean(np.square(delta_data), axis = 0))    # finds root-mean-square of differences at each wavelength within overlap

    if 0 in Plots:
        Rel_flux = plt.subplot(gs[p])
        #plt.title("".join(["$^{26}$Al / $^{27}$Al, t$_{res}$ = ", str(t_width_Al), " kyr", ", U$_{Al}$ = ", str(uptake_Al[0])]), fontdict = font)
        #plt.xlabel('Age [Myr]', fontdict = font)
        plt.ylabel('Relative, f$_{\lambda}$', fontdict = font)
        #plt.axis([Start_Al-0.05, End_Al+0.05, 0, 40])
        plt.minorticks_on()
        #plt.xticks(np.arange(Start_Al, End_Al+0.05, x_tik))
        #plt.yticks(np.arange(0, 41, 5))
        #plt.plot(xaxis_1, yaxis_1, label = "generic data", ls = '-')  # The next three lines have been commented out - nk
        plt.fill_between(xaxis_1, comp_data+rms_data, comp_data-rms_data, color = 'grey')        
        plt.plot(xaxis_1, comp_data, label = "Composite")
        plt.plot(xaxis_1, comp_data+rms_data, label = "+ RMS")
        plt.plot(xaxis_1, comp_data-rms_data, label = "- RMS")
        plt.legend(prop = {'family' : 'serif'})
        RFxticklabels = Rel_flux.get_xticklabels()        
        if Plots[len(Plots)-1] != 0:
            plt.setp(RFxticklabels, visible=False)
        else:
            plt.setp(RFxticklabels, visible=True)
        p = p+1

    if 1 in Plots:
        Resid = plt.subplot(gs[p], sharex = Rel_flux)
        #plt.title("".join(["$^{53}$Mn / $^{55}$Mn, t$_{res}$ = ", str(t_width_Mn), " kyr", ", U$_{Mn}$ = ", str(uptake_Mn[0])]), fontdict = font)
        #plt.xlabel('Age [Myr]', fontdict = font)
        plt.ylabel('Residuals', fontdict = font)
        #plt.axis([Start_Mn-0.05, End_Mn+0.05, 0, 10])
        #plt.minorticks_on()
        #plt.xticks(np.arange(Start_Mn, End_Mn+0.05, x_tik))
        #plt.yticks(np.arange(0, 11, 1))
        plt.plot(xaxis_1, rms_data, label = "RMS of residuals", ls = '-')
        #plt.legend(prop = {'family' : 'serif'})
        RSxticklabels = Resid.get_xticklabels()
        if Plots[len(Plots)-1] != 1:
            plt.setp(RSxticklabels, visible=False)
        else:
            plt.setp(RSxticklabels, visible=True)
        p = p+1

    if 2 in Plots:
        SpecBin = plt.subplot(gs[p], sharex = Rel_flux)
        #plt.title("".join(["$^{60}$Fe / $^{56}$Fe, t$_{res}$ = ", str(t_width_Fe), " kyr", ", U$_{Fe}$ = ", str(uptake_Fe[0])]), fontdict = font)
        #plt.xlabel('Age [Myr]', fontdict = font)
        plt.ylabel('Spectra/Bin', fontdict = font)
        #plt.axis([Start_Fe-0.05, End_Fe+0.05, 0, 40])
        #plt.minorticks_on()
        #plt.xticks(np.arange(Start_Fe, End_Fe+0.05, x_tik))
        #plt.yticks(np.arange(0, 41, 5))
        plt.plot(xaxis_1, 0*xaxis_1+3.0, label = "title goes here", ls = '-')
        #plt.legend(prop = {'family' : 'serif'})
        SBxticklabels = SpecBin.get_xticklabels()        
        if Plots[len(Plots)-1] != 2:
            plt.setp(SBxticklabels, visible=False)
        else:
            plt.setp(SBxticklabels, visible=True)
        p = p+1

    if 3 in Plots:
        Age = plt.subplot(gs[p], sharex = Rel_flux)
        #plt.title('Decay corrected $^{26}$Al / $^{27}$Al', fontdict = font)
        #plt.xlabel('Age [Myr]', fontdict = font)
        plt.ylabel('Age [d]', fontdict = font)
        #plt.axis([Start_Al-0.05, End_Al+0.05, 0, 30])
        #plt.minorticks_on()
        #plt.xticks(np.arange(Start_Al, End_Al+.05, x_tik))
        #plt.yticks(np.arange(0, 29, 5))
        plt.plot(xaxis_1, xaxis_1**3.0, label = "title goes here", ls = '-')
        #plt.legend(prop = {'family' : 'serif'})
        AGxticklabels = Age.get_xticklabels()        
        if Plots[len(Plots)-1] != 3:
            plt.setp(AGxticklabels, visible=False)
        else:
            plt.setp(AGxticklabels, visible=True)
        p = p+1
    
    if 4 in Plots:
        Delta = plt.subplot(gs[p], sharex = Rel_flux)
        #plt.title('Decay corrected $^{53}$Mn / $^{55}$Mn', fontdict = font)
        #plt.xlabel('Age [Myr]', fontdict = font)
        plt.ylabel('$\Delta$', fontdict = font)
        #plt.axis([Start_Mn-0.05, End_Mn+0.05, 0, 13])
        #plt.minorticks_on()
        #plt.xticks(np.arange(Start_Mn, End_Mn+0.05, x_tik))
        #plt.yticks(np.arange(0, 13, 2))
        plt.plot(xaxis_1, 1/xaxis_1, label = "title goes here", ls = '-')
        #plt.legend(prop = {'family' : 'serif'})
        DLxticklabels = Delta.get_xticklabels()
        if Plots[len(Plots)-1] != 4:            
            plt.setp(DLxticklabels, visible=False)
        else:
            plt.setp(DLxticklabels, visible=True)
        p = p+1
    
    if 5 in Plots:
        Redshift = plt.subplot(gs[p], sharex = Rel_flux)
        #plt.title('Decay corrected $^{60}$Fe / $^{56}$Fe', fontdict = font)
        #plt.xlabel('Age [Myr]', fontdict = font)
        plt.ylabel('Redshift', fontdict = font)
        #plt.axis([Start_Fe-0.05, End_Fe+0.05, 0, 70])
        #plt.minorticks_on()
        #plt.xticks(np.arange(Start_Fe, End_Fe+0.05, x_tik))
        #plt.yticks(np.arange(0, 70, 10))
        plt.plot(xaxis_1, xaxis_1**2.0-xaxis_1, label = "title goes here", ls = '-')
        #plt.legend(prop = {'family' : 'serif'})
        Zxticklabels = Redshift.get_xticklabels()        
        if Plots[len(Plots)-1] != 5:            
            plt.setp(Zxticklabels, visible=False)
        else:
            plt.setp(Zxticklabels, visible=True)
        p = p+1
    
    plt.xlabel('Rest Wavelength [$\AA$]', fontdict = font)

    if 6 in Plots:
        plt.figure(num = 2, dpi = 100, figsize = [8, 8], facecolor = 'w')
        for m in range(len(yaxis_1)):
            plt.plot(xaxis_1, yaxis_1[m], label = str(names_1[m]))
        plt.xlabel('Rest Wavelength [$\AA$]', fontdict = font)
        plt.ylabel('Relative, f$_{\lambda}$', fontdict = font)
        plt.minorticks_on()
        plt.legend(prop = {'family' : 'serif'})        

    if 7 in Plots:
        plt.figure(num = 3, dpi = 100, figsize = [8, 2*len(yaxis_1)], facecolor = 'w')
        plt.plot(xaxis_1, yaxis_1[0])
        plt.annotate(str(names_1[0]), xy = (max(xaxis_1), 0), xytext = (-20, 20), textcoords = 'offset points', fontsize = 8, family  = 'serif', weight = 'bold', ha = 'right')
        ymax = max(yaxis_1[0])
        for m in range(len(yaxis_1)-1):
            plt.plot(xaxis_1, yaxis_1[m+1]+ymax+max(yaxis_1[m+1])-min(yaxis_1[m+1]))
            plt.annotate(str(names_1[m+1]), xy = (max(xaxis_1), ymax+max(yaxis_1[m+1])-min(yaxis_1[m+1])), xytext = (-20, 20), textcoords = 'offset points', fontsize = 8, family  = 'serif', weight = 'bold', ha = 'right')
            ymax = max(yaxis_1[m+1]+ymax+max(yaxis_1[m+1])-min(yaxis_1[m+1]))
        plt.xlabel('Rest Wavelength [$\AA$]', fontdict = font)
        plt.ylabel('Relative, f$_{\lambda}$', fontdict = font)
        plt.minorticks_on()

# Remove legend box frame 
    #l = legend()
    #l.draw_frame(False)
    #plt.draw()

#Set the visual range. Automatic range is ugly. 
    #xmin = int(float(xaxis_1[0]))
    #xmax = int(float(xaxis_2[-1]))
    #plt.xlim((xmin,xmax))

#Label the figure and show
    #plt.xlabel( xlabel )
    plt.savefig( image_title )
    plt.show()


"""
# Data should be read in and then plotted, make it so the user doens't have to choose the figure to plot
	if fig_type == 2.3: # Plotting details for two figures with a total of three sets of data
		ax1 = subplot(2,1,1)
		plt.title( title )  # Placement of figure title in code is important
		plt.ylabel( ylabel_1 )
		ax1.plot(xaxis_1,yaxis_1,'b',label = legend_1 )
		ax1.plot(xaxis_2,yaxis_2,'g',label = legend_2 )

		# Below fills the error around the plot
		plt.fill_between(xaxis_1,err_p_1,err_n_1,alpha=1.5, edgecolor='#000080', facecolor='#AFEEEE')
		plt.fill_between(xaxis_2,err_p_2,err_n_2,alpha=1.5, edgecolor='#006400', facecolor='#98FB98')

		# Plotting details for two figures with one set of data
		ax2 = subplot(2,1,2, sharex=ax1)
		plt.ylabel( ylabel_2 )
		ax2.plot(xaxis_3,yaxis_3_1,'b',label = legend_3 )
		ax2.plot(xaxis_3,yaxis_3_2,'g',label = legend_4 )
		
#Removes x-axis labels for ax1. May need later. 	
	# 	Commented code is to remove labels for both figures
	#	xticklabels = ax1.get_xticklabels() + ax2.get_xticklabels()
	#	setp(xticklabels, visible=False)
		setp(ax1.get_xticklabels(), visible = False)
	
	elif fig_type == 1.2: # Plotting details for single figure with two sets of data
		ax1 = subplot(1,1,1)
		plt.title( title )  # Placement of figure title in code is important
		plt.ylabel( ylabel_1 )
		ax1.plot(xaxis_1,yaxis_1,'b',label = legend_1 )
		ax1.plot(xaxis_2,yaxis_2,'g',label = legend_2 )

		# Below fills the error around the plot
		plt.fill_between(xaxis_1,err_p_1,err_n_1,alpha=1.5, edgecolor='#000080', facecolor='#AFEEEE')
		plt.fill_between(xaxis_2,err_p_2,err_n_2,alpha=1.5, edgecolor='#006400', facecolor='#98FB98')

	else : # Plotting single plot with single set of data
		ax1 = subplot(1,1,1)
		plt.title( title )  # Placement of figure title in code is important
		plt.ylabel( ylabel_1 )
		ax1.plot(xaxis_1,yaxis_1,'k',label = legend_1 )
		plt.fill_between(xaxis_1,err_p_1,err_n_2,alpha=1.5, edgecolor='#000080', facecolor='#5F9EA0')

"""
"""

# Available Plots:  Relative Flux, Residuals, Spectra/Bin, Age, Delta, Redshift
#                   0              1          2            3    4      5
Height =           [8,             2,         3,           2,   2,     2]

Plots = [0,1] # Plots to generate

h = []

for m in Plots:
    h.append(Height[m])

params = {'legend.fontsize': 8, 
          'legend.linewidth': 2,
          'legend.font': 'serif',
          'xtick.labelsize': 8, 
          'ytick.labelsize': 8} # changes font size in the plot legend

plt.rcParams.update(params) # reset the plot parameters

font = {'family' : 'serif',
        'color'  : 'black',
        'weight' : 'bold',
        'size'   : 8,
        }

xaxis_1 = np.linspace(2000, 8000, 12001)

plt.figure(num = 2, dpi = 100, figsize = [8, np.sum(h)], facecolor = 'w')
gs = gridspec.GridSpec(len(Plots), 1, height_ratios = h, hspace = 0.001)
p = 0

if 0 in Plots:
    Rel_flux = plt.subplot(gs[p])
    #plt.title("".join(["$^{26}$Al / $^{27}$Al, t$_{res}$ = ", str(t_width_Al), " kyr", ", U$_{Al}$ = ", str(uptake_Al[0])]), fontdict = font)
    #plt.xlabel('Age [Myr]', fontdict = font)
    plt.ylabel('Relative f$_{\lambda}$', fontdict = font)
    #plt.axis([Start_Al-0.05, End_Al+0.05, 0, 40])
    plt.minorticks_on()
    #plt.xticks(np.arange(Start_Al, End_Al+0.05, x_tik))
    #plt.yticks(np.arange(0, 41, 5))
    plt.plot(xaxis_1, xaxis_1**2.0, label = "generic data", ls = '-')
    plt.legend(prop = {'family' : 'serif'})
    p = p+1

if 1 in Plots:
    Resid = plt.subplot(gs[p], sharex = Rel_flux)
    #plt.title("".join(["$^{53}$Mn / $^{55}$Mn, t$_{res}$ = ", str(t_width_Mn), " kyr", ", U$_{Mn}$ = ", str(uptake_Mn[0])]), fontdict = font)
    #plt.xlabel('Age [Myr]', fontdict = font)
    plt.ylabel('Residuals', fontdict = font)
    #plt.axis([Start_Mn-0.05, End_Mn+0.05, 0, 10])
    #plt.minorticks_on()
    #plt.xticks(np.arange(Start_Mn, End_Mn+0.05, x_tik))
    #plt.yticks(np.arange(0, 11, 1))
    plt.plot(xaxis_1, 2.0*xaxis_1, label = "title goes here", ls = '-')
    #plt.legend(prop = {'family' : 'serif'})
    p = p+1

if 2 in Plots:
    SpecBin = plt.subplot(gs[p], sharex = Rel_flux)
    #plt.title("".join(["$^{60}$Fe / $^{56}$Fe, t$_{res}$ = ", str(t_width_Fe), " kyr", ", U$_{Fe}$ = ", str(uptake_Fe[0])]), fontdict = font)
    #plt.xlabel('Age [Myr]', fontdict = font)
    plt.ylabel('Spectra/Bin', fontdict = font)
    #plt.axis([Start_Fe-0.05, End_Fe+0.05, 0, 40])
    #plt.minorticks_on()
    #plt.xticks(np.arange(Start_Fe, End_Fe+0.05, x_tik))
    #plt.yticks(np.arange(0, 41, 5))
    plt.plot(xaxis_1, 0*xaxis_1+3.0, label = "title goes here", ls = '-')
    #plt.legend(prop = {'family' : 'serif'})
    p = p+1

if 3 in Plots:
    Age = plt.subplot(gs[p], sharex = Rel_flux)
    #plt.title('Decay corrected $^{26}$Al / $^{27}$Al', fontdict = font)
    #plt.xlabel('Age [Myr]', fontdict = font)
    plt.ylabel('Age [d]', fontdict = font)
    #plt.axis([Start_Al-0.05, End_Al+0.05, 0, 30])
    #plt.minorticks_on()
    #plt.xticks(np.arange(Start_Al, End_Al+.05, x_tik))
    #plt.yticks(np.arange(0, 29, 5))
    plt.plot(xaxis_1, xaxis_1**3.0, label = "title goes here", ls = '-')
    #plt.legend(prop = {'family' : 'serif'})
    p = p+1

if 4 in Plots:
    Delta = plt.subplot(gs[p], sharex = Rel_flux)
    #plt.title('Decay corrected $^{53}$Mn / $^{55}$Mn', fontdict = font)
    #plt.xlabel('Age [Myr]', fontdict = font)
    plt.ylabel('$\Delta$', fontdict = font)
    #plt.axis([Start_Mn-0.05, End_Mn+0.05, 0, 13])
    #plt.minorticks_on()
    #plt.xticks(np.arange(Start_Mn, End_Mn+0.05, x_tik))
    #plt.yticks(np.arange(0, 13, 2))
    plt.plot(xaxis_1, 1/xaxis_1, label = "title goes here", ls = '-')
    #plt.legend(prop = {'family' : 'serif'})
    p = p+1

if 5 in Plots:
    Redshift = plt.subplot(gs[p], sharex = Rel_flux)
    #plt.title('Decay corrected $^{60}$Fe / $^{56}$Fe', fontdict = font)
    #plt.xlabel('Age [Myr]', fontdict = font)
    plt.ylabel('Redshift', fontdict = font)
    #plt.axis([Start_Fe-0.05, End_Fe+0.05, 0, 70])
    #plt.minorticks_on()
    #plt.xticks(np.arange(Start_Fe, End_Fe+0.05, x_tik))
    #plt.yticks(np.arange(0, 70, 10))
    plt.plot(xaxis_1, xaxis_1**2.0-xaxis_1, label = "title goes here", ls = '-')
    #plt.legend(prop = {'family' : 'serif'})
    p = p+1

if Plots[len(Plots)-1] != 0:
    RFxticklabels = Rel_flux.get_xticklabels()
    plt.setp(RFxticklabels, visible=False)
if Plots[len(Plots)-1] != 1:
    RSxticklabels = Resid.get_xticklabels()
    plt.setp(RSxticklabels, visible=False)
if Plots[len(Plots)-1] != 2:
    SBxticklabels = SpecBin.get_xticklabels()
    plt.setp(SBxticklabels, visible=False)
if Plots[len(Plots)-1] != 3:
    AGxticklabels = Age.get_xticklabels()
    plt.setp(AGxticklabels, visible=False)
if Plots[len(Plots)-1] != 4:
    DLxticklabels = Delta.get_xticklabels()
    plt.setp(DLxticklabels, visible=False)



plt.show()


"""

