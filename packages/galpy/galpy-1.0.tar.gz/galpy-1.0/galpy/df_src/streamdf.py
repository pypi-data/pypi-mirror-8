#The DF of a tidal stream
import copy
import numpy
import multiprocessing
import scipy
from scipy import special, interpolate, integrate
if int(scipy.__version__.split('.')[1]) < 10: #pragma: no cover
    from scipy.maxentropy import logsumexp
else:
    from scipy.misc import logsumexp
from galpy.orbit import Orbit
from galpy.util import bovy_coords, fast_cholesky_invert, \
    bovy_conversion, multi, bovy_plot, stable_cho_factor, bovy_ars
import warnings
from galpy.util import galpyWarning
_INTERPDURINGSETUP= True
_USEINTERP= True
_USESIMPLE= True
_labelDict= {'x': r'$X$',
             'y': r'$Y$',
             'z': r'$Z$',
             'r': r'$R$',
             'phi': r'$\phi$',
             'vx':r'$V_X$',
             'vy':r'$V_Y$',
             'vz':r'$V_Z$',
             'vr':r'$V_R$',
             'vt':r'$V_T$',
             'll':r'$\mathrm{Galactic\ longitude\, (deg)}$',
             'bb':r'$\mathrm{Galactic\ latitude\, (deg)}$',
             'dist':r'$\mathrm{distance\, (kpc)}$',
             'pmll':r'$\mu_l\,(\mathrm{mas\,yr}^{-1})$',
             'pmbb':r'$\mu_b\,(\mathrm{mas\,yr}^{-1})$',
             'vlos':r'$V_{\mathrm{los}}\,(\mathrm{km\,s}^{-1})$'}
class streamdf:
    """The DF of a tidal stream"""
    def __init__(self,sigv,progenitor=None,pot=None,aA=None,
                 tdisrupt=None,sigMeanOffset=6.,leading=True,
                 sigangle=None,
                 deltaAngleTrack=None,nTrackChunks=None,nTrackIterations=None,
                 Vnorm=220.,Rnorm=8.,
                 R0=8.,Zsun=0.025,vsun=[-11.1,8.*30.24,7.25],
                 multi=None,interpTrack=_INTERPDURINGSETUP,
                 useInterp=_USEINTERP,nosetup=False):
        """
        NAME:

           __init__

        PURPOSE:

           Initialize a quasi-isothermal DF

        INPUT:

           sigv - radial velocity dispersion of the progenitor

           tdisrupt= (5 Gyr) time since start of disruption (natural units)

           leading= (True) if True, model the leading part of the stream
                           if False, model the trailing part

           progenitor= progenitor orbit as Orbit instance (will be re-integrated, so don't bother integrating the orbit before)

           pot= Potential instance or list thereof

           aA= actionAngle instance used to convert (x,v) to actions

           sigMeanOffset= (6.) offset between the mean of the frequencies
                          and the progenitor, in units of the largest 
                          eigenvalue of the frequency covariance matrix 
                          (along the largest eigenvector), should be positive;
                          to model the trailing part, set leading=False

           sigangle= (sigv/122/[1km/s]=1.8sigv in natural coordinates)
                     estimate of the angle spread of the debris initially

           deltaAngleTrack= (None) angle to estimate the stream track over (rad)

           nTrackChunks= (floor(deltaAngleTrack/0.15)+1) number of chunks to divide the progenitor track in

           nTrackIterations= Number of iterations to perform when establishing the track; each iteration starts from a previous approximation to the track in (x,v) and calculates a new track based on the deviation between the previous track and the desired track in action-angle coordinates; if not set, an appropriate value is determined based on the magnitude of the misalignment between stream and orbit, with larger numbers of iterations for larger misalignments

           interpTrack= (might change), interpolate the stream track while 
                        setting up the instance (can be done by hand by 
                        calling self._interpolate_stream_track() and 
                        self._interpolate_stream_track_aA())

           useInterp= (might change), use interpolation by default when 
                      calculating approximated frequencies and angles

           nosetup= (False) if True, don't setup the stream track and anything
                            else that is expensive

           multi= (None) if set, use multi-processing

           Coordinate transformation inputs:

              Vnorm= (220) circular velocity to normalize velocities with

              Rnorm= (8) Galactocentric radius to normalize positions with

              R0= (8) Galactocentric radius of the Sun (kpc)

              Zsun= (0.025) Sun's height above the plane (kpc)

              vsun= ([-11.1,241.92,7.25]) Sun's motion in cylindrical coordinates (vR positive away from center)

        OUTPUT:

           object

        HISTORY:

           2013-09-16 - Started - Bovy (IAS)

           2013-11-25 - Started over - Bovy (IAS)

        """
        self._sigv= sigv
        if tdisrupt is None:
            self._tdisrupt= 5./bovy_conversion.time_in_Gyr(Vnorm,Rnorm)
        else:
            self._tdisrupt= tdisrupt
        self._sigMeanOffset= sigMeanOffset
        if pot is None: #pragma: no cover
            raise IOError("pot= must be set")
        self._pot= pot
        self._aA= aA
        if not self._aA._pot == self._pot:
            raise IOError("Potential in aA does not appear to be the same as given potential pot")
        self._progenitor= progenitor() #call to get new Orbit
        # Make sure we do not use physical coordinates
        self._progenitor.turn_physical_off()
        if (multi is True):   #if set to boolean, enable cpu_count processes
            self._multi= multiprocessing.cpu_count()
        else:
            self._multi= multi
        #Progenitor orbit: Calculate actions, frequencies, and angles for the progenitor
        acfs= self._aA.actionsFreqsAngles(self._progenitor,maxn=3,
                                    _firstFlip=(not leading))
        self._progenitor_jr= acfs[0][0]
        self._progenitor_lz= acfs[1][0]
        self._progenitor_jz= acfs[2][0]
        self._progenitor_Omegar= acfs[3]
        self._progenitor_Omegaphi= acfs[4]
        self._progenitor_Omegaz= acfs[5]
        self._progenitor_Omega= numpy.array([acfs[3],acfs[4],acfs[5]]).reshape(3)
        self._progenitor_angler= acfs[6]
        self._progenitor_anglephi= acfs[7]
        self._progenitor_anglez= acfs[8]
        self._progenitor_angle= numpy.array([acfs[6],acfs[7],acfs[8]]).reshape(3)
        #Calculate dO/dJ Jacobian at the progenitor
        self._dOdJp= calcaAJac(self._progenitor._orb.vxvv,
                               self._aA,dxv=None,dOdJ=True,
                               _initacfs=acfs)
        self._dOdJpEig= numpy.linalg.eig(self._dOdJp)
        #From the progenitor orbit, determine the sigmas in J and angle
        self._sigjr= (self._progenitor.rap()-self._progenitor.rperi())/numpy.pi*self._sigv
        self._siglz= self._progenitor.rperi()*self._sigv
        self._sigjz= 2.*self._progenitor.zmax()/numpy.pi*self._sigv
        #Estimate the frequency covariance matrix from a diagonal J matrix x dOdJ
        self._sigjmatrix= numpy.diag([self._sigjr**2.,
                                      self._siglz**2.,
                                      self._sigjz**2.])
        self._sigomatrix= numpy.dot(self._dOdJp,
                                    numpy.dot(self._sigjmatrix,self._dOdJp.T))
        #Estimate angle spread as the ratio of the largest to the middle eigenvalue
        self._sigomatrixEig= numpy.linalg.eig(self._sigomatrix)
        self._sigomatrixEigsortIndx= numpy.argsort(self._sigomatrixEig[0])
        self._sortedSigOEig= sorted(self._sigomatrixEig[0])
        if sigangle is None:
            self._sigangle= self._sigv*1.8
        else:
            self._sigangle= sigangle
        self._sigangle2= self._sigangle**2.
        self._lnsigangle= numpy.log(self._sigangle)
        #Estimate the frequency mean as lying along the direction of the largest eigenvalue
        self._dsigomeanProgDirection= self._sigomatrixEig[1][:,numpy.argmax(self._sigomatrixEig[0])]
        self._progenitor_Omega_along_dOmega= \
            numpy.dot(self._progenitor_Omega,self._dsigomeanProgDirection)
        #Make sure we are modeling the correct part of the stream
        self._leading= leading
        self._sigMeanSign= 1.
        if self._leading and self._progenitor_Omega_along_dOmega < 0.:
            self._sigMeanSign= -1.
        elif not self._leading and self._progenitor_Omega_along_dOmega > 0.:
            self._sigMeanSign= -1.
        self._progenitor_Omega_along_dOmega*= self._sigMeanSign 
        self._sigomean= self._progenitor_Omega\
            +self._sigMeanOffset*self._sigMeanSign\
            *numpy.sqrt(numpy.amax(self._sigomatrixEig[0]))\
            *self._dsigomeanProgDirection
#numpy.dot(self._dOdJp,
#                          numpy.array([self._sigjr,self._siglz,self._sigjz]))
        self._dsigomeanProg= self._sigomean-self._progenitor_Omega
        self._meandO= self._sigMeanOffset\
            *numpy.sqrt(numpy.amax(self._sigomatrixEig[0]))
        #Store cholesky of sigomatrix for fast evaluation
        self._sigomatrixNorm=\
            numpy.sqrt(numpy.sum(self._sigomatrix**2.))
        self._sigomatrixinv, self._sigomatrixLogdet= \
            fast_cholesky_invert(self._sigomatrix/self._sigomatrixNorm,
                                 tiny=10.**-15.,logdet=True)
        self._sigomatrixinv/= self._sigomatrixNorm

        deltaAngleTrackLim = (self._sigMeanOffset+4.) * numpy.sqrt(
            self._sortedSigOEig[2]) * self._tdisrupt
        if (deltaAngleTrack is None):  
            deltaAngleTrack = deltaAngleTrackLim
        else:
            if (deltaAngleTrack > deltaAngleTrackLim):
                warnings.warn("WARNING: angle range large compared to plausible value.", galpyWarning)
        #Set the coordinate-transformation parameters; check that these do not conflict with those in the progenitor orbit object; need to use the original, since this objects _progenitor has physical turned off
        if progenitor._roSet \
                and (numpy.fabs(Rnorm-progenitor._orb._ro) > 10.**-.8 \
                         or numpy.fabs(R0-progenitor._orb._ro) > 10.**-8.):
            warnings.warn("Warning: progenitor's ro does not agree with streamdf's Rnorm and R0; this may have unexpected consequences when projecting into observables", galpyWarning)
        if progenitor._voSet \
                and numpy.fabs(Vnorm-progenitor._orb._vo) > 10.**-8.:
            warnings.warn("Warning: progenitor's vo does not agree with streamdf's Vnorm; this may have unexpected consequences when projecting into observables", galpyWarning)
        if (progenitor._roSet or progenitor._voSet) \
                and numpy.fabs(Zsun-progenitor._orb._zo) > 10.**-8.:
            warnings.warn("Warning: progenitor's zo does not agree with streamdf's Zsun; this may have unexpected consequences when projecting into observables", galpyWarning)
        if (progenitor._roSet or progenitor._voSet) \
                and numpy.any(numpy.fabs(vsun-numpy.array([0.,Vnorm,0.])\
                                    -progenitor._orb._solarmotion) > 10.**-8.):
            warnings.warn("Warning: progenitor's solarmotion does not agree with streamdf's vsun (after accounting for Vnorm); this may have unexpected consequences when projecting into observables", galpyWarning)
        self._Vnorm= Vnorm
        self._Rnorm= Rnorm
        self._R0= R0
        self._Zsun= Zsun
        self._vsun= vsun
        #Determine the stream track
        if not nosetup:
            self._determine_nTrackIterations(nTrackIterations)
            self._determine_stream_track(deltaAngleTrack,nTrackChunks)
            self._useInterp= useInterp
            if interpTrack or self._useInterp:
                self._interpolate_stream_track()
                self._interpolate_stream_track_aA()
            self.calc_stream_lb()
            self._determine_stream_spread()
        return None

    def misalignment(self,isotropic=False):
        """
        NAME:

           misalignment

        PURPOSE:

           calculate the misalignment between the progenitor's frequency
           and the direction along which the stream disrupts

        INPUT:

           isotropic= (False), if True, return the misalignment assuming an isotropic action distribution

        OUTPUT:

           misalignment in degree

        HISTORY:

           2013-12-05 - Written - Bovy (IAS)

        """
        if isotropic:
            dODir= self._dOdJpEig[1][:,numpy.argmax(numpy.fabs(self._dOdJpEig[0]))]
        else:
            dODir= self._dsigomeanProgDirection
        out= numpy.arccos(numpy.sum(self._progenitor_Omega*dODir)/numpy.sqrt(numpy.sum(self._progenitor_Omega**2.)))/numpy.pi*180.
        if out > 90.: return out-180.
        else: return out

    def freqEigvalRatio(self,isotropic=False):
        """
        NAME:

           freqEigvalRatio

        PURPOSE:

           calculate the ratio between the largest and 2nd-to-largest (in abs)
           eigenvalue of sqrt(dO/dJ^T V_J dO/dJ) 
           (if this is big, a 1D stream will form)

        INPUT:

           isotropic= (False), if True, return the ratio assuming an isotropic action distribution (i.e., just of dO/dJ)

        OUTPUT:

           ratio between eigenvalues of |dO / dJ|

        HISTORY:

           2013-12-05 - Written - Bovy (IAS)

        """
        if isotropic:
            sortedEig= sorted(numpy.fabs(self._dOdJpEig[0]))
            return sortedEig[2]/sortedEig[1]
        else:
            return numpy.sqrt(self._sortedSigOEig)[2]\
                /numpy.sqrt(self._sortedSigOEig)[1]

    def estimateTdisrupt(self,deltaAngle):
        """
        NAME:

           estimateTdisrupt

        PURPOSE:

           estimate the time of disruption

        INPUT:

           deltaAngle- spread in angle since disruption

        OUTPUT:

           time in natural units

        HISTORY:

           2013-11-27 - Written - Bovy (IAS)

        """
        return deltaAngle\
            /numpy.sqrt(numpy.sum(self._dsigomeanProg**2.))

