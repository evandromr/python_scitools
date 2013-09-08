#!/usr/env python

import pp  # parallel python library
import os  # os utilitites
import astropy.io.fits as fits  # FITS manipulating py library
import numpy as np  # numeric python for array manipulation
import myscitools


if __name__ == '__main__':
    #input file informations and variables atributions----------------------
    inptname = str(raw_input('Input file (with extension): '))
    outptname = os.path.splitext(inptname)[0]+'_z2n_output.fits'
    inpt = fits.open(inptname)
    time = inpt[1].data.field('TIME')
    inpt.close()

    startf = float(raw_input('Enter the start frequency: '))
    endf = float(raw_input('Enter the last frequency: '))
    deltaf = float(raw_input('Enter the frequency interval: '))
    freqs = np.arange(startf, endf, deltaf)

    harm = int(raw_input('The Harmonic to be considered:'))

    #----------------- The parallelism starts here ------------------------
    ncpus = int(raw_input('Enter the number of processor to use: '))
    if ncpus < 1:
        ncpus = 1  # default number of cpus = 1

    freqlist = np.array_split(freqs, ncpus)

    ppservers = ()
    job_server = pp.Server(ncpus, ppservers=ppservers)

    print "\n Calculating with", job_server.get_ncpus(), "processor(s)\n"

    jobs = [job_server.submit(myscitools.z2n, (somefreqs, time, harm), (),
            ("numpy",)) for somefreqs in freqlist]

    results = []
    [[results.append(value) for value in job()] for job in jobs]

    # create and write the output.fits file
    col1 = [freqs, 'Frequency', 'E', 'Hz']
    col2 = [results, 'Z2n Power', 'E', 'arbitrary']
    myscitools.makefits(outptname, col1, col2)

    #prints jobs information
    job_server.print_stats()
