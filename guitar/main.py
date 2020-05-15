# coding: utf-8
import warnings
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from .env import *
from .utils import get_notes, get_intervals, find_notes_positions

class Guitar():
    def __init__(self, key="C", scale="major", dark_mode=False, name=""):
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
        self.name_ = name

    @property
    def name(self):
        return f"key_{self.key}-{self.scale}_scale"

    @property
    def png(self):
        name = "" if self.name_ == "" else self.name_ + "-"
        return name + self.name + ".png"

    @property
    def pdf(self):
        name = "" if self.name_ == "" else self.name_ + "-"
        return name + self.name + ".pdf"

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
            ax.set_title(self.name + f" [{chode}({string}s){mode}]", fontsize=20)
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
