import numpy as np
import matplotlib.pyplot as plt
import myscitools as tools
from astropy.io import fits


input1 = str(raw_input('First light curve: '))
input2 = str(raw_input('Second light curve: '))
lc1 = fits.open(input1)
lc2 = fits.open(input2)
time = lc1[1].data.field('TIME')
rate1 = lc1[1].data.field('RATE')
rate2 = lc2[1].data.field('RATE')
lc1.close()
lc2.close()

timecol = [time, 'TIME', 'E', 's']

try:
    sum = rate1+rate2
except ValueError:
    print " Coult not add lightcurves {0} and {1}".format(input1, input2)
else:
    sumcol = [sum, 'RATE', 'E', 'counts/s']

try:
    ratio = rate1/rate2
except ValueError:
    print " could not divide {0} and {1}!".format(input1, input2)
else:
    ratiocol = [ratio, 'RATIO', 'E', '']

try:
    hardness = (rate2-rate1)/sum
except ValueError:
    print " Could not calculate hardness. The sum of intensity is 0!"
else:
    hardcol = [hardness, 'HR', 'E', '']

try:
    tools.makefits(output, timecol, sumcol, ratiocol, hardcol)
except:
    print "no output"
