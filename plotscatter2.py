#!/usr/env python

import astropy.io.fits as fits
import matplotlib.pyplot as plt


if __name__ == '__main__':
    '''
    scatter 2 columns of 2 fits files
    '''

    inpt1 = str(raw_input("Nome do arquivo 1 (eixo x): "))
    inpt2 = str(raw_input("Nome do arquivo 2 (eixo y): "))
    field1 = str(raw_input("Nome da coluna do arquivo 1 (eixo x): "))
    field2 = str(raw_input("Nome da coluna do arquivo 2 (eixo y): "))

    tb1 = fits.open(inpt1)
    tb2 = fits.open(inpt2)

    x = tb1[1].data.field(field1)
    y = tb2[1].data.field(field2)

    plt.scatter(x, y)
    plt.xlabel(field1)
    plt.ylabel(field2)
    plt.show()
