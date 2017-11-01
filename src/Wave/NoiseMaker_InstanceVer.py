#!python3
import numpy as np
import random
import itertools
#import scipy.signal.sawtooth
try:
    from pyfftw.interfaces.numpy_fft import rfft, irfft       # Performs much better than numpy's fftpack
except ImportError:                                    # Use monkey-patching np.fft perhaps instead?
    from numpy.fft import rfft, irfft
#from .signal import self.__normalize
"""
ノイズを生成する。
Color  Power Power density
--------------------------
White  +3 dB  0 dB
Pink    0 dB -3 dB
Blue   +6 dB +3 dB
Brown  -3 dB -6 dB
Violet +9 dB +6 dB
"""
class NoiseMaker:
    def __init__(self):
        self._noise_generators = {
            'white'  : self.white,
            'pink'   : self.pink,
            'blue'   : self.blue,
            'brown'  : self.brown,
            'violet' : self.violet,
            }

#    def Sin(self, a=1, fs=8000, f0=440, sec=5):
    def Get(self, N=44100, color='white', state=None, a=1, sec=5):
        wav = []
        count = 0
        for noize in self.noise_generator(N=N, color=color, state=state):
            noize /= 3
            noize = 1.0 if 1.0 < noize else noize
            noize = -1.0 if noize < -1.0 else noize
    #        print(noize)
            wav.append(noize)
            count += 1
            if N * sec <= count: break
        return wav
    
    @property
    def Colors(self): return self._noise_generators.keys()

    #https://github.com/python-acoustics/python-acoustics/blob/master/acoustics/signal.py
    def __normalize(self, y, x=None):
        """self.__normalize power in y to a (standard normal) white noise signal.
        Optionally self.__normalize to power in signal `x`.
        #The mean power of a Gaussian with :math:`\\mu=0` and :math:`\\sigma=1` is 1.
        """
        #return y * np.sqrt( (np.abs(x)**2.0).mean() / (np.abs(y)**2.0).mean() )
        if x is not None:
            x = self.__ms(x)
        else:
            x = 1.0
        return y * np.sqrt( x / self.__ms(y) )
        #return y * np.sqrt( 1.0 / (np.abs(y)**2.0).mean() )

        ## Broken? Caused correlation in auralizations....weird!

    def __ms(self, x):
        """Mean value of signal `x` squared.
        :param x: Dynamic quantity.
        :returns: Mean squared of `x`.
        """
        return (np.abs(x)**2.0).mean()

    def noise(self, N, color='white', state=None):
        """Noise generator.
        
        :param N: Amount of samples.
        :param color: Color of noise.
        :param state: State of PRNG.
        :type state: :class:`np.random.RandomState`
        
        """
        try:
            return self._noise_generators[color](N, state)
        except KeyError:
            raise ValueError("Incorrect color.")

    def white(self, N, state=None):
        """
        White noise.
        
        :param N: Amount of samples.
        :param state: State of PRNG.
        :type state: :class:`np.random.RandomState`
        
        White noise has a constant power density. It's narrowband spectrum is therefore flat.
        The power in white noise will increase by a factor of two for each octave band, 
        and therefore increases with 3 dB per octave.
        """
        state = np.random.RandomState() if state is None else state
        return state.randn(N)

    def pink(self, N, state=None):
        """
        Pink noise. 
        
        :param N: Amount of samples.
        :param state: State of PRNG.
        :type state: :class:`np.random.RandomState`
        
        Pink noise has equal power in bands that are proportionally wide.
        Power density decreases with 3 dB per octave.
        
        """
        # This method uses the filter with the following coefficients.
        #b = np.array([0.049922035, -0.095993537, 0.050612699, -0.004408786])
        #a = np.array([1, -2.494956002, 2.017265875, -0.522189400])
        #return lfilter(B, A, np.random.randn(N))
        # Another way would be using the FFT
        #x = np.random.randn(N)
        #X = rfft(x) / N  
        state = np.random.RandomState() if state is None else state
        uneven = N%2
        X = state.randn(N//2+1+uneven) + 1j * state.randn(N//2+1+uneven)
        S = np.sqrt(np.arange(len(X))+1.) # +1 to avoid divide by zero
        y = (irfft(X/S)).real
        if uneven:
            y = y[:-1]
        return self.__normalize(y)

    def blue(self, N, state=None):
        """
        Blue noise. 
        
        :param N: Amount of samples.
        :param state: State of PRNG.
        :type state: :class:`np.random.RandomState`
        
        Power increases with 6 dB per octave.
        Power density increases with 3 dB per octave. 
        
        """
        state = np.random.RandomState() if state is None else state
        uneven = N%2
        X = state.randn(N//2+1+uneven) + 1j * state.randn(N//2+1+uneven)
        S = np.sqrt(np.arange(len(X)))# Filter
        y = (irfft(X*S)).real
        if uneven:
            y = y[:-1]
        return self.__normalize(y)

    def brown(self, N, state=None):
        """
        Violet noise.
        
        :param N: Amount of samples.
        :param state: State of PRNG.
        :type state: :class:`np.random.RandomState`
        
        Power decreases with -3 dB per octave.
        Power density decreases with 6 dB per octave. 
        """
        state = np.random.RandomState() if state is None else state
        uneven = N%2
        X = state.randn(N//2+1+uneven) + 1j * state.randn(N//2+1+uneven)
        S = (np.arange(len(X))+1)# Filter
        y = (irfft(X/S)).real
        if uneven:
            y = y[:-1]
        return self.__normalize(y)

    def violet(self, N, state=None):
    #def violet(N):
        """
        Violet noise. Power increases with 6 dB per octave. 
        
        :param N: Amount of samples.
        :param state: State of PRNG.
        :type state: :class:`np.random.RandomState`
        
        Power increases with +9 dB per octave.
        Power density increases with +6 dB per octave. 
        
        """
        state = np.random.RandomState() if state is None else state
        uneven = N%2
        X = state.randn(N//2+1+uneven) + 1j * state.randn(N//2+1+uneven)
        S = (np.arange(len(X)))# Filter
        y = (irfft(X*S)).real
        if uneven:
            y = y[:-1]
        return self.__normalize(y)

    def noise_generator(self, N=44100, color='white', state=None):
        """Noise generator. 
        :param N: Amount of unique samples to generate.
        :param color: Color of noise.
         
        Generate `N` amount of unique samples and cycle over these samples.
        
        """
        #yield from itertools.cycle(noise(N, color)) # Python 3.3
        for sample in itertools.cycle(self.noise(N, color, state)):
            yield sample        

    def __heaviside(self, N):
        """__heaviside.
        
        Returns the value 0 for `x < 0`, 1 for `x > 0`, and 1/2 for `x = 0`.
        """
        return 0.5 * (np.sign(N) + 1)
        

    __all__ = ['noise', 'white', 'pink', 'blue', 'brown', 'violet',
    'noise_generator', '__heaviside']

