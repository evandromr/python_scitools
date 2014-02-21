#!/usr/env python

import glob
import subprocess


if __name__ == '__main__':
    '''
    Add lightcurves
    MOS1 + MOS2 = MOSS
    PN + MOSS = EPIC
    '''
    mos1files = glob.glob('MOS1_lc_net*')
    mos2files = glob.glob('MOS2_lc_net*')
    pnfiles = glob.glob('PN_lc_net*')

    mos1files.sort()
    mos2files.sort()
    pnfiles.sort()

    mossfiles = ['MOSS'+mos1[4:] for mos1 in mos1files]
    epicfiles = ['EPIC'+mos1[4:] for mos1 in mos1files]



    for mos1, mos2, moss in zip(mos1files, mos2files, mossfiles):
        subprocess.call(['lcmath', mos1, mos2, moss, '1.', '1.', 'yes'])

    for pn, moss, epic in zip(pnfiles, mossfiles, epicfiles):
        subprocess.call(['lcmath', pn, moss, epic, '1.', '1.', 'yes'])
