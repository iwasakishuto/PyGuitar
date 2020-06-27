# coding: utf-8
import re

UFRET2PyGuitar_dict = {
    ""      : "major",
    "m"     : "minor",
    "7"     : "7th",
    "m7"    : "minor7th",
    "maj7"  : "major7th",
    "m7-5"  : "minor7th-flatted5th",
    "6"     : "major6th",
    "m6"    : "minor6th",
    "sus4"  : "sus4",
    "dim"   : "dim",
    "aug"   : "aug",
    "omit3" : "omit3",
    "add9"  : "add9",   
}

def ufret2pyguitar(chord, sep="_"):
    """
    U-FRET format -> PyGuitar format.
    TODE: I want to deal with it by adding an alias for `chord.json`
    """
    if chord == "":
        return ("", "", [])
    # numerator / denominator
    n, *d = chord.split("/")
    note, mode_ufret = re.sub(r"([A-G]#?♭?)(.*)", rf"\1{sep}\2", n).split(sep)
    mode_pyguitar = UFRET2PyGuitar_dict.get(mode_ufret)
    return (note, mode_pyguitar, d)
