# coding: utf-8
import re
from ..env import (NUM_FRETS, LEN_OCTAVES,
                   SCALE2INTERVALS, WHOLE_NOTES, GUITAR_STRINGS)

def split_chord(chord):
    """
    U-FRET format -> PyGuitar format.
    TODE: I want to deal with it by adding an alias for `chord.json`
    """
    note, mode = re.sub(r"([A-G]#?)(.*)", r"\1-\2", chord).split("-")
    if mode == "":
        mode = "major"
    elif mode == "m":
        mode = "minor"
    elif mode == "m7":
        mode = "minor7th"
    elif mode == "7":
        mode = "major7th"
    return note, mode

def get_intervals(scale):
    """ Get intervals from scale. """
    return SCALE2INTERVALS.get(scale.lower())

def get_notes(key, scale):
    """ Get notes corresponding to the specified scale and key.
    @params key   : (str) Code key.
    @params scale : (str) scale / (list) Scale positions.
    @return notes : Notes
    """
    if isinstance(scale, str):
        scale = get_intervals(scale)
    root = WHOLE_NOTES.index(key)
    octave = WHOLE_NOTES[root:root+LEN_OCTAVES]
    return [octave[i] for i in scale]

def find_notes_positions(notes):
    """ Find Notes positions in guitar strings. """
    notes_positions = dict()
    for init_key, string in GUITAR_STRINGS.items():
        indexes = []
        for note in notes:
            idx = string.index(note)
            while idx < NUM_FRETS:
                indexes.append(idx)
                idx += LEN_OCTAVES
        notes_positions[init_key] = indexes
    return notes_positions

def find_key_major_scale(majors=[], minors=[]):
    """
    Find key based on the 'chords' that appear in the music and the specified 'scale'
    """
    is_majors = [1,0,0,1,1,0,0]
    key_notes = {key: get_notes(key, SCALE2INTERVALS.get("major")) for key in WHOLE_NOTES[:LEN_OCTAVES]}
    return {
        k:v for k,v in key_notes.items()
        if all([major in [e for e,is_major in zip(v,is_majors) if is_major] for major in majors])
        and all([minor in [e for e,is_major in zip(v,is_majors) if not is_major] for minor in minors])
    }
