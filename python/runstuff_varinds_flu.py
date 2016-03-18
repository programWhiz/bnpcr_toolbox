# Autogenerated with SMOP version 
# /usr/local/bin/smop runstuff_varinds_flu.m -o ../python/runstuff_varinds_flu.py

from __future__ import division
try:
    from runtime import *
except ImportError:
    from smop.runtime import *

import os
import numpy as np
from numpy import diagonal
from numpy.linalg import inv, cholesky as chol
from .BNP_covreg_varinds import BNP_covreg_varinds_

FILE_DIR = os.path.dirname( os.path.abspath(__file__) )
data = load_(open(os.path.join( FILE_DIR, 'flu_US.mat' )))

month_names=[ 'January','February','March',
    'April','May','June','July','August','September','October','November','December' ]

flu = data['data'].T

for ii in xrange(size_(flu,1)):
    start_date_ii = 0
    for tt in xrange(size_(flu,2)):
        if np.isnan(flu[ii,tt]):
            start_date_ii += 1
    flu[ii,0:start_date_ii] = 0

q,T=size_(flu,nargout=2)

# normalize the flu data
flu_norms = np.sqrt( np.max(flu, axis=1) )
flu /= flu_norms[:, np.newaxis]
y = flu * 1.75  # why?

# Start only after date where there is data for all y vecs
tmp = np.cumsum(np.sum(y,axis=-1), axis=-1)
tmp = np.where(tmp == 0)[0]
if np.any(tmp):
    start_time = tmp[-1] + 1
    y = y[:][ start_time:-1 ]

# Boolean vector containing True for all 
# y vectors that have a value greater than zero
inds_y = np.ones(y.shape)
inds_y[np.where(y == 0)[0]] = 0
inds_y = inds_y > 0

p,N = y.shape
x = np.arange(1, N+1) / N
c=100
d=1
r=1e-05
K=np.zeros((N,N))

for ii in xrange(N):
    for jj in xrange(N):
        dist_ii_jj = np.abs(x[ii] - x[jj])
        K[ii,jj] = d * np.exp(- c * (dist_ii_jj ** 2))

K = K + diagonal(r * np.ones((1,N)))
print diagonal(K)
invK = inv(K)
logdetK=2 * np.sum(np.log(diagonal( chol(K))))

prior_params.K.c_prior=1
prior_params.K.invK=invK
prior_params.K.K=K
prior_params.K.logdetK=logdetK
prior_params.sig.a_sig=1
prior_params.sig.b_sig=0.1
prior_params.hypers.a_phi=1.5
prior_params.hypers.b_phi=1.5
prior_params.hypers.a1=10
prior_params.hypers.a2=10

settings.L=10
settings.k=20
settings.Niter=10000
settings.saveEvery=100
settings.storeEvery=10
settings.saveMin=1
settings.saveDir=char('flu')
settings.trial=1
settings.init2truth=0
settings.sample_K_flag=3
settings.latent_mean=1
settings.inds_y=inds_y

BNP_covreg_varinds_(y,prior_params,settings,0)