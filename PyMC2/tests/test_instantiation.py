###
# Test that decorators return the appropriate object.
# David Huard
# June 21, 2007
###

###
# TODO
# ----
# Add test for node
# Check discrete and binary parameters
# Test the distribution instantiators.
###

from numpy.testing import *
import PyMC2
from PyMC2 import Sampler, data, parameter, node, discrete_parameter, \
    Parameter,Node
from numpy import array, log, sum, ones, concatenate, inf
from PyMC2 import uniform_like, exponential_like, poisson_like


D_array =   array([ 4, 5, 4, 0, 1, 4, 3, 4, 0, 6, 3, 3, 4, 0, 2, 6,
                    3, 3, 5, 4, 5, 3, 1, 4, 4, 1, 5, 5, 3, 4, 2, 5,
                    2, 2, 3, 4, 2, 1, 3, 2, 2, 1, 1, 1, 1, 3, 0, 0,
                    1, 0, 1, 1, 0, 0, 3, 1, 0, 3, 2, 2, 0, 1, 1, 1,
                    0, 1, 0, 1, 0, 0, 0, 2, 1, 0, 0, 0, 1, 1, 0, 2,
                    3, 3, 1, 1, 2, 1, 1, 1, 1, 2, 4, 2, 0, 0, 1, 4,
                    0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1])

# Define data and parameters

@discrete_parameter
def s(value=50, length=110):
    """Change time for rate parameter."""
    return uniform_like(value, 0, length)

@parameter
def e(value=1., rate=1.):
    """Rate parameter of poisson distribution."""
    return exponential_like(value, rate)

@parameter
def l(value=.1, rate = 1.):
    """Rate parameter of poisson distribution."""
    return exponential_like(value, rate)
        
@data(discrete=True)
def D(  value = D_array,
        s = s,
        e = e,
        l = l):
    """Annual occurences of coal mining disasters."""
    return poisson_like(value[:s],e) + poisson_like(value[s:],l)

E = data(e)

@data
def F(value = D_array*.5,
        s = s,
        e = e,
        l = l):
    """Annual occurences of coal mining disasters."""
    return poisson_like(value[:s],e) + poisson_like(value[s:],l)
        
@data
@parameter
def G(value = D_array*.5,
        s = s,
        e = e,
        l = l):
    """Annual occurences of coal mining disasters."""
    return poisson_like(value[:s],e) + poisson_like(value[s:],l)
        
class test_instantiation(NumpyTestCase):
    def check_data(self):
        assert(isinstance(D, Parameter))
        assert(D.isdata)
        assert(isinstance(E, Parameter))
        assert(E.isdata)
        assert(isinstance(F, Parameter))
        assert(F.isdata)
        assert(isinstance(G, Parameter))
        assert(G.isdata)
    def check_parameter(self):
        assert(isinstance(l, Parameter))
        assert(not l.isdata)
if __name__ == '__main__':
    NumpyTest().run()
