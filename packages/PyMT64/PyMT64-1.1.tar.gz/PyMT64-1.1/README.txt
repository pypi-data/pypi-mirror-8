                     PyMT64
                     
PyMT64 is a Python version of the Mersenne Twister (MT) 64-bit pseudorandom number generator by Takuji Nishimura and Makoto Matsumoto (see http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/emt64.html and the references below).

This customised version is thread safe and was interfaced from C to Python (see pymt64.c)

This module provides the following methods:
- init : initialization of the state vector (mt) used by the pseudorandom number generator (PNG)
- uniform : generation of an uniform distribution
- normal : generation of two Normal distributions
- poisson : generation of a Poisson distribution

The period of the PNG is 2**19937-1.

Example:
	import time
	import pymt64
	seed = int(time.time()) # the initial seed
	mt = pymt64.init(seed) # initialisation of the state vector of MT
	u = pymt64.uniform(mt,10) # generation of an uniform distribution
	print u
	[ 0.94295421  0.47222327  0.634552    0.26012686  0.38431784  0.23995444
	  0.02175826  0.8209848   0.79266556  0.8638286 ]

For a complete example, see pymt64_test.py

Note: the state vector 'mt' returned by pymt64.init has 313 elements instead of the 312 elements of the original C code. This is because the 313th element store the associated counter (mti).

Change history:
1.1 : fix a problem with the initialization of the seed  (in the previous version the seed set by init() was not taken into account such that the results were not reproductible)

1.0 : initial version


R. Samadi (LESIA, Observatoire de Paris), 22 Dec. 2012	    

References:
   T. Nishimura, ``Tables of 64-bit Mersenne Twisters''
     ACM Transactions on Modeling and 
     Computer Simulation 10. (2000) 348--357.
   M. Matsumoto and T. Nishimura,
     ``Mersenne Twister: a 623-dimensionally equidistributed
       uniform pseudorandom number generator''
     ACM Transactions on Modeling and 
     Computer Simulation 8. (Jan. 1998) 3--30.
