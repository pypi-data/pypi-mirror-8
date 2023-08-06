###############################################################################
#   actionAngle: a Python module to calculate  actions, angles, and frequencies
#
#      class: actionAngleStaeckel
#
#             Use Binney (2012; MNRAS 426, 1324)'s Staeckel approximation for 
#             calculating the actions
#
#      methods:
#             __call__: returns (jr,lz,jz)
#
###############################################################################
import copy
import warnings
import numpy as nu
from scipy import optimize, integrate
from galpy.potential import evaluatePotentials, evaluateRforces, \
    evaluatezforces, evaluateR2derivs, evaluatez2derivs, evaluateRzderivs, \
    epifreq, omegac, verticalfreq
from galpy.util import bovy_coords #for prolate confocal transforms
from galpy.util import galpyWarning
from actionAngle import actionAngle, UnboundError
import actionAngleStaeckel_c
from actionAngleStaeckel_c import _ext_loaded as ext_loaded
from galpy.potential_src.Potential import _check_c
class actionAngleStaeckel():
    """Action-angle formalism for axisymmetric potentials using Binney (2012)'s Staeckel approximation"""
    def __init__(self,*args,**kwargs):
        """
        NAME:
           __init__
        PURPOSE:
           initialize an actionAngleStaeckel object
        INPUT:
           pot= potential or list of potentials (3D)

           delta= focus

           useu0 - use u0 to calculate dV (NOT recommended)

           c= if True, always use C for calculations
        OUTPUT:
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        if not kwargs.has_key('pot'): #pragma: no cover
            raise IOError("Must specify pot= for actionAngleStaeckel")
        self._pot= kwargs['pot']
        if not kwargs.has_key('delta'): #pragma: no cover
            raise IOError("Must specify delta= for actionAngleStaeckel")
        if ext_loaded and ((kwargs.has_key('c') and kwargs['c'])
                           or not kwargs.has_key('c')):           
            self._c= _check_c(self._pot)
            if kwargs.has_key('c') and kwargs['c'] and not self._c:
                warnings.warn("C module not used because potential does not have a C implementation",galpyWarning) #pragma: no cover
        else:
            self._c= False
        if kwargs.has_key('useu0') and kwargs['useu0']:
            self._useu0= True
        else:
            self._useu0= False
        self._delta= kwargs['delta']
        return None
    
    def __call__(self,*args,**kwargs):
        """
        NAME:
           __call__
        PURPOSE:
           evaluate the actions (jr,lz,jz)
        INPUT:
           Either:
              a) R,vR,vT,z,vz
              b) Orbit instance: initial condition used if that's it, orbit(t)
                 if there is a time given as well
            c= True/False; overrides the object's c= keyword to use C or not
           scipy.integrate.quadrature keywords
        OUTPUT:
           (jr,lz,jz)
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        if ((self._c and not (kwargs.has_key('c') and not kwargs['c']))\
                or (ext_loaded and ((kwargs.has_key('c') and kwargs['c'])))) \
                and _check_c(self._pot):
            if len(args) == 5: #R,vR.vT, z, vz
                R,vR,vT, z, vz= args
            elif len(args) == 6: #R,vR.vT, z, vz, phi
                R,vR,vT, z, vz, phi= args
            else:
                meta= actionAngle(*args)
                R= meta._R
                vR= meta._vR
                vT= meta._vT
                z= meta._z
                vz= meta._vz
            if isinstance(R,float):
                R= nu.array([R])
                vR= nu.array([vR])
                vT= nu.array([vT])
                z= nu.array([z])
                vz= nu.array([vz])
            Lz= R*vT
            if self._useu0:
                #First calculate u0
                if kwargs.has_key('u0'):
                    u0= nu.asarray(kwargs['u0'])
                else:
                    E= nu.array([evaluatePotentials(R[ii],z[ii],self._pot) +vR[ii]**2./2.+vz[ii]**2./2.+vT[ii]**2./2. for ii in range(len(R))])
                    u0= actionAngleStaeckel_c.actionAngleStaeckel_calcu0(E,Lz,
                                                                         self._pot,
                                                                         self._delta)[0]
                if kwargs.has_key('u0'): kwargs.pop('u0')
            else:
                u0= None
            jr, jz, err= actionAngleStaeckel_c.actionAngleStaeckel_c(\
                self._pot,self._delta,R,vR,vT,z,vz,u0=u0)
            if err == 0:
                return (jr,Lz,jz)
            else: #pragma: no cover
                raise RuntimeError("C-code for calculation actions failed; try with c=False")
        else:
            if kwargs.has_key('c') and kwargs['c'] and not self._c: #pragma: no cover
                warnings.warn("C module not used because potential does not have a C implementation",galpyWarning)
            if kwargs.has_key('c'): kwargs.pop('c')
            if (len(args) == 5 or len(args) == 6) \
                    and isinstance(args[0],nu.ndarray):
                ojr= nu.zeros((len(args[0])))
                olz= nu.zeros((len(args[0])))
                ojz= nu.zeros((len(args[0])))
                for ii in range(len(args[0])):
                    if len(args) == 5:
                        targs= (args[0][ii],args[1][ii],args[2][ii],
                                args[3][ii],args[4][ii])
                    elif len(args) == 6:
                        targs= (args[0][ii],args[1][ii],args[2][ii],
                                args[3][ii],args[4][ii],args[5][ii])
                    tjr,tlz,tjz= self(*targs,**copy.copy(kwargs))
                    ojr[ii]= tjr
                    ojz[ii]= tjz
                    olz[ii]= tlz
                return (ojr,olz,ojz)
            else:
                #Set up the actionAngleStaeckelSingle object
                aASingle= actionAngleStaeckelSingle(*args,pot=self._pot,
                                                     delta=self._delta)
                return (aASingle.JR(**copy.copy(kwargs)),
                        aASingle._R*aASingle._vT,
                        aASingle.Jz(**copy.copy(kwargs)))

    def actionsFreqs(self,*args,**kwargs):
        """
        NAME:
           actionsFreqs
        PURPOSE:
           evaluate the actions and frequencies (jr,lz,jz,Omegar,Omegaphi,Omegaz)
        INPUT:
           Either:
              a) R,vR,vT,z,vz
              b) Orbit instance: initial condition used if that's it, orbit(t)
                 if there is a time given as well
           scipy.integrate.quadrature keywords
        OUTPUT:
            (jr,lz,jz,Omegar,Omegaphi,Omegaz)
        HISTORY:
           2013-08-28 - Written - Bovy (IAS)
        """
        if ((self._c and not (kwargs.has_key('c') and not kwargs['c']))\
                or (ext_loaded and ((kwargs.has_key('c') and kwargs['c'])))) \
                and _check_c(self._pot):
            if len(args) == 5: #R,vR.vT, z, vz
                R,vR,vT, z, vz= args
            elif len(args) == 6: #R,vR.vT, z, vz, phi
                R,vR,vT, z, vz, phi= args
            else:
                meta= actionAngle(*args)
                R= meta._R
                vR= meta._vR
                vT= meta._vT
                z= meta._z
                vz= meta._vz
            if isinstance(R,float):
                R= nu.array([R])
                vR= nu.array([vR])
                vT= nu.array([vT])
                z= nu.array([z])
                vz= nu.array([vz])
            Lz= R*vT
            if self._useu0:
                #First calculate u0
                if kwargs.has_key('u0'):
                    u0= nu.asarray(kwargs['u0'])
                else:
                    E= nu.array([evaluatePotentials(R[ii],z[ii],self._pot) +vR[ii]**2./2.+vz[ii]**2./2.+vT[ii]**2./2. for ii in range(len(R))])
                    u0= actionAngleStaeckel_c.actionAngleStaeckel_calcu0(E,Lz,
                                                                         self._pot,
                                                                         self._delta)[0]
                if kwargs.has_key('u0'): kwargs.pop('u0')
            else:
                u0= None
            jr, jz, Omegar, Omegaphi, Omegaz, err= actionAngleStaeckel_c.actionAngleFreqStaeckel_c(\
                self._pot,self._delta,R,vR,vT,z,vz,u0=u0)
            # Adjustements for close-to-circular orbits
            indx= nu.isnan(Omegar)*(jr < 10.**-3.)+nu.isnan(Omegaz)*(jz < 10.**-3.) #Close-to-circular and close-to-the-plane orbits
            if nu.sum(indx) > 0:
                Omegar[indx]= [epifreq(self._pot,r) for r in R[indx]]
                Omegaphi[indx]= [omegac(self._pot,r) for r in R[indx]]
                Omegaz[indx]= [verticalfreq(self._pot,r) for r in R[indx]]
            if err == 0:
                return (jr,Lz,jz,Omegar,Omegaphi,Omegaz)
            else: #pragma: no cover
                raise RuntimeError("C-code for calculation actions failed; try with c=False")
        else:
            if kwargs.has_key('c') and kwargs['c'] and not self._c: #pragma: no cover
                warnings.warn("C module not used because potential does not have a C implementation",galpyWarning)
            raise NotImplementedError("actionsFreqs with c=False not implemented")

    def actionsFreqsAngles(self,*args,**kwargs):
        """
        NAME:
           actionsFreqsAngles
        PURPOSE:
           evaluate the actions, frequencies, and angles 
           (jr,lz,jz,Omegar,Omegaphi,Omegaz,angler,anglephi,anglez)
        INPUT:
           Either:
              a) R,vR,vT,z,vz,phi (MUST HAVE PHI)
              b) Orbit instance: initial condition used if that's it, orbit(t)
                 if there is a time given as well
           scipy.integrate.quadrature keywords
        OUTPUT:
            (jr,lz,jz,Omegar,Omegaphi,Omegaz,angler,anglephi,anglez)
        HISTORY:
           2013-08-28 - Written - Bovy (IAS)
        """
        if ((self._c and not (kwargs.has_key('c') and not kwargs['c']))\
                or (ext_loaded and ((kwargs.has_key('c') and kwargs['c'])))) \
                and _check_c(self._pot):
            if len(args) == 5: #R,vR.vT, z, vz pragma: no cover
                raise IOError("Must specify phi")
            elif len(args) == 6: #R,vR.vT, z, vz, phi
                R,vR,vT, z, vz, phi= args
            else:
                meta= actionAngle(*args)
                R= meta._R
                vR= meta._vR
                vT= meta._vT
                z= meta._z
                vz= meta._vz
                phi= meta._phi
            if isinstance(R,float):
                R= nu.array([R])
                vR= nu.array([vR])
                vT= nu.array([vT])
                z= nu.array([z])
                vz= nu.array([vz])
                phi= nu.array([phi])
            Lz= R*vT
            if self._useu0:
                #First calculate u0
                if kwargs.has_key('u0'):
                    u0= nu.asarray(kwargs['u0'])
                else:
                    E= nu.array([evaluatePotentials(R[ii],z[ii],self._pot) +vR[ii]**2./2.+vz[ii]**2./2.+vT[ii]**2./2. for ii in range(len(R))])
                    u0= actionAngleStaeckel_c.actionAngleStaeckel_calcu0(E,Lz,
                                                                         self._pot,
                                                                         self._delta)[0]
                if kwargs.has_key('u0'): kwargs.pop('u0')
            else:
                u0= None
            jr, jz, Omegar, Omegaphi, Omegaz, angler, anglephi,anglez, err= actionAngleStaeckel_c.actionAngleFreqAngleStaeckel_c(\
                self._pot,self._delta,R,vR,vT,z,vz,phi,u0=u0)
            # Adjustements for close-to-circular orbits
            indx= nu.isnan(Omegar)*(jr < 10.**-3.)+nu.isnan(Omegaz)*(jz < 10.**-3.) #Close-to-circular and close-to-the-plane orbits
            if nu.sum(indx) > 0:
                Omegar[indx]= [epifreq(self._pot,r) for r in R[indx]]
                Omegaphi[indx]= [omegac(self._pot,r) for r in R[indx]]
                Omegaz[indx]= [verticalfreq(self._pot,r) for r in R[indx]]
            if err == 0:
                return (jr,Lz,jz,Omegar,Omegaphi,Omegaz,angler,anglephi,anglez)
            else:
                raise RuntimeError("C-code for calculation actions failed; try with c=False") #pragma: no cover
        else: #pragma: no cover
            if kwargs.has_key('c') and kwargs['c'] and not self._c: #pragma: no cover
                warnings.warn("C module not used because potential does not have a C implementation",galpyWarning)
            raise NotImplementedError("actionsFreqs with c=False not implemented")

