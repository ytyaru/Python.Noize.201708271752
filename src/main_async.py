import pathlib
import Wave.Player
import Wave.Sampler
import Wave.WaveFile
import Wave.noise_generator
import Wave.NoiseMaker
import asyncio

async def main():
    await playNoise()

async def playNoise():
#    for x in range(1, 10): print(fizzbuzz(x))
#    return None
    hz = 44100
    second = 2
    p = Wave.Player.Player()
    p.Open(rate=hz)
    wavs = []
    for i in range(5):
        wavs.append(Wave.Sampler.Sampler().Sampling(Wave.NoiseMaker.NoiseMaker.Get(N=hz, color='pink', state=None, a=1, sec=second)))
    while True:
        if len(wavs) < 2:
            wavs.append(Wave.Sampler.Sampler().Sampling(Wave.NoiseMaker.NoiseMaker.Get(N=hz, color='pink', state=None, a=1, sec=second)))
        p.Play(wavs[0], rate=hz)
    p.Close()
    return None

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()

v = input('input?: ')
print('enter:', v)

"""
wf = Wave.WaveFile.WaveFile()
wf.BasePath = pathlib.PurePath(f'../res/noize/')
#nm = Wave.NoiseMaker.NoiseMaker()
for color in Wave.NoiseMaker.NoiseMaker._noise_colors:
#for color in nm._noise_generators.keys():
    print(color)
#    wav = Wave.Sampler.Sampler().Sampling(nm.Get(N=hz, color=color, state=None, a=1, sec=second))
    wav = Wave.Sampler.Sampler().Sampling(Wave.NoiseMaker.NoiseMaker.Get(N=hz, color=color, state=None, a=1, sec=second))
    p.Play(wav, rate=hz)
    wf.Write(wav, fs=hz, filename=color)

p.Close()
"""
