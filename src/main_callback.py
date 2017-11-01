import pathlib
import Wave.Player
import Wave.Sampler
import Wave.WaveFile
import Wave.noise_generator
import Wave.NoiseMaker
import asyncio
import pyaudio
#import time
#https://people.csail.mit.edu/hubert/pyaudio/docs/

# 最初に2秒間+5件のデータを蓄積させておく
wavs = []
hz = 44100
second = 2
for i in range(5):
    wavs.append(Wave.NoiseMaker.NoiseMaker.Get(N=hz, color='pink', state=None, a=1, sec=second))

# frames_per_bufferごとにデータを要求してくるので返してやる
# 返却データがローカル変数だとMemoryErrorになるので、グローバル変数にして毎回初期化する。
data = []
phase = 0
def callbackMakeNoise(in_data, frame_count, time_info, status):
    global wavs, data, phase
    data.clear()
    global wavs, phase
    for i in range(frame_count):
        if len(wavs[0]) <= phase:
            del wavs[0]
            if len(wavs) < 2: wavs.append(Wave.NoiseMaker.NoiseMaker.Get(N=hz, color='pink', state=None, a=1, sec=second))
            phase = 0
            print(len(wavs), len(wavs[0]))
        data.append(wavs[0][phase])
        phase += 1
    return (Wave.Sampler.Sampler().Sampling(data), pyaudio.paContinue)

#再生準備する
format=pyaudio.paInt16
channels=1
rate=44100
p = pyaudio.PyAudio()
stream = p.open(format=format,
                channels=channels,
                rate=int(rate),
                output=True,
                frames_per_buffer=44100,
                stream_callback=callbackMakeNoise)

#再生する
stream.start_stream()
while stream.is_active(): pass
#while stream.is_active(): time.sleep(0.5)

#終了する
stream.stop_stream()
stream.close()
p.terminate()

