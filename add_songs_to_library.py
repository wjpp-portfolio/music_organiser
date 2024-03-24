import tkinter as tk
from tkinter import ttk
from functools import partial
import configparser, os, types, math, json, re

class gui:
    def __init__(self) -> None:
        self.form = tk.Tk()
        self.form.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.form.geometry("550x500-50+80")
        self.form.title('Import song')
        self.form.resizable(True, True)
        self.form.attributes('-topmost', 1)
        
        self.form_controls = {}
        self.form_variables = {}
        self.form_controls['lbl_search_term'] = self.add_label('Search term:', 0, 0)

        self.form_variables['txt_search_term'] = tk.StringVar(self.form)
        self.form_variables['txt_search_term'].set('')
        self.form_controls['txt_search_term'] = self.add_textbox(1, 0 , self.form_variables['txt_search_term'])

        self.form_controls['btn_search'] = self.add_button('Search', 2, 0, self.search, self.form_controls['txt_search_term'].get())

        self.form_controls['lst_leadsheet'] = self.add_listbox(1, 2, [1,2,3,4,5])
        self.form_controls['lst_leadsheet'] = self.add_listbox(2, 2, [1,2,3,4,5])

        self.form.mainloop()

    def on_closing(self):
        self.form.destroy()

    def add_label(self, text: str, col: int, row: int, colour: str = '#000') -> tk.Label:
        l = ttk.Label(self.form, text=f'{text}', foreground=colour)
        l.grid(column=col, row=row, padx=5, pady=5, sticky=tk.EW)
        #l.bind("<Button-1>", lambda e:self.lbl_click(text))
        return l
    
    def add_textbox(self, col: int, row: int, stringVar: str) -> tk.Entry:
        t = ttk.Entry(self.form, textvariable=stringVar)
        t.grid(column=col, row=row)
        return t

    def add_button(self, text: str, col: int, row: int, command_function: types.FunctionType, p: any = None) -> tk.Button:
        b = ttk.Button(self.form, text=text, command=partial(command_function, p))
        b.grid(column=col, row=row, padx=0, pady=0, sticky=tk.E)
        return b
    
    def add_listbox(self, col, row, list_items) -> tk.Listbox:
        l = tk.Listbox()
        l.insert(0, *list_items)
        l.grid(column=col, row=row)
        return l

    def search(self, term: str):
        print(term)

#frm = gui()
LIBRARY_PATH = os.path.join(os.path.dirname(__file__), 'library.json')
NETWORK_PATH = r'Z:\Will\Music'
LOCATION_MAP = {
    'leadsheet': r'Scores\Mojos Onsong lead sheets',
    'editable_score': r'Scores\MuseScore scores',
    'score': r'Scores\Score PDF Exports',
    'band_mp3': r'Recordings\Smoking Mojos',
    'original_mp3': r'Recordings\Originals'
    }


def get_file_choice(search_term, search_location):
    l = []
    for obj in os.listdir(search_location):
        if os.path.isfile(os.path.join(search_location, obj)):
            if search_term.lower() in obj.lower():
            #a = re.search(search_term.lower(), obj.lower())
            #if a:
                l.append(obj)

    if not l:
        print('No match, continuing...')
        return None
    else:
        for i, j in enumerate(l):
            print(f'{i+1}. {j}')

        choice = input('Which item? ')

        return l[int(choice)-1]

def write_to_library(song_name, title_map):
    d = { song_name: {'files': title_map}}

    with open(LIBRARY_PATH) as file_read:
        json_data = json.load(file_read)

 
 
    if song_name in json_data['songs']:
        print(f'ERROR: {song_name} already exists as a song name')
        return


    json_data['songs'].update(d)

    with open(LIBRARY_PATH, 'w') as file_write:
       json.dump(json_data, file_write)

search_term = input('Enter search term: ')

mapping = {}
for k in LOCATION_MAP.keys():
    print(f'----- {k} -----')
    search_location = os.path.join(NETWORK_PATH, LOCATION_MAP[k])
    mapping[k] = get_file_choice(search_term, search_location)

song_name = input('Enter song name for library: ')
print('')
print(f'### {song_name} ###')
print('')
for k in mapping.keys():
    print(f'{mapping[k]}')

write = input('Write to library (y/n): ')

if 'y' in write:
    print('')
    write_to_library(song_name, mapping)