############################STREAM TRACK FUNCTIONS#############################
    def plotTrack(self,d1='x',d2='z',interp=True,spread=0,simple=_USESIMPLE,
                  *args,**kwargs):
        """
        NAME:

           plotTrack

        PURPOSE:

           plot the stream track

        INPUT:

           d1= plot this on the X axis ('x','y','z','R','phi','vx','vy','vz','vR','vt','ll','bb','dist','pmll','pmbb','vlos')

           d2= plot this on the Y axis (same list as for d1)

           interp= (True) if True, use the interpolated stream track

           spread= (0) if int > 0, also plot the spread around the track as spread x sigma

           scaleToPhysical= (False), if True, plot positions in kpc and velocities in km/s

           simple= (False), if True, use a simple estimate for the spread in perpendicular angle

           bovy_plot.bovy_plot args and kwargs

        OUTPUT:

           plot to output device

        HISTORY:

           2013-12-09 - Written - Bovy (IAS)

        """
        if not hasattr(self,'_ObsTrackLB') and \
                (d1.lower() == 'll' or d1.lower() == 'bb' 
                 or d1.lower() == 'dist' or d1.lower() == 'pmll' 
                 or d1.lower() == 'pmbb' or d1.lower() == 'vlos'
                 or d2.lower() == 'll' or d2.lower() == 'bb' 
                 or d2.lower() == 'dist' or d2.lower() == 'pmll' 
                 or d2.lower() == 'pmbb' or d2.lower() == 'vlos'):
            self.calc_stream_lb()
        if kwargs.has_key('scaleToPhysical'):
            phys= kwargs['scaleToPhysical']
            kwargs.pop('scaleToPhysical')
        else:
            phys= False
        tx= self._parse_track_dim(d1,interp=interp,phys=phys)
        ty= self._parse_track_dim(d2,interp=interp,phys=phys)
        bovy_plot.bovy_plot(tx,ty,*args,
                            xlabel=_labelDict[d1.lower()],
                            ylabel=_labelDict[d2.lower()],
                            **kwargs)
        if spread:
            addx, addy= self._parse_track_spread(d1,d2,interp=interp,phys=phys,
                                                 simple=simple)
            if (kwargs.has_key('ls') and kwargs['ls'] == 'none') \
                    or (kwargs.has_key('linestyle') \
                            and kwargs['linestyle'] == 'none'):
                if kwargs.has_key('ls'): kwargs.pop('ls')
                if kwargs.has_key('linestyle'): kwargs.pop('linestyle')
                spreadls= 'none'
            else:
                spreadls= '-.'
            if kwargs.has_key('marker'):
                spreadmarker= kwargs['marker']
                kwargs.pop('marker')
            else:
                spreadmarker= None
            if kwargs.has_key('color'):
                spreadcolor= kwargs['color']
            else:
                spreadcolor= None
            if kwargs.has_key('lw'):
                spreadlw= kwargs['lw']
            else:
                spreadlw= 1.
            bovy_plot.bovy_plot(tx+spread*addx,ty+spread*addy,ls=spreadls,
                                marker=spreadmarker,color=spreadcolor,
                                lw=spreadlw,
                                overplot=True)
            bovy_plot.bovy_plot(tx-spread*addx,ty-spread*addy,ls=spreadls,
                                marker=spreadmarker,color=spreadcolor,
                                lw=spreadlw,
                                overplot=True)            
        return None

    def plotProgenitor(self,d1='x',d2='z',*args,**kwargs):
        """
        NAME:

           plotProgenitor

        PURPOSE:

           plot the progenitor orbit

        INPUT:

           d1= plot this on the X axis ('x','y','z','R','phi','vx','vy','vz','vR','vt','ll','bb','dist','pmll','pmbb','vlos')

           d2= plot this on the Y axis (same list as for d1)

           scaleToPhysical= (False), if True, plot positions in kpc and velocities in km/s

           bovy_plot.bovy_plot args and kwargs

        OUTPUT:

           plot to output device

        HISTORY:

           2013-12-09 - Written - Bovy (IAS)

        """
        tts= self._progenitor._orb.t[self._progenitor._orb.t \
                                          < self._trackts[self._nTrackChunks-1]]
        obs= [self._R0,0.,self._Zsun]
        obs.extend(self._vsun)
        if kwargs.has_key('scaleToPhysical'):
            phys= kwargs['scaleToPhysical']
            kwargs.pop('scaleToPhysical')
        else:
            phys= False
        tx= self._parse_progenitor_dim(d1,tts,ro=self._Rnorm,vo=self._Vnorm,
                                       obs=obs,phys=phys)
        ty= self._parse_progenitor_dim(d2,tts,ro=self._Rnorm,vo=self._Vnorm,
                                       obs=obs,phys=phys)
        bovy_plot.bovy_plot(tx,ty,*args,
                            xlabel=_labelDict[d1.lower()],
                            ylabel=_labelDict[d2.lower()],
                            **kwargs)
        return None

    def _parse_track_dim(self,d1,interp=True,phys=False):
        """Parse the dimension to plot the stream track for"""
        if interp: interpStr= 'interpolated'
        else: interpStr= ''
        if d1.lower() == 'x':
            tx= self.__dict__['_%sObsTrackXY' % interpStr][:,0]
        elif d1.lower() == 'y':
            tx= self.__dict__['_%sObsTrackXY' % interpStr][:,1]
        elif d1.lower() == 'z':
            tx= self.__dict__['_%sObsTrackXY' % interpStr][:,2]
        elif d1.lower() == 'r':
            tx= self.__dict__['_%sObsTrack' % interpStr][:,0]
        elif d1.lower() == 'phi':
            tx= self.__dict__['_%sObsTrack' % interpStr][:,5]
        elif d1.lower() == 'vx': 
            tx= self.__dict__['_%sObsTrackXY' % interpStr][:,3]
        elif d1.lower() == 'vy':
            tx= self.__dict__['_%sObsTrackXY' % interpStr][:,4]
        elif d1.lower() == 'vz':
            tx= self.__dict__['_%sObsTrackXY' % interpStr][:,5]
        elif d1.lower() == 'vr':
            tx= self.__dict__['_%sObsTrack' % interpStr][:,1]
        elif d1.lower() == 'vt':
            tx= self.__dict__['_%sObsTrack' % interpStr][:,2]
        elif d1.lower() == 'll':
            tx= self.__dict__['_%sObsTrackLB' % interpStr][:,0]
        elif d1.lower() == 'bb':
            tx= self.__dict__['_%sObsTrackLB' % interpStr][:,1]
        elif d1.lower() == 'dist':
            tx= self.__dict__['_%sObsTrackLB' % interpStr][:,2]
        elif d1.lower() == 'pmll':
            tx= self.__dict__['_%sObsTrackLB' % interpStr][:,4]
        elif d1.lower() == 'pmbb':
            tx= self.__dict__['_%sObsTrackLB' % interpStr][:,5]
        elif d1.lower() == 'vlos':
            tx= self.__dict__['_%sObsTrackLB' % interpStr][:,3]
        if phys and (d1.lower() == 'x' or d1.lower() == 'y' \
                         or d1.lower() == 'z' or d1.lower() == 'r'):
            tx= copy.copy(tx)
            tx*= self._Rnorm
        if phys and (d1.lower() == 'vx' or d1.lower() == 'vy' \
                         or d1.lower() == 'vz' or d1.lower() == 'vr' \
                         or d1.lower() == 'vt'):
            tx= copy.copy(tx)
            tx*= self._Vnorm
        return tx        

    def _parse_progenitor_dim(self,d1,ts,ro=None,vo=None,obs=None,
                              phys=False):
        """Parse the dimension to plot the progenitor orbit for"""
        if d1.lower() == 'x':
            tx= self._progenitor.x(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'y':
            tx= self._progenitor.y(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'z':
            tx= self._progenitor.z(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'r':
            tx= self._progenitor.R(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'phi':
            tx= self._progenitor.phi(ts,ro=ro,vo=vo,obs=obs)
        elif d1.lower() == 'vx': 
            tx= self._progenitor.vx(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'vy':
            tx= self._progenitor.vy(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'vz':
            tx= self._progenitor.vz(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'vr':
            tx= self._progenitor.vR(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'vt':
            tx= self._progenitor.vT(ts,ro=ro,vo=vo,obs=obs,use_physical=False)
        elif d1.lower() == 'll':
            tx= self._progenitor.ll(ts,ro=ro,vo=vo,obs=obs)
        elif d1.lower() == 'bb':
            tx= self._progenitor.bb(ts,ro=ro,vo=vo,obs=obs)
        elif d1.lower() == 'dist':
            tx= self._progenitor.dist(ts,ro=ro,vo=vo,obs=obs)
        elif d1.lower() == 'pmll':
            tx= self._progenitor.pmll(ts,ro=ro,vo=vo,obs=obs)
        elif d1.lower() == 'pmbb':
            tx= self._progenitor.pmbb(ts,ro=ro,vo=vo,obs=obs)
        elif d1.lower() == 'vlos':
            tx= self._progenitor.vlos(ts,ro=ro,vo=vo,obs=obs)
        if phys and (d1.lower() == 'x' or d1.lower() == 'y' \
                         or d1.lower() == 'z' or d1.lower() == 'r'):
            tx= copy.copy(tx)
            tx*= self._Rnorm
        if phys and (d1.lower() == 'vx' or d1.lower() == 'vy' \
                         or d1.lower() == 'vz' or d1.lower() == 'vr' \
                         or d1.lower() == 'vt'):
            tx= copy.copy(tx)
            tx*= self._Vnorm
        return tx        

    def _parse_track_spread(self,d1,d2,interp=True,phys=False,
                            simple=_USESIMPLE):
        """Determine the spread around the track"""
        if not hasattr(self,'_allErrCovs'):
            self._determine_stream_spread(simple=simple)
        okaySpreadR= ['r','vr','vt','z','vz','phi']
        okaySpreadXY= ['x','y','z','vx','vy','vz']
        okaySpreadLB= ['ll','bb','dist','vlos','pmll','pmbb']
        #Determine which coordinate system we're in
        coord= [False,False,False] #R, XY, LB
        if d1.lower() in okaySpreadR and d2.lower() in okaySpreadR:
            coord[0]= True
        elif d1.lower() in okaySpreadXY and d2.lower() in okaySpreadXY:
            coord[1]= True
        elif d1.lower() in okaySpreadLB and d2.lower() in okaySpreadLB:
            coord[2]= True
        else:
            raise NotImplementedError("plotting the spread for coordinates from different systems not implemented yet ...")
        #Get the right 2D Jacobian
        indxDict= {}
        indxDict['r']= 0
        indxDict['vr']= 1
        indxDict['vt']= 2
        indxDict['z']= 3
        indxDict['vz']= 4
        indxDict['phi']= 5
        indxDictXY= {}
        indxDictXY['x']= 0
        indxDictXY['y']= 1
        indxDictXY['z']= 2
        indxDictXY['vx']= 3
        indxDictXY['vy']= 4
        indxDictXY['vz']= 5
        indxDictLB= {}
        indxDictLB['ll']= 0
        indxDictLB['bb']= 1
        indxDictLB['dist']= 2
        indxDictLB['vlos']= 3
        indxDictLB['pmll']= 4
        indxDictLB['pmbb']= 5
        if coord[0]:
            relevantCov= self._allErrCovs
            relevantDict= indxDict
            if phys:#apply scale factors
                tcov= copy.copy(relevantCov)
                scaleFac= numpy.array([self._Rnorm,self._Vnorm,self._Vnorm,
                                       self._Rnorm,self._Vnorm,1.])
                tcov*= numpy.tile(scaleFac,(6,1))
                tcov*= numpy.tile(scaleFac,(6,1)).T
                relevantCov= tcov
        elif coord[1]:
            relevantCov= self._allErrCovsXY
            relevantDict= indxDictXY
            if phys:#apply scale factors
                tcov= copy.copy(relevantCov)
                scaleFac= numpy.array([self._Rnorm,self._Rnorm,self._Rnorm,
                                       self._Vnorm,self._Vnorm,self._Vnorm])
                tcov*= numpy.tile(scaleFac,(6,1))
                tcov*= numpy.tile(scaleFac,(6,1)).T
                relevantCov= tcov
        elif coord[2]:
            relevantCov= self._allErrCovsLBUnscaled
            relevantDict= indxDictLB
        indx0= numpy.array([[relevantDict[d1.lower()],relevantDict[d1.lower()]],
                            [relevantDict[d2.lower()],relevantDict[d2.lower()]]])
        indx1= numpy.array([[relevantDict[d1.lower()],relevantDict[d2.lower()]],
                            [relevantDict[d1.lower()],relevantDict[d2.lower()]]])
        cov= relevantCov[:,indx0,indx1] #cov contains all nTrackChunks covs
        if not interp:
            out= numpy.empty((self._nTrackChunks,2))
            eigDir= numpy.array([1.,0.])
            for ii in range(self._nTrackChunks):
                covEig= numpy.linalg.eig(cov[ii])
                minIndx= numpy.argmin(covEig[0])
                minEigvec= covEig[1][:,minIndx] #this is the direction of the transverse spread
                if numpy.sum(minEigvec*eigDir) < 0.: minEigvec*= -1. #Keep them pointing in the same direction
                out[ii]= minEigvec*numpy.sqrt(covEig[0][minIndx])
                eigDir= minEigvec
        else:
            #We slerp the minor eigenvector and interpolate the eigenvalue
            #First store all of the eigenvectors on the track
            allEigval= numpy.empty(self._nTrackChunks)
            allEigvec= numpy.empty((self._nTrackChunks,2))
            eigDir= numpy.array([1.,0.])
            for ii in range(self._nTrackChunks):
                covEig= numpy.linalg.eig(cov[ii])
                minIndx= numpy.argmin(covEig[0])
                minEigvec= covEig[1][:,minIndx] #this is the direction of the transverse spread
                if numpy.sum(minEigvec*eigDir) < 0.: minEigvec*= -1. #Keep them pointing in the same direction
                allEigval[ii]= numpy.sqrt(covEig[0][minIndx])
                allEigvec[ii]= minEigvec
                eigDir= minEigvec
            #Now interpolate where needed
            interpEigval=\
                interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                         allEigval,k=3)
            interpolatedEigval= interpEigval(self._interpolatedThetasTrack)
            #Interpolate in chunks
            interpolatedEigvec= numpy.empty((len(self._interpolatedThetasTrack),
                                             2))
            for ii in range(self._nTrackChunks-1):
                slerpOmega= numpy.arccos(numpy.sum(allEigvec[ii]*allEigvec[ii+1]))
                slerpts= (self._interpolatedThetasTrack-self._thetasTrack[ii])/\
                    (self._thetasTrack[ii+1]-self._thetasTrack[ii])
                slerpIndx= (slerpts >= 0.)*(slerpts <= 1.)
                for jj in range(2):
                    interpolatedEigvec[slerpIndx,jj]=\
                        (numpy.sin((1-slerpts[slerpIndx])*slerpOmega)*allEigvec[ii,jj]
                         +numpy.sin(slerpts[slerpIndx]*slerpOmega)*allEigvec[ii+1,jj])/numpy.sin(slerpOmega)
            out= numpy.tile(interpolatedEigval.T,(2,1)).T*interpolatedEigvec
        if coord[2]: #if LB, undo rescalings that were applied before
            out[:,0]*= self._ErrCovsLBScale[relevantDict[d1.lower()]]
            out[:,1]*= self._ErrCovsLBScale[relevantDict[d2.lower()]]
        return (out[:,0],out[:,1])

    def plotCompareTrackAAModel(self,**kwargs):
        """
        NAME:

           plotCompareTrackAAModel

        PURPOSE:

           plot the comparison between the underlying model's dOmega_perp vs. dangle_r (line) and the track in (x,v)'s dOmega_perp vs. dangle_r (dots; explicitly calculating the track's action-angle coordinates)

        INPUT:

           bovy_plot.bovy_plot kwargs

        OUTPUT:

           plot

        HISTORY:

           2014-08-27 - Written - Bovy (IAS)

        """
        #First calculate the model
        model_adiff= (self._ObsTrackAA[:,3:]-self._progenitor_angle)[:,0]\
            *self._sigMeanSign
        model_operp= numpy.dot(self._ObsTrackAA[:,:3]-self._progenitor_Omega,
                               self._dsigomeanProgDirection)\
                               *self._sigMeanSign
        #Then calculate the track's frequency-angle coordinates
        if self._multi is None:
            aatrack= numpy.empty((self._nTrackChunks,6))
            for ii in range(self._nTrackChunks):
                aatrack[ii]= self._aA.actionsFreqsAngles(Orbit(self._ObsTrack[ii,:]),
                                                         maxn=3)[3:]
        else:
            aatrack= numpy.reshape(\
                multi.parallel_map(
                    (lambda x: self._aA.actionsFreqsAngles(Orbit(self._ObsTrack[x,:]), maxn=3)[3:]),
                    range(self._nTrackChunks),
                    numcores=numpy.amin([self._nTrackChunks,
                                         multiprocessing.cpu_count(),
                                         self._multi])),(self._nTrackChunks,6))
        track_adiff= (aatrack[:,3:]-self._progenitor_angle)[:,0]\
            *self._sigMeanSign
        track_operp= numpy.dot(aatrack[:,:3]-self._progenitor_Omega,
                               self._dsigomeanProgDirection)\
                               *self._sigMeanSign
        overplot= kwargs.pop('overplot',False)
        yrange= kwargs.pop('yrange',
                           [0.,numpy.amax(numpy.hstack((model_operp,track_operp)))*1.1])
        xlabel= kwargs.pop('xlabel',r'$\Delta \theta_R$')
        ylabel= kwargs.pop('ylabel',r'$\Delta \Omega_\parallel$')
        bovy_plot.bovy_plot(model_adiff,model_operp,'k-',overplot=overplot,
                            xlabel=xlabel,ylabel=ylabel,yrange=yrange,**kwargs)
        bovy_plot.bovy_plot(track_adiff,track_operp,'ko',overplot=True,
                            **kwargs)
        return None

    def _determine_nTrackIterations(self,nTrackIterations):
        """Determine a good value for nTrackIterations based on the misalignment between stream and orbit; just based on some rough experience for now"""
        if not nTrackIterations is None:
            self.nTrackIterations= nTrackIterations
            return None
        if numpy.fabs(self.misalignment()) < 1.:
            self.nTrackIterations= 0
        elif numpy.fabs(self.misalignment()) >= 1. \
                and numpy.fabs(self.misalignment()) < 3.:
            self.nTrackIterations= 1
        elif numpy.fabs(self.misalignment()) >= 3.:
            self.nTrackIterations= 2
        return None

    def _determine_stream_track(self,deltaAngleTrack,nTrackChunks):
        """Determine the track of the stream in real space"""
        #Determine how much orbital time is necessary for the progenitor's orbit to cover the stream
        self._deltaAngleTrack= deltaAngleTrack
        if nTrackChunks is None:
            #default is floor(self._deltaAngleTrack/0.15)+1
            self._nTrackChunks= int(numpy.floor(self._deltaAngleTrack/0.15))+1
        else:
            self._nTrackChunks= nTrackChunks
        dt= self._deltaAngleTrack\
            /self._progenitor_Omega_along_dOmega
        self._trackts= numpy.linspace(0.,2*dt,2*self._nTrackChunks-1) #to be sure that we cover it
        #Instantiate an auxiliaryTrack, which is an Orbit instance at the mean frequency of the stream, and zero angle separation wrt the progenitor; prog_stream_offset is the offset between this track and the progenitor at zero angle
        prog_stream_offset=\
            _determine_stream_track_single(self._aA,
                                           self._progenitor,
                                           0., #time = 0
                                           self._progenitor_angle,
                                           self._sigMeanSign,
                                           self._dsigomeanProgDirection,
                                           self.meanOmega,
                                           0.) #angle = 0
        auxiliaryTrack= Orbit(prog_stream_offset[3])
        if dt < 0.:
            self._trackts= numpy.linspace(0.,-2.*dt,2.*self._nTrackChunks-1)
            #Flip velocities before integrating
            auxiliaryTrack= auxiliaryTrack.flip()
        auxiliaryTrack.integrate(self._trackts,self._pot)
        if dt < 0.:
            #Flip velocities again
            auxiliaryTrack._orb.orbit[:,1]= -auxiliaryTrack._orb.orbit[:,1]
            auxiliaryTrack._orb.orbit[:,2]= -auxiliaryTrack._orb.orbit[:,2]
            auxiliaryTrack._orb.orbit[:,4]= -auxiliaryTrack._orb.orbit[:,4]
        #Calculate the actions, frequencies, and angle for this auxiliary orbit
        acfs= self._aA.actionsFreqs(auxiliaryTrack(0.),maxn=3)
        auxiliary_Omega= numpy.array([acfs[3],acfs[4],acfs[5]]).reshape(3\
)
        auxiliary_Omega_along_dOmega= \
            numpy.dot(auxiliary_Omega,self._dsigomeanProgDirection)
        #Now calculate the actions, frequencies, and angles + Jacobian for each chunk
        allAcfsTrack= numpy.empty((self._nTrackChunks,9))
        alljacsTrack= numpy.empty((self._nTrackChunks,6,6))
        allinvjacsTrack= numpy.empty((self._nTrackChunks,6,6))
        thetasTrack= numpy.linspace(0.,self._deltaAngleTrack,
                                    self._nTrackChunks)
        ObsTrack= numpy.empty((self._nTrackChunks,6))
        ObsTrackAA= numpy.empty((self._nTrackChunks,6))
        detdOdJps= numpy.empty((self._nTrackChunks))
        if self._multi is None:
            for ii in range(self._nTrackChunks):
                multiOut= _determine_stream_track_single(self._aA,
                                                         auxiliaryTrack,
                                                         self._trackts[ii]*numpy.fabs(self._progenitor_Omega_along_dOmega/auxiliary_Omega_along_dOmega), #this factor accounts for the difference in frequency between the progenitor and the auxiliary track
                                                         self._progenitor_angle,
                                                         self._sigMeanSign,
                                                         self._dsigomeanProgDirection,
                                                         self.meanOmega,
                                                         thetasTrack[ii])
                allAcfsTrack[ii,:]= multiOut[0]
                alljacsTrack[ii,:,:]= multiOut[1]
                allinvjacsTrack[ii,:,:]= multiOut[2]
                ObsTrack[ii,:]= multiOut[3]
                ObsTrackAA[ii,:]= multiOut[4]
                detdOdJps[ii]= multiOut[5]
        else:
            multiOut= multi.parallel_map(\
                (lambda x: _determine_stream_track_single(self._aA,auxiliaryTrack,
                                                          self._trackts[x]*numpy.fabs(self._progenitor_Omega_along_dOmega/auxiliary_Omega_along_dOmega),
                                                          self._progenitor_angle,
                                                          self._sigMeanSign,
                                                          self._dsigomeanProgDirection,
                                                          self.meanOmega,
                                                          thetasTrack[x])),
                range(self._nTrackChunks),
                numcores=numpy.amin([self._nTrackChunks,
                                     multiprocessing.cpu_count(),
                                     self._multi]))
            for ii in range(self._nTrackChunks):
                allAcfsTrack[ii,:]= multiOut[ii][0]
                alljacsTrack[ii,:,:]= multiOut[ii][1]
                allinvjacsTrack[ii,:,:]= multiOut[ii][2]
                ObsTrack[ii,:]= multiOut[ii][3]
                ObsTrackAA[ii,:]= multiOut[ii][4]
                detdOdJps[ii]= multiOut[ii][5]
        #Repeat the track calculation using the previous track, to get closer to it
        for nn in range(self.nTrackIterations):
            if self._multi is None:
                for ii in range(self._nTrackChunks):
                    multiOut= _determine_stream_track_single(self._aA,
                                                             Orbit(ObsTrack[ii,:]),
                                                             0.,
                                                             self._progenitor_angle,
                                                             self._sigMeanSign,
                                                             self._dsigomeanProgDirection,
                                                             self.meanOmega,
                                                             thetasTrack[ii])
                    allAcfsTrack[ii,:]= multiOut[0]
                    alljacsTrack[ii,:,:]= multiOut[1]
                    allinvjacsTrack[ii,:,:]= multiOut[2]
                    ObsTrack[ii,:]= multiOut[3]
                    ObsTrackAA[ii,:]= multiOut[4]
                    detdOdJps[ii]= multiOut[5]
            else:
                multiOut= multi.parallel_map(\
                    (lambda x: _determine_stream_track_single(self._aA,Orbit(ObsTrack[x,:]),0.,
                                                              self._progenitor_angle,
                                                              self._sigMeanSign,
                                                              self._dsigomeanProgDirection,
                                                              self.meanOmega,
                                                              thetasTrack[x])),
                    range(self._nTrackChunks),
                    numcores=numpy.amin([self._nTrackChunks,
                                         multiprocessing.cpu_count(),
                                         self._multi]))
                for ii in range(self._nTrackChunks):
                    allAcfsTrack[ii,:]= multiOut[ii][0]
                    alljacsTrack[ii,:,:]= multiOut[ii][1]
                    allinvjacsTrack[ii,:,:]= multiOut[ii][2]
                    ObsTrack[ii,:]= multiOut[ii][3]
                    ObsTrackAA[ii,:]= multiOut[ii][4]
                    detdOdJps[ii]= multiOut[ii][5]           
        #Store the track
        self._thetasTrack= thetasTrack
        self._ObsTrack= ObsTrack
        self._ObsTrackAA= ObsTrackAA
        self._allAcfsTrack= allAcfsTrack
        self._alljacsTrack= alljacsTrack
        self._allinvjacsTrack= allinvjacsTrack
        self._detdOdJps= detdOdJps
        self._meandetdOdJp= numpy.mean(self._detdOdJps)
        self._logmeandetdOdJp= numpy.log(self._meandetdOdJp)
        #Also calculate _ObsTrackXY in XYZ,vXYZ coordinates
        self._ObsTrackXY= numpy.empty_like(self._ObsTrack)
        TrackX= self._ObsTrack[:,0]*numpy.cos(self._ObsTrack[:,5])
        TrackY= self._ObsTrack[:,0]*numpy.sin(self._ObsTrack[:,5])
        TrackZ= self._ObsTrack[:,3]
        TrackvX, TrackvY, TrackvZ=\
            bovy_coords.cyl_to_rect_vec(self._ObsTrack[:,1],
                                        self._ObsTrack[:,2],
                                        self._ObsTrack[:,4],
                                        self._ObsTrack[:,5])
        self._ObsTrackXY[:,0]= TrackX
        self._ObsTrackXY[:,1]= TrackY
        self._ObsTrackXY[:,2]= TrackZ
        self._ObsTrackXY[:,3]= TrackvX
        self._ObsTrackXY[:,4]= TrackvY
        self._ObsTrackXY[:,5]= TrackvZ
        return None

    def _determine_stream_spread(self,simple=_USESIMPLE):
        """Determine the spread around the stream track, just sets matrices that describe the covariances"""
        allErrCovs= numpy.empty((self._nTrackChunks,6,6))
        if self._multi is None:
            for ii in range(self._nTrackChunks):
                allErrCovs[ii]= _determine_stream_spread_single(self._sigomatrixEig,
                                                                self._thetasTrack[ii],
                                                                self.sigOmega,
                                                                lambda y: self.sigangledAngle(y,simple=simple),
                                                                self._allinvjacsTrack[ii])
        else:
            multiOut= multi.parallel_map(\
                (lambda x: _determine_stream_spread_single(self._sigomatrixEig,
                                                                self._thetasTrack[x],
                                                                self.sigOmega,
                                                                lambda y: self.sigangledAngle(y,simple=simple),
                                                                self._allinvjacsTrack[x])),

                range(self._nTrackChunks),
                numcores=numpy.amin([self._nTrackChunks,
                                     multiprocessing.cpu_count(),
                                     self._multi]))
            for ii in range(self._nTrackChunks):
                allErrCovs[ii]= multiOut[ii]
        self._allErrCovs= allErrCovs
        #Also propagate to XYZ coordinates
        allErrCovsXY= numpy.empty_like(self._allErrCovs)
        allErrCovsEigvalXY= numpy.empty((len(self._thetasTrack),6))
        allErrCovsEigvecXY= numpy.empty_like(self._allErrCovs)
        eigDir= numpy.array([numpy.array([1.,0.,0.,0.,0.,0.]) for ii in range(6)])
        for ii in range(self._nTrackChunks):
            tjac= bovy_coords.cyl_to_rect_jac(*self._ObsTrack[ii])
            allErrCovsXY[ii]=\
                numpy.dot(tjac,numpy.dot(self._allErrCovs[ii],tjac.T))
            #Eigen decomposition for interpolation
            teig= numpy.linalg.eig(allErrCovsXY[ii])
            #Sort them to match them up later
            sortIndx= numpy.argsort(teig[0])
            allErrCovsEigvalXY[ii]= teig[0][sortIndx]
            #Make sure the eigenvectors point in the same direction
            for jj in range(6):
                if numpy.sum(eigDir[jj]*teig[1][:,sortIndx[jj]]) < 0.:
                    teig[1][:,sortIndx[jj]]*= -1.
                eigDir[jj]= teig[1][:,sortIndx[jj]]
            allErrCovsEigvecXY[ii]= teig[1][:,sortIndx]
        self._allErrCovsXY= allErrCovsXY
        #Interpolate the allErrCovsXY covariance matrices along the interpolated track
        #Interpolate the eigenvalues
        interpAllErrCovsEigvalXY=\
            [interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                      allErrCovsEigvalXY[:,ii],
                                                      k=3) for ii in range(6)]
        #Now build the interpolated allErrCovsXY using slerp
        interpolatedAllErrCovsXY= numpy.empty((len(self._interpolatedThetasTrack),
                                               6,6))
        interpolatedEigval=\
            numpy.array([interpAllErrCovsEigvalXY[ii](self._interpolatedThetasTrack) for ii in range(6)]) #6,ninterp
        #Interpolate in chunks
        interpolatedEigvec= numpy.empty((len(self._interpolatedThetasTrack),
                                         6,6))
        for ii in range(self._nTrackChunks-1):
            slerpOmegas=\
                [numpy.arccos(numpy.sum(allErrCovsEigvecXY[ii,:,jj]*allErrCovsEigvecXY[ii+1,:,jj])) for jj in range(6)]
            slerpts= (self._interpolatedThetasTrack-self._thetasTrack[ii])/\
                (self._thetasTrack[ii+1]-self._thetasTrack[ii])
            slerpIndx= (slerpts >= 0.)*(slerpts <= 1.)
            for jj in range(6):
                for kk in range(6):
                    interpolatedEigvec[slerpIndx,kk,jj]=\
                    (numpy.sin((1-slerpts[slerpIndx])*slerpOmegas[jj])*allErrCovsEigvecXY[ii,kk,jj]
                     +numpy.sin(slerpts[slerpIndx]*slerpOmegas[jj])*allErrCovsEigvecXY[ii+1,kk,jj])/numpy.sin(slerpOmegas[jj])
        for ii in range(len(self._interpolatedThetasTrack)):
            interpolatedAllErrCovsXY[ii]=\
                numpy.dot(interpolatedEigvec[ii],
                          numpy.dot(numpy.diag(interpolatedEigval[:,ii]),
                                    interpolatedEigvec[ii].T))
        self._interpolatedAllErrCovsXY= interpolatedAllErrCovsXY
        #Also interpolate in l and b coordinates
        self._determine_stream_spreadLB(simple=simple)
        return None

    def _determine_stream_spreadLB(self,simple=_USESIMPLE,
                                   Rnorm=None,Vnorm=None,
                                   R0=None,Zsun=None,vsun=None):
        """Determine the spread in the stream in observable coordinates"""
        if not hasattr(self,'_allErrCovs'):
            self._determine_stream_spread(simple=simple)
        if Rnorm is None:
            Rnorm= self._Rnorm
        if Vnorm is None:
            Vnorm= self._Vnorm
        if R0 is None:
            R0= self._R0
        if Zsun is None:
            Zsun= self._Zsun
        if vsun is None:
            vsun= self._vsun
        allErrCovsLB= numpy.empty_like(self._allErrCovs)
        obs= [R0,0.,Zsun]
        obs.extend(vsun)
        obskwargs= {}
        obskwargs['ro']= Rnorm
        obskwargs['vo']= Vnorm
        obskwargs['obs']= obs
        self._ErrCovsLBScale= [180.,90.,
                               self._progenitor.dist(**obskwargs),
                               numpy.fabs(self._progenitor.vlos(**obskwargs)),
                               numpy.sqrt(self._progenitor.pmll(**obskwargs)**2.
                                          +self._progenitor.pmbb(**obskwargs)**2.),
                               numpy.sqrt(self._progenitor.pmll(**obskwargs)**2.
                                          +self._progenitor.pmbb(**obskwargs)**2.)]
        allErrCovsEigvalLB= numpy.empty((len(self._thetasTrack),6))
        allErrCovsEigvecLB= numpy.empty_like(self._allErrCovs)
        eigDir= numpy.array([numpy.array([1.,0.,0.,0.,0.,0.]) for ii in range(6)])
        for ii in range(self._nTrackChunks):
            tjacXY= bovy_coords.galcenrect_to_XYZ_jac(*self._ObsTrackXY[ii])
            tjacLB= bovy_coords.lbd_to_XYZ_jac(*self._ObsTrackLB[ii],
                                               degree=True)
            tjacLB[:3,:]/= Rnorm 
            tjacLB[3:,:]/= Vnorm 
            for jj in range(6):
                tjacLB[:,jj]*= self._ErrCovsLBScale[jj]
            tjac= numpy.dot(numpy.linalg.inv(tjacLB),tjacXY)
            allErrCovsLB[ii]=\
                numpy.dot(tjac,numpy.dot(self._allErrCovsXY[ii],tjac.T))
            #Eigen decomposition for interpolation
            teig= numpy.linalg.eig(allErrCovsLB[ii])
            #Sort them to match them up later
            sortIndx= numpy.argsort(teig[0])
            allErrCovsEigvalLB[ii]= teig[0][sortIndx]
            #Make sure the eigenvectors point in the same direction
            for jj in range(6):
                if numpy.sum(eigDir[jj]*teig[1][:,sortIndx[jj]]) < 0.:
                    teig[1][:,sortIndx[jj]]*= -1.
                eigDir[jj]= teig[1][:,sortIndx[jj]]
            allErrCovsEigvecLB[ii]= teig[1][:,sortIndx]
        self._allErrCovsLBUnscaled= allErrCovsLB
        #Interpolate the allErrCovsLB covariance matrices along the interpolated track
        #Interpolate the eigenvalues
        interpAllErrCovsEigvalLB=\
            [interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                      allErrCovsEigvalLB[:,ii],
                                                      k=3) for ii in range(6)]
        #Now build the interpolated allErrCovsXY using slerp
        interpolatedAllErrCovsLB= numpy.empty((len(self._interpolatedThetasTrack),
                                               6,6))
        interpolatedEigval=\
            numpy.array([interpAllErrCovsEigvalLB[ii](self._interpolatedThetasTrack) for ii in range(6)]) #6,ninterp
        #Interpolate in chunks
        interpolatedEigvec= numpy.empty((len(self._interpolatedThetasTrack),
                                         6,6))
        for ii in range(self._nTrackChunks-1):
            slerpOmegas=\
                [numpy.arccos(numpy.sum(allErrCovsEigvecLB[ii,:,jj]*allErrCovsEigvecLB[ii+1,:,jj])) for jj in range(6)]
            slerpts= (self._interpolatedThetasTrack-self._thetasTrack[ii])/\
                (self._thetasTrack[ii+1]-self._thetasTrack[ii])
            slerpIndx= (slerpts >= 0.)*(slerpts <= 1.)
            for jj in range(6):
                for kk in range(6):
                    interpolatedEigvec[slerpIndx,kk,jj]=\
                    (numpy.sin((1-slerpts[slerpIndx])*slerpOmegas[jj])*allErrCovsEigvecLB[ii,kk,jj]
                     +numpy.sin(slerpts[slerpIndx]*slerpOmegas[jj])*allErrCovsEigvecLB[ii+1,kk,jj])/numpy.sin(slerpOmegas[jj])
        for ii in range(len(self._interpolatedThetasTrack)):
            interpolatedAllErrCovsLB[ii]=\
                numpy.dot(interpolatedEigvec[ii],
                          numpy.dot(numpy.diag(interpolatedEigval[:,ii]),
                                    interpolatedEigvec[ii].T))
        self._interpolatedAllErrCovsLBUnscaled= interpolatedAllErrCovsLB
        #Also calculate the (l,b,..) -> (X,Y,..) Jacobian at all of the interpolated and not interpolated points
        trackLogDetJacLB= numpy.empty_like(self._thetasTrack)
        interpolatedTrackLogDetJacLB=\
            numpy.empty_like(self._interpolatedThetasTrack)
        for ii in range(self._nTrackChunks):
            tjacLB= bovy_coords.lbd_to_XYZ_jac(*self._ObsTrackLB[ii],
                                                degree=True)
            trackLogDetJacLB[ii]= numpy.log(numpy.linalg.det(tjacLB))
        self._trackLogDetJacLB= trackLogDetJacLB
        for ii in range(len(self._interpolatedThetasTrack)):
            tjacLB=\
                bovy_coords.lbd_to_XYZ_jac(*self._interpolatedObsTrackLB[ii],
                                            degree=True)
            interpolatedTrackLogDetJacLB[ii]=\
                numpy.log(numpy.linalg.det(tjacLB))
        self._interpolatedTrackLogDetJacLB= interpolatedTrackLogDetJacLB
        return None

    def _interpolate_stream_track(self):
        """Build interpolations of the stream track"""
        if hasattr(self,'_interpolatedThetasTrack'):
            return None #Already did this
        TrackX= self._ObsTrack[:,0]*numpy.cos(self._ObsTrack[:,5])
        TrackY= self._ObsTrack[:,0]*numpy.sin(self._ObsTrack[:,5])
        TrackZ= self._ObsTrack[:,3]
        TrackvX, TrackvY, TrackvZ=\
            bovy_coords.cyl_to_rect_vec(self._ObsTrack[:,1],
                                        self._ObsTrack[:,2],
                                        self._ObsTrack[:,4],
                                        self._ObsTrack[:,5])
        #Interpolate
        self._interpTrackX=\
            interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                     TrackX,k=3)
        self._interpTrackY=\
            interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                     TrackY,k=3)
        self._interpTrackZ=\
            interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                     TrackZ,k=3)
        self._interpTrackvX=\
            interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                     TrackvX,k=3)
        self._interpTrackvY=\
            interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                     TrackvY,k=3)
        self._interpTrackvZ=\
            interpolate.InterpolatedUnivariateSpline(self._thetasTrack,
                                                     TrackvZ,k=3)
        #Now store an interpolated version of the stream track
        self._interpolatedThetasTrack=\
            numpy.linspace(0.,self._deltaAngleTrack,1001)
        self._interpolatedObsTrackXY= numpy.empty((len(self._interpolatedThetasTrack),6))
        self._interpolatedObsTrackXY[:,0]=\
            self._interpTrackX(self._interpolatedThetasTrack)
        self._interpolatedObsTrackXY[:,1]=\
            self._interpTrackY(self._interpolatedThetasTrack)
        self._interpolatedObsTrackXY[:,2]=\
            self._interpTrackZ(self._interpolatedThetasTrack)
        self._interpolatedObsTrackXY[:,3]=\
            self._interpTrackvX(self._interpolatedThetasTrack)
        self._interpolatedObsTrackXY[:,4]=\
            self._interpTrackvY(self._interpolatedThetasTrack)
        self._interpolatedObsTrackXY[:,5]=\
            self._interpTrackvZ(self._interpolatedThetasTrack)
        #Also in cylindrical coordinates
        self._interpolatedObsTrack= \
            numpy.empty((len(self._interpolatedThetasTrack),6))
        tR,tphi,tZ= bovy_coords.rect_to_cyl(self._interpolatedObsTrackXY[:,0],
                                            self._interpolatedObsTrackXY[:,1],
                                            self._interpolatedObsTrackXY[:,2])
        tvR,tvT,tvZ=\
            bovy_coords.rect_to_cyl_vec(self._interpolatedObsTrackXY[:,3],
                                        self._interpolatedObsTrackXY[:,4],
                                        self._interpolatedObsTrackXY[:,5],
                                        tR,tphi,tZ,cyl=True)
        self._interpolatedObsTrack[:,0]= tR
        self._interpolatedObsTrack[:,1]= tvR
        self._interpolatedObsTrack[:,2]= tvT
        self._interpolatedObsTrack[:,3]= tZ
        self._interpolatedObsTrack[:,4]= tvZ
        self._interpolatedObsTrack[:,5]= tphi
        return None

    def _interpolate_stream_track_aA(self):
        """Build interpolations of the stream track in action-angle coordinates"""
        if hasattr(self,'_interpolatedObsTrackAA'):
            return None #Already did this
        #Calculate 1D meanOmega on a fine grid in angle and interpolate
        if not hasattr(self,'_interpolatedThetasTrack'):
            self._interpolate_stream_track()
        dmOs= numpy.array([self.meanOmega(da,oned=True) 
                          for da in self._interpolatedThetasTrack])
        self._interpTrackAAdmeanOmegaOneD=\
            interpolate.InterpolatedUnivariateSpline(\
            self._interpolatedThetasTrack,dmOs,k=3)
        #Build the interpolated AA
        self._interpolatedObsTrackAA=\
            numpy.empty((len(self._interpolatedThetasTrack),6))
        for ii in range(len(self._interpolatedThetasTrack)):
            self._interpolatedObsTrackAA[ii,:3]=\
                self._progenitor_Omega+dmOs[ii]*self._dsigomeanProgDirection\
                *self._sigMeanSign   
            self._interpolatedObsTrackAA[ii,3:]=\
                self._progenitor_angle+self._interpolatedThetasTrack[ii]\
                *self._dsigomeanProgDirection*self._sigMeanSign
            self._interpolatedObsTrackAA[ii,3:]=\
                numpy.mod(self._interpolatedObsTrackAA[ii,3:],2.*numpy.pi)
        return None

    def calc_stream_lb(self,
                       Vnorm=None,Rnorm=None,
                       R0=None,Zsun=None,vsun=None):
        """
        NAME:

           calc_stream_lb

        PURPOSE:

           convert the stream track to observational coordinates and store

        INPUT:

           Coordinate transformation inputs (all default to the instance-wide
           values):

              Vnorm= circular velocity to normalize velocities with

              Rnorm= Galactocentric radius to normalize positions with

              R0= Galactocentric radius of the Sun (kpc)

              Zsun= Sun's height above the plane (kpc)

              vsun= Sun's motion in cylindrical coordinates (vR positive away from center)

        OUTPUT:

           (none)

        HISTORY:

           2013-12-02 - Written - Bovy (IAS)

        """
        if Vnorm is None:
            Vnorm= self._Vnorm
        if Rnorm is None:
            Rnorm= self._Rnorm
        if R0 is None:
            R0= self._R0
        if Zsun is None:
            Zsun= self._Zsun
        if vsun is None:
            vsun= self._vsun
        self._ObsTrackLB= numpy.empty_like(self._ObsTrack)
        XYZ= bovy_coords.galcencyl_to_XYZ(self._ObsTrack[:,0]*Rnorm,
                                          self._ObsTrack[:,5],
                                          self._ObsTrack[:,3]*Rnorm,
                                          Xsun=R0,Zsun=Zsun)
        vXYZ= bovy_coords.galcencyl_to_vxvyvz(self._ObsTrack[:,1]*Vnorm,
                                              self._ObsTrack[:,2]*Vnorm,
                                              self._ObsTrack[:,4]*Vnorm,
                                              self._ObsTrack[:,5],
                                              vsun=vsun)
        slbd=bovy_coords.XYZ_to_lbd(XYZ[0],XYZ[1],XYZ[2],
                                    degree=True)
        svlbd= bovy_coords.vxvyvz_to_vrpmllpmbb(vXYZ[0],vXYZ[1],vXYZ[2],
                                                slbd[:,0],slbd[:,1],slbd[:,2],
                                                degree=True)
        self._ObsTrackLB[:,0]= slbd[:,0]
        self._ObsTrackLB[:,1]= slbd[:,1]
        self._ObsTrackLB[:,2]= slbd[:,2]
        self._ObsTrackLB[:,3]= svlbd[:,0]
        self._ObsTrackLB[:,4]= svlbd[:,1]
        self._ObsTrackLB[:,5]= svlbd[:,2]
        if hasattr(self,'_interpolatedObsTrackXY'):
            #Do the same for the interpolated track
            self._interpolatedObsTrackLB=\
                numpy.empty_like(self._interpolatedObsTrackXY)
            XYZ=\
                bovy_coords.galcenrect_to_XYZ(\
                self._interpolatedObsTrackXY[:,0]*Rnorm,
                self._interpolatedObsTrackXY[:,1]*Rnorm,
                self._interpolatedObsTrackXY[:,2]*Rnorm,
                Xsun=R0,Zsun=Zsun)
            vXYZ=\
                bovy_coords.galcenrect_to_vxvyvz(\
                self._interpolatedObsTrackXY[:,3]*Vnorm,
                self._interpolatedObsTrackXY[:,4]*Vnorm,
                self._interpolatedObsTrackXY[:,5]*Vnorm,
                vsun=vsun)
            slbd=bovy_coords.XYZ_to_lbd(XYZ[0],XYZ[1],XYZ[2],
                                        degree=True)
            svlbd= bovy_coords.vxvyvz_to_vrpmllpmbb(vXYZ[0],vXYZ[1],vXYZ[2],
                                                    slbd[:,0],slbd[:,1],
                                                    slbd[:,2],
                                                    degree=True)
            self._interpolatedObsTrackLB[:,0]= slbd[:,0]
            self._interpolatedObsTrackLB[:,1]= slbd[:,1]
            self._interpolatedObsTrackLB[:,2]= slbd[:,2]
            self._interpolatedObsTrackLB[:,3]= svlbd[:,0]
            self._interpolatedObsTrackLB[:,4]= svlbd[:,1]
            self._interpolatedObsTrackLB[:,5]= svlbd[:,2]
        if hasattr(self,'_allErrCovsLBUnscaled'):
            #Re-calculate this
            self._determine_stream_spreadLB(simple=_USESIMPLE,
                                            Vnorm=Vnorm,Rnorm=Rnorm,
                                            R0=R0,Zsun=Zsun,vsun=vsun)
        return None

    def _find_closest_trackpoint(self,R,vR,vT,z,vz,phi,interp=True,xy=False,
                                 usev=False):
        """For backward compatibility"""
        return self.find_closest_trackpoint(R,vR,vT,z,vz,phi,
                                            interp=interp,xy=xy,
                                            usev=usev)
    def find_closest_trackpoint(self,R,vR,vT,z,vz,phi,interp=True,xy=False,
                                 usev=False):
        """
        NAME:

           find_closest_trackpoint

        PURPOSE:

           find the closest point on the stream track to a given point

        INPUT:

           R,vR,vT,z,vz,phi - phase-space coordinates of the given point

           interp= (True), if True, return the index of the interpolated track

           xy= (False) if True, input is X,Y,Z,vX,vY,vZ in Galactocentric rectangular coordinates; if xy, some coordinates may be missing (given as None) and they will not be used

           usev= (False) if True, also use velocities to find the closest point

        OUTPUT:

           index into the track of the closest track point

        HISTORY:

           2013-12-04 - Written - Bovy (IAS)

        """
        if xy:
            X= R
            Y= vR
            Z= vT
        else:
            X= R*numpy.cos(phi)
            Y= R*numpy.sin(phi)
            Z= z
        if xy and usev:
            vX= z
            vY= vz
            vZ= phi
        elif usev:
            vX= vR*numpy.cos(phi)-vT*numpy.sin(phi)
            vY= vR*numpy.sin(phi)+vT*numpy.cos(phi)
            vZ= vz
        present= [not X is None,not Y is None,not Z is None]
        if usev: present.extend([not vX is None,not vY is None,not vZ is None])
        present= numpy.array(present,dtype='float')
        if X is None: X= 0.
        if Y is None: Y= 0.
        if Z is None: Z= 0.
        if usev and vX is None: vX= 0.
        if usev and vY is None: vY= 0.
        if usev and vZ is None: vZ= 0.
        if interp:
            dist2= present[0]*(X-self._interpolatedObsTrackXY[:,0])**2.\
                +present[1]*(Y-self._interpolatedObsTrackXY[:,1])**2.\
                +present[2]*(Z-self._interpolatedObsTrackXY[:,2])**2.
            if usev:
                dist2+= present[3]*(vX-self._interpolatedObsTrackXY[:,3])**2.\
                    +present[4]*(vY-self._interpolatedObsTrackXY[:,4])**2.\
                    +present[5]*(vZ-self._interpolatedObsTrackXY[:,5])**2.
        else:
            dist2= present[0]*(X-self._ObsTrackXY[:,0])**2.\
                +present[1]*(Y-self._ObsTrackXY[:,1])**2.\
                +present[2]*(Z-self._ObsTrackXY[:,2])**2.
            if usev:
                dist2+= present[3]*(vX-self._ObsTrackXY[:,3])**2.\
                    +present[4]*(vY-self._ObsTrackXY[:,4])**2.\
                    +present[5]*(vZ-self._ObsTrackXY[:,5])**2.
        return numpy.argmin(dist2)

    def _find_closest_trackpointLB(self,l,b,D,vlos,pmll,pmbb,interp=True,
                                   usev=False):
        return self.find_closest_trackpointLB(l,b,D,vlos,pmll,pmbb,
                                              interp=interp,
                                              usev=usev)
    def find_closest_trackpointLB(self,l,b,D,vlos,pmll,pmbb,interp=True,
                                   usev=False):
        """
        NAME:

           find_closest_trackpointLB

        PURPOSE:
           find the closest point on the stream track to a given point in (l,b,...) coordinates

        INPUT:

           l,b,D,vlos,pmll,pmbb- coordinates in (deg,deg,kpc,km/s,mas/yr,mas/yr)

           interp= (True) if True, return the closest index on the interpolated track

           usev= (False) if True, also use the velocity components (default is to only use the positions)

        OUTPUT:

           index of closest track point on the interpolated or not-interpolated track
           
        HISTORY:

           2013-12-17- Written - Bovy (IAS)

        """
        if interp:
            nTrackPoints= len(self._interpolatedThetasTrack)
        else:
            nTrackPoints= len(self._thetasTrack)
        if l is None:
            l= 0.
            trackL= numpy.zeros(nTrackPoints)
        elif interp:
            trackL= self._interpolatedObsTrackLB[:,0]
        else:
            trackL= self._ObsTrackLB[:,0]
        if b is None:
            b= 0.
            trackB= numpy.zeros(nTrackPoints)
        elif interp:
            trackB= self._interpolatedObsTrackLB[:,1]
        else:
            trackB= self._ObsTrackLB[:,1]
        if D is None:
            D= 1.
            trackD= numpy.ones(nTrackPoints)
        elif interp:
            trackD= self._interpolatedObsTrackLB[:,2]
        else:
            trackD= self._ObsTrackLB[:,2]
        if usev:
            if vlos is None:
                vlos= 0.
                trackVlos= numpy.zeros(nTrackPoints)
            elif interp:
                trackVlos= self._interpolatedObsTrackLB[:,3]
            else:
                trackVlos= self._ObsTrackLB[:,3]
            if pmll is None:
                pmll= 0.
                trackPmll= numpy.zeros(nTrackPoints)
            elif interp:
                trackPmll= self._interpolatedObsTrackLB[:,4]
            else:
                trackPmll= self._ObsTrackLB[:,4]
            if pmbb is None:
                pmbb= 0.
                trackPmbb= numpy.zeros(nTrackPoints)
            elif interp:
                trackPmbb= self._interpolatedObsTrackLB[:,5]
            else:
                trackPmbb= self._ObsTrackLB[:,5]
        #Calculate rectangular coordinates
        XYZ= bovy_coords.lbd_to_XYZ(l,b,D,degree=True)
        trackXYZ= bovy_coords.lbd_to_XYZ(trackL,trackB,trackD,degree=True)
        if usev:
            vxvyvz= bovy_coords.vrpmllpmbb_to_vxvyvz(vlos,pmll,pmbb,
                                                     XYZ[0],XYZ[1],XYZ[2],
                                                     XYZ=True)
            trackvxvyvz= bovy_coords.vrpmllpmbb_to_vxvyvz(trackVlos,trackPmll,
                                                          trackPmbb,
                                                          trackXYZ[:,0],
                                                          trackXYZ[:,1],
                                                          trackXYZ[:,2],
                                                          XYZ=True)
        #Calculate distance
        dist2= (XYZ[0]-trackXYZ[:,0])**2.\
            +(XYZ[1]-trackXYZ[:,1])**2.\
            +(XYZ[2]-trackXYZ[:,2])**2.
        if usev:
            dist2+= (vxvyvz[0]-trackvxvyvz[:,0])**2.\
                +(vxvyvz[1]-trackvxvyvz[:,1])**2.\
                +(vxvyvz[2]-trackvxvyvz[:,2])**2.
        return numpy.argmin(dist2)            

    def _find_closest_trackpointaA(self,Or,Op,Oz,ar,ap,az,interp=True):
        """
        NAME:
           _find_closest_trackpointaA
        PURPOSE:
           find the closest point on the stream track to a given point in
           frequency-angle coordinates
        INPUT:
           Or,Op,Oz,ar,ap,az - phase-space coordinates of the given point
           interp= (True), if True, return the index of the interpolated track
        OUTPUT:
           index into the track of the closest track point
        HISTORY:
           2013-12-22 - Written - Bovy (IAS)
        """
        #Calculate angle offset along the stream parallel to the stream track
        angle= numpy.hstack((ar,ap,az))
        da= angle-self._progenitor_angle
        dapar= self._sigMeanSign*numpy.sum(da*self._dsigomeanProgDirection)
        if interp:
            dist= numpy.fabs(dapar-self._interpolatedThetasTrack)
        else:
            dist= numpy.fabs(dapar-self._thetasTrack)
        return numpy.argmin(dist)

