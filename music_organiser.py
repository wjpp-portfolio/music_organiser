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

def copy_file(index: int, full_file_path: str, file_type: str, collection: str, setlist_name_no_extension: str):
    if not full_file_path:
        return
    else:
        numbered_file_name = f'{index + 1:02d} {os.path.basename(full_file_path)}'
        destination_numbered_file_path = os.path.join(DESTINATION_FOLDER, file_type, setlist_name_no_extension, collection, numbered_file_name)
        pathlib.Path(os.path.join(DESTINATION_FOLDER, file_type, setlist_name_no_extension, collection)).mkdir(parents=True, exist_ok=True)
        shutil.copy(full_file_path, destination_numbered_file_path)

def identify_file(media_type: str, fallback_media_type: str, song_library: dict, song_name: str) -> str:

    if song_library['songs'][song_name]['files'][media_type]:
        track_type = media_type
        song_name_inc_ext = song_library['songs'][song_name]['files'][media_type]
    else:
        print(f'WARNING: {media_type} for {song_name} is missing.')
        if fallback_media_type and song_library['songs'][song_name]['files'][fallback_media_type]:
            track_type = fallback_media_type
            song_name_inc_ext = song_library['songs'][song_name]['files'][fallback_media_type]
        else:
            return ''
        
    file_path = os.path.join(NETWORK_PATH, song_library['config']['file_locations'][track_type], song_name_inc_ext)
    if test_path(file_path):
        return file_path
    else:
        print(f'{file_path} does not exist')
        return ''
        

DESTINATION_FOLDER = r'C:\Users\will\Desktop\song_export'
NETWORK_PATH = r'Z:\Will\Music'
LIBRARY = 'library.json'

song_library_path = os.path.join(os.path.dirname(__file__), LIBRARY)

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

        for index, song in enumerate(setlist):
            song = format_song_name(song)
            print(f'processing {song}...')
            if song in song_library['songs']:

                copy_file(index, identify_file('score', 'leadsheet', song_library, song), 'visual', 'scores', setlist_name_no_extension)
                copy_file(index, identify_file('leadsheet', '', song_library, song), 'visual', 'leadsheets', setlist_name_no_extension)
                copy_file(index, identify_file('band_mp3', 'original_mp3', song_library, song), 'audio', 'band', setlist_name_no_extension)
                copy_file(index, identify_file('original_mp3', '', song_library, song), 'audio', 'originals', setlist_name_no_extension)

            else:
                print(f'The song {song} is not in the library')
