import math, os
import numpy as N
import libstempo

from libstempo import GWB

day = 24 * 3600
year = 365.25 * day
DMk = 4.15e3           # Units MHz^2 cm^3 pc sec

def add_gwb(psr,dist=1,ngw=1000,seed=None,flow=1e-8,fhigh=1e-5,gwAmp=1e-20,alpha=-0.66,logspacing=True):
    """Add a stochastic background from inspiraling binaries, using the tempo2
    code that underlies the GWbkgrd plugin.

    Here 'dist' is the pulsar distance [in kpc]; 'ngw' is the number of binaries,
    'seed' (a negative integer) reseeds the GWbkgrd pseudorandom-number-generator,
    'flow' and 'fhigh' [Hz] determine the background band, 'gwAmp' and 'alpha'
    determine its amplitude and exponent, and setting 'logspacing' to False
    will use linear spacing for the individual sources.

    It is also possible to create a background object with

    gwb = GWB(ngw,seed,flow,fhigh,gwAmp,alpha,logspacing)

    then call the method gwb.add_gwb(pulsar[i],dist) repeatedly to get a
    consistent background for multiple pulsars.

    Returns the GWB object
    """
    

    gwb = GWB(ngw,seed,flow,fhigh,gwAmp,alpha,logspacing)
    gwb.add_gwb(psr,dist)

    return gwb

def add_dipole_gwb(psr,dist=1,ngw=1000,seed=None,flow=1e-8,fhigh=1e-5,gwAmp=1e-20, alpha=-0.66, \
        logspacing=True, dipoleamps=None, dipoledir=None, dipolemag=None):
        
    """Add a stochastic background from inspiraling binaries distributed
    according to a pure dipole distribution, using the tempo2
    code that underlies the GWdipolebkgrd plugin.

    The basic use is identical to that of 'add_gwb':
    Here 'dist' is the pulsar distance [in kpc]; 'ngw' is the number of binaries,
    'seed' (a negative integer) reseeds the GWbkgrd pseudorandom-number-generator,
    'flow' and 'fhigh' [Hz] determine the background band, 'gwAmp' and 'alpha'
    determine its amplitude and exponent, and setting 'logspacing' to False
    will use linear spacing for the individual sources.

    Additionally, the dipole component can be specified by using one of two
    methods:
    1) Specify the dipole direction as three dipole amplitudes, in the vector
    dipoleamps
    2) Specify the direction of the dipole as a magnitude dipolemag, and a vector
    dipoledir=[dipolephi, dipoletheta]

    It is also possible to create a background object with
    
    gwb = GWB(ngw,seed,flow,fhigh,gwAmp,alpha,logspacing)

    then call the method gwb.add_gwb(pulsar[i],dist) repeatedly to get a
    consistent background for multiple pulsars.
    
    Returns the GWB object
    """

    gwb = GWB(ngw,seed,flow,fhigh,gwAmp,alpha,logspacing,dipoleamps,dipoledir,dipolemag)
    gwb.add_gwb(psr,dist)
    
    return gwb

def _geti(x,i):
    return x[i] if isinstance(x,(tuple,list,N.ndarray)) else x

def fakepulsar(parfile,obstimes,toaerr,freq=1440.0,observatory='AXIS',flags=''):
    """Returns a libstempo tempopulsar object corresponding to a noiseless set
    of observations for the pulsar specified in 'parfile', with observations
    happening at times (MJD) given in the array (or list) 'obstimes', with
    measurement errors given by toaerr (us).

    A new timfile can then be saved with pulsar.savetim(). Re the other parameters:
    - 'toaerr' needs to be either a common error, or a list of errors
       of the same length of 'obstimes';
    - 'freq' can be either a common observation frequency in MHz, or a list;
       it defaults to 1440;
    - 'observatory' can be either a common observatory name, or a list;
       it defaults to the IPTA MDC 'AXIS';
    - 'flags' can be a string (such as '-sys EFF.EBPP.1360') or a list of strings;
       it defaults to an empty string."""

    import tempfile
    outfile = tempfile.NamedTemporaryFile(delete=False)

    outfile.write('FORMAT 1\n')
    outfile.write('MODE 1\n')

    obsname = 'fake_' + os.path.basename(parfile)
    if obsname[-4:] == '.par':
        obsname = obsname[:-4]

    for i,t in enumerate(obstimes):
        outfile.write('{0} {1} {2} {3} {4} {5}\n'.format(
            obsname,_geti(freq,i),t,_geti(toaerr,i),_geti(observatory,i),_geti(flags,i)
        ))

    timfile = outfile.name
    outfile.close()

    pulsar = libstempo.tempopulsar(parfile,timfile,dofit=False)
    pulsar.stoas[:] -= pulsar.residuals(updatebats=False) / 86400.0

    os.remove(timfile)

    return pulsar

def make_ideal(psr):
    """Adjust the TOAs so that the residuals to zero, then refit."""
    
    psr.stoas[:] -= psr.residuals() / 86400.0
    psr.fit()

