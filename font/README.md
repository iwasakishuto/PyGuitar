## How to use??

```sh
>>> import matplotlib.pyplot as plt
>>> plt.title("日本語")
Text(0.5, 1.0, '日本語')
>>> plt.savefig("japanese.png")
RuntimeWarning: Glyph 26085 missing from current font.

>>> from guitar.utils import japanize
>>> japanize(font_path='/font/ipam.ttf', family='IPAPMincho')
>>> plt.title("日本語")
Text(0.5, 1.0, '日本語')
>>> plt.savefig("japanese.png")
```

