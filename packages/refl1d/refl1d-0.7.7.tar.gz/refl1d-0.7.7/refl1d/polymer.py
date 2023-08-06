# -*- coding: utf-8 -*-
# This program is public domain
# Authors Paul Kienzle, Richard Sheridan
"""
Layer models for polymer systems.

Analytic Self-consistent Field (SCF) Brush profile\ [#Zhulina]_\ [#Karim]_

Analytical Self-consistent Field (SCF) Mushroom Profile\ [#Adamuti-Trache]_

Numerical Self-consistent Field (SCF) End-Tethered Polymer
Profile\ [#Cosgrove]_\ [#deVos]_\ [#Sheridan]_


.. [#Zhulina] Zhulina, EB; Borisov, OV; Pryamitsyn, VA; Birshtein, TM (1991)
    "Coil-Globule Type Transitions in Polymers. 1. Collapse of Layers
    of Grafted Polymer Chains", Macromolecules 24, 140-149.

.. [#Karim] Karim, A; Douglas, JF; Horkay, F; Fetters, LJ; Satija, SK (1996)
    "Comparative swelling of gels and polymer brush layers",
    Physica B 221, 331-336. doi:10.1016/0921-4526(95)00946-9
   
.. [#Adamuti-Trache] Adamuţi-Trache, M., McMullen, W. E. & Douglas, J. F.
    Segmental concentration profiles of end-tethered polymers with
    excluded-volume and surface interactions. J. Chem. Phys. 105, 4798 (1996).

.. [#Cosgrove] Cosgrove, T., Heath, T., Van Lent, B., Leermakers, F. A. M., 
    & Scheutjens, J. M. H. M. (1987). Configuration of terminally attached 
    chains at the solid/solvent interface: self-consistent field theory and 
    a Monte Carlo model. Macromolecules, 20(7), 1692–1696. 
    doi:10.1021/ma00173a041
    
.. [#deVos] De Vos, W. M., & Leermakers, F. A. M. (2009). Modeling the 
    structure of a polydisperse polymer brush. Polymer, 50(1), 305–316. 
    doi:10.1016/j.polymer.2008.10.025
    
.. [#Sheridan] Sheridan, R. J., Beers, K. L., et. al (2014). Direct observation
    of "surface theta" conditions. [in prep]

..  [#Vincent] Vincent, B., Edwards, J., Emmett, S., & Croot, R. (1988).
    Phase separation in dispersions of weakly-interacting particles in
    solutions of non-adsorbing polymer. Colloids and Surfaces, 31, 267–298.
    doi:10.1016/0166-6622(88)80200-2

"""

from __future__ import division

__all__ = ["PolymerBrush","PolymerMushroom","EndTetheredPolymer","VolumeProfile","layer_thickness"]

import inspect
import time

import numpy as np

from bumps.parameter import Parameter
from .model import Layer
from . import util
from time import time

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict
    
from numpy import real, imag, exp, sqrt, pi, hstack, ones_like, fabs

# This is okay to use as long as LAMBDA_ARRAY is symmetric,
# otherwise a slice LAMBDA_ARRAY[::-1] is necessary
from numpy.core.multiarray import correlate as raw_convolve

from numpy.core import add
addred = add.reduce
def norm(x): return sqrt(addred(x*x))

LAMBDA_1 = np.float64(1.0)/6.0 #always assume cubic lattice (1/6) for now
LAMBDA_0 = 1.0-2.0*LAMBDA_1
LAMBDA_ARRAY = np.asarray([LAMBDA_1,LAMBDA_0,LAMBDA_1])
MINLAT = 35
SQRT_PI=sqrt(pi)

