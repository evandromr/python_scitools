#!/usr/env python

import myscitools
import astropy.io.fits as fits


if __name__ == '__main__':
    '''
    Calculates the ratio between two (equally binned) lightcurves
    '''
    bins = ['5', '10', '50', '150', '350', '500']
    eranges = ['032keV', '245keV', '4510keV']
    cameras = ['PN', 'MOS1', 'MOS2', 'MOSS', 'EPIC']

    for camera in cameras:
        for bin in bins:
            for i, erange in enumerate(eranges[:-1]):
                lc1name = camera+"_lc_net_"+erange+"_bin"+bin+"_timed.ds"
                lc2name = camera+"_lc_net_"+eranges[i+1]+"_bin"+bin+"_timed.ds"
                output = camera+"_HR"+str(i+1)+"_bin"+bin+".ds"
                myscitools.ratiolc(lc1name, lc2name, output)
