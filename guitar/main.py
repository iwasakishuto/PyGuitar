# coding: utf-8
import os
import json
import warnings
from itertools import compress
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from . import DATA_DIR_PATH

NUM_FRETS   = 20
NUM_STRINGS = 6
LEN_OCTAVES = 12
INIT_KEYS   = ['E', 'A', 'D', 'G', 'B', 'E']
WHOLE_NOTES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']*3
GUITAR_STRINGS = {
    init_key : WHOLE_NOTES[WHOLE_NOTES.index(init_key):][:NUM_FRETS]
    for init_key in INIT_KEYS
}
with open(os.path.join(DATA_DIR_PATH, "scales.json"), mode="r") as f:
    SCALE2INTERVALS = json.load(f)
with open(os.path.join(DATA_DIR_PATH, "chord.json"), mode="r") as f:
    CHORDS = json.load(f)

def get_intervals(scale):
    return SCALE2INTERVALS.get(scale.lower())

def get_notes(key, intervals):
    """
    @params key       : Code key.
    @params intervals : Scale positions.
    @return notes     : Notes
    """
    if isinstance(intervals, str):
        intervals = get_intervals(scale)
    root = WHOLE_NOTES.index(key)
    octave = WHOLE_NOTES[root:root+LEN_OCTAVES]
    return [octave[i] for i in intervals]

def find_notes_positions(notes):
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
    is_majors = [1,0,0,1,1,0,0]
    key_notes = {key: get_notes(key, SCALE2INTERVALS.get("major")) for key in WHOLE_NOTES[:LEN_OCTAVES]}
    return {
        k:v for k,v in key_notes.items()
        if all([major in [e for e,is_major in zip(v,is_majors) if is_major] for major in majors])
        and all([minor in [e for e,is_major in zip(v,is_majors) if not is_major] for minor in minors])
    }

class Guitar():
    def __init__(self, key="C", scale="major", dark_mode=False):
        self.key = key
        self.scale = scale
        self.intervals = get_intervals(scale)
        self.notes = get_notes(key, self.intervals)
        self.notes_pos_in_string = find_notes_positions(self.notes)
        self.facecoloer, self.linecolor = {
            True  : ("black", "white"),
            False : ("white", "black")
        }[dark_mode]
        self.chords = []

    @property
    def name(self):
        return f"key_{self.key}-{self.scale}_scale"

    @property
    def png(self):
        return self.name + ".png"

    @property
    def pdf(self):
        return self.name + ".pdf"

    def chord_layout_create(self, n=1):
        fig, axes = plt.subplots(ncols=1, nrows=n, figsize=(NUM_FRETS, NUM_STRINGS*n))
        if n > 1:
            for ax in axes:
                ax = self.plot_chord_layout(ax=ax)
        else:
            axes = self.plot_chord_layout(ax=axes)
        return fig, axes

    def plot_chord_layout(self, ax=None):
        if ax is None:
            fig,ax = self.chord_layout_create(n=1)
        # Plot Strings
        for i in range(1, NUM_STRINGS+1):
            ax.plot([i for _ in range(NUM_FRETS+2)], color='gray')
        # Plot Frets
        for i in range(1, NUM_FRETS+1):
            if i%LEN_OCTAVES==0:
                ax.axvline(x=i, color='gray', linewidth=3.5)
            else:
                ax.axvline(x=i, color=self.linecolor, linewidth=0.5)
        ax.set_axisbelow(True)
        ax.set_facecolor(self.facecoloer)
        ax.set_xlim([0.5, 21])
        ax.set_xticks([i+0.5 for i in range(NUM_FRETS+1)])
        ax.set_xticklabels(range(NUM_FRETS+2), fontsize=20)
        ax.set_ylim([0.4, 6.5])
        ax.set_yticks(range(1, NUM_STRINGS+1))
        ax.set_yticklabels(INIT_KEYS, fontsize=20)
        return ax

    def set_chord(self, chode, string=6, mode="major", set_title=True):
        self.chords.append({
            "chode"     : chode,
            "string"    : string,
            "mode"      : mode,
            "set_title" : set_title
        })

    def export_chord_book(self, filename=None, fmt="pdf"):
        num_chords = len(self.chords)
        n_rows = num_chords//2+2 if num_chords%2 else num_chords//2+1
        fig = plt.figure(figsize=(NUM_FRETS, NUM_STRINGS*n_rows))

        ax_strings = plt.subplot2grid((n_rows, 2), (0, 0), colspan=2)
        ax_strings = self.plot_chord_layout(ax=ax_strings)
        ax_strings = self.plot_strings(ax=ax_strings)

        for i,chords in enumerate(self.chords):
            root_pos  = GUITAR_STRINGS.get(INIT_KEYS[6-chords.get("string")]).index(chords.get("chode"))

            ax = plt.subplot2grid(shape=(n_rows, 2), loc=(1+i//2, i%2))
            ax = self.plot_chord_layout(ax=ax)
            ax = self.plot_chord(**chords, ax=ax)
            ax.set_xlim([root_pos, min(root_pos+5, 21)])
            ax.set_yticklabels([GUITAR_STRINGS.get(init_key)[root_pos-1] for init_key in INIT_KEYS], fontsize=20)

        if fmt.lower() == "pdf":
            fig.savefig(filename or self.pdf)
        else:
            fig.savefig(filename or self.png)

    def plot_chord(self, chode, string=6, mode="major", set_title=True, ax=None):
        if chode not in self.notes:
            warnings.warn(f"{chode} is not included in the {self.notes}")
        elif mode[:5] in ["major", "minor"]:
            if self.notes.index(chode) in [0,3,4]:
                mode = "major" + mode[5:]
            else:
                mode = "minor" + mode[5:]

        positions = CHORDS.get(mode).get(str(string))
        root_pos  = GUITAR_STRINGS.get(INIT_KEYS[6-string]).index(chode)
        is_mutes  = [pos==False for pos in positions]
        positions = [pos+root_pos for pos in positions]

        ax = self.plot_chord_layout(ax)
        for i,(y_val, pos, is_mute) in enumerate(zip([1,2,3,4,5,6], positions, is_mutes)):
            x = pos+0.5
            note = GUITAR_STRINGS.get(INIT_KEYS[i])[pos]
            if 7-y_val == string:
                font, color, radius = (14, "red", 0.4)
            elif is_mute:
                font, color, radius = (12, "green", 0.3)
            else:
                font, color, radius = (12, None, 0.3)
            ax.add_patch(mpatches.Circle(xy=(x, y_val), radius=radius, color=color))
            ax.annotate(note, (x, y_val), color='w', weight='bold',
                        fontsize=font, ha='center', va='center')

        if set_title:
            plt.title(self.name + f" [{chode}({string}s){mode}]", fontsize=20)
        return ax

    def plot_strings(self, ax=None, set_title=True, width=20):
        ax = self.plot_chord_layout(ax)
        for y_val, init_key in zip([1,2,3,4,5,6], INIT_KEYS):
            string = GUITAR_STRINGS.get(init_key)
            for i in self.notes_pos_in_string.get(init_key):
                x = i+0.5
                note = string[i]
                if note == self.key:
                    font, color, radius = (16, "green", 0.4)
                else:
                    font, color, radius = (12,    None, 0.3)
                ax.add_patch(mpatches.Circle(xy=(x, y_val), radius=radius, color=color))
                ax.annotate(note, (x, y_val), color='w', weight='bold',
                            fontsize=font, ha='center', va='center')
        if set_title:
            ax.set_title(self.name, fontsize=20)
        return ax
