import composite
import Plotting
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import sys
import galrun

def run():
	#Allows user to build queries, and starts with selecting the morphologies to use.
	name='Composite_comparison,'
	num=input('Number of queries: ')
	morph_range=[]
	i=0
	while (i<num):
		morph=input('Select morphology range: (E=1,E/S0=2,S0=3,S0a=4,Sa=5,Sab=6,Sb=7,Sbc=8,Sc=9,Scd=10,Sd/Irr=11)')
		morph_range.append(morph)
		i+=1
	
	labels=[]
	for morph in morph_range:
		label=''
		n=''
		if morph[0] <= 1 <= morph[1]:
			label+=',E'
			n+=',E'
		if morph[0] <= 2 <= morph[1]:
			label+=',E&S0'
			n+=',E&S0'
		if morph[0] <= 3 <= morph[1]:
			label+=',S0'
			n+=',S0'
		if morph[0] <= 4 <= morph[1]:
			label+=',S0a'
			n+=',S0a'
		if morph[0] <= 5 <= morph[1]:
			label+=',SA'
			n+=',SA'
		if morph[0] <= 6 <= morph[1]:
			label+=',SAB'
			n+=',SAB'
		if morph[0] <= 7 <= morph[1]:
			label+=',SB'
			n+=',SB'
		if morph[0] <= 8 <= morph[1]:
			label+=',SBC'
			n+=',SBC'
		if morph[0] <= 9 <= morph[1]:
			label+=',SC'
			n+=',SC'
		if morph[0] <= 10 <= morph[1]:
			label+=',SCD'
			n+=',SCD'
		if morph[0] <= 11 <= morph[1]:
			label+=',SD&Irr'
			n+=',SD&Irr'
		n=n[1:]
		n='['+n+']'
		label=label[1:]
		labels.append(label)
		name+=n
	
	#Choose parameters to constrain query, will use same constraints on each range of morphologies
	params=input('Select parameters: (Redshift=1,Phase=2,Dm15=3,M_B=4,B_mMinusV_m=5)')
	query='SELECT * FROM Supernovae Where '
	if 1 in params:
		range=input('Select redshift range: [xmin,xmax]')
		query += 'redshift BETWEEN ' + str(range[0]) + ' AND ' + str(range[1]) + ' AND '
		name+=',redshift['+str(range[0])+','+str(range[1])+']'		
	if 2 in params:
		range=input('Select phase range: [xmin,xmax]')
		query += 'Phase BETWEEN ' + str(range[0]) + ' AND ' + str(range[1]) + ' AND '
		name+=',phase['+str(range[0])+','+str(range[1])+']'
	if 3 in params:
		range=input('Select Dm15 range: [xmin,xmax]')
		query += 'Dm15 BETWEEN ' + str(range[0]) + ' AND ' + str(range[1]) + ' AND '
		name+=',dm15['+str(range[0])+','+str(range[1])+']'
	if 4 in params:
		range=input('Select M_B range: [xmin,xmax]')
		query += 'M_B BETWEEN ' + str(range[0]) + ' AND ' + str(range[1]) + ' AND '
		name+=',M_B['+str(range[0])+','+str(range[1])+']'
	if 5 in params:
		range=input('Select B_mMinusV_m range: [xmin,xmax]')
		query += 'B_mMinusV_m BETWEEN ' + str(range[0]) + ' AND ' + str(range[1]) + ' AND '
		name+=',B_m-V_m['+str(range[0])+','+str(range[1])+']'

	query += 'Morphology '

	#builds input to galrun.py
	queries=[]
	queries.append(sys.argv)
	queries.append(str(num))
	for morph in morph_range:
		queries.append(query + ' BETWEEN ' + str(morph[0]) + ' AND ' + str(morph[1]))

	#scales=composite.find_scales(composites,composites[0].flux,composites[0].ivar)
		
	plot_name = name # + ',avgphase-' + str("%.2f" % avgphase) + ',avgred-' + str("%.2f" % avgred)
	
	plots=input('Choose plots: (RelFlux=0,Var=1,Res=2,Sp/Bin=3,Age=4,Delta=5,Red=6,Multi Spec=6,Stack Spec=7)')
	
	galrun.main(queries,plot_name,plots,labels)
	
cont=0
while(cont==0):
	run()
	if (raw_input('Make another query? (y/n)') == 'y'):
		cont=0
	else:
		cont +=1
	