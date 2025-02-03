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
    def __init__(self, name: str, passed: object):
        self.song_title = name
        self.data = passed

class SetList():
    def __init__(self, setlist_name: str, song_list: list = []):
        self.name = setlist_name
        self.songs = song_list


class Model():
    def __init__(self):
        self.log_messsage = []
        self.library_path = 'library.yml'
        self.setlists_path = 'setlists.yml'
        self.library = {}
        self.config = yaml.safe_load(open('config.yml'))
        self.import_library()
        self.enumerate_setlists()
        

    def import_library(self):
        """Takes yaml library and turns each entry to discreet Song()"""

        for item in detect_yaml_duplicate_key(self.library_path):
            self.post_warning_to_log(f'WARNING: Duplicate song in Library ({item}).  Using final library entry.  See {self.library_path} for guidance.')

        library = yaml.safe_load(open(self.library_path))

        for song_name, obj in library.items():
            for version, obj2 in obj['versions'].items():
                self.library[f'{song_name} - {version}'] = Song(song_name, obj2)

        self.library = dict(sorted(self.library.items()))

    def post_warning_to_log(self, message):
        self.log_messsage.append(message)

    def enumerate_setlists(self):
        self.setlists = []
        setlists = yaml.safe_load(open(self.setlists_path))
        self.setlists.append(SetList('New Setlist'))
        for s, song_list in setlists.items():
            self.setlists.append(SetList(s, song_list))      

class View(tk.Frame):
    def __init__(self, parent, width, height):
        super().__init__(parent)
        self.form_controls = {}
        self.width = width
        self.height = height

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
        tk.Button(left_button_bar, text="Save Setlist", command=self.controller.btn_setlist_save_clicked).pack(anchor='center', side='left', fill='x', expand=True, padx=5, pady=2)
        tk.Button(left_button_bar, text="Delete Setlist", command=self.controller.btn_setlist_delete_clicked).pack(anchor='center', side='left', fill='x', expand=True, padx=5, pady=2)

        left_main_frame = tk.Frame(left_frame, width=0, height=0)
        left_main_frame.pack(side='top', fill='both', padx=0, pady=0, expand=True)

        self.form_controls['stringvar_setlists'] = tk.StringVar(self)
        self.form_controls['option_setlists'] = tk.OptionMenu(left_main_frame, self.form_controls['stringvar_setlists'], None, (), command=self.controller.option_setlist_changed)
        self.form_controls['option_setlists'].pack(side='top', fill='x', expand=False, anchor='n')
     
        self.form_controls['lstbox_setlists'] = tk.Listbox(left_main_frame, selectmode='browse')
        self.form_controls['lstbox_setlists'].pack(side='top', fill='both', expand=True)
       
        tk.Button(left_main_frame, text="Export Files", command=self.controller.btn_setlist_export_clicked).pack(anchor='center', side='bottom', fill='none', expand=False, padx=0, pady=10)

        # MIDDLE

        middle_frame = tk.Frame(main_frame, height=height, width=remainder)
        middle_frame.pack_propagate(False)
        middle_frame.pack(side='left', fill='none', padx=0, pady=0, expand=True)
        tk.Button(middle_frame, text="<", command=self.controller.btn_add_to_setlist).pack(anchor='s', side='top', fill='none', expand=True, pady=10)
        tk.Button(middle_frame, text="X", fg='red', command=self.controller.btn_remove_from).pack(anchor='n', side='top', fill='none', expand=True, pady=10)

        # RIGHT

        right_frame = tk.Frame(main_frame, height=self.height * 0.75, width=self.width/side_frames_scalar)
        right_frame.pack_propagate(False)
        right_frame.pack(side='left', fill='none', padx=0, pady=0, expand=True)

        right_label_bar = tk.Frame(right_frame, width=50, height=50)
        right_label_bar.pack(side='top', fill='x', padx=0,  pady=0, expand=False)
        tk.Label(right_label_bar, text="Library", font=('Helvetica', 12, 'bold')).pack()
    
        right_button_bar = tk.Frame(right_frame, width=50, height=50)
        right_button_bar.pack(side='top', fill='x', padx=0, pady=0, expand=False)
        tk.Button(right_button_bar, text="Add Song", command=self.controller.btn_library_add_clicked).pack(anchor='center', side='left', fill='x',expand=True, padx=5, pady=2)
        tk.Button(right_button_bar, text="Edit Song", command=self.controller.btn_library_edit_clicked).pack(anchor='center', side='left', fill='x',expand=True, padx=5, pady=2)

        right_main_frame = tk.Frame(right_frame, width=0, height=0)
        right_main_frame.pack(side='top', fill='both', padx=0, pady=0, expand=True)


        right_blanking_frame = tk.Frame(right_main_frame, width=0, height=31) #hight is hard-coded to correspond to height of setlist optionMeu.  .wininfo_height() doesn't set a value until after the parent form is set
        right_blanking_frame.pack(side='top', fill='x', padx=0, pady=0, expand=False)

        self.form_controls['lstbox_library'] = tk.Listbox(right_main_frame, selectmode='browse')
        self.form_controls['lstbox_library'].pack(anchor='center', side='top', fill='both', expand=True)

        tk.Button(right_main_frame, text="Close", command=self.controller.btn_close_clicked).pack(anchor='center', side='bottom', fill='none', expand=False, padx=0, pady=10)

        # BOTTOM

        self.form_controls['label_log'] = tk.Listbox(self, height=int(self.height * 0.015), bg='white')
        self.form_controls['label_log'].pack(side='bottom', padx=0, pady=10, fill='both', expand=True)

    def set_controller(self, controller) -> None:
        self.controller = controller

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

    def add_item_to_library_listbox(self, items: str):
        """clears library and re-writes all entries.  Does not do piecemeal"""
        self.clear_library()
        for item in items:
            self.form_controls['lstbox_library'].insert('end', item)

    def populate_option_setlists(self, items: list):
        self.form_controls['option_setlists']['menu'].delete(0, 'end')
        self.form_controls['stringvar_setlists'].set(items[0])
        for i in items:
            self.form_controls['option_setlists']['menu'].add_command(label=i, command=lambda i=i: self.controller.option_setlist_changed(i))


    def populate_listview_setlist(self, setlist_items: list):
        self.clear_setlists()
        if not setlist_items:
           return
         
        for item in setlist_items:
            self.form_controls['lstbox_setlists'].insert('end', item)
         
        #self.form_controls['option_setlists'] = tk.OptionMenu(left_main_frame, self.form_controls['stringvar_setlists'], None, (), command=self.controller.option_setlist_changed)
        #self.form_controls['option_setlists'].pack(side='top', fill='x', expand=False, anchor='n')
  
    def return_listbox_selected_item(self, listbox_name: str) -> str:
        '''returns first selected item  only'''
        a = self.form_controls[listbox_name].curselection()
        if a:
            return self.form_controls[listbox_name].get(a[0])
        else:
            return ''


