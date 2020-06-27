# coding: utf-8
import os
import argparse
from kerasy.utils import toBLUE, toGREEN

from guitar import Guitar
from guitar.ufret import get_ufret_chords
from guitar.utils import get_chord_components
from guitar.utils import find_key_major_scale

here = os.path.dirname(os.path.abspath(__file__))
print(f"Here is {toBLUE(here)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", type=str, required=True)
    parser.add_argument("-t", "--theme", type=str, default="rainbow")
    parser.add_argument("-s", "--scale", type=str, default="major")
    parser.add_argument("-c", "--capo",  type=str, default="0")
    parser.add_argument("-k", "--key",   type=str)
    args = parser.parse_args()

    url   = args.url
    theme = args.theme
    scale = args.scale
    capo  = args.capo
    key   = args.key

    title, capo, data = get_ufret_chords(url=url, capo=capo, to_json=False)
    if key is None:
        majors, minors = get_chord_components(data, fmt="ufret")
        key = find_key_major_scale(majors=majors, minors=minors)
    print(f"""Create the following guitar books
    * url : {toBLUE(url)}
    * theme : {toGREEN(theme)}
    * scale : {toGREEN(scale)}
    * capo  : {toGREEN(capo)}
    * key   : {toGREEN(key)}
    """)
    guitar = Guitar(key=key, scale=args.scale, dark_mode=False, theme=args.theme, name=title)
    guitar.create_chord_book(data=data, nrows=5, filename=None, verbose=1)