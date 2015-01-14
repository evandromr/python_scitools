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

print 'TIME =', max(time)
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
f, p = ss.welch(nrate, fs=freqmax)#, nperseg=len(nrate))

plt.plot(f, p, linestyle='steps', label='T$_{{peak}} = {0:.3f} s'.format(1.0/f[np.argmax(p)]))
plt.xlabel('Frequency (Hz)')#, fontsize=12)
plt.ylabel('Power')#, fontsize=12)
plt.legend(loc='best', frameon=False)

# show plot
plt.savefig('welch.pdf', orientation='landscape', papertype='a4', format='pdf',
        bbox_inches='tight')
plt.show()
