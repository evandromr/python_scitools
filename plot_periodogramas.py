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
mean = nrate.mean()
nrate -= nrate.mean()

# ------------------------------------------- FOR periodogram()
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
plt.plot(f, pnorm, 'b-',
    label='T$_{{pico}}$ = {0:.0f} s'.format(1/f[np.argmax(pnorm)]))
plt.xlabel('Frequencia (Hz)', fontsize=12)
plt.ylabel('Potencia', fontsize=12)
plt.xlim(min(f), max(f))
plt.legend(loc=1)

# ------------------------------------------- FOR lombscargle()

# normalization to the periodogram
norm = ntime.shape[0]
# duration of observation
interval = time.max()-time.min()
# minimum frequency limited to 0,01/T
freqmin = 0.001/interval
# maximium Nyquist frequency limited by time resolution
freqmax = 1.0/(2.0*bin)
# size of the array of frequencies
nint = 10*len(nrate)
# Frequency array
freqs = np.linspace(freqmin, freqmax, nint)
# scipy.signal.lombscargle uses angular frequencies
afreqs = 2.0*np.pi*freqs
print 'f_max = ', max(freqs)
print 'f_min = ', min(freqs)
print "T_obs =", interval
print "N_points = ", norm
print "N_freqs = ", nint
# Ther periodogram itself
pgram = ss.lombscargle(ntime, nrate, afreqs)
# Normalize pgram to units of nrate/freq
pnorm = np.sqrt(4.0*(pgram/norm))
plt.plot(freqs, pnorm, 'k--', lw=1.5, alpha=0.9,
    label='T$_{{pico}}$ = {0:.0f} s'.format(1.0/freqs[np.argmax(pnorm)]))
plt.xlabel('Frequencia (Hz)', fontsize=12)
plt.ylabel('Potencia', fontsize=12)
plt.xlim(min(freqs), max(freqs))
plt.legend(loc=1)
#-------------------------------------------------------------

# save and show plot
plt.savefig("periodogramas_testes.pdf", orientation='landscape', papertype='a4',
        format='pdf', bbox_inches='tight')
plt.show()
