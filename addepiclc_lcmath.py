#!/usr/env python

import glob
import subprocess


if __name__ == '__main__':
    '''
    Add lightcurves
    MOS1 + MOS2 = MOSS
    PN + MOSS = EPIC
    '''
    mos1files = glob.glob('mos1_lc_net*')
    mos2files = glob.glob('mos2_lc_net*')
    pnfiles = glob.glob('pn_lc_net*')

    mos1files.sort()
    mos2files.sort()
    pnfiles.sort()

    mossfiles = ['moss'+mos1[4:] for mos1 in mos1files]
    epicfiles = ['epic'+mos1[4:] for mos1 in mos1files]

    for mos1, mos2, moss in zip(mos1files, mos2files, mossfiles):
        subprocess.call(['lcmath', mos1, mos2, moss, '1.', '1.', 'yes'])

    for pn, moss, epic in zip(pnfiles, mossfiles, epicfiles):
        subprocess.call(['lcmath', pn, moss, epic, '1.', '1.', 'yes'])

    mos1files = glob.glob('mos1_lc_bkg*')
    mos2files = glob.glob('mos2_lc_bkg*')
    pnfiles = glob.glob('pn_lc_bkg*')

    mos1files.sort()
    mos2files.sort()
    pnfiles.sort()

    mossfiles = ['moss'+mos1[4:] for mos1 in mos1files]
    epicfiles = ['epic'+mos1[4:] for mos1 in mos1files]

    for mos1, mos2, moss in zip(mos1files, mos2files, mossfiles):
        subprocess.call(['lcmath', mos1, mos2, moss, '1.', '1.', 'yes'])

    for pn, moss, epic in zip(pnfiles, mossfiles, epicfiles):
        subprocess.call(['lcmath', pn, moss, epic, '1.', '1.', 'yes'])

