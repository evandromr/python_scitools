#!/usr/env python

import matplotlib.pyplot as plt
import astropy.io.fits as fits

if __name__ == "__main__":
    '''
    shows the plot 2 given coluns of a fits file
    '''

    inpt1 = str(raw_input("Nome do Arquivo 1 (eixo x): "))
    inpt2 = str(raw_input("Nome do Arquivo 2 (eixo y): "))
    field1 = str(raw_input("Nome da coluna do arquivo 1 (eixo x): "))
    field2 = str(raw_input("Nome da coluna do arquivo 2 (eixo y): "))

    tb1 = fits.open(inpt1)
    tb2 = fits.open(inpt2)
    x = tb1[1].data.field(field1)
    y = tb2[1].data.field(field2)
    tb.close()

    plt.plot(x, y)
    plt.xlabel(field1)
    plt.ylabel(field2)
    plt.show()
