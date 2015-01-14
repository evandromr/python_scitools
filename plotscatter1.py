#!/usr/env python

import astropy.io.fits as fits
import matplotlib.pyplot as plt


if __name__ == '__main__':
    '''
    scatter 2 columns of a fits files
    '''

    inpt1 = str(raw_input("Nome do primeiro arquivo: "))
    field1 = str(raw_input("Nome da coluna X: "))
    field2 = str(raw_input("Nome da coluna Y: "))

    tb1 = fits.open(inpt1)

    x = tb1[1].data.field(field1)
    y = tb1[1].data.field(field2)

    plt.scatter(x, y)
    plt.xlabel(field1)
    plt.xlabel(field2)
    plt.show()