def add_efac(psr,efac=1.0,seed=None):
    """Add nominal TOA errors, multiplied by `efac` factor.
    Optionally take a pseudorandom-number-generator seed."""
    
    if seed is not None:
        N.random.seed(seed)

    psr.stoas[:] += efac * psr.toaerrs * (1e-6 / day) * N.random.randn(psr.nobs)

def add_equad(psr,equad,seed=None):
    """Add quadrature noise of rms `equad` [s].
    Optionally take a pseudorandom-number-generator seed."""

    if seed is not None:
        N.random.seed(seed)
    
    psr.stoas[:] += (equad / day) * N.random.randn(psr.nobs)

def quantize(times,dt=1):
    bins    = N.arange(N.min(times),N.max(times)+dt,dt)
    indices = N.digitize(times,bins) # indices are labeled by "right edge"
    counts  = N.bincount(indices,minlength=len(bins)+1)

    bign, smalln = len(times), N.sum(counts > 0)

    t = N.zeros(smalln,'d')
    U = N.zeros((bign,smalln),'d')

    j = 0
    for i,c in enumerate(counts):
        if c > 0:
            U[indices == i,j] = 1
            t[j] = N.mean(times[indices == i])
            j = j + 1
    
    return t, U

def quantize_fast(times,dt=1):
    isort = N.argsort(times)
    
    bucket_ref = [times[isort[0]]]
    bucket_ind = [[isort[0]]]
    
    for i in isort[1:]:
        if times[i] - bucket_ref[-1] < dt:
            bucket_ind[-1].append(i)
        else:
            bucket_ref.append(times[i])
            bucket_ind.append([i])
    
    t = N.array([N.mean(times[l]) for l in bucket_ind],'d')
    
    U = N.zeros((len(times),len(bucket_ind)),'d')
    for i,l in enumerate(bucket_ind):
        U[l,i] = 1
    
    return t, U

# check that the two versions match
# t, U = quantize(N.array(psr.toas(),'d'),dt=1)
# t2, U2 = quantize_fast(N.array(psr.toas(),'d'),dt=1)
# print N.sum((t - t2)**2), N.all(U == U2)

def add_jitter(psr,equad,coarsegrain=0.1,seed=None):
    """Add correlated quadrature noise of rms `equad` [s],
    with coarse-graining time `coarsegrain` [days].
    Optionally take a pseudorandom-number-generator seed."""
    
    if seed is not None:
        N.random.seed(seed)

    t, U = quantize_fast(N.array(psr.toas(),'d'),0.1)
    psr.stoas[:] += (equad / day) * N.dot(U,N.random.randn(U.shape[1]))

def add_rednoise(psr,A,gamma,components=10,seed=None):
    """Add red noise with P(f) = A^2 / (12 pi^2) (f year)^-gamma,
    using `components` Fourier bases.
    Optionally take a pseudorandom-number-generator seed."""

    if seed is not None:
        N.random.seed(seed)
    
    t = psr.toas()
    minx, maxx = N.min(t), N.max(t)
    x = (t - minx) / (maxx - minx)
    T = (day/year) * (maxx - minx)

    size = 2*components
    F = N.zeros((psr.nobs,size),'d')
    f = N.zeros(size,'d')

    for i in range(components):
        F[:,2*i]   = N.cos(2*math.pi*(i+1)*x)
        F[:,2*i+1] = N.sin(2*math.pi*(i+1)*x)

        f[2*i] = f[2*i+1] = (i+1) / T

    norm = A**2 * year**2 / (12 * math.pi**2 * T)
    prior = norm * f**(-gamma)
    
    y = N.sqrt(prior) * N.random.randn(size)
    psr.stoas[:] += (1.0/day) * N.dot(F,y)

def add_dm(psr,A,gamma,components=10,seed=None):
    """Add DM variations with P(f) = A^2 / (12 pi^2) (f year)^-gamma,
    using `components` Fourier bases.
    Optionally take a pseudorandom-number-generator seed."""

    if seed is not None:
        N.random.seed(seed)
    
    t = psr.toas()
    v = DMk / psr.freqs**2

    minx, maxx = N.min(t), N.max(t)
    x = (t - minx) / (maxx - minx)
    T = (day/year) * (maxx - minx)

    size = 2*components
    F = N.zeros((psr.nobs,size),'d')
    f = N.zeros(size,'d')

    for i in range(components):
        F[:,2*i]   = N.cos(2*math.pi*(i+1)*x)
        F[:,2*i+1] = N.sin(2*math.pi*(i+1)*x)

        f[2*i] = f[2*i+1] = (i+1) / T

    norm = A**2 * year**2 / (12 * math.pi**2 * T)
    prior = norm * f**(-gamma)
    
    y = N.sqrt(prior) * N.random.randn(size)
    psr.stoas[:] += (1.0/day) * v * N.dot(F,y)
    
def add_line(psr,f,A,offset=0.5):
    """Add a line of frequency `f` [Hz] and amplitude `A` [s],
    with origin at a fraction `offset` through the dataset."""
    
    t = psr.toas()
    t0 = offset * (N.max(t) - N.min(t))
    sine = A * N.cos(2 * math.pi * f * day * (t - t0))

    psr.stoas[:] += sine / day
