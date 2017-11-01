import pathlib
import Wave.Player
import Wave.Sampler
import Wave.WaveFile
import Wave.noise_generator
import Wave.NoiseMaker
import asyncio
import pyaudio
#import time

#別スレッドで動作しなかった…
#https://people.csail.mit.edu/hubert/pyaudio/docs/

class NoiseStreamMaker:
    def __init__(self, hz=44100, second=2, noise_color='pink'):
        self.__wavs = []
        self.__hz = hz
        self.__second = second
        self.__data = []
        self.__phase = 0
        self.__noise_color = noise_color
        self.__create_init_data()

    # 最初に2秒間+5件のデータを蓄積させておく
    def __create_init_data(self):
#        for i in range(5): self.__wavs.append(Wave.NoiseMaker.NoiseMaker.Get(N=self.__hz, color='pink', state=None, a=1, sec=self.__second))
        for i in range(5): self.__wavs.append(self.__create_noise())
    
    # ノイズ生成メソッド呼出
    def __create_noise(self, N=None, color=None, state=None, a=None, sec=None):
        if None is N: N=self.__hz
        if None is color: color=self.__noise_color
        if None is state: state=None
        if None is a: a=1
        if None is sec: sec=self.__second
#        return Wave.NoiseMaker.NoiseMaker.Get(N=self.__hz, color=self.__noise_color, state=None, a=1, sec=self.__second)
        return Wave.NoiseMaker.NoiseMaker.Get(N=N, color=color, state=state, a=a, sec=sec)

    # PyAudioで呼び出されるコールバック関数（ノイズ音データを返す）
    def callback(self, in_data, frame_count, time_info, status):
        self.__data.clear()
        for i in range(frame_count):
            if len(self.__wavs[0]) <= self.__phase:
                del self.__wavs[0]
                if len(self.__wavs) < 2: self.__wavs.append(self.__create_noise())
                self.__phase = 0
                print(len(self.__wavs), len(self.__wavs[0]))
            self.__data.append(self.__wavs[0][self.__phase])
            self.__phase += 1
        return (Wave.Sampler.Sampler().Sampling(self.__data), pyaudio.paContinue)

if __name__ == '__main__':
    async def main(): await playNoise()
    async def playNoise():
        #設定データ
        format=pyaudio.paInt16
        channels=1
        rate=44100
        second = 2
        noise_color = 'pink'
        #ノイズデータのコールバック実装クラス
        nsm = NoiseStreamMaker(hz=rate, second=second, noise_color=noise_color)
        #再生準備する
        p = pyaudio.PyAudio()
        stream = p.open(format=format,
                        channels=channels,
                        rate=int(rate),
                        output=True,
                        frames_per_buffer=rate,
                        stream_callback=nsm.callback)
        #再生する
        stream.start_stream()
        while stream.is_active(): pass
        #終了する
        stream.stop_stream()
        stream.close()
        p.terminate()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

    v = input('input?: ')
    print('enter:', v)

