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


DESTINATION_FOLDER = r'C:\Users\will\Desktop\song_export'
NETWORK_PATH = r'Z:\Will\Music'
LOCATION_MAP = {
    'leadsheet': r'Scores\Mojos Onsong lead sheets',
    'editable_score': r'Scores\MuseScore scores',
    'score': r'Scores\Score PDF Exports',
    'band_mp3': r'Recordings\Smoking Mojos',
    'original_mp3': r'Recordings\Originals'
    }

errors = []
song_library_path = os.path.join(os.path.dirname(__file__), 'library.json')

#read library json
with open(song_library_path) as file_read:
    song_library = json.load(file_read)


search_location = os.path.join(os.path.dirname(__file__), 'Sets')

for setlist_filename in os.listdir(search_location):
    setlist = []
    setlist_path = os.path.join(search_location, setlist_filename)
    if os.path.isfile(setlist_path):
  
        setlist_name_no_extension = pathlib.Path(setlist_filename).stem
        print(f'### {setlist_name_no_extension} ###')

        #read set list txt
        with open(setlist_path) as file_read:
            for line in file_read:
                setlist.append(line.rstrip("\n"))

        #create folder structure

        for t in LOCATION_MAP.keys():
            if t in song_library['config']['audio']:
                media_type = 'audio'
            elif t in song_library['config']['visual']:
                media_type = 'visual'
            else:
                continue
            pathlib.Path(os.path.join(DESTINATION_FOLDER, media_type, setlist_name_no_extension, t)).mkdir(parents=True, exist_ok=True)

        for index, song in enumerate(setlist):
            song = format_song_name(song)
            print(f'processing {song}...')
            if song in song_library['songs']:
                for i in song_library['songs'][song]['files']:
                    mt = [k for k,v in song_library['config'].items() if i in v]
                    if not mt:
                        continue

                    #if i in song_library['config'][media_type]:
                    try:
                        file_path = os.path.join(NETWORK_PATH, LOCATION_MAP[i], song_library['songs'][song]['files'][i])
                        test_path(file_path)
                    except:
                        errors.append(f'{i} for {song} does not exist')
                        continue

                    numbered_file_name = f'{index + 1:02d} {os.path.basename(file_path)}'

                    destination_numbered_file_path = os.path.join(DESTINATION_FOLDER, mt[0], setlist_name_no_extension, i, numbered_file_name)
                    shutil.copy(file_path, destination_numbered_file_path)
                    
            else:
                errors.append(f'The song {song} is not in the library')

print('')
for e in errors:
    print(e)