class PolymerBrush(Layer):
    r"""
    Polymer brushes in a solvent

    :Parameters:
        *thickness* 
            the thickness of the solvent layer
        *interface* 
            the roughness of the solvent surface
        *polymer* 
            the polymer material
        *solvent* 
            the solvent material or vacuum
        *base_vf* 
            volume fraction (%) of the polymer brush at the interface
        *base* 
            the thickness of the brush interface (A)
        *length* 
            the length of the brush above the interface (A)
        *power* 
            the rate of brush thinning
        *sigma* 
            rms brush roughness (A)

    The materials can either use the scattering length density directly,
    such as PDMS = SLD(0.063, 0.00006) or they can use chemical composition
    and material density such as PDMS=Material("C2H6OSi",density=0.965).

    These parameters combine in the following profile formula:

    .. math::

        V(z) &= \left\{
          \begin{array}{ll}
            V_o                        & \mbox{if } z <= z_o \\
            V_o (1 - ((z-z_o)/L)^2)^p  & \mbox{if } z_o < z < z_o + L \\
            0                          & \mbox{if } z >= z_o + L
          \end{array}
        \right. \\
        V_\sigma(z)
           &= V(z) \star
                 \frac{e^{-\frac{1}{2}(z/\sigma)^2}}{\sqrt{2\pi\sigma^2}} \\
        \rho(z) &= \rho_p V_\sigma(z) + \rho_s (1-V_\sigma(z))

    where $V_\sigma(z)$ is volume fraction convoluted with brush
    roughness $\sigma$ and $\rho(z)$ is the complex scattering
    length density of the profile.
    """
    def __init__(self, thickness=0, interface=0, name="brush",
                 polymer=None, solvent=None, base_vf=None,
                 base=None, length=None, power=None, sigma=None):
        self.thickness = Parameter.default(thickness, name="brush thickness")
        self.interface = Parameter.default(interface, name="brush interface")
        self.base_vf = Parameter.default(base_vf, name="base_vf")
        self.base = Parameter.default(base, name="base")
        self.length = Parameter.default(length, name="length")
        self.power = Parameter.default(power, name="power")
        self.sigma = Parameter.default(sigma, name="sigma")
        self.solvent = solvent
        self.polymer = polymer
        self.name = name
        # Constraints:
        #   base_vf in [0,1]
        #   base,length,sigma,thickness,interface>0
        #   base+length+3*sigma <= thickness
    def parameters(self):
        return {'solvent':self.solvent.parameters(),
                'polymer':self.polymer.parameters(),
                'base_vf':self.base_vf,
                'base':self.base,
                'length':self.length,
                'power':self.power,
                'sigma':self.sigma,
                }
                
    def profile(self, z):
        base_vf, base, length, power, sigma \
            = [p.value for p in (self.base_vf, self.base,
               self.length, self.power, self.sigma)]
        base_vf /= 100. # % to fraction
        L0 = base  # if base < thickness else thickness
        L1 = base+length # if base+length < thickness else thickness-L0
        if length == 0:
            v = np.ones_like(z)
        else:
            v = (1 - ((z-L0)/(L1-L0))**2)
        v[z<L0] = 1
        v[z>L1] = 0
        brush_profile = base_vf * v**power
        # TODO: we could use Nevot-Croce rather than smearing the profile
        vf = smear(z, brush_profile, sigma)
        return vf

    def render(self, probe, slabs):
        thickness = self.thickness.value
        Pw,Pz = slabs.microslabs(thickness)
        # Skip layer if it falls to zero thickness.  This may lead to
        # problems in the fitter, since R(thickness) is non-differentiable
        # at thickness = 0.  "Clip to boundary" range handling will at
        # least allow this point to be found.
        # TODO: consider using this behaviour on all layer types.
        if len(Pw) == 0: return

        Mr,Mi = self.polymer.sld(probe)
        Sr,Si = self.solvent.sld(probe)
        M = Mr + 1j*Mi
        S = Sr + 1j*Si
        try: M,S = M[0],S[0]  # Temporary hack
        except: pass

        vf = self.profile(Pz)
        Pw,vf = util.merge_ends(Pw, vf, tol=1e-3)
        P = M*vf + S*(1-vf)
        Pr, Pi = real(P), imag(P)
        slabs.extend(rho=[Pr], irho=[Pi], w=Pw)

def layer_thickness(z):
    """
    Return the thickness of a layer given the microslab z points.

    The z points are at the centers of the bins.  we can use the recurrence
    that boundary b[k] = z[k-1] + (z[k-1] - b[k-1]) to compute the
    total length of the layer.
    """
    return 2 * (np.sum(z[-1::-2]) - np.sum(z[-2::-2]))

