# coding: utf-8
import os
import json
import warnings
import numpy as np
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

def get_notes(key, intervals):
    """
    @params key       : Code key.
    @params intervals : Scale positions.
    @return notes     : Notes
    """
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

class Guitar():
    def __init__(self, key="C", scale="major"):
        self.key = key
        self.scale = scale
        self.intervals = SCALE2INTERVALS.get(scale.lower())
        self.notes = get_notes(key, self.intervals)
        self.notes_pos_in_string = find_notes_positions(self.notes)

    @property
    def name(self):
        return f"key_{self.key}-{self.scale}_scale"

    @property
    def png(self):
        return self.name + ".png"

    @property
    def pdf(self):
        return self.name + ".pdf"

    def _plot_chord_layout(self, dark_model=False):
        facecoloer, linecolor = {
            True  : ("black", "white"),
            False : ("white", "black")
        }[dark_model]

        fig,ax = plt.subplots(figsize=(NUM_FRETS, NUM_STRINGS))
        # Plot Strings
        for i in range(1, NUM_STRINGS+1):
            ax.plot([i for _ in range(NUM_FRETS+2)], color='gray')
        # Plot Frets
        for i in range(1, NUM_FRETS+1):
            if i == LEN_OCTAVES:
                ax.axvline(x=i, color='gray', linewidth=3.5)
            else:
                ax.axvline(x=i, color=linecolor, linewidth=0.5)
        ax.set_axisbelow(True)
        ax.set_xlim([0.5, 21]), ax.set_ylim([0.4, 6.5])
        ax.set_facecolor(facecoloer)
        plt.xticks(np.arange(NUM_FRETS+1)+0.5, np.arange(NUM_FRETS+2), fontsize=20)
        plt.yticks(np.arange(1,NUM_STRINGS+1), INIT_KEYS, fontsize=20)
        return fig, ax

    def plot_chord(self, chode, string=6, mode="major", dark_model=False):
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

        fig, ax = self._plot_chord_layout(dark_model=dark_model)
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
        plt.title(self.name + f" [{chode}({string}s){mode}]", fontsize=20)
        plt.show()

    def plot_strings(self, dark_model=False, save=False):
        fig, ax = self._plot_chord_layout(dark_model=dark_model)
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
        plt.title(self.name, fontsize=20)
        plt.show()
        if save:
            fig.savefig(self.png)
            fig.savefig(self.pdf)
