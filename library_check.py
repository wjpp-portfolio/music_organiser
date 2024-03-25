import os, json

NETWORK_PATH = r'Z:\Will\Music'
LOCATION_MAP = {
    'leadsheet': r'Scores\Mojos Onsong lead sheets',
    'editable_score': r'Scores\MuseScore scores',
    'score': r'Scores\Score PDF Exports',
    'band_mp3': r'Recordings\Smoking Mojos',
    'original_mp3': r'Recordings\Originals'
    }

def test_path(fpath) -> bool:
    return os.path.isfile(fpath)

song_library_path = os.path.join(os.path.dirname(__file__), 'library.json')
with open(song_library_path) as file_read:
    song_library = json.load(file_read)


songs_with_no_file = []
songs_with_missing_or_invaite_file_path = []
for s in song_library['songs']:

    for i in song_library['songs'][s]['files']:
        if not song_library['songs'][s]['files'][i]:
            songs_with_no_file.append(f'{i} is missing for {s}')
        else:
            file_path = os.path.join(NETWORK_PATH, LOCATION_MAP[i], song_library['songs'][s]['files'][i])
            if not test_path(file_path):
                songs_with_missing_or_invaite_file_path.append(f'Invalid or missing file: {file_path}')

for e in songs_with_no_file:
    print(e) 
for e in songs_with_missing_or_invaite_file_path:
    print(e)