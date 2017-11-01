# このソフトウェアについて

Pythonでノイズ音を永続的に生成してみた。

ファイル|概要
--------|----
main.py|ノイズを再生しつつ、ノイズ色を指定できる。スレッドを正常終了できない。
main_loop.py|無限ループ版
main_async.py|非同期版（音が汚く正常に再生されない）
main_callback.py.py|コールバック版
main_callback_async.py|asyncを使ってみた。思い通りに動かない。
main_callback_class.py|コードを整えた。
main_callback_thread.py|スレッドを使うことで音声再生と入力受付を並列できそう。
main_callback_thread_2.py|音声再生と入力受付を並列できたが正常終了できない。Pythonスレッドの仕様。これはひどい。

# 実行

```sh
$ cd src/
$ python main.py
...
========== Noise Player ==========
[w]hite, [p]ink, brow[n], [b]lue, [v]iolet: 
```

# 開発環境

* Linux Mint 17.3 MATE 32bit
* [libav](http://ytyaru.hatenablog.com/entry/2018/08/24/000000)
    * [各コーデック](http://ytyaru.hatenablog.com/entry/2018/08/23/000000)
* [pyenv](https://github.com/pylangstudy/201705/blob/master/27/Python%E5%AD%A6%E7%BF%92%E7%92%B0%E5%A2%83%E3%82%92%E7%94%A8%E6%84%8F%E3%81%99%E3%82%8B.md) 1.0.10
    * Python 3.6.1
        * [pydub](http://ytyaru.hatenablog.com/entry/2018/08/25/000000)
        * [PyAudio](http://ytyaru.hatenablog.com/entry/2018/07/27/000000) 0.2.11
            * [ALSA lib pcm_dmix.c:1022:(snd_pcm_dmix_open) unable to open slave](http://ytyaru.hatenablog.com/entry/2018/07/29/000000)
        * [matplotlib](http://ytyaru.hatenablog.com/entry/2018/07/22/000000)
            * [matplotlibでのグラフ表示を諦めた](http://ytyaru.hatenablog.com/entry/2018/08/05/000000)

# 参考

感謝。

* https://ja.wikipedia.org/wiki/%E3%82%AB%E3%83%A9%E3%83%BC%E3%83%89%E3%83%8E%E3%82%A4%E3%82%BA

## サイン波のスピーカ再生

* http://www.non-fiction.jp/2015/08/17/sin_wave/
* http://aidiary.hatenablog.com/entry/20110607/1307449007
* http://ism1000ch.hatenablog.com/entry/2013/11/15/182442

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

## ライブラリ

感謝。

Library|License|Copyright
-------|-------|---------
[python-acoustics](https://github.com/python-acoustics/python-acoustics)|[BSD 3-clause](https://github.com/python-acoustics/python-acoustics/blob/master/LICENSE)|[Copyright (c) 2013, Python Acoustics](https://github.com/python-acoustics/python-acoustics/blob/master/LICENSE)
[pydub](https://github.com/jiaaro/pydub)|[MIT](https://github.com/jiaaro/pydub/blob/master/LICENSE)|[Copyright (c) 2011 James Robert, http://jiaaro.com](https://github.com/jiaaro/pydub/blob/master/LICENSE)
[pygame](http://www.pygame.org/)|[LGPL](https://www.pygame.org/docs/)|[pygame](http://www.pygame.org/)

