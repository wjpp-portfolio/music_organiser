import os, json, shutil, pathlib

class Song:
    def __init__(self, name, files):
        self.name = name
        
        self.leadsheet = os.path.join(NETWORK_PATH, LOCATION_MAP['leadsheet'], files['leadsheet'])
        if not test_path(self.leadsheet):
            self.leadsheet = ""
        self.editable_score = os.path.join(NETWORK_PATH, LOCATION_MAP['editable_score'], files['editable_score'])
        if not test_path(self.editable_score):
            self.editable_score = ""
        self.score = os.path.join(NETWORK_PATH, LOCATION_MAP['score'], files['score'])
        if not test_path(self.score):
            self.score = ""
        self.band_mp3 = os.path.join(NETWORK_PATH, LOCATION_MAP['band_mp3'], files['band_mp3'])
        if not test_path(self.band_mp3):
            self.band_mp3 = ""
        self.original_mp3 = os.path.join(NETWORK_PATH, LOCATION_MAP['original_mp3'], files['original_mp3'])
        if not test_path(self.original_mp3):
            self.original_mp3 = ""
        
def test_path(fpath) -> bool:
    return os.path.isfile(fpath)
    
DESTINATION_FOLDER = r'C:\Users\will\Desktop\song_export'
NETWORK_PATH = r'F:\Will\Music'
LOCATION_MAP = {
    'leadsheet': r'Scores\Mojos Onsong lead sheets',
    'editable_score': r'Scores\MuseScore scores',
    'score': r'Scores\Score PDF Exports',
    'band_mp3': r'Recordings\Smoking Mojos',
    'original_mp3': r'Recordings\Originals'
    }


song_library_path = os.path.join(os.path.dirname(__file__), 'library.json')
with open(song_library_path) as file_read:
    song_library = json.load(file_read)

setlist_folder = r'C:\Users\will\Documents\GitHub\music_organiser\Sets'
setlist_filename = r'SM 2024 Electric Set 1.txt'
setlist_path = os.path.join(os.path.dirname(__file__), setlist_folder, setlist_filename)
setlist = []
with open(setlist_path) as file_read:
    for line in file_read:
        setlist.append(line.rstrip("\n"))


songs = []
for song in setlist:
    
    try:
        songs.append(Song(song, song_library['Songs'][song]['Files']))
    except:
        print(f'The song {song} is not in the library')

pathlib.Path(f'{DESTINATION_FOLDER}\Leadsheets').mkdir(parents=True, exist_ok=True)
pathlib.Path(f'{DESTINATION_FOLDER}\Editable Scores').mkdir(parents=True, exist_ok=True)
pathlib.Path(f'{DESTINATION_FOLDER}\Scores').mkdir(parents=True, exist_ok=True)
pathlib.Path(f'{DESTINATION_FOLDER}\Band Version').mkdir(parents=True, exist_ok=True)
pathlib.Path(f'{DESTINATION_FOLDER}\Original Version').mkdir(parents=True, exist_ok=True)

for i, item in enumerate(songs):
    if item.leadsheet:
        file_name = f'{i + 1} {os.path.basename(item.leadsheet)}'
        d = os.path.join(DESTINATION_FOLDER, 'Leadsheets', file_name)
        shutil.copy(item.leadsheet, d)
    else:
        print(f'{item.name}: missing leadsheet')

    if item.editable_score:
        file_name = f'{i + 1} {os.path.basename(item.editable_score)}'
        d = os.path.join(DESTINATION_FOLDER, 'Editable Scores', file_name)
        shutil.copy(item.editable_score, d)
    else:
        print(f'{item.name}: missing editable score')
        
    if item.score:
        file_name = f'{i + 1} {os.path.basename(item.score)}'
        d = os.path.join(DESTINATION_FOLDER, 'Scores', file_name)
        shutil.copy(item.score, d)
    else:
        print(f'{item.name}: missing score')
        
    if item.band_mp3:
        file_name = f'{i + 1} {os.path.basename(item.band_mp3)}'
        d = os.path.join(DESTINATION_FOLDER, 'Band Version', file_name)
        shutil.copy(item.band_mp3, d)
    else:
        print(f'{item.name}: missing band mp3')
        
    if item.original_mp3:
        file_name = f'{i + 1} {os.path.basename(item.original_mp3)}'
        d = os.path.join(DESTINATION_FOLDER, 'Original Version', file_name)
        shutil.copy(item.original_mp3, d)
    else:
        print(f'{item.name}: missing original mp3')
    

    