class VolumeProfile(Layer):
    """
    Generic volume profile function

    :Parameters:

        *thickness* 
            the thickness of the solvent layer
        *interface* 
            the roughness of the solvent surface
        *material* 
            the polymer material
        *solvent* 
            the solvent material
        *profile* 
            the profile function, suitably parameterized

    The materials can either use the scattering length density directly,
    such as PDMS = SLD(0.063, 0.00006) or they can use chemical composition
    and material density such as PDMS=Material("C2H6OSi",density=0.965).

    These parameters combine in the following profile formula::

        sld = material.sld * profile + solvent.sld * (1 - profile)

    The profile function takes a depth z and returns a density rho.

    For volume profiles, the returned rho should be the volume fraction
    of the material.  For SLD profiles, rho should be complex scattering
    length density of the material.

    Fitting parameters are the available named arguments to the function.
    The first argument must be *z*, which is the array of depths at which
    the profile is to be evaluated.  It is guaranteed to be increasing, with
    step size 2*z[0].

    Initial values for the function parameters can be given using name=value.
    These values can be scalars or fitting parameters.  The function will
    be called with the current parameter values as arguments.  The layer
    thickness can be computed as :func: `layer_thickness`.

    """
    # TODO: test that thickness(z) matches the thickness of the layer
    def __init__(self, thickness=0, interface=0, name="VolumeProfile",
                 material=None, solvent=None, profile=None, **kw):
        if interface != 0: raise NotImplementedError("interface not yet supported")
        if profile is None or material is None or solvent is None:
            raise TypeError("Need polymer, solvent and profile")
        self.name = name
        self.thickness = Parameter.default(thickness, name="solvent thickness")
        self.interface = Parameter.default(interface, name="solvent interface")
        self.profile = profile
        self.solvent = solvent
        self.material = material

        # Query profile function for the list of arguments
        vars = inspect.getargspec(profile)[0]
        #print "vars",vars
        if inspect.ismethod(profile): vars = vars[1:]  # Chop self
        vars = vars[1:]  # Chop z
        #print vars
        unused = [k for k in kw.keys() if k not in vars]
        if len(unused) > 0:
            raise TypeError("Profile got unexpected keyword argument '%s'"%unused[0])
        dups = [k for k in vars
                if k in ('thickness','interface','polymer','solvent','profile')]
        if len(dups) > 0:
            raise TypeError("Profile has conflicting argument '%s'"%dups[0])
        for k in vars: kw.setdefault(k,0)
        for k,v in kw.items():
            setattr(self,k,Parameter.default(v,name=k))

        self._parameters = vars

    def parameters(self):
        P = {'solvent':self.solvent.parameters(),
             'material':self.material.parameters(),
             }
        for k in self._parameters:
            P[k] = getattr(self,k)
        return P

    def render(self, probe, slabs):
        Mr,Mi = self.material.sld(probe)
        Sr,Si = self.solvent.sld(probe)
        M = Mr + 1j*Mi
        S = Sr + 1j*Si
        #M,S = M[0],S[0]  # Temporary hack
        Pw,Pz = slabs.microslabs(self.thickness.value)
        if len(Pw)== 0: return
        kw = dict((k,getattr(self,k).value) for k in self._parameters)
        #print kw
        phi = self.profile(Pz,**kw)
        try:
            if phi.shape != Pz.shape: raise Exception
        except:
            raise TypeError("profile function '%s' did not return array phi(z)"
                            %self.profile.__name__)
        Pw,phi = util.merge_ends(Pw, phi, tol=1e-3)
        P = M*phi + S*(1-phi)
        slabs.extend(rho = [real(P)], irho = [imag(P)], w = Pw)
        #slabs.interface(self.interface.value)


def smear(z, P, sigma):
    """
    Gaussian smearing

    :Parameters:
        *z* | vector
            equally spaced sample times
        *P* | vector
            sample values
        *sigma* | real
            root-mean-squared convolution width
    :Returns:
        *Ps* | vector
            smeared sample values
    """
    if len(z) < 3: return P
    dz = z[1]-z[0]
    if 3*sigma < dz: return P
    w = int(3*sigma/dz)
    G = exp(-0.5*(np.arange(-w,w+1)*(dz/sigma))**2)
    full = np.hstack( ([P[0]]*w, P, [P[-1]]*w) )
    return np.convolve(full,G/np.sum(G),'valid')

class PolymerMushroom(Layer):
    """ 
    Polymer mushrooms in a solvent (volume profile)

    :Parameters:
        *delta* | real scalar
            interaction parameter
        *vf* | real scalar
            not quite volume fraction (dimensionless grafting density)
        *sigma* | real scalar
            convolution roughness (A)
    
    Using analytical SCF methods for gaussian chains, which are scaled
    by the radius of gyration of the equivalent free polymer as an 
    approximation to results of renormalization group methods.\ [#Adamuti-Trache]_
    
    Solutions are only strictly valid for vf << 1. 
    """
    
    def __init__(self, thickness=0, interface=0, name="shroom",
                 polymer=None, solvent=None, sigma=0,
                 vf=0, delta=0):
        self.thickness = Parameter.default(thickness, name="shroom thickness")
        self.interface = Parameter.default(interface, name="shroom interface")
        self.delta = Parameter.default(delta, name="delta")
        self.vf = Parameter.default(vf, name="vf")
        self.sigma = Parameter.default(sigma, name="sigma")
        self.solvent = solvent
        self.polymer = polymer
        self.name = name
    def parameters(self):
        return {'solvent':self.solvent.parameters(),
                'polymer':self.polymer.parameters(),
                'delta':self.delta,
                'vf':self.vf,
                'sigma':self.sigma,
                'thickness':self.thickness,
                'interface':self.interface
                }
                
    def profile(self, z):
        delta, sigma, vf, thickness \
            = [p.value for p in self.delta, self.sigma, self.vf, self.thickness]

        return smear(z, MushroomProfile(z, delta, vf, sigma), sigma)


    def render(self, probe, slabs):
        thickness = self.thickness.value
        Pw,Pz = slabs.microslabs(thickness)
        # Skip layer if it falls to zero thickness.  This may lead to
        # problems in the fitter, since R(thickness) is non-differentiable
        # at thickness = 0.  "Clip to boundary" range handling will at
        # least allow this point to be found.
        # TODO: consider using this behaviour on all layer types.
        if len(Pw) == 0: return

        Mr,Mi = self.polymer.sld(probe)
        Sr,Si = self.solvent.sld(probe)
        M = Mr + 1j*Mi
        S = Sr + 1j*Si
        try: M,S = M[0],S[0]  # Temporary hack
        except: pass

        phi = self.profile(Pz)
        Pw,phi = util.merge_ends(Pw, phi, tol=1e-3)
        P = M*phi + S*(1-phi)
        Pr, Pi = np.real(P), np.imag(P)
        slabs.extend(rho=[Pr], irho=[Pi], w=Pw)