class actionAngleStaeckelSingle(actionAngle):
    """Action-angle formalism for axisymmetric potentials using Binney (2012)'s Staeckel approximation"""
    def __init__(self,*args,**kwargs):
        """
        NAME:
           __init__
        PURPOSE:
           initialize an actionAngleStaeckelSingle object
        INPUT:
           Either:
              a) R,vR,vT,z,vz
              b) Orbit instance: initial condition used if that's it, orbit(t)
                 if there is a time given as well
              pot= potential or list of potentials
        OUTPUT:
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        actionAngle.__init__(self,*args,**kwargs)
        if not kwargs.has_key('pot'): #pragma: no cover
            raise IOError("Must specify pot= for actionAngleStaeckelSingle")
        self._pot= kwargs['pot']
        if not kwargs.has_key('delta'): #pragma: no cover
            raise IOError("Must specify delta= for actionAngleStaeckel")
        self._delta= kwargs['delta']
        #Pre-calculate everything
        self._ux, self._vx= bovy_coords.Rz_to_uv(self._R,self._z,
                                                 delta=self._delta)
        self._sinvx= nu.sin(self._vx)
        self._cosvx= nu.cos(self._vx)
        self._coshux= nu.cosh(self._ux)
        self._sinhux= nu.sinh(self._ux)
        self._pux= self._delta*(self._vR*self._coshux*self._sinvx
                                +self._vz*self._sinhux*self._cosvx)
        self._pvx= self._delta*(self._vR*self._sinhux*self._cosvx
                                -self._vz*self._coshux*self._sinvx)
        EL= self.calcEL()
        self._E= EL[0]
        self._Lz= EL[1]
        #Determine umin and umax
        self._u0= self._ux #u0 as defined by Binney does not matter for a 
        #single action evaluation, so we don't determine it here
        self._sinhu0= nu.sinh(self._u0)
        self._potu0v0= potentialStaeckel(self._u0,self._vx,
                                         self._pot,self._delta)
        self._I3U= self._E*self._sinhux**2.-self._pux**2./2./self._delta**2.\
            -self._Lz**2./2./self._delta**2./self._sinhux**2.
        self._potupi2= potentialStaeckel(self._ux,nu.pi/2.,
                                         self._pot,self._delta)
        dV= (self._coshux**2.*self._potupi2
             -(self._sinhux**2.+self._sinvx**2.)
             *potentialStaeckel(self._ux,self._vx,
                                self._pot,self._delta))
        self._I3V= -self._E*self._sinvx**2.+self._pvx**2./2./self._delta**2.\
            +self._Lz**2./2./self._delta**2./self._sinvx**2.\
            -dV
        self.calcUminUmax()
        self.calcVmin()
        return None
    
    def angleR(self,**kwargs):
        """
        NAME:
           AngleR
        PURPOSE:
           Calculate the radial angle
        INPUT:
           scipy.integrate.quadrature keywords
        OUTPUT:
           w_R(R,vT,vT) in radians + 
           estimate of the error (does not include TR error)
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        raise NotImplementedError("'angleR' not yet implemented for Staeckel approximation")

    def TR(self,**kwargs):
        """
        NAME:
           TR
        PURPOSE:
           Calculate the radial period for a power-law rotation curve
        INPUT:
           scipy.integrate.quadrature keywords
        OUTPUT:
           T_R(R,vT,vT)*vc/ro + estimate of the error
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        raise NotImplementedError("'TR' not implemented yet for Staeckel approximation")

    def Tphi(self,**kwargs):
        """
        NAME:
           Tphi
        PURPOSE:
           Calculate the azimuthal period
        INPUT:
           +scipy.integrate.quadrature keywords
        OUTPUT:
           T_phi(R,vT,vT)/ro/vc + estimate of the error
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        raise NotImplementedError("'Tphi' not implemented yet for Staeckel approxximation")

    def I(self,**kwargs):
        """
        NAME:
           I
        PURPOSE:
           Calculate I, the 'ratio' between the radial and azimutha period
        INPUT:
           +scipy.integrate.quadrature keywords
        OUTPUT:
           I(R,vT,vT) + estimate of the error
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        raise NotImplementedError("'I' not implemented yet for Staeckel approxximation")

    def Jphi(self): #pragma: no cover
        """
        NAME:
           Jphi
        PURPOSE:
           Calculate the azimuthal action
        INPUT:
        OUTPUT:
           J_R(R,vT,vT)/ro/vc
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        return self._R*self._vT

    def JR(self,**kwargs):
        """
        NAME:
           JR
        PURPOSE:
           Calculate the radial action
        INPUT:
           fixed_quad= (False) if True, use n=10 fixed_quad
           +scipy.integrate.quad keywords
        OUTPUT:
           J_R(R,vT,vT)/ro/vc + estimate of the error (nan for fixed_quad)
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        if hasattr(self,'_JR'): #pragma: no cover
            return self._JR
        umin, umax= self.calcUminUmax()
        #print self._ux, self._pux, (umax-umin)/umax
        if (umax-umin)/umax < 10.**-6: return nu.array([0.])
        if kwargs.has_key('fixed_quad') and kwargs['fixed_quad']:
            kwargs.pop('fixed_quad')
            # factor in next line bc integrand=/2delta^2
            self._JR= 1./nu.pi*nu.sqrt(2.)*self._delta\
                *integrate.fixed_quad(_JRStaeckelIntegrand,
                                      umin,umax,
                                      args=(self._E,self._Lz,self._I3U,
                                            self._delta,
                                            self._u0,self._sinhu0**2.,
                                            self._vx,self._sinvx**2.,
                                            self._potu0v0,self._pot),
                                      n=10,
                                      **kwargs)[0]
        else:
            if kwargs.has_key('fixed_quad'): kwargs.pop('fixed_quad')
            self._JR= 1./nu.pi*nu.sqrt(2.)*self._delta\
                *integrate.quad(_JRStaeckelIntegrand,
                                umin,umax,
                                args=(self._E,self._Lz,self._I3U,
                                      self._delta,
                                      self._u0,self._sinhu0**2.,
                                      self._vx,self._sinvx**2.,
                                      self._potu0v0,self._pot),
                                **kwargs)[0]
        return self._JR

    def Jz(self,**kwargs):
        """
        NAME:
           Jz
        PURPOSE:
           Calculate the vertical action
        INPUT:
           fixed_quad= (False) if True, use n=10 fixed_quad
           +scipy.integrate.quad keywords
        OUTPUT:
           J_z(R,vT,vT)/ro/vc + estimate of the error
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        if hasattr(self,'_JZ'): #pragma: no cover
            return self._JZ
        vmin= self.calcVmin()
        if (nu.pi/2.-vmin) < 10.**-7: return nu.array([0.])
        if kwargs.has_key('fixed_quad') and kwargs['fixed_quad']:
            kwargs.pop('fixed_quad')
            # factor in next line bc integrand=/2delta^2
            self._JZ= 2./nu.pi*nu.sqrt(2.)*self._delta \
                *integrate.fixed_quad(_JzStaeckelIntegrand,
                                      vmin,nu.pi/2,
                                      args=(self._E,self._Lz,self._I3V,
                                            self._delta,
                                            self._ux,self._coshux**2.,
                                            self._sinhux**2.,
                                            self._potupi2,self._pot),
                                      n=10,
                                      **kwargs)[0]
        else:
            if kwargs.has_key('fixed_quad'): kwargs.pop('fixed_quad')
            # factor in next line bc integrand=/2delta^2
            self._JZ= 2./nu.pi*nu.sqrt(2.)*self._delta \
                *integrate.quad(_JzStaeckelIntegrand,
                                vmin,nu.pi/2,
                                args=(self._E,self._Lz,self._I3V,
                                      self._delta,
                                      self._ux,self._coshux**2.,
                                      self._sinhux**2.,
                                      self._potupi2,self._pot),
                                **kwargs)[0]
        return self._JZ

    def calcEL(self,**kwargs):
        """
        NAME:
           calcEL
        PURPOSE:
           calculate the energy and angular momentum
        INPUT:
           scipy.integrate.quadrature keywords
        OUTPUT:
           (E,L)
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """                           
        E,L= calcELStaeckel(self._R,self._vR,self._vT,self._z,self._vz,
                            self._pot)
        return (E,L)

    def calcUminUmax(self,**kwargs):
        """
        NAME:
           calcUminUmax
        PURPOSE:
           calculate the u 'apocenter' and 'pericenter'
        INPUT:
        OUTPUT:
           (umin,umax)
        HISTORY:
           2012-11-27 - Written - Bovy (IAS)
        """
        if hasattr(self,'_uminumax'): #pragma: no cover
            return self._uminumax
        E, L= self._E, self._Lz
        if nu.fabs(self._pux) < 10.**-7.: #We are at umin or umax
            eps= 10.**-8.
            peps= _JRStaeckelIntegrandSquared(self._ux+eps,
                                           E,L,self._I3U,self._delta,
                                           self._u0,self._sinhu0**2.,
                                           self._vx,self._sinvx**2.,
                                           self._potu0v0,self._pot)
            meps= _JRStaeckelIntegrandSquared(self._ux-eps,
                                              E,L,self._I3U,self._delta,
                                              self._u0,self._sinhu0**2.,
                                              self._vx,self._sinvx**2.,
                                              self._potu0v0,self._pot)
            if peps < 0. and meps > 0.: #we are at umax
                umax= self._ux
                rstart,prevr= _uminUmaxFindStart(self._ux,
                                               E,L,self._I3U,self._delta,
                                               self._u0,self._sinhu0**2.,
                                               self._vx,self._sinvx**2.,
                                               self._potu0v0,self._pot)
                if rstart == 0.: umin= 0.
                else: 
                    try:
                        umin= optimize.brentq(_JRStaeckelIntegrandSquared,
                                              rstart,self._ux-eps,
                                              (E,L,self._I3U,self._delta,
                                               self._u0,self._sinhu0**2.,
                                               self._vx,self._sinvx**2.,
                                               self._potu0v0,self._pot),
                                              maxiter=200)
                    except RuntimeError: #pragma: no cover
                        raise UnboundError("Orbit seems to be unbound")
            elif peps > 0. and meps < 0.: #we are at umin
                umin= self._ux
                rend,prevr= _uminUmaxFindStart(self._ux,
                                               E,L,self._I3U,self._delta,
                                               self._u0,self._sinhu0**2.,
                                               self._vx,self._sinvx**2.,
                                               self._potu0v0,self._pot,
                                               umax=True)
                umax= optimize.brentq(_JRStaeckelIntegrandSquared,
                                      self._ux+eps,rend,
                                      (E,L,self._I3U,self._delta,
                                       self._u0,self._sinhu0**2.,
                                       self._vx,self._sinvx**2.,
                                       self._potu0v0,self._pot),
                                      maxiter=200)
            else: #circular orbit
                umin= self._ux
                umax= self._ux
        else:
            rstart,prevr= _uminUmaxFindStart(self._ux,
                                             E,L,self._I3U,self._delta,
                                             self._u0,self._sinhu0**2.,
                                             self._vx,self._sinvx**2.,
                                             self._potu0v0,self._pot)
            if rstart == 0.: umin= 0.
            else: 
                if nu.fabs(prevr-self._ux) < 10.**-2.: rup= self._ux
                else: rup= prevr
                try:
                    umin= optimize.brentq(_JRStaeckelIntegrandSquared,
                                          rstart,rup,
                                          (E,L,self._I3U,self._delta,
                                           self._u0,self._sinhu0**2.,
                                           self._vx,self._sinvx**2.,
                                           self._potu0v0,self._pot),
                                           maxiter=200)
                except RuntimeError: #pragma: no cover
                    raise UnboundError("Orbit seems to be unbound")
            rend,prevr= _uminUmaxFindStart(self._ux,
                                           E,L,self._I3U,self._delta,
                                           self._u0,self._sinhu0**2.,
                                           self._vx,self._sinvx**2.,
                                           self._potu0v0,self._pot,
                                           umax=True)
            umax= optimize.brentq(_JRStaeckelIntegrandSquared,
                                  prevr,rend,
                                  (E,L,self._I3U,self._delta,
                                   self._u0,self._sinhu0**2.,
                                   self._vx,self._sinvx**2.,
                                   self._potu0v0,self._pot),
                                  maxiter=200)
        self._uminumax= (umin,umax)
        return self._uminumax

    def calcVmin(self,**kwargs):
        """
        NAME:
           calcVmin
        PURPOSE:
           calculate the v 'pericenter'
        INPUT:
        OUTPUT:
           vmin
        HISTORY:
           2012-11-28 - Written - Bovy (IAS)
        """
        if hasattr(self,'_vmin'): #pragma: no cover
            return self._vmin
        E, L= self._E, self._Lz
        if nu.fabs(self._pvx) < 10.**-7.: #We are at vmin or vmax
            eps= 10.**-8.
            peps= _JzStaeckelIntegrandSquared(self._vx+eps,
                                              E,L,self._I3V,self._delta,
                                              self._ux,self._coshux**2.,
                                              self._sinhux**2.,
                                              self._potupi2,self._pot)
            meps= _JzStaeckelIntegrandSquared(self._vx-eps,
                                              E,L,self._I3V,self._delta,
                                              self._ux,self._coshux**2.,
                                              self._sinhux**2.,
                                              self._potupi2,self._pot)
            if peps < 0. and meps > 0.: #we are at vmax, which cannot happen
                rstart= _vminFindStart(self._vx,
                                       E,L,self._I3V,self._delta,
                                       self._ux,self._coshux**2.,
                                       self._sinhux**2.,
                                       self._potupi2,self._pot)
                if rstart == 0.: vmin= 0.
                else:
                    try:
                        vmin= optimize.brentq(_JzStaeckelIntegrandSquared,
                                              rstart,self._vx-eps,
                                              (E,L,self._I3V,self._delta,
                                               self._ux,self._coshux**2.,
                                               self._sinhux**2.,
                                               self._potupi2,self._pot),
                                              maxiter=200)
                    except RuntimeError: #pragma: no cover
                        raise UnboundError("Orbit seems to be unbound")
            elif peps > 0. and meps < 0.: #we are at vmin
                vmin= self._vx
            else: #planar orbit
                vmin= self._vx
        else:
            rstart= _vminFindStart(self._vx,
                                   E,L,self._I3V,self._delta,
                                   self._ux,self._coshux**2.,
                                   self._sinhux**2.,
                                   self._potupi2,self._pot)
            if rstart == 0.: vmin= 0.
            else:
                try:
                    vmin= optimize.brentq(_JzStaeckelIntegrandSquared,
                                          rstart,rstart/0.9,
                                          (E,L,self._I3V,self._delta,
                                           self._ux,self._coshux**2.,
                                           self._sinhux**2.,
                                           self._potupi2,self._pot),
                                          maxiter=200)
                except RuntimeError: #pragma: no cover
                    raise UnboundError("Orbit seems to be unbound")
        self._vmin= vmin
        return self._vmin

