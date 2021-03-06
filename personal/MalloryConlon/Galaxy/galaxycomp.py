#separate spectra between elliptical and spiral host galaxy
#create composite and RMS spectrum for each type of galaxy

import numpy as np
import os
from astropy.table import Table
import scipy.interpolate as inter
import glob
import matplotlib.pyplot as plt
import math

#Reads in spectra file names
spectra_files=Table.read('MaxSpectra.dat',format='ascii')
spectra_arrays=[]
spectra_names=[]
bad_files=[]

num=len(spectra_files)	#number of spectra to analyse, eventually will be len(spectra_files)

for i in range(num):
	spectrum_file=spectra_files[i]
	try:
		spectra_arrays.append(Table.read(spectrum_file["col2"],format='ascii'))
		spectra_names.append(spectrum_file["col1"])
	except ValueError:
		bad_files.append(spectra_files[i])

host_info=Table.read('../../MalloryConlon/Galaxy/host_info.dat',format='ascii')
sn_name=host_info["col1"]
host_type=host_info["col2"]
elliptical=[]
S0=[]
spiral=[]
irregular=[]
anon=[]
for j in range(len(host_info)):
	if host_type[j]==1 or host_type[j]==2:
		elliptical.append(sn_name[j])
	if host_type[j]==3 or host_type[j]==4:
		S0.append(sn_name[j])
	if host_type[j]==5 or host_type[j]==6 or host_type[j]==7 or host_type[j]==8 or host_type[j]==9 or host_type[j]==10:
		spiral.append(sn_name[j])
	if host_type[j]==11:
		irregular.append(sn_name[j])
	if host_type[j]==0:
		anon.append(sn_name[j])

sn_elliptical=[]
for i in range(len(elliptical)):
	for j in range(len(spectra_arrays)):
		if spectra_names[j] in elliptical[i]:
			sn_elliptical.append(spectra_arrays[j])

sn_S0=[]
for i in range(len(S0)):
	for j in range(len(spectra_arrays)):
		if spectra_names[j] in S0[i]:
			sn_S0.append(spectra_arrays[j])

sn_spiral=[]
for i in range(len(spiral)):
	for j in range(len(spectra_arrays)):
		if spectra_names[j] in spiral[i]:
			sn_spiral.append(spectra_arrays[j])

sn_irr=[]
for i in range(len(irregular)):
	for j in range(len(spectra_arrays)):
		if spectra_names[j] in irregular[i]:
			sn_irr.append(spectra_arrays[j])

def gal_comp_res(spectra_arrays):
	#deredshift data
	parameters = Table.read('../../../data/cfa/cfasnIa_param.dat',format='ascii')
	sn_name = parameters["col1"]
	sn_z = parameters["col2"]
	for i in range(len(spectra_arrays)):
		old_spectrum=spectra_arrays[i]
		z=0
		for j in range(len(sn_name)):
			if sn_name[j] in spectra_arrays[i]:
				z=sn_z[j]
		lambda_obs=old_spectrum["col1"]
		lambda_emit= lambda_obs/(1+z)
		spectra_arrays[i]=Table([lambda_emit,old_spectrum["col2"]],names=('col1','col2'))
    
	#scale spectra
	wave_min=0  #arbitrary minimum of wavelength range
	wave_max=1000000   #arbitrary maximum of wavelength range
    
	for i in range(len(spectra_arrays)):
		spectra = spectra_arrays[i]
		if (min(spectra["col1"]) > wave_min): #changes minimum wavelength if larger than previous
			wave_min=min(spectra["col1"])
		if (max(spectra["col1"]) < wave_max):  #changes maximum wavelength if smaller than previous
			wave_max=max(spectra["col1"])
    
	wavelength = np.linspace(wave_min,wave_max,wave_max-wave_min)  #creates 100 equally spaced wavelength values between the smallest range
	#generates composite spectrum
	fitted_flux=[]	#new interpolated flux values over wavelength range
	for i in range(len(spectra_arrays)):
		new_spectrum=spectra_arrays[i]	#declares new spectrum from list
		new_wave=new_spectrum["col1"]	#wavelengths
		new_flux=new_spectrum["col2"]	#fluxes
		lines=np.where((new_wave>wave_min) & (new_wave<wave_max))	#creates an array of wavelength values between minimum and maximum wavelengths from new spectrum
		sm1=inter.splrep(new_wave[lines],new_flux[lines])	#creates b-spline from new spectrum
		y1=inter.splev(wavelength,sm1)	#fits b-spline over wavelength range
		y1 /= np.median(y1)
		fitted_flux.append(y1)
    
	avg_flux = np.mean(fitted_flux,axis=0)	#finds average flux at each wavelength
    
	avg_spectrum=Table([wavelength,avg_flux],names=('col1','col2'))	#puts together the average spectrum
	
	#RMS Spectrum, Residual
	delta=[]
	scatter=[]
	for i in range(len(fitted_flux)):
		delta.append(avg_flux-fitted_flux[i])
    
	rms_flux = np.sqrt(np.mean(np.square(delta),axis=0))	#creates RMS value of flux at each wavelength
	
	for i in range(len(rms_flux)):
		scatter.append(rms_flux[i]/avg_flux[i]*100)	#creates residual values
	return wavelength, avg_flux, rms_flux, scatter


e_wavelength, e_avg_flux, e_rms_flux, e_scatter = gal_comp_res(sn_elliptical)
e_wave_min=min(e_wavelength)
e_wave_max=max(e_wavelength)


