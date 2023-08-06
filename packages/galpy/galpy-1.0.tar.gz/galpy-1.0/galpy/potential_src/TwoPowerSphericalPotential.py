###############################################################################
#   TwoPowerSphericalPotential.py: General class for potentials derived from 
#                                  densities with two power-laws
#
#                                                    amp
#                             rho(r)= ------------------------------------
#                                      (r/a)^\alpha (1+r/a)^(\beta-\alpha)
###############################################################################
import math as m
import numpy
from scipy import special, optimize
from galpy.util import bovy_conversion
from Potential import Potential
class TwoPowerSphericalPotential(Potential):
    """Class that implements spherical potentials that are derived from 
    two-power density models

    .. math::

        \\rho(r) = \\frac{\\mathrm{amp}}{4\\,\\pi\\,a^3}\\,\\frac{1}{(r/a)^\\alpha\\,(1+r/a)^{\\beta-\\alpha}}
    """
    def __init__(self,amp=1.,a=5.,alpha=1.5,beta=3.5,normalize=False):
        """
        NAME:

           __init__

        PURPOSE:

           initialize a two-power-density potential

        INPUT:

           amp - amplitude to be applied to the potential (default: 1)

           a - "scale" (in terms of Ro)

           alpha - inner power

           beta - outer power

           normalize - if True, normalize such that vc(1.,0.)=1., or, if given as a number, such that the force is this fraction of the force necessary to make vc(1.,0.)=1.

        OUTPUT:

           (none)

        HISTORY:

           2010-07-09 - Started - Bovy (NYU)

        """
        self.a= a
        self._scale= self.a
        self.alpha= alpha
        self.beta= beta
        if alpha == round(alpha) and beta == round(beta):
            Potential.__init__(self,amp=amp)
            integerSelf= TwoPowerIntegerSphericalPotential(amp=1.,a=a,
                                                           alpha=int(alpha),
                                                           beta=int(beta),
                                                           normalize=False)
            self.integerSelf= integerSelf
        else:
            Potential.__init__(self,amp=amp)
            self.integerSelf= None
        if normalize or \
                (isinstance(normalize,(int,float)) \
                     and not isinstance(normalize,bool)): #pragma: no cover
            self.normalize(normalize)
        return None

    def _evaluate(self,R,z,phi=0.,t=0.,_forceFloatEval=False):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2010-07-09 - Started - Bovy (NYU)
        """
        if not _forceFloatEval and not self.integerSelf == None:
            return self.integerSelf._evaluate(R,z,phi=phi,t=t)
        elif self.beta == 3.:
            r= numpy.sqrt(R**2.+z**2.)
            return (1./self.a)\
                *(r-self.a*(r/self.a)**(3.-self.alpha)/(3.-self.alpha)\
                      *special.hyp2f1(3.-self.alpha,
                                      2.-self.alpha,
                                      4.-self.alpha,
                                      -r/self.a))/(self.alpha-2.)/r
        else:
            r= numpy.sqrt(R**2.+z**2.)
            return special.gamma(self.beta-3.)\
                *((r/self.a)**(3.-self.beta)/special.gamma(self.beta-1.)\
                      *special.hyp2f1(self.beta-3.,
                                      self.beta-self.alpha,
                                      self.beta-1.,
                                      -self.a/r)
                  -special.gamma(3.-self.alpha)/special.gamma(self.beta-self.alpha))/r

    def _Rforce(self,R,z,phi=0.,t=0.,_forceFloatEval=False):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the radial force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        if not _forceFloatEval and not self.integerSelf == None:
            return self.integerSelf._Rforce(R,z,phi=phi,t=t)
        else:
            r= numpy.sqrt(R**2.+z**2.)
            return -R/r**self.alpha*self.a**(self.alpha-3.)/(3.-self.alpha)\
                *special.hyp2f1(3.-self.alpha,
                                self.beta-self.alpha,
                                4.-self.alpha,
                                -r/self.a)

    def _zforce(self,R,z,phi=0.,t=0.,_forceFloatEval=False):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the vertical force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        if not _forceFloatEval and not self.integerSelf == None:
            return self.integerSelf._zforce(R,z,phi=phi,t=t)
        else:
            r= numpy.sqrt(R**2.+z**2.)
            return -z/r**self.alpha*self.a**(self.alpha-3.)/(3.-self.alpha)\
                *special.hyp2f1(3.-self.alpha,
                                self.beta-self.alpha,
                                4.-self.alpha,
                                -r/self.a)

    def _dens(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _dens
        PURPOSE:
           evaluate the density force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the density
        HISTORY:
           2010-08-08 - Written - Bovy (NYU)
        """
        r= numpy.sqrt(R**2.+z**2.)
        return (self.a/r)**self.alpha/(1.+r/self.a)**(self.beta-self.alpha)/4./m.pi/self.a**3.

    def _z2deriv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _z2deriv
        PURPOSE:
           evaluate the second vertical derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           the second vertical derivative
        HISTORY:
           2012-07-26 - Written - Bovy (IAS@MPIA)
        """
        return self._R2deriv(numpy.fabs(z),R) #Spherical potential

    def _mass(self,R,z=0.,t=0.):
        """
        NAME:
           _mass
        PURPOSE:
           evaluate the mass within R for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           t - time
        OUTPUT:
           the mass enclosed
        HISTORY:
           2014-04-01 - Written - Erkal (IoA)
        """
        if z is None: r= R
        else: r= numpy.sqrt(R**2.+z**2.)
        return (r/self.a)**(3.-self.alpha)/(3.-self.alpha)*special.hyp2f1(3.-self.alpha,-self.alpha+self.beta,4.-self.alpha,-r/self.a)

class TwoPowerIntegerSphericalPotential(TwoPowerSphericalPotential):
    """Class that implements the two-power-density spherical potentials in 
    the case of integer powers"""
    def __init__(self,amp=1.,a=1.,alpha=1,beta=3,normalize=False):
        """
        NAME:
           __init__
        PURPOSE:
           initialize a two-power-density potential for integer powers
        INPUT:
           amp - amplitude to be applied to the potential (default: 1)
           a - "scale" (in terms of Ro)
           alpha - inner power (default: NFW)
           beta - outer power (default: NFW)
           normalize - if True, normalize such that vc(1.,0.)=1., or, if 
                       given as a number, such that the force is this fraction 
                       of the force necessary to make vc(1.,0.)=1.
        OUTPUT:
           (none)
        HISTORY:
           2010-07-09 - Started - Bovy (NYU)
        """
        self.alpha= alpha
        self.beta= beta
        self.a= a
        self._scale= self.a
        if alpha == 1 and beta == 4:
            Potential.__init__(self,amp=amp)
            HernquistSelf= HernquistPotential(amp=1.,a=a,normalize=False)
            self.HernquistSelf= HernquistSelf
            self.JaffeSelf= None
            self.NFWSelf= None
        elif alpha == 2 and beta == 4:
            Potential.__init__(self,amp=amp)
            JaffeSelf= JaffePotential(amp=1.,a=a,normalize=False)
            self.HernquistSelf= None
            self.JaffeSelf= JaffeSelf
            self.NFWSelf= None
        elif alpha == 1 and beta == 3:
            Potential.__init__(self,amp=amp)
            NFWSelf= NFWPotential(amp=1.,a=a,normalize=False)
            self.HernquistSelf= None
            self.JaffeSelf= None
            self.NFWSelf= NFWSelf
        else:
            Potential.__init__(self,amp=amp)
            self.HernquistSelf= None
            self.JaffeSelf= None
            self.NFWSelf= None
        if normalize or \
                (isinstance(normalize,(int,float)) \
                     and not isinstance(normalize,bool)): #pragma: no cover
            self.normalize(normalize)
        return None

    def _evaluate(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2010-07-09 - Started - Bovy (NYU)
        """
        if not self.HernquistSelf == None:
            return self.HernquistSelf._evaluate(R,z,phi=phi,t=t)
        elif not self.JaffeSelf == None:
            return self.JaffeSelf._evaluate(R,z,phi=phi,t=t)
        elif not self.NFWSelf == None:
            return self.NFWSelf._evaluate(R,z,phi=phi,t=t)
        else:
            return TwoPowerSphericalPotential._evaluate(self,R,z,
                                                        phi=phi,t=t,
                                                        _forceFloatEval=True)

    def _Rforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the radial force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        if not self.HernquistSelf == None:
            return self.HernquistSelf._Rforce(R,z,phi=phi,t=t)
        elif not self.JaffeSelf == None:
            return self.JaffeSelf._Rforce(R,z,phi=phi,t=t)
        elif not self.NFWSelf == None:
            return self.NFWSelf._Rforce(R,z,phi=phi,t=t)
        else:
            return TwoPowerSphericalPotential._Rforce(self,R,z,
                                                      phi=phi,t=t,
                                                      _forceFloatEval=True)

    def _zforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the vertical force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        if not self.HernquistSelf == None:
            return self.HernquistSelf._zforce(R,z,phi=phi,t=t)
        elif not self.JaffeSelf == None:
            return self.JaffeSelf._zforce(R,z,phi=phi,t=t)
        elif not self.NFWSelf == None:
            return self.NFWSelf._zforce(R,z,phi=phi,t=t)
        else:
            return TwoPowerSphericalPotential._zforce(self,R,z,
                                                      phi=phi,t=t,
                                                      _forceFloatEval=True)

