import os
import shutil
import warnings
import tempfile
import pickle
import numpy
import scipy.linalg as linalg
class galpyWarning(Warning):
    pass
def _warning(
    message,
    category = galpyWarning,
    filename = '',
    lineno = -1):
    if issubclass(category,galpyWarning):
        print("galpyWarning: "+str(message))
    else:
        print(warnings.formatwarning(message,category,filename,lineno))
warnings.showwarning = _warning
def save_pickles(savefilename,*args,**kwargs):
    """
    NAME:
       save_pickles
    PURPOSE:
       relatively safely save things to a pickle
    INPUT:
       savefilename - name of the file to save to; actual save operation will be performed on a temporary file and then that file will be shell mv'ed to savefilename
       +things to pickle (as many as you want!)
    OUTPUT:
       none
    HISTORY:
       2010-? - Written - Bovy (NYU)
       2011-08-23 - generalized and added to galpy.util - Bovy (NYU)
    """
    saving= True
    interrupted= False
    file, tmp_savefilename= tempfile.mkstemp() #savefilename+'.tmp'
    os.close(file) #Easier this way
    while saving:
        try:
            savefile= open(tmp_savefilename,'wb')
            file_open= True
            if kwargs.get('testKeyboardInterrupt',False) and not interrupted:
                raise KeyboardInterrupt
            for f in args:
                pickle.dump(f,savefile)
            savefile.close()
            file_open= False
            shutil.move(tmp_savefilename,savefilename)
            saving= False
            if interrupted:
                raise KeyboardInterrupt
        except KeyboardInterrupt:
            if not saving:
                raise
            print "KeyboardInterrupt ignored while saving pickle ..."
            interrupted= True
        finally:
            if file_open:
                savefile.close()

def logsumexp(arr,axis=0):
    """Faster logsumexp?"""
    minarr= numpy.amax(arr,axis=axis)
    if axis == 1:
        minarr= numpy.reshape(minarr,(arr.shape[0],1))
    if axis == 0:
        minminarr= numpy.tile(minarr,(arr.shape[0],1))
    elif axis == 1:
        minminarr= numpy.tile(minarr,(1,arr.shape[1]))
    elif axis == None:
        minminarr= numpy.tile(minarr,arr.shape)
    else:
        raise NotImplementedError("'galpy.util.logsumexp' not implemented for axis > 2")
    if axis == 1:
        minarr= numpy.reshape(minarr,(arr.shape[0]))
    return minarr+numpy.log(numpy.sum(numpy.exp(arr-minminarr),axis=axis))

_TINY= 0.000000001
def stable_cho_factor(x,tiny=_TINY):
    """
    NAME:
       stable_cho_factor
    PURPOSE:
       Stable version of the cholesky decomposition
    INPUT:
       x - (sc.array) positive definite matrix
       tiny - (double) tiny number to add to the covariance matrix to make the decomposition stable (has a default)
    OUTPUT:
       (L,lowerFlag) - output from scipy.linalg.cho_factor for lower=True
    REVISION HISTORY:
       2009-09-25 - Written - Bovy (NYU)
    """
    return linalg.cho_factor(x+numpy.sum(numpy.diag(x))*tiny*numpy.eye(x.shape[0]),lower=True)

def fast_cholesky_invert(A,logdet=False,tiny=_TINY):
    """
    NAME:
       fast_cholesky_invert
    PURPOSE:
       invert a positive definite matrix by using its Cholesky decomposition
    INPUT:
       A - matrix to be inverted
       logdet - (Bool) if True, return the logarithm of the determinant as well
       tiny - (double) tiny number to add to the covariance matrix to make the decomposition stable (has a default)
    OUTPUT:
       A^{-1}
    REVISION HISTORY:
       2009-10-07 - Written - Bovy (NYU)
    """
    L= stable_cho_factor(A,tiny=tiny)
    if logdet:
        return (linalg.cho_solve(L,numpy.eye(A.shape[0])),
                2.*numpy.sum(numpy.log(numpy.diag(L[0]))))
    else:
        return linalg.cho_solve(L,numpy.eye(A.shape[0]))