def calcELStaeckel(R,vR,vT,z,vz,pot,vc=1.,ro=1.):
    """
    NAME:
       calcELStaeckel
    PURPOSE:
       calculate the energy and angular momentum
    INPUT:
       R - Galactocentric radius (/ro)
       vR - radial part of the velocity (/vc)
       vT - azimuthal part of the velocity (/vc)
       vc - circular velocity
       ro - reference radius
    OUTPUT:
       (E,L)
    HISTORY:
       2012-11-30 - Written - Bovy (IAS)
    """                           
    return (evaluatePotentials(R,z,pot)+vR**2./2.+vT**2./2.+vz**2./2.,R*vT)

def potentialStaeckel(u,v,pot,delta):
    """
    NAME:
       potentialStaeckel
    PURPOSE:
       return the potential
    INPUT:
       u - confocal u
       v - confocal v
       pot - potential
       delta - focus
    OUTPUT:
       Phi(u,v)
    HISTORY:
       2012-11-29 - Written - Bovy (IAS)
    """
    R,z= bovy_coords.uv_to_Rz(u,v,delta=delta)
    return evaluatePotentials(R,z,pot)

def FRStaeckel(u,v,pot,delta): #pragma: no cover because unused
    """
    NAME:
       FRStaeckel
    PURPOSE:
       return the radial force
    INPUT:
       u - confocal u
       v - confocal v
       pot - potential
       delta - focus
    OUTPUT:
       FR(u,v)
    HISTORY:
       2012-11-30 - Written - Bovy (IAS)
    """
    R,z= bovy_coords.uv_to_Rz(u,v,delta=delta)
    return evaluateRforces(R,z,pot)

