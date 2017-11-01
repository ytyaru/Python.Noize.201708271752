#!python3.6
import pathlib
import noise_generator

"""所定の音声ファイルを再生させるためのHTML5<audio>タグを生成するスクリプト。"""

#def GetToneName(keyId): return ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B'][keyId]
#def GetScaleFilename(scaleName, keyId): return GetToneName(keyId).replace('#','+')+scaleName

class TagMaker:
    def __init__(self):
        self.__basepath = pathlib.PurePath('res/scales')
        self.__username = 'ytyaru'
        self.__repo_name = 'Python.Noize.201708270906'
#    def __get_tag_audio(name, ext, dirs): return '<audio controls src={0}></audio>'.format(get_url(name, ext, dirs))
    def get_audios(self, name, dirs=None):
        sources = ''
        for ext in ['wav','flac','ogg','mp3']: sources += f'<source src={self.__get_url(name, ext, dirs)}>'
        return f'<audio controls>{sources}</audio>'
    def __get_url(self, name, ext, dirs=None):
        if None is dirs: dirs = str(self.__basepath)
        return f'https://raw.githubusercontent.com/{self.__username}/{self.__repo_name}/master/{dirs}/{ext}/{name}.{ext}'
    def get_audios_noize(self, name): return self.get_audios(name, f'res/noize')

if __name__ == '__main__':
    tm = TagMaker()
    body = ''
    
    table_body = 'ノイズ色|Player' + '\n' + '--------|------' + '\n'
    for color in noise_generator._noise_generators.keys():
        table_body += color + '|' + tm.get_audios_noize(color) + '\n'
    body += table_body + '\n'
    
    print(body)

