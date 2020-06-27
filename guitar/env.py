# coding: utf-8
import os
import json

__all__ = [
    # "LIB_DIR_PATH", "REPO_DIR_PATH", "DATA_DIR_PATH",
    "NUM_FRETS", "NUM_STRINGS", "LEN_OCTAVES", "INIT_KEYS",
    "NOTES", "WHOLE_NOTES", "GUITAR_STRINGS", "MAJOR_MODES", 
    "A4SIZE",
    "SCALE2INTERVALS", "CHORDS",
]

# PATH
LIB_DIR_PATH  = os.path.dirname(os.path.abspath(__file__))
REPO_DIR_PATH = os.path.dirname(LIB_DIR_PATH)
DATA_DIR_PATH = os.path.join(LIB_DIR_PATH, "data")

# Variables.
NUM_FRETS   = 20
NUM_STRINGS = 6
LEN_OCTAVES = 12
INIT_KEYS   = ['E', 'A', 'D', 'G', 'B', 'E']
NOTES       = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
WHOLE_NOTES = NOTES*3
GUITAR_STRINGS = {
    init_key : WHOLE_NOTES[WHOLE_NOTES.index(init_key):][:NUM_FRETS]
    for init_key in INIT_KEYS
}
MAJOR_MODES = ["major", "major7th", "major6th", "sus4", "aug", "omit3", "add9"]

# PDF
A4SIZE=(21.0, 29.7)

# Json data.
with open(os.path.join(DATA_DIR_PATH, "scales.json"), mode="r") as f:
    SCALE2INTERVALS = json.load(f)
with open(os.path.join(DATA_DIR_PATH, "chord.json"), mode="r") as f:
    CHORDS = json.load(f)