def FZStaeckel(u,v,pot,delta): #pragma: no cover because unused
    """
    NAME:
       FZStaeckel
    PURPOSE:
       return the vertical force
    INPUT:
       u - confocal u
       v - confocal v
       pot - potential
       delta - focus
    OUTPUT:
       FZ(u,v)
    HISTORY:
       2012-11-30 - Written - Bovy (IAS)
    """
    R,z= bovy_coords.uv_to_Rz(u,v,delta=delta)
    return evaluatezforces(R,z,pot)

def _JRStaeckelIntegrand(u,E,Lz,I3U,delta,u0,sinh2u0,v0,sin2v0,
                         potu0v0,pot):
    return nu.sqrt(_JRStaeckelIntegrandSquared(u,E,Lz,I3U,delta,u0,sinh2u0,
                                               v0,sin2v0,
                                               potu0v0,pot))

def _JRStaeckelIntegrandSquared(u,E,Lz,I3U,delta,u0,sinh2u0,v0,sin2v0,
                                potu0v0,pot):
    #potu0v0= potentialStaeckel(u0,v0,pot,delta)
    """The J_R integrand: p^2_u(u)/2/delta^2"""
    sinh2u= nu.sinh(u)**2.
    dU= (sinh2u+sin2v0)*potentialStaeckel(u,v0,
                                          pot,delta)\
        -(sinh2u0+sin2v0)*potu0v0
    return E*sinh2u-I3U-dU-Lz**2./2./delta**2./sinh2u