#########DISTRIBUTION AS A FUNCTION OF ANGLE ALONG THE STREAM##################
    def meanOmega(self,dangle,oned=False):
        """
        NAME:

           meanOmega

        PURPOSE:

           calculate the mean frequency as a function of angle, assuming a uniform time distribution up to a maximum time

        INPUT:

           dangle - angle offset

           oned= (False) if True, return the 1D offset from the progenitor (along the direction of disruption)

        OUTPUT:

           mean Omega

        HISTORY:

           2013-12-01 - Written - Bovy (IAS)

        """
        dOmin= dangle/self._tdisrupt
        meandO= self._meandO
        dO1D= ((numpy.sqrt(2./numpy.pi)*numpy.sqrt(self._sortedSigOEig[2])\
                   *numpy.exp(-0.5*(meandO-dOmin)**2.\
                                   /self._sortedSigOEig[2])/
                (1.+special.erf((meandO-dOmin)\
                                    /numpy.sqrt(2.*self._sortedSigOEig[2]))))\
                   +meandO)
        if oned: return dO1D
        else:
            return self._progenitor_Omega+dO1D*self._dsigomeanProgDirection\
                *self._sigMeanSign

    def sigOmega(self,dangle):
        """
        NAME:

           sigmaOmega

        PURPOSE:

           calculate the 1D sigma in frequency as a function of angle, assuming a uniform time distribution up to a maximum time

        INPUT:

           dangle - angle offset

        OUTPUT:

           sigma Omega

        HISTORY:

           2013-12-05 - Written - Bovy (IAS)

        """
        dOmin= dangle/self._tdisrupt
        meandO= self._meandO
        sO1D2= ((numpy.sqrt(2./numpy.pi)*numpy.sqrt(self._sortedSigOEig[2])\
                     *(meandO+dOmin)\
                     *numpy.exp(-0.5*(meandO-dOmin)**2.\
                                   /self._sortedSigOEig[2])/
                (1.+special.erf((meandO-dOmin)\
                                    /numpy.sqrt(2.*self._sortedSigOEig[2]))))\
                   +meandO**2.+self._sortedSigOEig[2])
        mO= self.meanOmega(dangle,oned=True)
        return numpy.sqrt(sO1D2-mO**2.)

    def ptdAngle(self,t,dangle):
        """
        NAME:

           ptdangle

        PURPOSE:

           return the probability of a given stripping time at a given angle along the stream

        INPUT:

           t - stripping time

           dangle - angle offset along the stream

        OUTPUT:

           p(td|dangle)

        HISTORY:

           2013-12-05 - Written - Bovy (IAS)

        """
        if isinstance(t,(int,float,numpy.float32,numpy.float64)):
            t= numpy.array([t])
        out= numpy.zeros(len(t))
        if t > 0.:
            dO= dangle/t[t < self._tdisrupt]
        else:
            return 0.
        #p(t|a) = \int dO p(O,t|a) = \int dO p(t|O,a) p(O|a) = \int dO delta (t-a/O)p(O|a) = O*2/a p(O|a); p(O|a) = \int dt p(a|O,t) p(O)p(t) = 1/O p(O)
        out[t < self._tdisrupt]=\
            dO**2./dangle*numpy.exp(-0.5*(dO-self._meandO)**2.\
                                         /self._sortedSigOEig[2])/\
                                         numpy.sqrt(self._sortedSigOEig[2])
        return out

    def meantdAngle(self,dangle):
        """
        NAME:

           meantdAngle

        PURPOSE:

           calculate the mean stripping time at a given angle

        INPUT:

           dangle - angle offset along the stream

        OUTPUT:

           mean stripping time at this dangle

        HISTORY:

           2013-12-05 - Written - Bovy (IAS)

        """
        Tlow= dangle/(self._meandO+3.*numpy.sqrt(self._sortedSigOEig[2]))
        Thigh= dangle/(self._meandO-3.*numpy.sqrt(self._sortedSigOEig[2]))
        num= integrate.quad(lambda x: x*self.ptdAngle(x,dangle),
                              Tlow,Thigh)[0]
        denom= integrate.quad(self.ptdAngle,Tlow,Thigh,(dangle,))[0]
        if denom == 0.: return self._tdisrupt
        elif numpy.isnan(denom): return 0.
        else: return num/denom

    def sigtdAngle(self,dangle):
        """
        NAME:

           sigtdAngle

        PURPOSE:

           calculate the dispersion in the stripping times at a given angle

        INPUT:

           dangle - angle offset along the stream

        OUTPUT:

           dispersion in the stripping times at this angle

        HISTORY:

           2013-12-05 - Written - Bovy (IAS)

        """
        Tlow= dangle/(self._meandO+3.*numpy.sqrt(self._sortedSigOEig[2]))
        Thigh= dangle/(self._meandO-3.*numpy.sqrt(self._sortedSigOEig[2]))
        numsig2= integrate.quad(lambda x: x**2.*self.ptdAngle(x,dangle),
                                Tlow,Thigh)[0]
        nummean= integrate.quad(lambda x: x*self.ptdAngle(x,dangle),
                                Tlow,Thigh)[0]
        denom= integrate.quad(self.ptdAngle,Tlow,Thigh,(dangle,))[0]
        if denom == 0.: return numpy.nan
        else: return numpy.sqrt(numsig2/denom-(nummean/denom)**2.)

    def pangledAngle(self,angleperp,dangle,smallest=False):
        """
        NAME:

           pangledAngle

        PURPOSE:
           return the probability of a given perpendicular angle  at a given angle along the stream

        INPUT:

           angleperp - perpendicular angle

           dangle - angle offset along the stream

           smallest= (False) calculate for smallest eigenvalue direction rather than for middle

        OUTPUT:

           p(angle_perp|dangle)

        HISTORY:

           2013-12-06 - Written - Bovy (IAS)

        """
        if isinstance(angleperp,(int,float,numpy.float32,numpy.float64)):
            angleperp= numpy.array([angleperp])
        out= numpy.zeros(len(angleperp))
        out= numpy.array([\
                integrate.quad(self._pangledAnglet,0.,self._tdisrupt,
                               (ap,dangle,smallest))[0] for ap in angleperp])
        return out

    def meanangledAngle(self,dangle,smallest=False):
        """
        NAME:

           meanangledAngle

        PURPOSE:

           calculate the mean perpendicular angle at a given angle

        INPUT:

           dangle - angle offset along the stream

           smallest= (False) calculate for smallest eigenvalue direction rather than for middle

        OUTPUT:

           mean perpendicular angle

        HISTORY:

           2013-12-06 - Written - Bovy (IAS)

        """
        if smallest: eigIndx= 0
        else: eigIndx= 1
        aplow= numpy.amax([numpy.sqrt(self._sortedSigOEig[eigIndx])\
                               *self._tdisrupt*5.,
                           self._sigangle])
        num= integrate.quad(lambda x: x*self.pangledAngle(x,dangle,smallest),
                            aplow,-aplow)[0]
        denom= integrate.quad(self.pangledAngle,aplow,-aplow,
                              (dangle,smallest))[0]
        if denom == 0.: return numpy.nan
        else: return num/denom

    def sigangledAngle(self,dangle,assumeZeroMean=True,smallest=False,
                       simple=False):
        """
        NAME:

           sigangledAngle

        PURPOSE:

           calculate the dispersion in the perpendicular angle at a given angle

        INPUT:

           dangle - angle offset along the stream

           assumeZeroMean= (True) if True, assume that the mean is zero (should be)

           smallest= (False) calculate for smallest eigenvalue direction rather than for middle

           simple= (False), if True, return an even simpler estimate

        OUTPUT:

           dispersion in the perpendicular angle at this angle

        HISTORY:

           2013-12-06 - Written - Bovy (IAS)

        """
        if smallest: eigIndx= 0
        else: eigIndx= 1
        if simple:
            dt= self.meantdAngle(dangle)
            return numpy.sqrt(self._sigangle2
                              +self._sortedSigOEig[eigIndx]*dt**2.)
        aplow= numpy.amax([numpy.sqrt(self._sortedSigOEig[eigIndx])*self._tdisrupt*5.,
                           self._sigangle])
        numsig2= integrate.quad(lambda x: x**2.*self.pangledAngle(x,dangle),
                                    aplow,-aplow)[0]
        if not assumeZeroMean:
            nummean= integrate.quad(lambda x: x*self.pangledAngle(x,dangle),
                                    aplow,-aplow)[0]
        else:
            nummean= 0.
        denom= integrate.quad(self.pangledAngle,aplow,-aplow,(dangle,))[0]
        if denom == 0.: return numpy.nan
        else: return numpy.sqrt(numsig2/denom-(nummean/denom)**2.)

    def _pangledAnglet(self,t,angleperp,dangle,smallest):
        """p(angle_perp|angle_par,time)"""
        if smallest: eigIndx= 0
        else: eigIndx= 1      
        if isinstance(angleperp,(int,float,numpy.float32,numpy.float64)):
            angleperp= numpy.array([angleperp])
            t= numpy.array([t])
        out= numpy.zeros_like(angleperp)
        tindx= t < self._tdisrupt
        out[tindx]=\
            numpy.exp(-0.5*angleperp[tindx]**2.\
                           /(t[tindx]**2.*self._sortedSigOEig[eigIndx]+self._sigangle2))/\
                           numpy.sqrt(t[tindx]**2.*self._sortedSigOEig[eigIndx]+self._sigangle2)\
                           *self.ptdAngle(t[t < self._tdisrupt],dangle)
        return out

