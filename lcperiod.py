#!/bin/env python

import numpy as np
import scipy.signal as ss
import astropy.io.fits as fits
import matplotlib.pyplot as plt

inpt = str(raw_input("Nome do Arquivo: "))
lc = fits.open(inpt)

# Convert to big-endian array is necessary to the lombscargle function
time = np.array(lc[1].data["TIME"], dtype='float64')
rate = np.array(lc[1].data["RATE"], dtype='float64')
norm = timecolumn.shape[0]

# Probably buggy, check the units (angular vs Hz)
freqs = np.linspace(0.0001,0.001,900)

# Ther periodogram itself
pgram = ss.lombscargle(time,rate,freqs)

# Plot lightcurve on top panel and powerspectrum on bottom panel
plt.subplot(2,1,1)
plt.plot(time,rate,'b+')
plt.subplot(2,1,2)
plt.plot(freqs,np.sqrt(4*(pgram/norm)))
plt.show()
