# coding: utf-8
import os
import json
import argparse
from kerasy.utils import toBLUE, toGREEN

from guitar import Guitar
from guitar.ufret import get_ufret_chords
from guitar.utils import get_chord_components
from guitar.utils import find_key_major_scale
from guitar.utils import japanize

here = os.path.dirname(os.path.abspath(__file__))
print(f"Here is {toBLUE(here)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u",   "--url",     type=str, required=True)
    parser.add_argument("-t",   "--theme",   type=str, default="rainbow")
    parser.add_argument("-s",   "--scale",   type=str, default="major")
    parser.add_argument("-c",   "--capo",    type=str, default="0")
    parser.add_argument("-k",   "--key",     type=str)
    parser.add_argument("-d",   "--dir",     type=str, default="/data")
    parser.add_argument("-fmt", "--format",  type=str, default="pdf")
    parser.add_argument("--font_path",  type=str, default="/font/ipam.ttf")
    parser.add_argument("--family",     type=str, default="IPAPMincho")
    args = parser.parse_args()

    url   = args.url
    theme = args.theme
    scale = args.scale
    capo  = args.capo
    key   = args.key
    dir   = args.dir
    fmt   = args.format
    font_path = args.font_path
    family    = args.family

    title, capo, data = get_ufret_chords(url=url, capo=capo)
    if key is None:
        majors, minors = get_chord_components(data, fmt="ufret")
        key = find_key_major_scale(majors=majors, minors=minors)
    title = repr(title.replace("/", "|"))
    print(f"""Create the following chordbooks:
    * url   : {toBLUE(url)}
    * theme : {toGREEN(theme)}
    * scale : {toGREEN(scale)}
    * capo  : {toGREEN(capo)}
    * key   : {toGREEN(key)}
    """)
    guitar = Guitar(key=key, scale=args.scale, dark_mode=False, theme=args.theme, name=title)
    filename = os.path.join(dir, guitar.pdf) if dir is not None else None
    if fmt=="pdf":
        japanize(font_path=font_path, family=family)
        guitar.create_chord_book(data=data, nrows=5, filename=filename, verbose=1)
    else:
        filename = filename.replace(".pdf", ".json")
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Save data at {toBLUE(filename)}")