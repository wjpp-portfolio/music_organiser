import tkinter as tk
from tkinter import ttk
import yaml


def detect_yaml_duplicate_key(file) -> list:
    """Returns duplicate yaml keys.  Only detects top-level keys"""
    keys = []
    with open(file) as stream:
        for line in stream:
            line = line.split(':')[0]
            if ' ' not in line[0] and '#' not in line[0]: #if the first character is not a space or a comment then it is a yaml key
                keys.append(line)
    
    return [item for item in set(keys) if keys.count(item) > 1] #gets any item that appears in keys more than once
  
class Song():
    def __init__(self, name: str, in_library: bool, version: str = '',  data_object: object = object):
        self.in_library = in_library
        self.data = data_object
        self.song_title = name
        if self.in_library:
            self.display = f'{name} - {version}'   
            self.version = version
        else:
            self.display = f'{name} (not in library)' 
            self.version = ''

class SetList():
    def __init__(self, setlist_name: str, song_list: list = []):
        self.name = setlist_name
        self.songs = song_list
        self.changed = False

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.width = 700
        self.height = 500

        self.edge_padding = 10

        self.title('Music Organiser')
        self.protocol("WM_DELETE_WINDOW", self.exit_app)
        self.geometry(f'{self.width}x{self.height}-50+80')
        self.resizable(False, False)
        self.attributes('-topmost', 0)

    
        #self.grid(row=0, column=0, padx=self.edge_padding, pady=self.edge_padding) #this line is really important! without it nothing shows unless I use parent instead of self in View

        self.library_path = 'library.yml'
        self.setlists_path = 'setlists.yml'
        self.library = {}
        self.setlists = {}
        self.active_setlist = {}
        self.config = yaml.safe_load(open('config.yml'))
        self.import_library()
        
        self.enumerate_setlists()

        self.form_controls = {}     
        
        self.build_layout()
        self.populate_library_listbox()
        self.populate_setlists_optionmenu()

    def exit_app(self):
        print('Save Changes?')
        self.destroy()

    def build_layout(self) -> None:
        
        side_frames_scalar = 2.25
        remainder = self.width - ((self.width/side_frames_scalar) * 2)
        height = self.height * 0.75

        # TOP
        main_frame = tk.Frame(self, height=self.height, width=self.width)
        main_frame.pack(anchor='n', side='top', fill='both', padx=0, pady=0, expand=True) 

        # LEFT
        left_frame = tk.Frame(main_frame, height=height, width=self.width/side_frames_scalar)
        left_frame.pack_propagate(False)
        left_frame.pack(side='left', fill='none', padx=0, pady=0, expand=True)

        left_label_bar = tk.Frame(left_frame, width=50, height=50)
        left_label_bar.pack(side='top', fill='x', padx=0, pady=0, expand=False)
        tk.Label(left_label_bar, text="Set Lists", font=('Helvetica', 12, 'bold')).pack()

        left_button_bar = tk.Frame(left_frame, width=50, height=50)
        left_button_bar.pack(side='top', fill='x', padx=0, pady=0, expand=False)
        tk.Button(left_button_bar, text="Save Setlist", command=self.btn_setlist_save_clicked).pack(anchor='center', side='left', fill='x', expand=True, padx=5, pady=2)
        tk.Button(left_button_bar, text="Delete Setlist", command=self.btn_setlist_delete_clicked).pack(anchor='center', side='left', fill='x', expand=True, padx=5, pady=2)

        left_main_frame = tk.Frame(left_frame, width=0, height=0)
        left_main_frame.pack(side='top', fill='both', padx=0, pady=0, expand=True)

        self.form_controls['stringvar_setlists'] = tk.StringVar(self)
        self.form_controls['option_setlists'] = tk.OptionMenu(left_main_frame, self.form_controls['stringvar_setlists'], None, (), command=self.option_setlist_changed)
        self.form_controls['option_setlists'].pack(side='top', fill='x', expand=False, anchor='n')
     
        self.form_controls['lstbox_setlists'] = tk.Listbox(left_main_frame, selectmode='browse')
        self.form_controls['lstbox_setlists'].pack(side='top', fill='both', expand=True)
       
        tk.Button(left_main_frame, text="Export Files", command=self.btn_setlist_export_clicked).pack(anchor='center', side='bottom', fill='none', expand=False, padx=0, pady=10)

        # MIDDLE

        middle_frame = tk.Frame(main_frame, height=height, width=remainder)
        middle_frame.pack_propagate(False)
        middle_frame.pack(side='left', fill='none', padx=0, pady=0, expand=True)
        tk.Button(middle_frame, text="<", command=self.btn_add_to_setlist).pack(anchor='s', side='top', fill='none', expand=True, pady=10)
        tk.Button(middle_frame, text="X", fg='red', command=self.btn_remove_from).pack(anchor='n', side='top', fill='none', expand=True, pady=10)

        # RIGHT

        right_frame = tk.Frame(main_frame, height=self.height * 0.75, width=self.width/side_frames_scalar)
        right_frame.pack_propagate(False)
        right_frame.pack(side='left', fill='none', padx=0, pady=0, expand=True)

        right_label_bar = tk.Frame(right_frame, width=50, height=50)
        right_label_bar.pack(side='top', fill='x', padx=0,  pady=0, expand=False)
        tk.Label(right_label_bar, text="Library", font=('Helvetica', 12, 'bold')).pack()
    
        right_button_bar = tk.Frame(right_frame, width=50, height=50)
        right_button_bar.pack(side='top', fill='x', padx=0, pady=0, expand=False)
        tk.Button(right_button_bar, text="Add Song", command=self.btn_library_add_clicked).pack(anchor='center', side='left', fill='x',expand=True, padx=5, pady=2)
        tk.Button(right_button_bar, text="Edit Song", command=self.btn_library_edit_clicked).pack(anchor='center', side='left', fill='x',expand=True, padx=5, pady=2)

        right_main_frame = tk.Frame(right_frame, width=0, height=0)
        right_main_frame.pack(side='top', fill='both', padx=0, pady=0, expand=True)


        right_blanking_frame = tk.Frame(right_main_frame, width=0, height=31) #hight is hard-coded to correspond to height of setlist optionMeu.  .wininfo_height() doesn't set a value until after the parent form is set
        right_blanking_frame.pack(side='top', fill='x', padx=0, pady=0, expand=False)

        self.form_controls['lstbox_library'] = tk.Listbox(right_main_frame, selectmode='browse')
        self.form_controls['lstbox_library'].pack(anchor='center', side='top', fill='both', expand=True)

        tk.Button(right_main_frame, text="Close", command=self.btn_close_clicked).pack(anchor='center', side='bottom', fill='none', expand=False, padx=0, pady=10)

        # BOTTOM

        self.form_controls['label_log'] = tk.Listbox(self, height=int(self.height * 0.015), bg='white')
        self.form_controls['label_log'].pack(side='bottom', padx=0, pady=10, fill='both', expand=True)

    def btn_setlist_save_clicked(self):
        pass

    def btn_setlist_delete_clicked(self):
        pass

    def btn_library_add_clicked(self):
        pass

    def btn_library_edit_clicked(self):
        pass

    def option_setlist_changed(self, *args):
        self.clear_log()
        temp_song_list = []
        self.form_controls['stringvar_setlists'].set(args[0])
        for song in self.setlists[args[0]].songs:
            if not song.in_library:
                self.write_log(f'WARNING: setlist item not in library: {song.song_title}')
            else:
                temp_song_list.append(song.display)
        self.populate_listview_setlist(self.setlists[self.form_controls['stringvar_setlists'].get()].songs)

    def btn_add_to_setlist(self):
        library_selected_item = self.return_listbox_selected_item('lstbox_library')
        if library_selected_item:
            self.setlists[self.form_controls['stringvar_setlists'].get()].songs.append(self.library[library_selected_item])

        self.populate_listview_setlist(self.setlists[self.form_controls['stringvar_setlists'].get()].songs)

    def btn_remove_from(self):
        pass

    def btn_setlist_export_clicked(self):
        self.write_log('-----Exporting Setlist-----', True)

    def btn_close_clicked(self):
        self.exit_app()    

    def import_library(self):
        """Takes yaml library and turns each entry to discreet Song()"""
        for item in detect_yaml_duplicate_key(self.library_path):
            self.write_log(f'WARNING: Duplicate song in Library ({item}).  Using final library entry.  See {self.library_path} for guidance.')

        library = yaml.safe_load(open(self.library_path))

        for song_name, obj in library.items():
            for version, obj2 in obj['versions'].items():
                s = Song(name=song_name, version=version, data_object=obj2, in_library=True)
                self.library[s.display] = s

        self.library = dict(sorted(self.library.items()))

    def enumerate_setlists(self):
        '''Build each setlist and determine if any songs are not in the library'''
        setlists = yaml.safe_load(open(self.setlists_path))
        self.setlists['New Setlist'] = (SetList('New Setlist', []))
        self.active_setlist = self.setlists['New Setlist']
        list_of_songs = []
        for s, song_list in setlists.items():
            list_of_songs = []
            for song in song_list:
                if song in self.library:
                    list_of_songs.append(self.library[song])
                else:
                    list_of_songs.append(Song(name=song, in_library=False))
            self.setlists[s] = SetList(s, list_of_songs)

    def write_log(self, text: str, append: bool = True):
        if not append:
            self.clear_log()
        self.form_controls['label_log'].insert('end', text)
        self.form_controls['label_log'].yview_scroll(9999, 'page')

    def clear_log(self):
        self.form_controls['label_log'].delete('0', 'end')

    def clear_library(self):
        self.form_controls['lstbox_library'].delete('0', 'end')

    def clear_setlists(self):
        self.form_controls['lstbox_setlists'].delete('0', 'end')

    def populate_library_listbox(self):
        """clears library and re-writes all entries.  Does not do piecemeal"""
        self.clear_library()
        for name, obj in self.library.items():
            self.form_controls['lstbox_library'].insert('end', obj.display)

    def populate_setlists_optionmenu(self):
        s = []
        for set, songs in self.setlists.items():
            s.append(set)

        self.form_controls['option_setlists']['menu'].delete(0, 'end')
        #self.form_controls['stringvar_setlists'].set(s[0])
        self.option_setlist_changed(s[0])
        for i in s:
            self.form_controls['option_setlists']['menu'].add_command(label=i, command=lambda i=i: self.option_setlist_changed(i))


    def populate_listview_setlist(self, setlist_items: list[Song]):
        self.clear_setlists()
        if not setlist_items:
           return
         
        for item in setlist_items:
            self.form_controls['lstbox_setlists'].insert('end', item.display)
         
        #self.form_controls['option_setlists'] = tk.OptionMenu(left_main_frame, self.form_controls['stringvar_setlists'], None, (), command=self.controller.option_setlist_changed)
        #self.form_controls['option_setlists'].pack(side='top', fill='x', expand=False, anchor='n')
  
    def return_listbox_selected_item(self, listbox_name: str) -> str:
        '''returns first selected item  only'''
        index = self.form_controls[listbox_name].curselection()
        if index:
            return self.form_controls[listbox_name].get(index[0])
        else:
            return ''



        


if __name__ == '__main__':
    app = App()
    app.mainloop()

        