################APPROXIMATE FREQUENCY-ANGLE TRANSFORMATION#####################
    def _approxaA(self,R,vR,vT,z,vz,phi,interp=True):
        """
        NAME:
           _approxaA
        PURPOSE:
           return action-angle coordinates for a point based on the linear 
           approximation around the stream track
        INPUT:
           R,vR,vT,z,vz,phi - phase-space coordinates of the given point
           interp= (True), if True, use the interpolated track
        OUTPUT:
           (Or,Op,Oz,ar,ap,az)
        HISTORY:
           2013-12-03 - Written - Bovy (IAS)
        """
        if isinstance(R,(int,float,numpy.float32,numpy.float64)): #Scalar input
            R= numpy.array([R])
            vR= numpy.array([vR])
            vT= numpy.array([vT])
            z= numpy.array([z])
            vz= numpy.array([vz])
            phi= numpy.array([phi])
        closestIndx= [self._find_closest_trackpoint(R[ii],vR[ii],vT[ii],
                                                    z[ii],vz[ii],phi[ii],
                                                    interp=interp,
                                                    xy=False) 
                      for ii in range(len(R))]
        out= numpy.empty((6,len(R)))
        for ii in range(len(R)):
            dxv= numpy.empty(6)
            if interp:
                dxv[0]= R[ii]-self._interpolatedObsTrack[closestIndx[ii],0]
                dxv[1]= vR[ii]-self._interpolatedObsTrack[closestIndx[ii],1]
                dxv[2]= vT[ii]-self._interpolatedObsTrack[closestIndx[ii],2]
                dxv[3]= z[ii]-self._interpolatedObsTrack[closestIndx[ii],3]
                dxv[4]= vz[ii]-self._interpolatedObsTrack[closestIndx[ii],4]
                dxv[5]= phi[ii]-self._interpolatedObsTrack[closestIndx[ii],5]
                jacIndx= self._find_closest_trackpoint(R[ii],vR[ii],vT[ii],
                                                       z[ii],vz[ii],phi[ii],
                                                       interp=False,
                                                       xy=False)
            else:
                dxv[0]= R[ii]-self._ObsTrack[closestIndx[ii],0]
                dxv[1]= vR[ii]-self._ObsTrack[closestIndx[ii],1]
                dxv[2]= vT[ii]-self._ObsTrack[closestIndx[ii],2]
                dxv[3]= z[ii]-self._ObsTrack[closestIndx[ii],3]
                dxv[4]= vz[ii]-self._ObsTrack[closestIndx[ii],4]
                dxv[5]= phi[ii]-self._ObsTrack[closestIndx[ii],5]
                jacIndx= closestIndx[ii]
            #Make sure phi hasn't wrapped around
            if dxv[5] > numpy.pi:
                dxv[5]-= 2.*numpy.pi
            elif dxv[5] < -numpy.pi:
                dxv[5]+= 2.*numpy.pi
            #Apply closest jacobian
            out[:,ii]= numpy.dot(self._alljacsTrack[jacIndx,:,:],
                                 dxv)
            if interp:
                out[:,ii]+= self._interpolatedObsTrackAA[closestIndx[ii]]
            else:
                out[:,ii]+= self._ObsTrackAA[closestIndx[ii]]
        return out            

    def _approxaAInv(self,Or,Op,Oz,ar,ap,az,interp=True):
        """
        NAME:
           _approxaAInv
        PURPOSE:
           return R,vR,... coordinates for a point based on the linear 
           approximation around the stream track
        INPUT:
           Or,Op,Oz,ar,ap,az - phase space coordinates in frequency-angle 
                               space
           interp= (True), if True, use the interpolated track
        OUTPUT:
           (R,vR,vT,z,vz,phi)
        HISTORY:
           2013-12-22 - Written - Bovy (IAS)
        """
        if isinstance(Or,(int,float,numpy.float32,numpy.float64)): #Scalar input
            Or= numpy.array([Or])
            Op= numpy.array([Op])
            Oz= numpy.array([Oz])
            ar= numpy.array([ar])
            ap= numpy.array([ap])
            az= numpy.array([az])
        #Calculate apar, angle offset along the stream
        closestIndx= [self._find_closest_trackpointaA(Or[ii],Op[ii],Oz[ii],
                                                      ar[ii],ap[ii],az[ii],
                                                      interp=interp)\
                          for ii in range(len(Or))]
        out= numpy.empty((6,len(Or)))
        for ii in range(len(Or)):
            dOa= numpy.empty(6)
            if interp:
                dOa[0]= Or[ii]-self._interpolatedObsTrackAA[closestIndx[ii],0]
                dOa[1]= Op[ii]-self._interpolatedObsTrackAA[closestIndx[ii],1]
                dOa[2]= Oz[ii]-self._interpolatedObsTrackAA[closestIndx[ii],2]
                dOa[3]= ar[ii]-self._interpolatedObsTrackAA[closestIndx[ii],3]
                dOa[4]= ap[ii]-self._interpolatedObsTrackAA[closestIndx[ii],4]
                dOa[5]= az[ii]-self._interpolatedObsTrackAA[closestIndx[ii],5]
                jacIndx= self._find_closest_trackpointaA(Or[ii],Op[ii],Oz[ii],
                                                         ar[ii],ap[ii],az[ii],
                                                         interp=False)
            else:
                dOa[0]= Or[ii]-self._ObsTrackAA[closestIndx[ii],0]
                dOa[1]= Op[ii]-self._ObsTrackAA[closestIndx[ii],1]
                dOa[2]= Oz[ii]-self._ObsTrackAA[closestIndx[ii],2]
                dOa[3]= ar[ii]-self._ObsTrackAA[closestIndx[ii],3]
                dOa[4]= ap[ii]-self._ObsTrackAA[closestIndx[ii],4]
                dOa[5]= az[ii]-self._ObsTrackAA[closestIndx[ii],5]
                jacIndx= closestIndx[ii]
            #Make sure the angles haven't wrapped around
            if dOa[3] > numpy.pi:
                dOa[3]-= 2.*numpy.pi
            elif dOa[3] < -numpy.pi:
                dOa[3]+= 2.*numpy.pi
            if dOa[4] > numpy.pi:
                dOa[4]-= 2.*numpy.pi
            elif dOa[4] < -numpy.pi:
                dOa[4]+= 2.*numpy.pi
            if dOa[5] > numpy.pi:
                dOa[5]-= 2.*numpy.pi
            elif dOa[5] < -numpy.pi:
                dOa[5]+= 2.*numpy.pi
            #Apply closest jacobian
            out[:,ii]= numpy.dot(self._allinvjacsTrack[jacIndx,:,:],
                                 dOa)
            if interp:
                out[:,ii]+= self._interpolatedObsTrack[closestIndx[ii]]
            else:
                out[:,ii]+= self._ObsTrack[closestIndx[ii]]
        return out            

