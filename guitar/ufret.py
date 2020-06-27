#coding: utf-8
import os
import re
import tqdm
import json
from selenium.webdriver.support.ui import Select

from .utils import driver_wrapper
from kerasy.utils import toBLUE, toGREEN

UFRET_TITLE_PATTERN = r"\sギターコード\/ウクレレコード\/ピアノコード - U-フレット"

def get_ufret_chords_with_driver(driver, url, capo="0"):
    print(f"Accessing to {toBLUE(url)}...")
    driver.get(url)

    # capo
    if isinstance(capo, int) and capo!=0:
        capo = f"{capo:+}"
    elif capo != "0" and capo[0] not in ["+", "-"]:
        capo = f"{int(capo):+}"
    print(f"Set capo to {toGREEN(capo)}")
    capo_select = driver.find_element_by_name('keyselect')
    capo_select = Select(capo_select)
    capo_select.select_by_value(capo)

    # title
    title = driver.title
    title_match = re.search(pattern=UFRET_TITLE_PATTERN, string=title)
    if title_match is not None:
        title = title[:title_match.start()]
    print(f"title: {toGREEN(title)}")

    # Chord
    my_chord_data = driver.find_elements_by_id("my-chord-data")
    NOTES, LYRICS = [], []
    if len(my_chord_data)>0:
        my_chord_data = my_chord_data[0]
        for row in tqdm.tqdm(my_chord_data.find_elements_by_class_name("row")):
            chords = row.find_elements_by_css_selector(".chord")
            if len(chords)==0: continue
            notes, lyrics = [],[]
            for chord in chords:
                note = "".join([rt.text for rt in chord.find_elements_by_tag_name("rt")])
                lyric = "".join([col.text for col in chord.find_elements_by_class_name("col")])
                notes.append(note)
                lyrics.append(lyric)
            NOTES.append(notes)
            LYRICS.append(lyrics)

    data = {
        i: {
            "chord": note,
            "lyric": lyric
        } for i,(note,lyric) in enumerate(zip(NOTES, LYRICS))
    }
    return (title, capo, data)

def get_ufret_chords(url, capo="0"):
    return driver_wrapper(get_ufret_chords_with_driver, url, capo=capo)