def MushroomProfile(z, delta=0.1, vf=1.0, sigma=1.0):
    thickness = layer_thickness(z)
    thresh=1e-10
    
    base = 3.0*sigma # tail is erf, capture 95% of the mixing
    Rg = (thickness-base) / 4.0 # profile ends by ~4 RG, so we can tether these
    keep = (z-base) >= 0.0    
    x = (z[keep] - base) / Rg
    
    """
    mushroom_profile_math has a divide by zero problem at delta=0.
    Fix it by weighted average of the profile above and below a threshold.
    No visual difference when delta is between +-0.001, and there's no
    floating point error until ~+-1e-14.
    """
    
    if fabs(delta) > thresh:
        mushroom_profile = mushroom_math(x,delta,vf)
    else: # we should RARELY get here
        scale = (delta+thresh)/2.0/thresh             
        mushroom_profile = (scale*mushroom_math(x,thresh,vf) 
                            + (1.0-scale)*mushroom_math(x,-thresh,vf))

    try:
        # make the base connect with the profile
        zextra = z[np.logical_not(keep)]
        base_profile = ones_like(zextra)*mushroom_profile[0]
    except IndexError:
        base_profile = ones_like(z)*mushroom_profile[0]
        
    return hstack((base_profile, mushroom_profile))

def mushroom_math(x,delta=.1,vf=.1):
    """
    new method, rewrite for numerical stability at high delta
    delta=0 causes divide by zero error!! Compensate elsewhere.
    http://ab-initio.mit.edu/wiki/index.php/Faddeeva_Package
    """
    
    from scipy.special import erfc, erfcx
    
    x_half=x/2.0
    delta_double=2.0*delta
    return (
            (
             erfc(x_half) 
             -erfcx(delta_double+x_half)/exp(x_half*x_half)
             -erfc(x)
             + (
                (.25-delta*(x+delta_double))*erfcx(delta_double+x)
                + delta/SQRT_PI
               ) * 4.0 / exp(x*x)
            ) * vf / (delta_double * erfcx(delta_double))
           )

