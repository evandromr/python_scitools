#!/usr/env python

import pprocess  # parallel computing module
import os  # os utilitites
import time  # keep track of time

import astropy.io.fits as fits  # FITS manipulating library
import matplotlib.pyplot as plt
import numpy as np  # numeric python for array manipulation

import myscitools  # my personal tools


#input file informations and variables atributions----------------------
inptname = str(raw_input('Input file (with extension): '))
outptname = os.path.splitext(inptname)[0]+'_z2n_output.fits'
inpt = fits.open(inptname)
times = inpt[1].data.field('TIME')
inpt.close()

interval = float(times.max()-times.min())
startf = 1.0/interval

print "The start frequency is: ", startf
query = str(raw_input("Change the start frequency? (y/n): "))
if (query == 'y') or (query == 'Y'):
    startf = float(raw_input('Enter the start frequency: '))
else:
    pass

endf = float(raw_input('Enter the last frequency: '))

over = float(raw_input('Enter oversample factor: '))
fact = 1.0/over
deltaf = fact/interval

print "The frequency step will be: ", deltaf
query2 = str(raw_input('Change frequency step? (y/n): '))
if (query2 == 'y') or (query2 == 'Y'):
    deltaf = float(raw_input('Enter the frequency interval: '))
else:
    pass

freqs = np.arange(startf, endf, deltaf)

#harm = int(raw_input('The Harmonic to be considered:'))
harm = 1
#----------------- The parallelism starts here ------------------------
nproc = int(raw_input('Enter the number of processor to use: '))
if nproc < 1:
    nproc = 1  # default number of cpus = 1

freqlist = np.array_split(freqs, nproc)

results = pprocess.Map(limit=nproc, reuse=1)
parallel_z2n = results.manage(pprocess.MakeReusable(myscitools.z2n))

print "\n Calculating with ", nproc, " processor(s)\n"

tic = time.time()
[parallel_z2n(somefreqs, times, harm) for somefreqs in freqlist]

z2n = []
for result in results:
    for value in result:
        z2n.append(value)

print 'time = {0}'.format(time.time() - tic)

plt.plot(freqs, z2n)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Z2n Power')
plt.title(inptname)
plt.show()
plt.plot(freqs, z2n)
plt.savefig('z2n.png')

#create and write the output.fits file
col1 = [freqs, 'frequency', 'E', 'Hz']
col2 = [z2n, 'z2nPower', 'E', 'arbitrary']
myscitools.makefits(outptname, col1, col2)
