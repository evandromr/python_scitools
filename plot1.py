#!/usr/env python

import matplotlib.pyplot as plt
import astropy.io.fits as fits

if __name__ == "__main__":
    '''
    shows the plot 2 given coluns of a fits file
    '''

    inptname = str(raw_input("Nome do Arquivo: "))
    field1 = str(raw_input("Nome da coluna X: "))
    field2 = str(raw_input("Nome da coluna Y: "))

    tb = fits.open(inptname)
    x = tb[1].data.field(field1)
    y = tb[1].data.field(field2)
    tb.close()

    plt.plot(x,y)
    plt.show()
