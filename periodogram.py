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

# sample frequecy limited by resolution
fsample = 1.0/(bin)

numb = 10*len(time)

# Thr periodogram itself
f, p = ss.periodogram(nrate, fs=fsample, nfft=numb, scaling='spectrum')

# normalize the periodogram to unts of nrate/freq
pnorm = np.sqrt(p*2.0)

print 'f_max = ', max(f)
print 'f_min = ', min(f)
print 'T_obs =', max(time)

# # Plot lightcurve on top panel
# plt.subplot(2, 1, 1)
# plt.plot(ntime, nrate, 'bo-')
# plt.xlabel('Tempo (s)', fontsize=12)
# plt.ylabel('Cts. s$^{{-1}}$', fontsize=12)
#
# # Plot powerspectrum on bottom panel
# plt.subplot(2, 1, 2)
plt.plot(f, pnorm, 'b-',
    label='T$_{{pico}}$ = {0:.0f} s'.format(1/f[np.argmax(pnorm)]))
plt.xlabel('Frequencia (Hz)', fontsize=12)
plt.ylabel('Potencia', fontsize=12)
plt.xlim(min(f), max(f))
plt.legend(loc=1)

# save and show plot
plt.savefig("periodogram_testes.pdf", orientation='landscape', papertype='a4',
        format='pdf', bbox_inches='tight')
plt.show()
