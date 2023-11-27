
# Relevant:
# https://github.com/Skuldur/Classical-Piano-Composer

from multiprocessing import Pool
import json
from music21 import converter
from music21.stream import Part
from glob import glob

from .melody import Melody


def read_melodies_from_file(file: str):
    print(f"Processing file: {file}")
    try:
        score = converter.parse(file)
    except Exception:
        print(f"An error ocurred, skipping file: {file}")
        return []
    parts = filter(lambda stream: isinstance(stream, Part), score)
    return list(map(lambda part: Melody(part), parts))


def process(midi_folder, output_file):
    midi_files = glob(midi_folder + "/**/*.[Mm][Ii][Dd]", recursive=True)

    pool = Pool()
    unflattened_melodies = pool.imap_unordered(
        read_melodies_from_file, midi_files)
    melodies = [m for melodies in unflattened_melodies for m in melodies]
    with open(output_file, "w") as output:
        raw_melodies = list(map(lambda melody: melody.to_notes(), melodies))
        output.write(json.dumps(raw_melodies))