class EndTetheredPolymer(Layer):
    r"""
    Polymer end-tethered to an interface in a solvent
    
    Uses a numerical self-consistent field profile.\ [#Cosgrove]_\ [#deVos]_\ [#Sheridan]_
    
    **Parameters**
    
        :*chi*:
            solvent interaction parameter
        :*chi_s*:
            surface interaction parameter
        :*h_dry*:
            thickness of the neat polymer layer
        :*l_lat*:
            real length per lattice site
        :*mn*:
            Number average molecular weight
        :*m_lat*:
            real mass per lattice segment
        :*pdi*:
            Dispersity (Polydispersity index)
        :*thickness*:
            Slab thickness should be greater than the contour 
            length of the polymer
        :*interface*:
            should be zero
        :*material*:
            the polymer material
        :*solvent*:
            the solvent material
    
    Previous layer should not have roughness! Use a spline to simulate it. 
    You can put this material in the *above* slot of :class:`refl1d.freeform.FreeLayer`.
    
    According to [#Vincent]_, $l_\rm{lat}$ and $m_\rm{lat}$ should be
    calculated by the formulas:

    .. math::
    
        l_{\rm{lat}} &=& \frac{a^2 m/l}{p_l} \\
        m_{\rm{lat}} &=& \frac{(a m/l)^2}{p_l}
    
    where $l$ is the real polymer's bond length, $m$ is the real segment mass,
    and $a$ is the proportionality constant between molecular weight and radius
    of gyration at theta conditions. The lattice persistence, $p_l$, is:

    .. math::
    
        p_l = \frac16 \frac{1+1/Z}{1-1/Z}
    
    with coordination number $Z = 6$ for a cubic lattice, $p_l = .233$.
    """
    
    def __init__(self, thickness=0, interface=0, name="EndTetheredPolymer",
                 polymer=None, solvent=None, chi=0, chi_s=0, h_dry=None, 
                 l_lat=1, mn=None, m_lat=1, pdi=1):
        if interface != 0: raise NotImplementedError("interface not yet supported")
        if polymer is None or solvent is None or h_dry is None or mn is None:
            raise TypeError("Need polymer, solvent and profile")
        
        self.thickness = Parameter.default(thickness, name="SCF thickness")
        self.interface = Parameter.default(interface, name="SCF interface")
        self.chi   = Parameter.default(chi, name="chi")
        self.chi_s = Parameter.default(chi_s, name="surface chi")
        self.h_dry = Parameter.default(h_dry, name="dry thickness")
        self.l_lat = Parameter.default(l_lat, name="lattice layer length")
        self.mn    = Parameter.default(mn, name="Num. Avg. MW")
        self.m_lat = Parameter.default(m_lat, name="lattice segment mass")
        self.pdi   = Parameter.default(pdi, name="Dispersity")
        self.phi_prev = None
        self.solvent = solvent
        self.polymer = polymer
        self.name = name
        
    def parameters(self):
        return {'solvent':self.solvent.parameters(),
                'polymer':self.polymer.parameters(),
                'chi':self.chi,
                'chi_s':self.chi_s,
                'h_dry':self.h_dry,
                'l_lat':self.l_lat,
                'mn':self.mn,
                'm_lat':self.m_lat,
                'pdi':self.pdi,
                'thickness':self.thickness,
                'interface':self.interface
                }
                
    def profile(self, z):
        SCFparams = dict(chi=self.chi.value, chi_s=self.chi_s.value, 
             h_dry=self.h_dry.value,l_lat=self.l_lat.value, mn=self.mn.value, 
             m_lat=self.m_lat.value, pdi=self.pdi.value)
        # If the SCF parameters are exactly equal to the ones that generated
        # the previous solution, just return the previous solution
        if (self.prev['params'] == SCFparams 
            and np.array_equal(z,self.prev['z'])):
                return self.prev['phi']
            
        phi = SCFprofile(z, **SCFparams)
                
        # Save copy of phi so it doesn't mutate unexpectedly
        self.prev['phi'] = phi.copy()
        self.prev['z'] = z
        self.prev['params'] = SCFparams
        return phi

    def render(self, probe, slabs):
        thickness = self.thickness.value
        Pw,Pz = slabs.microslabs(thickness)
        # Skip layer if it falls to zero thickness.  This may lead to
        # problems in the fitter, since R(thickness) is non-differentiable
        # at thickness = 0.  "Clip to boundary" range handling will at
        # least allow this point to be found.
        # TODO: consider using this behaviour on all layer types.
        if len(Pw) == 0: return

        Mr,Mi = self.polymer.sld(probe)
        Sr,Si = self.solvent.sld(probe)
        M = Mr + 1j*Mi
        S = Sr + 1j*Si
        try: M,S = M[0],S[0]  # Temporary hack
        except: pass

        phi = self.profile(Pz)
        Pw,phi = util.merge_ends(Pw, phi, tol=1e-3)
        P = M*phi + S*(1-phi)
        Pr, Pi = np.real(P), np.imag(P)
        slabs.extend(rho=[Pr], irho=[Pi], w=Pw)

def SCFprofile(z, chi=None, chi_s=None, h_dry=None, l_lat=1, mn=None, 
               m_lat=1, pdi=1, disp=False):
    """
    Generate volume fraction profile for Refl1D based on real parameters.
    
    The field theory is a lattice-based one, so we need to move between lattice
    and real space. This is done using the parameters l_lat and m_lat, the 
    lattice size and the mass of a lattice segment, respectivley. We use h_dry
    (dry thickness) as a convenient measure of surface coverage, along with mn
    (number average molecular weight) as the real inputs.
    
    Make sure your inputs for h_dry/l_lat and mn/m_lat match dimensions! 
    Angstroms and daltons are good choices.
    
    This function is suitable for use as a VolumeProfile, as well as the 
    default EndTetheredPolymer class.
    """
    
    # calculate lattice space parameters    
    theta = h_dry/l_lat
    r = int(mn/m_lat-.5)
    
    # pull an inital guess out of the cache    
    phi0 = phi0_cache(chi,chi_s,pdi,theta,r,disp)

    # solve the self consistent field equations    
    phi_lat = SCFsolve(chi,chi_s,pdi,theta,r,disp,phi0)
    if disp: print "lattice segments: ", r
    
    # re-dimensionalize the solution
    layers = len(phi_lat)
    z_end = l_lat*(layers+.5)
    keep = z<=z_end
    z_lat = np.linspace(l_lat/2,z_end,num=layers)
    phi = np.interp(z[keep],z_lat,phi_lat)

    # fill in the end with zeros
    zextra = z[np.logical_not(keep)]
    
    return hstack((phi,np.zeros_like(zextra)))
    