class HernquistPotential(TwoPowerIntegerSphericalPotential):
    """Class that implements the Hernquist potential

    .. math::

        \\rho(r) = \\frac{\\mathrm{amp}}{4\\,\\pi\\,a^3}\\,\\frac{1}{(r/a)\\,(1+r/a)^{3}}

    """
    def __init__(self,amp=1.,a=1.,normalize=False):
        """
        NAME:

           __init__

        PURPOSE:

           Initialize a Hernquist potential

        INPUT:

           amp - amplitude to be applied to the potential

           a - "scale" (in terms of Ro)

           normalize - if True, normalize such that vc(1.,0.)=1., or, if given as a number, such that the force is this fraction of the force necessary to make vc(1.,0.)=1.

        OUTPUT:

           (none)

        HISTORY:

           2010-07-09 - Written - Bovy (NYU)

        """
        Potential.__init__(self,amp=amp)
        self.a= a
        self._scale= self.a
        self.alpha= 1
        self.beta= 4
        if normalize or \
                (isinstance(normalize,(int,float)) \
                     and not isinstance(normalize,bool)):
            self.normalize(normalize)
        self.hasC= True
        self.hasC_dxdv= True
        return None

    def _evaluate(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2010-07-09 - Started - Bovy (NYU)
        """
        return -1./(1.+numpy.sqrt(R**2.+z**2.)/self.a)/2./self.a

    def _Rforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           the radial force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return -R/self.a/sqrtRz/(1.+sqrtRz/self.a)**2./2./self.a

    def _zforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           t - time
        OUTPUT:
           the vertical force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return -z/self.a/sqrtRz/(1.+sqrtRz/self.a)**2./2./self.a

    def _R2deriv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _R2deriv
        PURPOSE:
           evaluate the second radial derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           the second radial derivative
        HISTORY:
           2011-10-09 - Written - Bovy (IAS)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return (self.a*z**2.+(z**2.-2.*R**2.)*sqrtRz)/sqrtRz**3.\
            /(self.a+sqrtRz)**3./2.

    def _Rzderiv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rzderiv
        PURPOSE:
           evaluate the mixed R,z derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t- time
        OUTPUT:
           d2phi/dR/dz
        HISTORY:
           2013-08-28 - Written - Bovy (IAS)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return -R*z*(self.a+3.*sqrtRz)*(sqrtRz*(self.a+sqrtRz))**-3./2.

    def _mass(self,R,z=0.,t=0.):
        """
        NAME:
           _mass
        PURPOSE:
           calculate the mass out to a given radius
        INPUT:
           R - radius at which to return the enclosed mass
           z - (don't specify this) vertical height
        OUTPUT:
           mass in natural units
        HISTORY:
           2014-01-29 - Written - Bovy (IAS)
        """
        if z is None: r= R
        else: r= numpy.sqrt(R**2.+z**2.)
        return (r/self.a)**2./2./(1.+r/self.a)**2.

class JaffePotential(TwoPowerIntegerSphericalPotential):
    """Class that implements the Jaffe potential

    .. math::

        \\rho(r) = \\frac{\\mathrm{amp}}{4\\,\\pi\\,a^3}\\,\\frac{1}{(r/a)^2\\,(1+r/a)^{2}}

    """
    def __init__(self,amp=1.,a=1.,normalize=False):
        """
        NAME:

           __init__

        PURPOSE:

           Initialize a Jaffe potential

        INPUT:

           amp - amplitude to be applied to the potential

           a - "scale" (in terms of Ro)

           normalize - if True, normalize such that vc(1.,0.)=1., or, if given as a number, such that the force is this fraction of the force necessary to make vc(1.,0.)=1.

        OUTPUT:

           (none)

        HISTORY:

           2010-07-09 - Written - Bovy (NYU)

        """
        Potential.__init__(self,amp=amp)
        self.a= a
        self._scale= self.a
        self.alpha= 2
        self.beta= 4
        if normalize or \
                (isinstance(normalize,(int,float)) \
                     and not isinstance(normalize,bool)): #pragma: no cover
            self.normalize(normalize)
        self.hasC= True
        self.hasC_dxdv= True
        return None

    def _evaluate(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2010-07-09 - Started - Bovy (NYU)
        """
        return -numpy.log(1.+self.a/numpy.sqrt(R**2.+z**2.))/self.a

    def _Rforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the radial force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return -R/sqrtRz**3./(1.+self.a/sqrtRz)

    def _zforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the vertical force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return -z/sqrtRz**3./(1.+self.a/sqrtRz)

    def _R2deriv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _R2deriv
        PURPOSE:
           evaluate the second radial derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the second radial derivative
        HISTORY:
           2011-10-09 - Written - Bovy (IAS)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return (self.a*(z**2.-R**2.)+(z**2.-2.*R**2.)*sqrtRz)\
            /sqrtRz**4./(self.a+sqrtRz)**2.

    def _Rzderiv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rzderiv
        PURPOSE:
           evaluate the mixed R,z derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           d2phi/dR/dz
        HISTORY:
           2013-08-28 - Written - Bovy (IAS)
        """
        sqrtRz= numpy.sqrt(R**2.+z**2.)
        return -R*z*(2.*self.a+3.*sqrtRz)*sqrtRz**-4.\
            *(self.a+sqrtRz)**-2.

    def _mass(self,R,z=0.,t=0.):
        """
        NAME:
           _mass
        PURPOSE:
           calculate the mass out to a given radius
        INPUT:
           R - radius at which to return the enclosed mass
           z - (don't specify this) vertical height
        OUTPUT:
           mass in natural units
        HISTORY:
           2014-01-29 - Written - Bovy (IAS)
        """
        if z is None: r= R
        else: r= numpy.sqrt(R**2.+z**2.)
        return r/self.a/(1.+r/self.a)

class NFWPotential(TwoPowerIntegerSphericalPotential):
    """Class that implements the NFW potential

    .. math::

        \\rho(r) = \\frac{\\mathrm{amp}}{4\\,\\pi\\,a^3}\\,\\frac{1}{(r/a)\\,(1+r/a)^{2}}

    """
    def __init__(self,amp=1.,a=1.,normalize=False,
                 conc=None,mvir=None,
                 vo=220.,ro=8.,
                 H=70.,Om=0.3,overdens=200.,wrtcrit=False):
        """
        NAME:

           __init__

        PURPOSE:

           Initialize a NFW potential

        INPUT:

           amp - amplitude to be applied to the potential

           a - "scale" (in terms of Ro)

           normalize - if True, normalize such that vc(1.,0.)=1., or, if given as a number, such that the force is this fraction of the force necessary to make vc(1.,0.)=1.


           Alternatively, NFW potentials can be initialized using 

              conc= concentration

              mvir= virial mass in 10^12 Msolar

           in which case you also need to supply the following keywords
           
              vo= (220.) velocity unit in km/s

              ro= (8.) length unit in kpc

              H= (default: 70) Hubble constant in km/s/Mpc
           
              Om= (default: 0.3) Omega matter
       
              overdens= (200) overdensity which defines the virial radius

              wrtcrit= (False) if True, the overdensity is wrt the critical density rather than the mean matter density
           
        OUTPUT:

           (none)

        HISTORY:

           2010-07-09 - Written - Bovy (NYU)

           2014-04-03 - Initialization w/ concentration and mass - Bovy (IAS)

        """
        Potential.__init__(self,amp=amp)
        if conc is None:
            self.a= a
            self.alpha= 1
            self.beta= 3
            if normalize or \
                    (isinstance(normalize,(int,float)) \
                         and not isinstance(normalize,bool)):
                self.normalize(normalize)
        else:
            if wrtcrit:
                od= overdens/bovy_conversion.dens_in_criticaldens(vo,ro,H=H)
            else:
                od= overdens/bovy_conversion.dens_in_meanmatterdens(vo,ro,H=H,Om=Om)
            mvirNatural= mvir*100./bovy_conversion.mass_in_1010msol(vo,ro)
            rvir= (3.*mvirNatural/od/4./numpy.pi)**(1./3.)
            self.a= rvir/conc
            self._amp= mvirNatural/(numpy.log(1.+conc)-conc/(1.+conc))
        self._scale= self.a
        self.hasC= True
        self.hasC_dxdv= True
        return None

    def _evaluate(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _evaluate
        PURPOSE:
           evaluate the potential at R,z
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           Phi(R,z)
        HISTORY:
           2010-07-09 - Started - Bovy (NYU)
        """
        r= numpy.sqrt(R**2.+z**2.)
        return -numpy.log(1.+r/self.a)/r

    def _Rforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rforce
        PURPOSE:
           evaluate the radial force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the radial force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        Rz= R**2.+z**2.
        sqrtRz= numpy.sqrt(Rz)
        return R*(1./Rz/(self.a+sqrtRz)-numpy.log(1.+sqrtRz/self.a)/sqrtRz/Rz)

    def _zforce(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _zforce
        PURPOSE:
           evaluate the vertical force for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the vertical force
        HISTORY:
           2010-07-09 - Written - Bovy (NYU)
        """
        Rz= R**2.+z**2.
        sqrtRz= numpy.sqrt(Rz)
        return z*(1./Rz/(self.a+sqrtRz)-numpy.log(1.+sqrtRz/self.a)/sqrtRz/Rz)

    def _R2deriv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _R2deriv
        PURPOSE:
           evaluate the second radial derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           the second radial derivative
        HISTORY:
           2011-10-09 - Written - Bovy (IAS)
        """
        Rz= R**2.+z**2.
        sqrtRz= numpy.sqrt(Rz)
        return (3.*R**4.+2.*R**2.*(z**2.+self.a*sqrtRz)\
                    -z**2.*(z**2.+self.a*sqrtRz)\
                    -(2.*R**2.-z**2.)*(self.a**2.+R**2.+z**2.+2.*self.a*sqrtRz)\
                    *numpy.log(1.+sqrtRz/self.a))\
                    /Rz**2.5/(self.a+sqrtRz)**2.

    def _Rzderiv(self,R,z,phi=0.,t=0.):
        """
        NAME:
           _Rzderiv
        PURPOSE:
           evaluate the mixed R,z derivative for this potential
        INPUT:
           R - Galactocentric cylindrical radius
           z - vertical height
           phi - azimuth
           t - time
        OUTPUT:
           d2phi/dR/dz
        HISTORY:
           2013-08-28 - Written - Bovy (IAS)
        """
        Rz= R**2.+z**2.
        sqrtRz= numpy.sqrt(Rz)
        return -R*z*(-4.*Rz-3.*self.a*sqrtRz+3.*(self.a**2.+Rz+2.*self.a*sqrtRz)*numpy.log(1.+sqrtRz/self.a))*Rz**-2.5*(self.a+sqrtRz)**-2.

    def _mass(self,R,z=0.,t=0.):
        """
        NAME:
           _mass
        PURPOSE:
           calculate the mass out to a given radius
        INPUT:
           R - radius at which to return the enclosed mass
           z - (don't specify this) vertical height
        OUTPUT:
           mass in natural units
        HISTORY:
           2014-01-29 - Written - Bovy (IAS)
        """
        if z is None: r= R
        else: r= numpy.sqrt(R**2.+z**2.)
        return numpy.log(1+r/self.a)-r/self.a/(1.+r/self.a)

    def rvir(self,vo,ro,H=70.,Om=0.3,overdens=200.,wrtcrit=False):
        """
        NAME:

           rvir

        PURPOSE:

           calculate the virial radius for this density distribution

        INPUT:

           vo - velocity unit in km/s

           ro - length unit in kpc

           H= (default: 70) Hubble constant in km/s/Mpc
           
           Om= (default: 0.3) Omega matter
       
           overdens= (200) overdensity which defines the virial radius

           wrtcrit= (False) if True, the overdensity is wrt the critical density rather than the mean matter density
           
        OUTPUT:
        
           virial radius in natural units
        
        HISTORY:

           2014-01-29 - Written - Bovy (IAS)

        """
        if wrtcrit:
            od= overdens/bovy_conversion.dens_in_criticaldens(vo,ro,H=H)
        else:
            od= overdens/bovy_conversion.dens_in_meanmatterdens(vo,ro,H=H,Om=Om)
        dc= 12.*self.dens(self.a,0.)/od
        x= optimize.brentq(lambda y: (numpy.log(1.+y)-y/(1.+y))/y**3.-1./dc,
                           0.01,100.)
        return x*self.a
