#!/bin/env python

import numpy as np
import scipy.signal as ss
import astropy.io.fits as fits
import matplotlib.pyplot as plt


inpt = str(raw_input("Nome do Arquivo: "))
lc = fits.open(inpt)
bin = float(raw_input("bin size (or camera resolution): "))

# Convert to big-endian array is necessary to the lombscargle function
time = np.array(lc[1].data["TIME"], dtype='float64')
time -= time.min()
rate = np.array(lc[1].data["RATE"], dtype='float64')

# Exclude NaN and negative values -------------------------
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
#-----------------------------------------------------------

# normalize rate array
nrate -= nrate.mean()

# normalization to the periodogram
norm = ntime.shape[0]

# duration of observation
interval = time.max()-time.min()

# minimum frequency limited by observed time
freqmin = 1.0/(interval-bin)

# maximium frequency limited by time resolution
freqmax = 1.0/(2.0*bin)

# size of the array of frequencies
nint = 10*len(nrate)

# Frequency array
freqs = np.linspace(freqmin, freqmax, nint)

# scipy.signal.lombscargle uses angular frequencies
afreqs = 2.0*np.pi*freqs

# Ther periodogram itself
pgram = ss.lombscargle(ntime, nrate, afreqs)

# Plot lightcurve on top panel
plt.subplot(2, 1, 1)
plt.plot(ntime, nrate, 'bo-')
plt.xlabel('Time [s]', fontsize=12)
plt.ylabel('Normalized Count Rate [counts/s]', fontsize=12)
plt.xlim(time.min(), time.max())

# Plot powerspectrum on bottom panel
plt.subplot(2, 1, 2)
plt.plot(freqs, np.sqrt(4*(pgram/norm)), 'b.-',
        label='f = {0:.3e}'.format(freqs[np.argmax(pgram)]))
plt.xlabel('Frequency [Hz]', fontsize=12)
plt.ylabel('$Z_n^2$ Power', fontsize=12)
plt.xlim(freqmin, freqmax)

# show plot
plt.legend(loc='best')
plt.show()