def _JzStaeckelIntegrand(v,E,Lz,I3V,delta,u0,cosh2u0,sinh2u0,
                         potu0pi2,pot):
    return nu.sqrt(_JzStaeckelIntegrandSquared(v,E,Lz,I3V,delta,u0,cosh2u0,
                                               sinh2u0,
                                               potu0pi2,pot))
def _JzStaeckelIntegrandSquared(v,E,Lz,I3V,delta,u0,cosh2u0,sinh2u0,
                                potu0pi2,pot):
    #potu0pi2= potentialStaeckel(u0,nu.pi/2.,pot,delta)
    """The J_z integrand: p_v(v)/2/delta^2"""
    sin2v= nu.sin(v)**2.
    dV= cosh2u0*potu0pi2\
        -(sinh2u0+sin2v)*potentialStaeckel(u0,v,pot,delta)
    return E*sin2v+I3V+dV-Lz**2./2./delta**2./sin2v

def _uminUmaxFindStart(u,
                       E,Lz,I3U,delta,u0,sinh2u0,v0,sin2v0,
                       potu0v0,pot,umax=False):
    """
    NAME:
       _uminUmaxFindStart
    PURPOSE:
       Find adequate start or end points to solve for umin and umax
    INPUT:
       same as JRStaeckelIntegrandSquared
    OUTPUT:
       rstart or rend
    HISTORY:
       2012-11-30 - Written - Bovy (IAS)
    """
    if umax:
        utry= u*1.1
    else:
        utry= u*0.9
    prevu= u
    while _JRStaeckelIntegrandSquared(utry,
                                      E,Lz,I3U,delta,u0,sinh2u0,v0,sin2v0,
                                      potu0v0,pot) >= 0. \
                                      and utry > 0.000000001:
        prevu= utry
        if umax:
            if utry > 100.:
                raise UnboundError("Orbit seems to be unbound")
            utry*= 1.1
        else:
            utry*= 0.9
    if utry < 0.000000001: return (0.,prevu)
    return (utry,prevu)