################################EVALUATE THE DF################################
    def __call__(self,*args,**kwargs):
        """
        NAME:

           __call__

        PURPOSE:

           evaluate the DF

        INPUT:

           Either:

              a) R,vR,vT,z,vz,phi ndarray [nobjects]

              b) (Omegar,Omegaphi,Omegaz,angler,anglephi,anglez) tuple if aAInput

                where:

                    Omegar - radial frequency

                    Omegaphi - azimuthal frequency

                    Omegaz - vertical frequency

                    angler - radial angle

                    anglephi - azimuthal angle

                    anglez - vertical angle

              c) Orbit instance or list thereof

           log= if True, return the natural log

           aaInput= (False) if True, option b above

        OUTPUT:

           value of DF

        HISTORY:

           2013-12-03 - Written - Bovy (IAS)

        """
        #First parse log
        if kwargs.has_key('log'):
            log= kwargs['log']
            kwargs.pop('log')
        else:
            log= True
        dOmega, dangle= self.prepData4Call(*args,**kwargs)
        #Omega part
        dOmega4dfOmega= dOmega\
            -numpy.tile(self._dsigomeanProg.T,(dOmega.shape[1],1)).T
        logdfOmega= -0.5*numpy.sum(dOmega4dfOmega*
                                   numpy.dot(self._sigomatrixinv,
                                             dOmega4dfOmega),
                                   axis=0)-0.5*self._sigomatrixLogdet\
                                   +numpy.log(numpy.fabs(numpy.dot(self._dsigomeanProgDirection,dOmega)))
        #Angle part
        dangle2= numpy.sum(dangle**2.,axis=0)
        dOmega2= numpy.sum(dOmega**2.,axis=0)
        dOmegaAngle= numpy.sum(dOmega*dangle,axis=0)
        logdfA= -0.5/self._sigangle2*(dangle2-dOmegaAngle**2./dOmega2)\
            -2.*self._lnsigangle-0.5*numpy.log(dOmega2)
        #Finite stripping part
        a0= dOmegaAngle/numpy.sqrt(2.)/self._sigangle/numpy.sqrt(dOmega2)
        ad= numpy.sqrt(dOmega2)/numpy.sqrt(2.)/self._sigangle\
            *(self._tdisrupt-dOmegaAngle/dOmega2)
        loga= numpy.log((special.erf(a0)+special.erf(ad))/2.) #divided by 2 st 0 for well-within the stream
        out= logdfA+logdfOmega+loga+self._logmeandetdOdJp
        if log:
            return out
        else:
            return numpy.exp(out)

    def prepData4Call(self,*args,**kwargs):
        """
        NAME:
           prepData4Call
        PURPOSE:
           prepare stream data for the __call__ method
        INPUT:
           __call__ inputs
        OUTPUT:
           (dOmega,dangle); wrt the progenitor; each [3,nobj]
        HISTORY:
           2013-12-04 - Written - Bovy (IAS)
        """
        #First calculate the actionAngle coordinates if they're not given 
        #as such
        freqsAngles= self._parse_call_args(*args,**kwargs)
        dOmega= freqsAngles[:3,:]\
            -numpy.tile(self._progenitor_Omega.T,(freqsAngles.shape[1],1)).T
        dangle= freqsAngles[3:,:]\
            -numpy.tile(self._progenitor_angle.T,(freqsAngles.shape[1],1)).T
        #Assuming single wrap, resolve large angle differences (wraps should be marginalized over)
        dangle[(dangle < -4.)]+= 2.*numpy.pi
        dangle[(dangle > 4.)]-= 2.*numpy.pi
        return (dOmega,dangle)

    def _parse_call_args(self,*args,**kwargs):
        """Helper function to parse the arguments to the __call__ and related functions,
        return [6,nobj] array of frequencies (:3) and angles (3:)"""
        if kwargs.has_key('interp'):
            interp= kwargs['interp']
        else:
            interp= self._useInterp
        if len(args) == 5:
            raise IOError("Must specify phi for streamdf")
        elif len(args) == 6:
            if kwargs.has_key('aAInput') and kwargs['aAInput']:
                if isinstance(args[0],(int,float,numpy.float32,numpy.float64)):
                    out= numpy.empty((6,1))
                else:
                    out= numpy.empty((6,len(args[0])))
                for ii in range(6):
                    out[ii,:]= args[ii]
                return out
            else:
                return self._approxaA(*args,interp=interp)
        elif isinstance(args[0],Orbit):
            o= args[0]
            return self._approxaA(o.R(),o.vR(),o.vT(),o.z(),o.vz(),o.phi(),
                                  interp=interp)
        elif isinstance(args[0],list) and isinstance(args[0][0],Orbit):
            R, vR, vT, z, vz, phi= [], [], [], [], [], []
            for o in args[0]:
                R.append(o.R())
                vR.append(o.vR())
                vT.append(o.vT())
                z.append(o.z())
                vz.append(o.vz())
                phi.append(o.phi())
            return self._approxaA(numpy.array(R),numpy.array(vR),
                                  numpy.array(vT),numpy.array(z),
                                  numpy.array(vz),numpy.array(phi),
                                  interp=interp)
    def callMarg(self,xy,**kwargs):
        """
        NAME:

           callMarg

        PURPOSE:
           evaluate the DF, marginalizing over some directions, in Galactocentric rectangular coordinates (or in observed l,b,D,vlos,pmll,pmbb) coordinates)

        INPUT:

           xy - phase-space point [X,Y,Z,vX,vY,vZ]; the distribution of the dimensions set to None is returned

           interp= (object-wide interp default) if True, use the interpolated stream track

           cindx= index of the closest point on the (interpolated) stream track if not given, determined from the dimensions given          

           nsigma= (3) number of sigma to marginalize the DF over (approximate sigma)

           ngl= (5) order of Gauss-Legendre integration

           lb= (False) if True, xy contains [l,b,D,vlos,pmll,pmbb] in [deg,deg,kpc,km/s,mas/yr,mas/yr] and the marginalized PDF in these coordinates is returned          

           Vnorm= (220) circular velocity to normalize with when lb=True

           Rnorm= (8) Galactocentric radius to normalize with when lb=True

           R0= (8) Galactocentric radius of the Sun (kpc)

           Zsun= (0.025) Sun's height above the plane (kpc)

           vsun= ([-11.1,241.92,7.25]) Sun's motion in cylindrical coordinates (vR positive away from center)

        OUTPUT:

           p(xy) marginalized over missing directions in xy

        HISTORY:

           2013-12-16 - Written - Bovy (IAS)

        """
        coordGiven= numpy.array([not x is None for x in xy],dtype='bool')
        if numpy.sum(coordGiven) == 6:
            raise NotImplementedError("When specifying all coordinates, please use __call__ instead of callMarg")
        #First construct the Gaussian approximation at this xy
        gaussmean, gaussvar= self.gaussApprox(xy,**kwargs)
        cholvar, chollower= stable_cho_factor(gaussvar)
        #Now Gauss-legendre integrate over missing directions
        if kwargs.has_key('ngl'):
            ngl= kwargs['ngl']
        else:
            ngl= 5
        if kwargs.has_key('nsigma'):
            nsigma= kwargs['nsigma']
        else:
            nsigma= 3
        glx, glw= numpy.polynomial.legendre.leggauss(ngl)
        coordEval= []
        weightEval= []
        jj= 0
        baseX= (glx+1)/2.
        baseX= list(baseX)
        baseX.extend(-(glx+1)/2.)
        baseX= numpy.array(baseX)
        baseW= glw
        baseW= list(baseW)
        baseW.extend(glw)
        baseW= numpy.array(baseW)
        for ii in range(6):
            if not coordGiven[ii]:
                coordEval.append(nsigma*baseX)
                weightEval.append(baseW)
                jj+= 1
            else:
                coordEval.append(xy[ii]*numpy.ones(1))
                weightEval.append(numpy.ones(1))
        mgrid= numpy.meshgrid(*coordEval,indexing='ij')
        mgridNotGiven= numpy.array([mgrid[ii].flatten() for ii in range(6) 
                                    if not coordGiven[ii]])
        mgridNotGiven= numpy.dot(cholvar,mgridNotGiven)
        jj= 0
        if coordGiven[0]: iX= mgrid[0]
        else:
            iX= mgridNotGiven[jj]+gaussmean[jj]
            jj+= 1
        if coordGiven[1]: iY= mgrid[1]
        else:
            iY= mgridNotGiven[jj]+gaussmean[jj]
            jj+= 1
        if coordGiven[2]: iZ= mgrid[2]
        else:
            iZ= mgridNotGiven[jj]+gaussmean[jj]
            jj+= 1
        if coordGiven[3]: ivX= mgrid[3]
        else:
            ivX= mgridNotGiven[jj]+gaussmean[jj]
            jj+= 1
        if coordGiven[4]: ivY= mgrid[4]
        else:
            ivY= mgridNotGiven[jj]+gaussmean[jj]
            jj+= 1
        if coordGiven[5]: ivZ= mgrid[5]
        else:
            ivZ= mgridNotGiven[jj]+gaussmean[jj]
            jj+= 1
        iXw, iYw, iZw, ivXw, ivYw, ivZw=\
            numpy.meshgrid(*weightEval,indexing='ij')
        if kwargs.has_key('lb') and kwargs['lb']: #Convert to Galactocentric cylindrical coordinates
            #Setup coordinate transformation kwargs
            if not kwargs.has_key('Vnorm'):
                Vnorm= self._Vnorm
            else:
                Vnorm= kwargs['Vnorm']
            if not kwargs.has_key('Rnorm'):
                Rnorm= self._Rnorm
            else:
                Rnorm= kwargs['Rnorm']
            if not kwargs.has_key('R0'):
                R0= self._R0
            else:
                R0= kwargs['R0']
            if not kwargs.has_key('Zsun'):
                Zsun= self._Zsun
            else:
                Zsun= kwargs['Zsun']
            if not kwargs.has_key('vsun'):
                vsun= self._vsun
            else:
                vsun= kwargs['vsun']
            tXYZ= bovy_coords.lbd_to_XYZ(iX.flatten(),iY.flatten(),
                                         iZ.flatten(),
                                         degree=True)
            iR,iphi,iZ= bovy_coords.XYZ_to_galcencyl(tXYZ[:,0],tXYZ[:,1],
                                                     tXYZ[:,2],
                                                     Xsun=R0,Ysun=0.,Zsun=Zsun)
            tvxvyvz= bovy_coords.vrpmllpmbb_to_vxvyvz(ivX.flatten(),
                                                      ivY.flatten(),
                                                      ivZ.flatten(),
                                                      tXYZ[:,0],tXYZ[:,1],
                                                      tXYZ[:,2],XYZ=True)
            ivR,ivT,ivZ= bovy_coords.vxvyvz_to_galcencyl(tvxvyvz[:,0],
                                                         tvxvyvz[:,1],
                                                         tvxvyvz[:,2],
                                                         iR,iphi,iZ,
                                                         galcen=True,
                                                         vsun=vsun)
            iR/= Rnorm
            iZ/= Rnorm
            ivR/= Vnorm
            ivT/= Vnorm
            ivZ/= Vnorm
        else:
            #Convert to cylindrical coordinates
            iR,iphi,iZ=\
                bovy_coords.rect_to_cyl(iX.flatten(),iY.flatten(),iZ.flatten())
            ivR,ivT,ivZ=\
                bovy_coords.rect_to_cyl_vec(ivX.flatten(),ivY.flatten(),
                                            ivZ.flatten(),
                                            iR,iphi,iZ,cyl=True)
        #Add the additional Jacobian dXdY/dldb... if necessary
        if kwargs.has_key('lb') and kwargs['lb']:
            #Find the nearest track point
            if kwargs.has_key('interp'):
                interp= kwargs['interp']
            else:
                interp= self._useInterp
            if not kwargs.has_key('cindx'):
                cindx= self._find_closest_trackpointLB(*xy,interp=interp,
                                                        usev=True)
            else:
                cindx= kwargs['cindx']
            #Only l,b,d,... to Galactic X,Y,Z,... is necessary because going
            #from Galactic to Galactocentric has Jacobian determinant 1
            if interp:
                addLogDet= self._interpolatedTrackLogDetJacLB[cindx]
            else:
                addLogDet= self._trackLogDetJacLB[cindx]
        else:
            addLogDet= 0.
        logdf= self(iR,ivR,ivT,iZ,ivZ,iphi,log=True)
        return logsumexp(logdf
                         +numpy.log(iXw.flatten())
                         +numpy.log(iYw.flatten())
                         +numpy.log(iZw.flatten())
                         +numpy.log(ivXw.flatten())
                         +numpy.log(ivYw.flatten())
                         +numpy.log(ivZw.flatten()))\
                         +0.5*numpy.log(numpy.linalg.det(gaussvar))\
                         +addLogDet

    def gaussApprox(self,xy,**kwargs):
        """
        NAME:

           gaussApprox

        PURPOSE:

           return the mean and variance of a Gaussian approximation to the stream DF at a given phase-space point in Galactocentric rectangular coordinates (distribution is over missing directions)

        INPUT:

           xy - phase-space point [X,Y,Z,vX,vY,vZ]; the distribution of the dimensions set to None is returned

           interp= (object-wide interp default) if True, use the interpolated stream track

           cindx= index of the closest point on the (interpolated) stream track if not given, determined from the dimensions given

           lb= (False) if True, xy contains [l,b,D,vlos,pmll,pmbb] in [deg,deg,kpc,km/s,mas/yr,mas/yr] and the Gaussian approximation in these coordinates is returned

        OUTPUT:

           (mean,variance) of the approximate Gaussian DF for the missing directions in xy

        HISTORY:

           2013-12-12 - Written - Bovy (IAS)

        """
        if kwargs.has_key('interp'):
            interp= kwargs['interp']
        else:
            interp= self._useInterp
        if kwargs.has_key('lb'):
            lb= kwargs['lb']
        else:
            lb= False
        #What are we looking for
        coordGiven= numpy.array([not x is None for x in xy],dtype='bool')
        nGiven= numpy.sum(coordGiven)
        #First find the nearest track point
        if not kwargs.has_key('cindx') and lb:
            cindx= self._find_closest_trackpointLB(*xy,interp=interp,
                                                  usev=True)
        elif not kwargs.has_key('cindx') and not lb:
            cindx= self._find_closest_trackpoint(*xy,xy=True,interp=interp,
                                                  usev=True)
        else:
            cindx= kwargs['cindx']
        #Get the covariance matrix
        if interp and lb:
            tcov= self._interpolatedAllErrCovsLBUnscaled[cindx]
            tmean= self._interpolatedObsTrackLB[cindx]
        elif interp and not lb:
            tcov= self._interpolatedAllErrCovsXY[cindx]
            tmean= self._interpolatedObsTrackXY[cindx]
        elif not interp and lb:
            tcov= self._allErrCovsLBUnscaled[cindx]
            tmean= self._ObsTrackLB[cindx]
        elif not interp and not lb:
            tcov= self._allErrCovsXY[cindx]
            tmean= self._ObsTrackXY[cindx]
        if lb:#Apply scale factors
            tcov= copy.copy(tcov)
            tcov*= numpy.tile(self._ErrCovsLBScale,(6,1))
            tcov*= numpy.tile(self._ErrCovsLBScale,(6,1)).T
        #Fancy indexing to recover V22, V11, and V12; V22, V11, V12 as in Appendix B of 0905.2979v1
        V11indx0= numpy.array([[ii for jj in range(6-nGiven)] for ii in range(6) if not coordGiven[ii]])
        V11indx1= numpy.array([[ii for ii in range(6) if not coordGiven[ii]] for jj in range(6-nGiven)])
        V11= tcov[V11indx0,V11indx1]
        V22indx0= numpy.array([[ii for jj in range(nGiven)] for ii in range(6) if coordGiven[ii]])
        V22indx1= numpy.array([[ii for ii in range(6) if coordGiven[ii]] for jj in range(nGiven)])
        V22= tcov[V22indx0,V22indx1]
        V12indx0= numpy.array([[ii for jj in range(nGiven)] for ii in range(6) if not coordGiven[ii]])
        V12indx1= numpy.array([[ii for ii in range(6) if coordGiven[ii]] for jj in range(6-nGiven)])
        V12= tcov[V12indx0,V12indx1]
        #Also get m1 and m2, again following Appendix B of 0905.2979v1
        m1= tmean[True-coordGiven]
        m2= tmean[coordGiven]
        #conditional mean and variance
        V22inv= numpy.linalg.inv(V22)
        v2= numpy.array([xy[ii] for ii in range(6) if coordGiven[ii]])
        condMean= m1+numpy.dot(V12,numpy.dot(V22inv,v2-m2))
        condVar= V11-numpy.dot(V12,numpy.dot(V22inv,V12.T))
        return (condMean,condVar)

