import os, json, shutil, pathlib
      
def test_path(fpath) -> bool:
    return os.path.isfile(fpath)

def format_song_name(name: str) -> str:
    temp = name.split(' ')
    new = ''
    for i, j in enumerate(temp):
        new += j.capitalize()
        if i < len(temp) - 1:
            new += ' '
    new = new.replace("'", '')
    new = new.replace("!", '')
    new = new.replace("?", '')
    return new

setlist_filename = r'SM 2024 Festival Set'

SETLIST_FOLDER = r'C:\Users\will\Documents\GitHub\music_organiser\Sets'
DESTINATION_FOLDER = r'C:\Users\will\Desktop\song_export'
NETWORK_PATH = r'Z:\Will\Music'
LOCATION_MAP = {
    'leadsheet': r'Scores\Mojos Onsong lead sheets',
    'editable_score': r'Scores\MuseScore scores',
    'score': r'Scores\Score PDF Exports',
    'band_mp3': r'Recordings\Smoking Mojos',
    'original_mp3': r'Recordings\Originals'
    }

song_library_path = os.path.join(os.path.dirname(__file__), 'library.json')
setlist_path = os.path.join(os.path.dirname(__file__), SETLIST_FOLDER, setlist_filename + '.txt')
setlist = []
songs = []
errors = []

#read library json
with open(song_library_path) as file_read:
    song_library = json.load(file_read)

#read set list txt
with open(setlist_path) as file_read:
    for line in file_read:
        setlist.append(line.rstrip("\n"))

#create folder structure
for t in LOCATION_MAP.keys():
    pathlib.Path(os.path.join(DESTINATION_FOLDER, setlist_filename, t)).mkdir(parents=True, exist_ok=True) 

for index, song in enumerate(setlist):
    song = format_song_name(song)
    print(f'processing {song}...')
    if song in song_library['songs']:
        for i in song_library['songs'][song]['files']:
            try:
                file_path = os.path.join(NETWORK_PATH, LOCATION_MAP[i], song_library['songs'][song]['files'][i])
                test_path(file_path)
            except:
                errors.append(f'{i} for {song} does not exist')
                continue

            numbered_file_name = f'{index + 1} {os.path.basename(file_path)}'

            destination_numbered_file_path = os.path.join(DESTINATION_FOLDER, setlist_filename, i, numbered_file_name)
            shutil.copy(file_path, destination_numbered_file_path)
            
    else:
        errors.append(f'The song {song} is not in the library')

print('')
for e in errors:
    print(e)