# coding: utf-8
from collections import defaultdict

from .fmt_utils import ufret2pyguitar
from ..env import (NUM_FRETS, LEN_OCTAVES, MAJOR_MODES,
                   SCALE2INTERVALS, WHOLE_NOTES, GUITAR_STRINGS)

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
    is_majors  = [1,0,0,1,1,0,0]
    num_majors = len(majors); num_minors = len(minors)
    if num_majors+num_minors==0:
        raise ValueError("Couldn't find key from nothing.")

    # If majors/minors is dict, they have the frequencies, and we can use them as weights.
    if not isinstance(majors, dict):
        majors = dict(zip(majors, [1 for _ in range(majors)]))
    if not isinstance(minors, dict):
        minors = dict(zip(minors, [1 for _ in range(minors)]))
    
    get_score = {
        (True, True)  : lambda maj,min : maj/num_majors + min/num_minors,
        (True, False) : lambda maj,min : maj/num_majors,
        (False, True) : lambda maj,min : min/num_minors,
    }[(num_majors>0, num_minors>0)]

    best_score = -1
    for key in WHOLE_NOTES[:LEN_OCTAVES]:
        maj = min = 0
        notes = get_notes(key, SCALE2INTERVALS.get("major"))
        for is_maj,note in zip(is_majors, notes):
            if is_maj and note in majors: 
                maj+=majors.get(note)
            elif (not is_maj) and note in minors: 
                min+=minors.get(note)
        score = get_score(maj, min)
        if score > best_score:
            best_score=score
            best_key=key
    return best_key

def get_chord_components(data, fmt="ufret"):
    majors = defaultdict(int)
    minors = defaultdict(int)

    chord_convertor = {
        "ufret" : ufret2pyguitar
    }.get(fmt, ufret2pyguitar)

    for row in data.values():
        for chord in row.get("chord"):
            if chord == "": 
                continue
            note, mode, d = chord_convertor(chord)
            if mode in MAJOR_MODES:
                majors[note] += 1
            else:
                minors[note] += 1
    return majors, minors