S0_wavelength, S0_avg_flux, S0_rms_flux, S0_scatter = gal_comp_res(sn_S0)
S0_wave_min=min(S0_wavelength)
S0_wave_max=max(S0_wavelength)


spiral_wavelength, spiral_avg_flux, spiral_rms_flux, spiral_scatter = gal_comp_res(sn_spiral)
spiral_wave_min=min(spiral_wavelength)
spiral_wave_max=max(spiral_wavelength)

irr_wavelength, irr_avg_flux, irr_rms_flux, irr_scatter = gal_comp_res(sn_irr)
irr_wave_min=min(irr_wavelength)
irr_wave_max=max(irr_wavelength)


plt.figure(1)
plt.subplot(211)
plot1,=plt.plot(e_wavelength,e_avg_flux,label='comp')
plot2,=plt.plot(e_wavelength,e_avg_flux+e_rms_flux,label='rms+')
plot3,=plt.plot(e_wavelength,e_avg_flux-e_rms_flux,label='rms-')
legend=plt.legend(loc='upper right', shadow=True)
plt.xlim(e_wave_min,e_wave_max)
plt.ylabel('Scaled Flux')
plt.subplot(212)
plot1,=plt.plot(e_wavelength,e_scatter)
plt.xlim(e_wave_min,e_wave_max)
plt.ylim(0,100)
plt.xlabel('Rest Wavelength')
plt.ylabel('Rms Flux/Average Flux')
plt.savefig('EllipticalPlot.png')
plt.show()

plt.figure(2)
plt.subplot(211)
plot1,=plt.plot(S0_wavelength,S0_avg_flux,label='comp')
plot2,=plt.plot(S0_wavelength,S0_avg_flux+S0_rms_flux,label='rms+')
plot3,=plt.plot(S0_wavelength,S0_avg_flux-S0_rms_flux,label='rms-')
legend=plt.legend(loc='upper right', shadow=True)
plt.xlim(S0_wave_min,S0_wave_max)
plt.ylabel('Scaled Flux')
plt.subplot(212)
plot1,=plt.plot(S0_wavelength,S0_scatter)
plt.xlim(S0_wave_min,S0_wave_max)
plt.ylim(0,100)
plt.xlabel('Rest Wavelength')
plt.ylabel('Rms Flux/Average Flux')
plt.savefig('S0Plot.png')
plt.show()

plt.figure(3)
plt.subplot(211)
plot1,=plt.plot(spiral_wavelength,spiral_avg_flux,label='comp')
plot2,=plt.plot(spiral_wavelength,spiral_avg_flux+spiral_rms_flux,label='rms+')
plot3,=plt.plot(spiral_wavelength,spiral_avg_flux-spiral_rms_flux,label='rms-')
legend=plt.legend(loc='upper right', shadow=True)
plt.xlim(spiral_wave_min,spiral_wave_max)
plt.ylabel('Scaled Flux')
plt.subplot(212)
plot1,=plt.plot(spiral_wavelength,spiral_scatter)
plt.xlim(spiral_wave_min,spiral_wave_max)
plt.ylim(0,100)
plt.xlabel('Rest Wavelength')
plt.ylabel('Rms Flux/Average Flux')
plt.savefig('SpiralPlot.png')
plt.show()

plt.figure(4)
plt.subplot(211)
plot1,=plt.plot(irr_wavelength,irr_avg_flux,label='comp')
plot2,=plt.plot(irr_wavelength,irr_avg_flux+irr_rms_flux,label='rms+')
plot3,=plt.plot(irr_wavelength,irr_avg_flux-irr_rms_flux,label='rms-')
legend=plt.legend(loc='upper right', shadow=True)
plt.xlim(irr_wave_min,irr_wave_max)
plt.ylabel('Scaled Flux')
plt.subplot(212)
plot1,=plt.plot(irr_wavelength,irr_scatter)
plt.xlim(irr_wave_min,irr_wave_max)
plt.ylim(0,100)
plt.xlabel('Rest Wavelength')
plt.ylabel('Rms Flux/Average Flux')
plt.savefig('IrrPlot.png')
plt.show()

plt.figure(5)
plot1,=plt.plot(spiral_wavelength,spiral_avg_flux,label='Spiral Composite')
plot2,=plt.plot(e_wavelength,e_avg_flux,label='Elliptical Composite')
plot3,=plt.plot(S0_wavelength,S0_avg_flux,label='S0 Composite')
plot4,=plt.plot(irr_wavelength,irr_avg_flux,label='Irregular Composite')
legend=plt.legend(loc='upper right', shadow=True)
plt.ylabel('Scaled Flux')
plt.xlabel('Rest Wavelength')
plt.savefig('all_composites.png')
plt.show()

"""
    plt.figure(4)
    plt.subplot(211)
    plot1,=plt.plot(i_wavelength,i_avg_flux,label='comp')
    plot2,=plt.plot(i_wavelength,i_avg_flux+i_rms_flux,label='rms+')
    plot3,=plt.plot(i_wavelength,i_avg_flux-i_rms_flux,label='rms-')
    legend=plt.legend(loc='upper right', shadow=True)
    plt.xlim(i_wave_min,i_wave_max)
    plt.ylabel('Flux')
    plt.subplot(212)
    plot1,=plt.plot(i_wavelength,i_scatter)
    plt.xlim(i_wave_min,i_wave_max)
    plt.ylim(0,100)
    plt.xlabel('Wavelength')
    plt.ylabel('Rms Flux/Average Flux')
    plt.savefig('IrregularPlot.png')
    plt.show()
    """