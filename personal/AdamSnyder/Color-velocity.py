import os
#import glob
#from specutils import extinction as ex
#import astroquery
#from astroquery.ned import Ned
#from astroquery.irsa_dust import IrsaDust
from astropy.table import Table
from astropy.io import ascii
import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as inter
import math
#from datafidelity import *  # Get variance from the datafidelity outcome
import msgpack as msg
import msgpack_numpy as mn
import sqlite3 as sq3

mn.patch()

class supernova():
    """stuff"""

#Sets up some lists for later
SN_Array = []
full_array = []

def grab(sql_input, Full_query):
    print "Collecting data..."
    SN_Array = []
    cur.execute(sql_input)
    for row in cur:
        if 1 == 1:
            SN           = supernova()
            SN.filename  = row[0]
            SN.name      = row[1]
            SN.source    = row[2]
            SN.redshift  = row[3]
            SN.phase     = row[4]
            SN.minwave   = row[5]
            SN.maxwave   = row[6]
            SN.dm15      = row[7]
            SN.m_b       = row[8]
            SN.B_minus_v = row[9]
            SN.velocity  = row[10]
            SN.morph     = row[11]
            SN.carbon    = row[12]
            SN.GasRich   = row[13]
            SN.SNR       = row[14]
            interp       = msg.unpackb(row[15])
            SN.interp    = interp
            try:
                SN.wavelength = SN.interp[0,:]
                SN.flux       = SN.interp[1,:]
                SN.ivar       = SN.interp[2,:]
            except TypeError:
                continue
            full_array.append(SN)
            SN_Array.append(SN)
            # print SN.filename
        else:
            print "Invalid query...more support will come"
    print len(SN_Array), "spectra found"
    return SN_Array

def findunique(SN_Array):
    Names = []
    indices = []
    for i in range(len(SN_Array)):
        if SN_Array[i].name in Names:
            pass
        else:
            Names.append(SN_Array[i].name)
            indices.append(i)

    print indices

    return indices

# Connect to database
con = sq3.connect('..\..\data\SNe.db')
cur = con.cursor()
sql_input = 'SELECT * FROM Supernovae WHERE B_mMinusV_m < 0.0 AND Velocity > -20 AND Phase BETWEEN -2 AND 2 AND Dm15 BETWEEN 1.0 AND 1.5'
X = []
Y = []
high_bv = []
low_bv = []
high_vel = []
low_vel = []

SN_Array_old = grab(sql_input, sql_input)
SN_Array = np.array([])

unique_SN = findunique(SN_Array_old)

for i in range(len(unique_SN)):
    SN_Array = np.append(SN_Array_old[unique_SN[i]], SN_Array)

print len(SN_Array)

for SN in SN_Array:
    Y.append(SN.B_minus_v)
    X.append(SN.velocity)
    print SN.carbon
    if SN.velocity <= -12:
        high_vel.append(SN.velocity)
        high_bv.append(SN.B_minus_v)
    elif SN.velocity > -12:
        low_vel.append(SN.velocity)
        low_bv.append(SN.B_minus_v)

avg_high_bv = np.mean(high_bv)
avg_low_bv = np.mean(low_bv)

print len(high_vel), len(low_vel)
print avg_high_bv, avg_low_bv

# Create figure
fig = plt.figure()
plt.title('Color vs. Si II line Velocity')
plt.ylabel('Observed B - V [mag]')
plt.xlabel(r'$v_\mathrm{abs}$ (Si II $\lambda 6355$) [$10^3$ km/s]')

# Create best fit line
fit = np.polyfit(X,Y,1)
fit_fn = np.poly1d(fit)
fit_label = 'B-V = {0:.4f} {1:.4f} x (v / 10^3 km/s)'.format(fit[1], fit[0])

#calculate Pearson correlation coefficient
correlation = np.corrcoef(X,Y)[0, 1]
print "Correlation coefficient is", correlation

plt.gca().invert_xaxis()
plt.plot(high_vel, high_bv, 'ro', low_vel, low_bv, 'bo')
plt.plot(X, fit_fn(X), '-', label=fit_label)
plt.legend(loc='lower right')
plt.savefig('color-velocity-scatter.png')

#plt.scatter(X, Y)
plt.show()