################################SAMPLE THE DF##################################
    def sample(self,n,returnaAdt=False,returndt=False,interp=None,
               xy=False,lb=False,
               Vnorm=None,Rnorm=None,
               R0=None,Zsun=None,vsun=None):
        """
        NAME:

            sample

        PURPOSE:

            sample from the DF

        INPUT:

            n - number of points to return

            returnaAdt= (False) if True, return (Omega,angle,dt)

            returndT= (False) if True, also return the time since the star was stripped

            interp= (object-wide default) use interpolation of the stream track

            xy= (False) if True, return Galactocentric rectangular coordinates

            lb= (False) if True, return Galactic l,b,d,vlos,pmll,pmbb coordinates

            +Coordinate transformation inputs (all default to the instance-wide
            values):

              Vnorm= circular velocity to normalize velocities with

              Rnorm= Galactocentric radius to normalize positions with

              R0= Galactocentric radius of the Sun (kpc)

              Zsun= Sun's height above the plane (kpc)

              vsun= Sun's motion in cylindrical coordinates (vR positive away from center)

        OUTPUT:

            (R,vR,vT,z,vz,phi) of points on the stream in 6,N array

        HISTORY:

            2013-12-22 - Written - Bovy (IAS)

        """
        if interp is None:
            interp= self._useInterp
        #First sample frequencies
        #Sample frequency along largest eigenvalue using ARS
        dO1s=\
            bovy_ars.bovy_ars([0.,0.],[True,False],
                              [self._meandO-numpy.sqrt(self._sortedSigOEig[2]),
                               self._meandO+numpy.sqrt(self._sortedSigOEig[2])],
                              _h_ars,_hp_ars,nsamples=n,
                              hxparams=(self._meandO,self._sortedSigOEig[2]),
                              maxn=100)
        dO1s= numpy.array(dO1s)*self._sigMeanSign
        dO2s= numpy.random.normal(size=n)*numpy.sqrt(self._sortedSigOEig[1])
        dO3s= numpy.random.normal(size=n)*numpy.sqrt(self._sortedSigOEig[0])
        #Rotate into dOs in R,phi,z coordinates
        dO= numpy.vstack((dO3s,dO2s,dO1s))
        dO= numpy.dot(self._sigomatrixEig[1][:,self._sigomatrixEigsortIndx],
                      dO)
        Om= dO+numpy.tile(self._progenitor_Omega.T,(n,1)).T
        #Also generate angles
        da= numpy.random.normal(size=(3,n))*self._sigangle
        #And a random time
        dt= numpy.random.uniform(size=n)*self._tdisrupt
        #Integrate the orbits relative to the progenitor
        da+= dO*numpy.tile(dt,(3,1))
        angle= da+numpy.tile(self._progenitor_angle.T,(n,1)).T
        if returnaAdt:
            return (Om,angle,dt)
        #Propagate to R,vR,etc.
        RvR= self._approxaAInv(Om[0,:],Om[1,:],Om[2,:],
                               angle[0,:],angle[1,:],angle[2,:],
                               interp=interp)
        if returndt and not xy and not lb:
            return (RvR,dt)
        elif not xy and not lb:
            return RvR
        if xy:
            sX= RvR[0]*numpy.cos(RvR[5])
            sY= RvR[0]*numpy.sin(RvR[5])
            sZ= RvR[3]
            svX, svY, svZ=\
                bovy_coords.cyl_to_rect_vec(RvR[1],
                                            RvR[2],
                                            RvR[4],
                                            RvR[5])            
            out= numpy.empty((6,n))
            out[0]= sX
            out[1]= sY
            out[2]= sZ
            out[3]= svX
            out[4]= svY
            out[5]= svZ
            if returndt:
                return (out,dt)
            else:
                return out
        if lb:
            if Vnorm is None:
                Vnorm= self._Vnorm
            if Rnorm is None:
                Rnorm= self._Rnorm
            if R0 is None:
                R0= self._R0
            if Zsun is None:
                Zsun= self._Zsun
            if vsun is None:
                vsun= self._vsun
            XYZ= bovy_coords.galcencyl_to_XYZ(RvR[0]*Rnorm,
                                              RvR[5],
                                              RvR[3]*Rnorm,
                                              Xsun=R0,Zsun=Zsun)
            vXYZ= bovy_coords.galcencyl_to_vxvyvz(RvR[1]*Vnorm,
                                                  RvR[2]*Vnorm,
                                                  RvR[4]*Vnorm,
                                                  RvR[5],
                                                  vsun=vsun)
            slbd=bovy_coords.XYZ_to_lbd(XYZ[0],XYZ[1],XYZ[2],
                                        degree=True)
            svlbd= bovy_coords.vxvyvz_to_vrpmllpmbb(vXYZ[0],vXYZ[1],vXYZ[2],
                                                    slbd[:,0],slbd[:,1],
                                                    slbd[:,2],
                                                    degree=True)
            out= numpy.empty((6,n))
            out[0]= slbd[:,0]
            out[1]= slbd[:,1]
            out[2]= slbd[:,2]
            out[3]= svlbd[:,0]
            out[4]= svlbd[:,1]
            out[5]= svlbd[:,2]
            if returndt:
                return (out,dt)
            else:
                return out