def phi0_cache(chi,chi_s,pdi,theta,r,disp=False,cache=OrderedDict()):
    """
    Scale and round the parameters, then return a memoized result.
    
    Using an OrderedDict (because I want to prune keys FIFO)
    """
    # prime the cache with a known easy solution
    if not cache: 
        cache[(0,0,0,1,.1)] = SCFsolve(theta=10,r=100)
        
    # Try to keep the parameters between 0 and 1. Factors are arbitrary.
    scaled_parameters = (chi,chi_s*3,pdi-1,theta/r*10,r/1000)
    
    # round them to a reasonable number of digits
    rounded_parameters = tuple(round(p,3) for p in scaled_parameters)
    
    if rounded_parameters in cache:
        return cache[rounded_parameters]
    
    # On a miss, generate the result by walking from the closest in cache
    
    # Numpy setup
    rp_array = np.asarray(rounded_parameters)
    cp = cache.keys()
    cp_array = np.asarray(cp)
    
    # Calculate "nearest" cached solution
    deltas = rp_array - cp_array # Parameter space displacement vectors
    norms = sqrt(addred(deltas*deltas,axis=1)) # and their magnitudes
    closest_index = norms.argmin()
    
    # Organize closest point data for later use
    closest_delta = deltas[closest_index]
    closest_cp = cp[closest_index]
    closest_cp_array = np.asarray(closest_cp)
    phi0 = cache[closest_cp]
    
    """
    We must walk from the previously cached point to the desired region.
    This is goes from step=0 (cached) and step=1 (finish), where the step=0
    is implicit above. We try the full step first, so that this function only
    calls SCFsolve one extra time during normal cache misses.
    
    The solver may not converge if the step size is too big. In that case,
    we retry with half the step size. This should find the edge of the basin
    of attraction for the solution eventually. On successful steps we increase
    stepsize slightly to accelerate after getting stuck.
    """
    
    step = 1.0 # Fractional distance between cached and requested
    dstep = 1.0 # Step size increment
    flag = True
    while flag:
        
        if step >= 1.0: # end on 1.0 exactly every time
            step = 1.0
            flag = False

        current_p = closest_cp_array + step*closest_delta
        p_tup = tuple(round(p,3) for p in current_p)

        # between adaptive stepping and rounding, it's not obvious if each
        # step is cached, so checking is probably cheaper than try/except
        if p_tup in cache:
            phi0 = cache[p_tup]
            dstep *= 1.05
            step += dstep
        else:
            parameters = (p_tup[0], p_tup[1]*(1/3), p_tup[2]+1, 
                          p_tup[3]*p_tup[4]*100, p_tup[4]*1000)
            try:
                phi0 = SCFsolve(*parameters,phi0=phi0,disp=disp)
                cache[p_tup] = phi0
                dstep *= 1.05
                step += dstep
            except RuntimeError as e:
                if e.message != "solver couldn't converge":
                    raise
                else:
                    flag = True # Reset this so we don't quit if step=1.0 fails
                    dstep *= .5
                    step -= dstep
    
    # keep the cache from consuming all things
    if len(cache)>9000:
        for i in xrange(1000):
            cache.popitem(last=False)
        
    return phi0


