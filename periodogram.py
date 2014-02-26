#!/bin/env python

import numpy as np
import scipy.signal as ss
import astropy.io.fits as fits
import matplotlib.pyplot as plt


inpt = str(raw_input("Nome do Arquivo: "))
lc = fits.open(inpt)
bin = float(raw_input("bin size (or camera resolution): "))

# Convert to big-endian array is necessary to the lombscargle function
rate = np.array(lc[1].data["RATE"], dtype='float64')
time = np.array(lc[1].data["TIME"], dtype='float64')
time -= time.min()

# Exclue NaN values -------------------------
print ''
print 'Excluding nan and negative values...'
print ''

exclude = []
for i in xrange(len(rate)):
    if rate[i] > 0:
        pass
    else:
        exclude.append(i)

exclude = np.array(exclude)
nrate = np.delete(rate, exclude)
ntime = np.delete(time, exclude)
# --------------------------------------------

# normalize count rate
nrate -= nrate.mean()

# maximum frequecy limited by resolution
freqmax = 1.0/bin

# Ther periodogram itself
f, p = ss.periodogram(nrate, fs=freqmax)

# Plot lightcurve on top panel
plt.subplot(2, 1, 1)
plt.plot(ntime, nrate, 'bo-')
plt.xlabel('Time [s]', fontsize=12)
plt.ylabel('Normalized Count Rate [counts/s]', fontsize=12)

# Plot powerspectrum on bottom panel
plt.subplot(2, 1, 2)
plt.plot(f, p, 'b.-', label='f = {0}'.format(f[np.argmax(p)]))
plt.xlabel('Frequency [Hz]', fontsize=12)
plt.ylabel('Power', fontsize=12)
plt.legend(loc='best')

# show plot
plt.show()
