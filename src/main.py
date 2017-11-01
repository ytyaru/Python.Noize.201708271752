import pathlib
import Wave.Player
import Wave.Sampler
import Wave.WaveFile
import Wave.noise_generator
import Wave.NoiseMaker
#import asyncio
import threading
import pyaudio
import time

#Pythonはスレッドの終了ができないらしい……
#> 現状では、優先度 (priority)やスレッドグループがなく、スレッドの破壊 (destroy)、中断 (stop)、一時停止 (suspend)、復帰 (resume)、割り込み (interrupt) は行えません
#http://qiita.com/xeno1991/items/b207d55a413664513e5f
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

    @property
    def Color(self): return self.__noise_color
    @Color.setter
    def Color(self, v):
        if v in Wave.NoiseMaker.NoiseMaker._noise_colors: self.__noise_color = v

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
#                print(len(self.__wavs), len(self.__wavs[0]))
            self.__data.append(self.__wavs[0][self.__phase])
            self.__phase += 1
        return (Wave.Sampler.Sampler().Sampling(self.__data), pyaudio.paContinue)

class NoisePlayerThread():
    def __init__(self):
        rate=44100
        second = 2
        noise_color = 'pink'
        self.__NoiseStreamMaker = NoiseStreamMaker(hz=rate, second=second, noise_color=noise_color)
#        self.__NoiseStreamMaker = None
        self.__pyaudio = None
        self.__stream = None
        self.stop_event = threading.Event() #停止させるかのフラグ
        self.set_noise_color_event = threading.Event()  #ノイズ色を設定するフラグ
        #スレッドの作成と開始
        self.thread = threading.Thread(target=self.run)
        self.thread.start()
    
    @property
    def NoiseColor(self): return self.__NoiseStreamMaker.Color
    @NoiseColor.setter
    def NoiseColor(self, v): self.__NoiseStreamMaker.Color = v

    """
    def start(self):
        if None is self.thread:
            self.thread = threading.Thread(target=self.run)
            self.thread.start()
    """
    def run(self):
#        if self.stop_event.is_set(): return
#        if None is self.thread: return
        #設定データ
        format=pyaudio.paInt16
        channels=1
        rate=44100
        second = 2
        noise_color = 'pink'
        #再生準備する
        self.__pyaudio = pyaudio.PyAudio()
        self.__stream = self.__pyaudio.open(format=format,
                        channels=channels,
                        rate=int(rate),
                        output=True,
                        frames_per_buffer=rate,
                        stream_callback=self.__NoiseStreamMaker.callback)
        #再生する
        self.__stream.start_stream()
        while self.__stream.is_active(): pass
        #終了する
        self.__stream.stop_stream()
        self.__stream.close()
        self.__pyaudio.terminate()

    def stop(self):
        self.__stream.stop_stream()
        self.__stream.close()
        self.__pyaudio.terminate()
        self.thread.join()
#        self.thread = None

if __name__ == '__main__':
    th = NoisePlayerThread()
    time.sleep(2)
    print('========== Noise Player ==========')
    while True:
        v = input('[w]hite, [p]ink, brow[n], [b]lue, [v]iolet: ').lower().strip()
#        print('[w]hite, [p]ink, brow[n], [b]lue, [v]iolet:')
#        v = input('noise color: ').lower().strip()
#        print('enter:', v)
        if 0 == len(v) or v in ['end', 'quit', 'close', 'stop', 'finish', 'fin']: break
        elif 'w' == v: th.NoiseColor = 'white'
        elif 'p' == v: th.NoiseColor = 'pink'
        elif 'n' == v: th.NoiseColor = 'brown'
        elif 'b' == v: th.NoiseColor = 'blue'
        elif 'v' == v: th.NoiseColor = 'violet'
        else: continue
        th.NoiseColor = v
    
    print('END')
    th.stop()