def SCFsolve(chi=0,chi_s=0,pdi=1,theta=None,r=None,disp=False,phi0=None):
    """
    Solve SCF equations using an initial guess and lattice parameters
    
    This function checks which special case self consistent field equations
    we are using, evaluates any starting guess against a simple default, then
    finds a solution for the equations where the lattice size is sufficiently
    large.
    
    The Newton-Krylov solver really makes this one. krylov+gmres was faster
    than the other scipy.optimize alternatives by quite a lot.
    """
    
    from scipy.optimize import root
    
    sigma = theta/r

    if sigma >= 1:
        raise ValueError('Chains that short cannot be squeezed that high')

    p_i = SZdist(pdi,r)
    
    starttime = time()
    
    # TODO: Better initial guess for chi>.6t
    default_layers, default_phi0 = default_guess(theta,sigma)

    # Check if default guess is a better guess than input
    using_default_phi0=True
    if phi0 is None:
        phi0 = default_phi0
        layers = default_layers
        if disp: print '\nno guess passed, using default phi0: layers =',layers,'\n'
    else:
        phi0 = fabs(phi0)
        phi0[phi0>1.0] = 1.0
        layers = len(phi0)
        try:
            eps = SCFeqns(phi0,chi,chi_s,sigma,r,p_i)
        except:
            eps = np.inf    
        try:
            default_eps = SCFeqns(default_phi0,chi,chi_s,sigma,r,p_i)
        except:
            default_eps = np.inf
        if norm(eps)/sqrt(layers) > norm(default_eps)/sqrt(default_layers):
            if disp: print "\ndefault phi0 is better: layers =",default_layers,'\n'
            phi0 = default_phi0
        else:
            if disp: print "\npassed phi0 is better: layers =", layers,'\n'
            using_default_phi0=False
    
    jac_solve_method = 'gmres'
    done = False
    tol = 2e-6*theta # We tolerate up to 2ppm of our polymer in the last layer
    ratio = 1.2 # otherwise we grow it by 20%
    # if the loop sees that it can shrink 20%, it will, but it can lead to
    # endless loops. This flag shows if it has grown before, so it knows to
    # quit instead of shrinking
    growing = False
    
    # apparently scope rules dictate that we can change 'layers' without a
    # redefinition of this callback, so i got rid of the one in the while block    
    def callback(x,*args,**kwargs): 
        _proto_callback(x,disp,layers,tol,ratio)
    
    while not done:
        if disp: print "\nSolving SCF equation set..."
        
        try:
            layers=len(phi0)
            result = root(
                SCFeqns,phi0,args=(chi,chi_s,sigma,r,p_i),
                method='Krylov',callback=callback,
                options={'disp':bool(disp),'maxiter':20,
                         'jac_options':{'method':jac_solve_method}})
            if disp: 
                print '\nSolver exit code:',result.status,result.message
                
            if result.status == 1:
                phi = fabs(result.x)
            elif result.status == 2:
                if not using_default_phi0:
                    phi0 = default_phi0
                    using_default_phi0 = True
                    continue
                else:
                    raise RuntimeError("solver couldn't converge")
                
        except ShortCircuitError as e:
            growing = False # scrub this flag so we don't quit directly (rare)
            phi = e.x
            if disp: print e
                
        except ValueError as e:
            if e.message == 'array must not contain infs or NaNs':
                if not using_default_phi0:
                    phi0 = default_phi0
                    using_default_phi0 = True
                    continue
                else: 
                    raise RuntimeError("solver couldn't converge")

        except RuntimeError as e:
            if e.message == 'gmres is not re-entrant':
                jac_solve_method = 'lgmres'
                continue
            else:
                raise
            
        if disp: print 'phi(L)/sum(phi) =',phi[-1] / theta * 1e6,'(ppm)\n'
        
        if phi[-1] > tol:
            # if the last layer is beyond tolerance, grow the lattice
            newlayers = max(1,round(layers*(ratio-1)))
            if disp: print 'Growing undersized lattice by', newlayers
            phi0 = np.append(phi,np.linspace(phi[-1],0,num=newlayers))
            growing = True
        elif layers > MINLAT and phi[round(layers/ratio)] < tol:
            # if the layer at 83% of the thickenss is less than the tolerance,
            # we can shrink it, but not if it's already a small lattice, or 
            # if we grew after the last successful call of root()
            if growing:
                done = True
            else:
                if disp: print 'Shrinking undersized lattice...'
                phi0 = phi[:round(layers/ratio)]
        else:
            # otherwise, we are done for real
            done = True
            
    if disp:
        print "execution time:", round(time()-starttime,3), "s"
        print "lattice size:", layers
    
    return phi    

def SZdist(pdi,nn):
    """ Calculate Shultz-Zimm distribution from PDI and number average DP
    
    Shultz-Zimm is a "realistic" distribution for linear polymers. Numerical
    problems arise when the distribution gets too uniform, so if we find them,
    default to an exact uniform calculation.
    """
    
    from scipy.special import gammaln
    
    if pdi == 1.0:
        p_ni = _fzeros(1,nn)
        p_ni[0,-1] = 1
        return p_ni
    elif pdi < 1.0:
        raise ValueError('Invalid PDI')
        
    x = 1.0/(pdi-1.0)
    cutoff = 9000
    
    ni = np.arange(1,cutoff+1,dtype=np.float64)
    r = ni/nn
    
    p_ni = exp(np.log(x/ni) - gammaln(x+1) + x*r*(np.log(x*r)/r-1))
    
    if (p_ni>=1.0).any():
        p_ni = _fzeros(1,nn)
        p_ni[0,-1] = 1
        return p_ni
    
    mysums = np.cumsum(p_ni)
    keep = np.logical_and(np.logical_or(r < 1.0, p_ni >= 1.0e-6), mysums < 1.0)
        
    return p_ni[keep].reshape(1,-1)

def default_guess(theta=1,sigma=.5,chi=0,chi_s=0):
    """ Produce an initial guess for phi via analytical approximants.
    
    For now, a line using numbers from scaling theory
    """
    default_layers = round(max(MINLAT,theta/sqrt(sigma)))
    default_phi0 = np.linspace(sqrt(sigma),0,num=default_layers)
    return default_layers, default_phi0.ravel()
    
class ShortCircuitError(Exception):
    """ Special error to stop root() before a solution is found.
    
    """
    def __init__(self, value,x):
         self.value = value
         self.x = x
    def __str__(self):
         return repr(self.value)
         
