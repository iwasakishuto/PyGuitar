#coding: utf-8
import re
import tqdm
import json
from selenium.webdriver.support.ui import Select

from .utils import driver_wrapper
from kerasy.utils import toBLUE, toGREEN

UFRET_TITLE_PATTERN = r"\sギターコード\/ウクレレコード\/ピアノコード - U-フレット"

def get_ufret_chords_with_driver(driver, url, key="0", to_json=False):
    print(f"Accessing to {toBLUE(url)}...")
    driver.get(url)

    # Key
    if isinstance(key, int) and key!=0:
        key = f"{key:+}"
    elif key != "0" and key[0] not in ["+", "-"]:
        key = f"{int(key):+}"
    print(f"Set key to {toGREEN(key)}...")
    key_select = driver.find_element_by_name('keyselect')
    key_select = Select(key_select)
    key_select.select_by_value(key)

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
    if to_json:
        with open(f"{title.replace('/', '')} | key-{key}.json", 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    else:
        return (title, key, data)

def get_ufret_chords(url, key="0", to_json=False):
    return driver_wrapper(get_ufret_chords_with_driver, url, key=key, to_json=to_json)
