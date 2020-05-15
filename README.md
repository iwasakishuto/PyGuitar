# PyGuitar: Chord book generator

![PyGuitar](https://github.com/iwasakishuto/PyGuitar/blob/master/image/pyguitar.png?raw=true)

[![PyPI version](https://badge.fury.io/py/PyGuitar.svg)](https://pypi.org/project/PyGuitar/)
[![GitHub version](https://badge.fury.io/gh/iwasakishuto%2FPyGuitar.svg)](https://github.com/iwasakishuto/PyGuitar)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg?maxAge=2592000)](https://github.com/iwasakishuto/PyGuitar/blob/gh-pages/LICENSE)

**PyGuitar** generates an **easy-to-practice** chord book.

## Installation

There are two ways to install PyGuitar:

- **Install PyGuitar from PyPI (recommended):**
    ```
    $ sudo pip install PyGuitar
    ```
- **Alternatively: install PyGuitar from the GitHub source:**
    ```
    $ git clone https://github.com/iwasakishuto/PyGuitar.git
    $ cd PyGuitar
    $ sudo python setup.py install
    ```

## How to use

- **Create Guitar Instance**
    ```python
    from guitar import Guitar
    guitar = Guitar(key="C", scale="major")
    ```
- **plot guitar layout**
    ```python
    guitar.plot_chord_layout()
    ```
    ![chord layout](https://github.com/iwasakishuto/PyGuitar/blob/master/image/chord-layout.png?raw=true)
- **plot guitar strings**
  ```python
  guitar.plot_strings()
  ```
  ![guitar strings](https://github.com/iwasakishuto/PyGuitar/blob/master/image/guitar-strings.png?raw=true)
- **plot chord**
  ```python
  guitar.plot_chord(chode="G#", string=6, mode="minor")
  ```
  ![chord-G#.png](https://github.com/iwasakishuto/PyGuitar/blob/master/image/chord-sample.png?raw=true)
- **export notebook**
  ```python
  guitar = Guitar(key="B", scale="major", dark_mode=False)
  guitar.set_chord(chode="D#", string=5, mode="minor")
  guitar.set_chord(chode="G#", string=6, mode="minor")
  guitar.set_chord(chode="E",  string=6, mode="major")
  guitar.set_chord(chode="B",  string=5, mode="major")
  guitar.set_chord(chode="F#", string=6, mode="minor")
  guitar.set_chord(chode="C#", string=5, mode="major")
  guitar.set_chord(chode="F#", string=6, mode="sus4")
  guitar.set_chord(chode="C#", string=5, mode="7th")
  guitar.set_chord(chode="D#", string=5, mode="7th")
  guitar.export_chord_book(fmt="pdf")
  ```
  ![chord-G#.png](https://github.com/iwasakishuto/PyGuitar/blob/master/image/chordbook-sample.png?raw=true)

### Reference

- [Learn Guitar with Python](https://medium.com/better-programming/how-to-learn-guitar-with-python-978a1896a47)