def _vminFindStart(v,E,Lz,I3V,delta,u0,cosh2u0,sinh2u0,
                                potu0pi2,pot):
    """
    NAME:
       _vminFindStart
    PURPOSE:
       Find adequate start point to solve for vmin
    INPUT:
       same as JzStaeckelIntegrandSquared
    OUTPUT:
       rstart
    HISTORY:
       2012-11-28 - Written - Bovy (IAS)
    """
    vtry= 0.9*v
    while _JzStaeckelIntegrandSquared(vtry,
                                      E,Lz,I3V,delta,u0,cosh2u0,sinh2u0,
                                      potu0pi2,pot) >= 0. \
                                      and vtry > 0.000000001:
        vtry*= 0.9
    if vtry < 0.000000001: return 0.   
    return vtry

def estimateDeltaStaeckel(R,z,pot=None):
    """
    NAME:
       estimateDeltaStaeckel
    PURPOSE:
       Estimate a good value for delta using eqn. (9) in Sanders (2012)
    INPUT:
       R,z = coordinates (if these are arrays, the median estimated delta is returned, i.e., if this is an orbit)
       pot= Potential instance or list thereof
    OUTPUT:
       delta
    HISTORY:
       2013-08-28 - Written - Bovy (IAS)
    """
    if pot is None: #pragma: no cover
        raise IOError("pot= needs to be set to a Potential instance or list thereof")
    if isinstance(R,nu.ndarray):
        delta2= nu.array([(z[ii]**2.-R[ii]**2. #eqn. (9) has a sign error
                           +(3.*R[ii]*evaluatezforces(R[ii],z[ii],pot)
                             -3.*z[ii]*evaluateRforces(R[ii],z[ii],pot)
                             +R[ii]*z[ii]*(evaluateR2derivs(R[ii],z[ii],pot)
                                           -evaluatez2derivs(R[ii],z[ii],pot)))/evaluateRzderivs(R[ii],z[ii],pot)) for ii in range(len(R))])
        indx= (delta2 < 0.)*(delta2 > -10.**-10.)
        delta2[indx]= 0.
        delta2= nu.median(delta2[True-nu.isnan(delta2)])
    else:
        delta2= (z**2.-R**2. #eqn. (9) has a sign error
                 +(3.*R*evaluatezforces(R,z,pot)
                   -3.*z*evaluateRforces(R,z,pot)
                   +R*z*(evaluateR2derivs(R,z,pot)
                         -evaluatez2derivs(R,z,pot)))/evaluateRzderivs(R,z,pot))
        if delta2 < 0. and delta2 > -10.**-10.: delta2= 0.
    return nu.sqrt(delta2)
