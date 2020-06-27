#coding: utf-8
import os
import re
import json
import argparse
from kerasy.utils import toBLUE

from guitar import Guitar
from guitar.ufret import get_ufret_chords
from guitar.utils import get_chord_components
from guitar.utils import find_key_major_scale

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i",   "--input",  type=str, required=True)
    parser.add_argument("-o",   "--output", type=str, default=".")
    parser.add_argument("-t",   "--theme", type=str, default="rainbow")
    parser.add_argument("-s",   "--scale",   type=str, default="major")
    args = parser.parse_args()

    base_dir = args.input
    output_dir = args.output
    theme = args.theme
    scale = args.scale

    for fn in os.listdir(base_dir):
        if os.path.splitext(fn)[1] != ".json": 
            continue
        try:
            title = re.findall(pattern=r"'(.*)'", string=fn)[0]
            path = os.path.join(base_dir, fn)
            with open(path) as f:
                data = json.load(f)
            majors, minors = get_chord_components(data, fmt="ufret")
            key = find_key_major_scale(majors=majors, minors=minors)
            guitar = Guitar(key=key, scale=scale, dark_mode=False, theme=theme, name=title)
            filename = os.path.join(output_dir, guitar.pdf)
            guitar.create_chord_book(data=data, nrows=5, filename=filename, verbose=1)
        except:
            print(f"Error occured in {toBLUE(fn)}")