class Controller(tk.Tk):
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

        # create a model
        self.model = Model()

        # create a view and place it on the root window
        self.view = View(self, self.width - (self.edge_padding * 2), self.height - (self.edge_padding * 2))
        
        self.view.grid(row=0, column=0, padx=self.edge_padding, pady=self.edge_padding) #this line is really important! without it nothing shows unless I use parent instead of self in View

        #self.controller = Controller(model, view)
        self.view.set_controller(self)
        self.view.build_layout()
        self.write_library_import_warnings()
        self.write_library_items()
        self.populate_setlist_option_menu()

    def exit_app(self):
        print('Save Changes?')
        self.destroy()

    def option_setlist_changed(self, *args):
        self.view.clear_log()
        self.view.form_controls['stringvar_setlists'].set(args[0])
        for s in self.model.setlists:
            if s.name == args[0]:   
                temp_song_list = s.songs.copy()
                for each_song in temp_song_list.copy():
                    if each_song not in self.model.library:
                        temp_song_list.remove(each_song)
                        self.view.write_log(f'WARNING: setlist item not in library: {each_song}')             
                self.write_setlist_items(temp_song_list)

    def btn_setlist_save_clicked(self):
        pass

    def btn_setlist_delete_clicked(self):
        pass

    def btn_library_add_clicked(self):
        pass

    def btn_library_edit_clicked(self):
        pass

    def btn_add_to_setlist(self):
        print(self.view.return_listbox_selected_item('lstbox_library'))

    def btn_remove_from(self):
        pass

    def btn_setlist_export_clicked(self):
        self.view.write_log('-----Exporting Setlist-----', True)

    def btn_close_clicked(self):
        self.exit_app()

    def write_library_import_warnings(self):
        for item in self.model.log_messsage:
            self.view.write_log(item)
        self.model.log_messsage = []

    def write_library_items(self):
        self.view.add_item_to_library_listbox(self.model.library.keys())

    def write_setlist_items(self, items: list):
        self.view.populate_listview_setlist(items)

    def populate_setlist_option_menu(self):
        s = []
        for item in self.model.setlists:
            s.append(item.name)
        self.view.populate_option_setlists(s)
        


if __name__ == '__main__':
    app = Controller()
    app.mainloop()

        