def _h_ars(x,params):
    """ln p(Omega) for ARS"""
    mO, sO2= params
    return -0.5*(x-mO)**2./sO2+numpy.log(x)
def _hp_ars(x,params):
    """d ln p(Omega) / d Omega for ARS"""
    mO, sO2= params
    return -(x-mO)/sO2+1./x

def _determine_stream_track_single(aA,progenitorTrack,trackt,
                                   progenitor_angle,sigMeanSign,
                                   dsigomeanProgDirection,meanOmega,
                                   thetasTrack):
    #Setup output
    allAcfsTrack= numpy.empty((9))
    alljacsTrack= numpy.empty((6,6))
    allinvjacsTrack= numpy.empty((6,6))
    ObsTrack= numpy.empty((6))
    ObsTrackAA= numpy.empty((6))
    detdOdJ= numpy.empty(6)
    #Calculate
    tacfs= aA.actionsFreqsAngles(progenitorTrack(trackt),
                                       maxn=3)
    allAcfsTrack[0]= tacfs[0][0]
    allAcfsTrack[1]= tacfs[1][0]
    allAcfsTrack[2]= tacfs[2][0]
    for jj in range(3,9):
        allAcfsTrack[jj]= tacfs[jj]
    tjac= calcaAJac(progenitorTrack(trackt)._orb.vxvv,
                    aA,
                    dxv=None,actionsFreqsAngles=True,
                    lb=False,
                    _initacfs=tacfs)
    alljacsTrack[:,:]= tjac[3:,:]
    tinvjac= numpy.linalg.inv(tjac[3:,:])
    allinvjacsTrack[:,:]= tinvjac
    #Also store detdOdJ
    jindx= numpy.array([True,True,True,False,False,False,True,True,True],
                       dtype='bool')
    dOdJ= numpy.dot(tjac[3:,:],numpy.linalg.inv(tjac[jindx,:]))[0:3,0:3]
    detdOdJ= numpy.linalg.det(dOdJ)
    theseAngles= numpy.mod(progenitor_angle\
                               +thetasTrack\
                               *sigMeanSign\
                               *dsigomeanProgDirection,
                           2.*numpy.pi)
    ObsTrackAA[3:]= theseAngles
    diffAngles= theseAngles-allAcfsTrack[6:]
    diffAngles[(diffAngles > numpy.pi)]= diffAngles[(diffAngles > numpy.pi)]-2.*numpy.pi
    diffAngles[(diffAngles < -numpy.pi)]= diffAngles[(diffAngles < -numpy.pi)]+2.*numpy.pi
    thisFreq= meanOmega(thetasTrack)
    ObsTrackAA[:3]= thisFreq
    diffFreqs= thisFreq-allAcfsTrack[3:6]
    ObsTrack[:]= numpy.dot(tinvjac,
                              numpy.hstack((diffFreqs,diffAngles)))
    ObsTrack[0]+= \
        progenitorTrack(trackt).R()
    ObsTrack[1]+= \
        progenitorTrack(trackt).vR()
    ObsTrack[2]+= \
        progenitorTrack(trackt).vT()
    ObsTrack[3]+= \
        progenitorTrack(trackt).z()
    ObsTrack[4]+= \
        progenitorTrack(trackt).vz()
    ObsTrack[5]+= \
        progenitorTrack(trackt).phi()
    return [allAcfsTrack,alljacsTrack,allinvjacsTrack,ObsTrack,ObsTrackAA,
            detdOdJ]

