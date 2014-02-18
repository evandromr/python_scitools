#!/usr/env python

import pprocess  # parallel computing module
import os  # os utilitites
import time  # 

import astropy.io.fits as fits  # FITS manipulating library
import matplotlib.pyplot as plt
import numpy as np  # numeric python for array manipulation

import myscitools # my personal tools


#input file informations and variables atributions----------------------
inptname = str(raw_input('Input file (with extension): '))
outptname = os.path.splitext(inptname)[0]+'_z2n_output_t.fits'
inpt = fits.open(inptname)
times = inpt[1].data.field('TIME')
inpt.close()

startf = float(raw_input('Enter the start frequency: '))
endf = float(raw_input('Enter the last frequency: '))
deltaf = float(raw_input('Enter the frequency interval: '))
freqs = np.arange(startf, endf, deltaf)

harm = int(raw_input('The Harmonic to be considered:'))

#----------------- The parallelism starts here ------------------------
nproc = int(raw_input('Enter the number of processor to use: '))
if nproc < 1:
    nproc = 1  # default number of cpus = 1

freqlist = np.array_split(freqs, nproc)


results = pprocess.Map(limit=nproc, reuse=1)
parallel_z2n = results.manage(pprocess.MakeReusable(myscitools.z2n))

print "\n Calculating with ", nproc, " processor(s)\n"

tic = clock.time()
[parallel_z2n(somefreqs, times, harm) for somefreqs in freqlist]

print 'time = {0}'.format(time.time() - tic)
z2n = []
for result in results:
    for value in result:
        z2n.append(value)

print z2n

plt.plot(freqs, z2n)
plt.savefig('teste.png')

#create and write the output.fits file
col1 = [freqs, 'Frequency', 'E', 'Hz']
col2 = [z2n, 'Z2nPower', 'E', 'arbitrary']
myscitools.makefits(outptname, col1, col2)
