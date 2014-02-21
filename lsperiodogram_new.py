#!/bin/env python

import numpy as np
import scipy.signal as ss
import astropy.io.fits as fits
import matplotlib.pyplot as plt

inpt = str(raw_input("Nome do Arquivo: "))
lc = fits.open(inpt)
bin = float(raw_input("bin size (or camera resolution): "))
oversample = float(raw_input('Fator de Oversample:'))

# Convert to big-endian array is necessary to the lombscargle function
time = np.array(lc[1].data["TIME"], dtype='float64')
rate = np.array(lc[1].data["RATE"], dtype='float64')
norm = time.shape[0]

exclude = []
for i in xrange(len(rate)):
    if rate[i] > 0 :
        pass
    else:
        exclude.append(i)

exclude = np.array(exclude)
nrate = np.delete(rate, exclude)
ntime = np.delete(time, exclude)

print 'rate array'
print rate
print ''
print 'Excluding nan and negative values...'
print ''

timemax = max(time)
timemin = min(time)
interval = timemax-timemin
freqmin = 2.0/interval
freqmax = 1.0/bin
nint = oversample/freqmin
# Probably buggy, check the units (angular vs Hz)
freqs = np.linspace(freqmin, freqmax, nint)
afreqs = 2.0*np.pi*freqs

# Ther periodogram itself
pgram = ss.lombscargle(ntime, nrate, afreqs)

# Plot lightcurve on top panel and powerspectrum on bottom panel
plt.subplot(2, 1, 1)
plt.plot(time, rate, 'k-')
plt.subplot(2, 1, 2)
plt.plot(freqs, np.sqrt(4*(pgram/norm)), 'b-')
plt.show()
