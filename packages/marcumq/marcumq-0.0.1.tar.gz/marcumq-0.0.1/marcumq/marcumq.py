import numpy as np
import scipy.stats

def marcumq(nu,a,b):
    return scipy.stats.ncx2.sf(b**2, 2*nu, a**2)