def _proto_callback(x,disp,layers,tol,ratio):
    """ Special callback to stop root() before solution is found.
    
    This kills root if the tolerances are exceeded by 4 times the tolerances
    of the lattice resizing loop. This seems to work well empirically to 
    restart the solver when necessary without cutting out of otherwise 
    reasonable solver trajectories.
    """
    if disp: print "Iterating..."
    if x[-1] > 4*tol:
        raise ShortCircuitError('Stopping, lattice too small',x)
    elif layers > MINLAT and x[min(layers-1,round(layers/ratio))] < tol/4:
        raise ShortCircuitError('Stopping, lattice too big',x)

def SCFeqns(phi_z,chi,chi_s,sigma,navgsegments,p_i):
    """ System of SCF equation for terminally attached polymers.
    
        Formatted for input to a nonlinear minimizer or solver.
    """
    
    # let the solver go negative if it wants
    phi_z = fabs(phi_z.ravel())
    
    # attempts to try fields with values greater than one are penalized
    if (phi_z>.99999).any():
        return np.ones_like(phi_z)*1e10
    
    phi_z_0 = 1.0 - phi_z
    
    layers = phi_z.size
    cutoff = p_i.size
    
    # calculate all needed quantities for new g_z
    delta = _fzeros(layers)
    delta[0] = 1.0
    phi_z_avg = calc_phi_z_avg(phi_z)
    
    # calculate new g_z (Boltzmann weighting factors)
    g_z = phi_z_0*exp(2*chi*phi_z_avg + delta*chi_s) #(LAMBDA_1*chi-chi_s))
    
    # normalize g_z for numerical stability
    u = -np.log(g_z)
    uavg = np.mean(u)
    g_z_norm = g_z*exp(uavg)
    
    # calculate weighting factors for terminally attached chains
    g_zs_ta_norm = calc_g_zs(g_z_norm,1,layers,cutoff)
    
    # calculate normalization constants from 1/(single chain partition fn)
    if cutoff == navgsegments:
        c_i_norm = sigma*p_i/addred(g_zs_ta_norm[:,-1]) # shortcut if uniform
    else:
        c_i_norm = sigma*p_i/addred(g_zs_ta_norm,axis=0)
    
    # calculate weighting factors for free chains
    g_zs_free_ngts_norm = calc_g_zs(g_z_norm,c_i_norm,layers,cutoff)
    
    phi_z_new = calc_phi_z(g_zs_ta_norm,g_zs_free_ngts_norm,g_z_norm)
    eps_z = phi_z-phi_z_new
    
    return eps_z

def _fzeros(*args):
    return np.zeros(args,dtype=np.float64,order='F')

def calc_phi_z_avg(phi_z):
    return raw_convolve(phi_z,LAMBDA_ARRAY,1)
    
def calc_phi_z(g_ta,g_free,g_z):
    return addred(g_ta*np.fliplr(g_free),axis=1)/g_z

def calc_g_zs(g_z,c_i,layers,segments):
    from refl1d.calc_g_zs_cex import _calc_g_zs_inner
    
    # initialize
    g_zs=np.empty((layers,segments),dtype=np.float64,order='F')
    
    # choose special case
    if np.size(c_i) == 1:
        # terminally attached chains
        c_i = _fzeros(1,segments)
        g_zs[:,0] = _fzeros(layers)
        g_zs[0,0] = g_z[0]
    else:
        # free chains
        g_zs[:,0] = c_i[0,segments-1]*g_z
    
    # inner loops
    
    # FASTEST: call some custom C code identical to "SLOW" loop
        # beware, this changes g_zs _in_place!_
    _calc_g_zs_inner(g_z,c_i,g_zs,LAMBDA_0,LAMBDA_1,layers,segments)
    
    # FASTER: use the convolve function to partially vectorize  
#    pg_zs=g_zs[:,0]    
#    for r in range(1,segments):
#        pg_zs=g_z*(c_i[0,segments-r-1]+raw_convolve(pg_zs,LAMBDA_ARRAY,1))
#        g_zs[:,r]=pg_zs
    
    # SLOW: loop outright, pulling some slicing out of the innermost loop  
#    pg_zs=g_zs[:,0] 
#    for r in range(1,segments):
#        c=c_i[0,segments-r-1]
#        z=0
#        g_zs[z,r]=(pg_zs[z]*LAMBDA_0+pg_zs[z+1]*LAMBDA_1+c)*g_z[z]
#        for z in range(1,(layers-1)):
#            g_zs[z,r]=(pg_zs[z-1]*LAMBDA_1+pg_zs[z]*LAMBDA_0+pg_zs[z+1]*LAMBDA_1+c)*g_z[z]
#        z=layers-1
#        g_zs[z,r]=(pg_zs[z]*LAMBDA_0+pg_zs[z-1]*LAMBDA_1+c)*g_z[z]
#        pg_zs=g_zs[:,r]
               
    return g_zs