def _determine_stream_spread_single(sigomatrixEig,
                                    thetasTrack,
                                    sigOmega,
                                    sigAngle,
                                    allinvjacsTrack):
    """sigAngle input may either be a function that returns the dispersion in
    perpendicular angle as a function of parallel angle, or a value"""
    #Estimate the spread in all frequencies and angles
    sigObig2= sigOmega(thetasTrack)**2.
    tsigOdiag= copy.copy(sigomatrixEig[0])
    tsigOdiag[numpy.argmax(tsigOdiag)]= sigObig2
    tsigO= numpy.dot(sigomatrixEig[1],
                     numpy.dot(numpy.diag(tsigOdiag),
                               numpy.linalg.inv(sigomatrixEig[1])))
    #angles
    if hasattr(sigAngle,'__call__'):
        sigangle2= sigAngle(thetasTrack)**2.
    else:
        sigangle2= sigAngle**2.
    tsigadiag= numpy.ones(3)*sigangle2
    tsigadiag[numpy.argmax(tsigOdiag)]= 1.
    tsiga= numpy.dot(sigomatrixEig[1],
                    numpy.dot(numpy.diag(tsigadiag),
                              numpy.linalg.inv(sigomatrixEig[1])))
    #correlations, assume half correlated for now (can be calculated)
    correlations= numpy.diag(0.5*numpy.ones(3))*numpy.sqrt(tsigOdiag*tsigadiag)
    correlations[numpy.argmax(tsigOdiag),numpy.argmax(tsigOdiag)]= 0.
    correlations= numpy.dot(sigomatrixEig[1],
                            numpy.dot(correlations,
                                      numpy.linalg.inv(sigomatrixEig[1])))
    #Now convert
    fullMatrix= numpy.empty((6,6))
    fullMatrix[:3,:3]= tsigO
    fullMatrix[3:,3:]= tsiga
    fullMatrix[3:,:3]= correlations
    fullMatrix[:3,3:]= correlations.T
    return numpy.dot(allinvjacsTrack,numpy.dot(fullMatrix,allinvjacsTrack.T))

def calcaAJac(xv,aA,dxv=None,freqs=False,dOdJ=False,actionsFreqsAngles=False,
              lb=False,coordFunc=None,
              Vnorm=220.,Rnorm=8.,R0=8.,Zsun=0.025,vsun=[-11.1,8.*30.24,7.25],
              _initacfs=None):
    """
    NAME:
       calcaAJac
    PURPOSE:
       calculate the Jacobian d(J,theta)/d(x,v)
    INPUT:
       xv - phase-space point: Either
          1) [R,vR,vT,z,vz,phi]
          2) [l,b,D,vlos,pmll,pmbb] (if lb=True, see below)
          3) list/array of 6 numbers that can be transformed into (normalized) R,vR,vT,z,vz,phi using coordFunc

       aA - actionAngle instance

       dxv - infinitesimal to use (rescaled for lb, so think fractionally))

       freqs= (False) if True, go to frequencies rather than actions

       dOdJ= (False), actually calculate d Frequency / d action

       actionsFreqsAngles= (False) if True, calculate d(action,freq.,angle)/d (xv)

       lb= (False) if True, start with (l,b,D,vlos,pmll,pmbb) in (deg,deg,kpc,km/s,mas/yr,mas/yr)
       Vnorm= (220) circular velocity to normalize with when lb=True
       Rnorm= (8) Galactocentric radius to normalize with when lb=True
       R0= (8) Galactocentric radius of the Sun (kpc)
       Zsun= (0.025) Sun's height above the plane (kpc)
       vsun= ([-11.1,241.92,7.25]) Sun's motion in cylindrical coordinates (vR positive away from center)

       coordFunc= (None) if set, this is a function that takes xv and returns R,vR,vT,z,vz,phi in normalized units (units where vc=1 at r=1 if the potential is normalized that way, for example)

    OUTPUT:
       Jacobian matrix
    HISTORY:
       2013-11-25 - Written - Bovy (IAS) 
    """
    if lb:
        coordFunc= lambda x: lbCoordFunc(xv,Vnorm,Rnorm,R0,Zsun,vsun)
    if not coordFunc is None:
        R, vR, vT, z, vz, phi= coordFunc(xv)
    else:
        R, vR, vT, z, vz, phi= xv[0],xv[1],xv[2],xv[3],xv[4],xv[5]
    if dxv is None:
        dxv= 10.**-8.*numpy.ones(6)
    if lb:
        #Re-scale some of the differences, to be more natural
        dxv[0]*= 180./numpy.pi
        dxv[1]*= 180./numpy.pi
        dxv[2]*= Rnorm
        dxv[3]*= Vnorm
        dxv[4]*= Vnorm/4.74047/xv[2]
        dxv[5]*= Vnorm/4.74047/xv[2]
    if actionsFreqsAngles:
        jac= numpy.zeros((9,6))
    else:
        jac= numpy.zeros((6,6))
    if dOdJ:
        jac2= numpy.zeros((6,6))
    if _initacfs is None:
        jr,lz,jz,Or,Ophi,Oz,ar,aphi,az\
            = aA.actionsFreqsAngles(R,vR,vT,z,vz,phi,maxn=3)
    else:
        jr,lz,jz,Or,Ophi,Oz,ar,aphi,az\
            = _initacfs
    for ii in range(6):
        temp= xv[ii]+dxv[ii] #Trick to make sure dxv is representable
        dxv[ii]= temp-xv[ii]
        xv[ii]+= dxv[ii]
        if not coordFunc is None:
            tR, tvR, tvT, tz, tvz, tphi= coordFunc(xv)
        else:
            tR, tvR, tvT, tz, tvz, tphi= xv[0],xv[1],xv[2],xv[3],xv[4],xv[5]
        tjr,tlz,tjz,tOr,tOphi,tOz,tar,taphi,taz\
            = aA.actionsFreqsAngles(tR,tvR,tvT,tz,tvz,tphi,maxn=3)
        xv[ii]-= dxv[ii]
        angleIndx= 3
        if actionsFreqsAngles:
            jac[0,ii]= (tjr-jr)/dxv[ii]
            jac[1,ii]= (tlz-lz)/dxv[ii]
            jac[2,ii]= (tjz-jz)/dxv[ii]
            jac[3,ii]= (tOr-Or)/dxv[ii]
            jac[4,ii]= (tOphi-Ophi)/dxv[ii]
            jac[5,ii]= (tOz-Oz)/dxv[ii]           
            angleIndx= 6
        elif freqs:
            jac[0,ii]= (tOr-Or)/dxv[ii]
            jac[1,ii]= (tOphi-Ophi)/dxv[ii]
            jac[2,ii]= (tOz-Oz)/dxv[ii]
        else:        
            jac[0,ii]= (tjr-jr)/dxv[ii]
            jac[1,ii]= (tlz-lz)/dxv[ii]
            jac[2,ii]= (tjz-jz)/dxv[ii]
        if dOdJ:
            jac2[0,ii]= (tOr-Or)/dxv[ii]
            jac2[1,ii]= (tOphi-Ophi)/dxv[ii]
            jac2[2,ii]= (tOz-Oz)/dxv[ii]
        #For the angles, make sure we do not hit a turning point
        if tar-ar > numpy.pi:
            jac[angleIndx,ii]= (tar-ar-2.*numpy.pi)/dxv[ii]
        elif tar-ar < -numpy.pi:
            jac[angleIndx,ii]= (tar-ar+2.*numpy.pi)/dxv[ii]
        else:
            jac[angleIndx,ii]= (tar-ar)/dxv[ii]
        if taphi-aphi > numpy.pi:
            jac[angleIndx+1,ii]= (taphi-aphi-2.*numpy.pi)/dxv[ii]
        elif taphi-aphi < -numpy.pi:
            jac[angleIndx+1,ii]= (taphi-aphi+2.*numpy.pi)/dxv[ii]
        else:
            jac[angleIndx+1,ii]= (taphi-aphi)/dxv[ii]
        if taz-az > numpy.pi:
            jac[angleIndx+2,ii]= (taz-az-2.*numpy.pi)/dxv[ii]
        if taz-az < -numpy.pi:
            jac[angleIndx+2,ii]= (taz-az+2.*numpy.pi)/dxv[ii]
        else:
            jac[angleIndx+2,ii]= (taz-az)/dxv[ii]
    if dOdJ:
        jac2[3,:]= jac[3,:]
        jac2[4,:]= jac[4,:]
        jac2[5,:]= jac[5,:]
        jac= numpy.dot(jac2,numpy.linalg.inv(jac))[0:3,0:3]
    return jac

def lbCoordFunc(xv,Vnorm,Rnorm,R0,Zsun,vsun):
    #Input is (l,b,D,vlos,pmll,pmbb) in (deg,deg,kpc,km/s,mas/yr,mas/yr)
    X,Y,Z= bovy_coords.lbd_to_XYZ(xv[0],xv[1],xv[2],degree=True)
    R,phi,Z= bovy_coords.XYZ_to_galcencyl(X,Y,Z,
                                          Xsun=R0,Ysun=0.,Zsun=Zsun)
    vx,vy,vz= bovy_coords.vrpmllpmbb_to_vxvyvz(xv[3],xv[4],xv[5],
                                               X,Y,Z,XYZ=True)
    vR,vT,vZ= bovy_coords.vxvyvz_to_galcencyl(vx,vy,vz,R,phi,Z,galcen=True,
                                              vsun=vsun)
    R/= Rnorm
    Z/= Rnorm
    vR/= Vnorm
    vT/= Vnorm
    vZ/= Vnorm
    return (R,vR,vT,Z,vZ,phi)
