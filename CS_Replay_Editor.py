import json
import os
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, messagebox


class Replay:
    replay = None
    header = None

    def __init__(self, filename):
        self.filename = filename
        self.load(filename)

    def load(self, filename):
        # Load both the .replay and the .header files
        self.replay = ReplayFile(filename)
        self.header = HeaderFile(filename)

    def save(self, filename):
        # Save both the .replay and the .header files
        self.replay.save(filename)
        self.header.save(filename)

    def get_race_info(self):
        # Collect race information that should be displayed
        # Returns timestamp, track, path, scenario and scenario_index
        return self.header.get_race_info()

    def get_drivers(self):
        # Return a list of the drivers in the replay
        return self.replay.get_drivers()

    def get_driver_info(self, id):
        # Return the driver info needed for edit
        return self.replay.get_driver_info(id)

    def get_car_info(self, id):
        # Return the car info needed for edit
        return self.replay.get_car_info(id)

    def change_driver_info(self, id, driver_info):
        # Change the driver info in both the replay and the header
        self.replay.change_driver_info(id, driver_info)
        self.header.change_driver_info(id, driver_info)

    def change_car_info(self, id, car_info):
        # Change the driver info in both the replay and the header
        self.replay.change_car_info(id, car_info)
        self.header.change_car_info(id, car_info)


class ReplayFile:
    data = []

    def __init__(self, filename):
        self.filename = filename
        self.load(filename)

    def load(self, filename):
        # Decode .replay file from JSON format
        with open('{}.replay'.format(filename), 'r') as file:
            self.data = json.loads(file.readline())

    def save(self, filename):
        # Encode .replay file into JSON format
        with open('{}.replay'.format(filename), 'w') as file:
            file.write(json.dumps(self.data, separators=(',', ':')))

    def get_drivers(self):
        # Return a list of the drivers in the replay
        # Entries are tupels in the form: (racingTeamID, racerName, startPos)
        drivers = []
        for d in self.data:
            id = d['racingTeamID']
            name = d['racingTeamConfiguration']['racerName']
            grid = d['startPositionIndex'] + 1
            drivers.append((id, name, grid))
        return drivers

    def get_driver_info(self, id):
        # Return the driver info needed for edit
        # Search for correct driver in data
        for driver in self.data:
            if driver['racingTeamID'] == id:
                info = driver['racingTeamConfiguration']
                racername = info['racerName']
                driverskin = info['driverSkin']
                driverskinlivery = info['driverSkinLivery']
                helmet = info['helmet']
                helmetlivery = info['helmetLivery']
                idleanimation = info['idleAnimation']
                celebrationanimation = info['celebrationAnimation']
                return {'racerName': racername, 'driverSkin': driverskin,
                        'driverSkinLivery': driverskinlivery, 'helmet': helmet,
                        'helmetLivery': helmetlivery,
                        'idleAnimation': idleanimation,
                        'celebrationAnimation': celebrationanimation}
        # If id can't be found, return None
        return None

    def change_driver_info(self, id, driver_info):
        # Change the driver info in the replay
        # Search for correct driver in data
        for driver in self.data:
            if driver['racingTeamID'] == id:
                info = driver['racingTeamConfiguration']
                info['racerName'] = driver_info['racerName']
                info['driverSkin'] = driver_info['driverSkin']
                info['driverSkinLivery'] = driver_info['driverSkinLivery']
                info['helmet'] = driver_info['helmet']
                info['helmetLivery'] = driver_info['helmetLivery']
                info['idleAnimation'] = driver_info['idleAnimation']
                info['celebrationAnimation'] = driver_info['celebrationAnimation']

    def get_car_info(self, id):
        # Return the car info needed for edit
        # Search for correct driver in data
        for driver in self.data:
            if driver['racingTeamID'] == id:
                info = driver['racingTeamConfiguration']
                racername = info['racerName']
                vehicle = info['vehicle']
                vehiclelivery = info['vehicleLivery']
                return {'racerName': racername, 'vehicle': vehicle,
                        'vehicleLivery': vehiclelivery}
        # If Id can't be found, return None
        return None

    def change_car_info(self, id, car_info):
        # Change the car info in the replay
        # Search for correct driver in data
        for driver in self.data:
            if driver['racingTeamID'] == id:
                info = driver['racingTeamConfiguration']
                info['vehicle'] = car_info['vehicle']
                info['vehicleLivery'] = car_info['vehicleLivery']


class HeaderFile:
    data = {}

    def __init__(self, filename):
        self.filename = filename
        self.load(filename)

    def load(self, filename):
        # Decode .header file from JSON format
        with open('{}.header'.format(filename), 'r') as file:
            self.data = json.loads(file.readline())

    def save(self, filename):
        # Encode .header file into JSON format
        with open('{}.header'.format(filename), 'w') as file:
            file.write(json.dumps(self.data, separators=(',', ':')))

    def get_race_info(self):
        # Return race data
        timestamp = self.data['timeStampUtc']
        track = self.data['track']
        path = self.data['path']
        scenario = self.data['metadata']['scenario_name']
        scenario_index = self.data['metadata']['index_in_scenario']
        return timestamp, track, path, scenario, scenario_index

    def change_driver_info(self, id, driver_info):
        # Change the driver info in the header
        # Search for correct driver in data
        data = self.data['configsById']
        for driver in data:
            if driver == id:
                data[driver]['racerName'] = driver_info['racerName']
                data[driver]['driverSkin'] = driver_info['driverSkin']
                data[driver]['driverSkinLivery'] = driver_info[
                    'driverSkinLivery']
                data[driver]['helmet'] = driver_info['helmet']
                data[driver]['helmetLivery'] = driver_info['helmetLivery']
                data[driver]['idleAnimation'] = driver_info['idleAnimation']
                data[driver]['celebrationAnimation'] = driver_info[
                    'celebrationAnimation']

    def change_car_info(self, id, car_info):
        # Change the car info in the header
        # Search for correct driver in data
        data = self.data['configsById']
        for driver in data:
            if driver == id:
                data[driver]['vehicle'] = car_info['vehicle']
                data[driver]['vehicleLivery'] = car_info['vehicleLivery']


class Config:
    def __init__(self):
        # Open config file and read all entries
        # If the file doesn't exist, create it
        self.config = {}
        if os.path.isfile('config'):
            with open('config') as file:
                for line in file:
                    key, value = line.strip().split('=', 1)
                    self.config[key] = value
        else:
            open('config', 'a').close()

    def save_config(self):
        # Save config file
        with open('config', 'w') as file:
            for key in self.config:
                file.write('{}={}\n'.format(key, self.config[key]))

    def get_path(self):
        # Return path saved in config file
        # If path doesn't exist, set current path as default path and return it
        if 'PATH' in self.config:
            if os.path.exists(self.config['PATH']):
                return self.config['PATH']
        else:
            # Get current path
            path = os.getcwd()
            self.set_path(path)
            return path

    def set_path(self, path):
        # Update path in config file
        path = path.replace('\\', '/')  # No backslash in path
        if os.path.exists(path):
            self.config['PATH'] = path
            self.save_config()


class GUI:
    config = Config()
    dir = config.get_path()
    files = []
    selected = None
    replay_info = {}

    def __init__(self):
        # Create window
        self.root = tk.Tk()
        self.root.title('CS Replay Editor')
        self.root.resizable(False, False)

        # Adapt size of rows and columns to window
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)

        # Label and button to display and change the selected directory
        dir_select = tk.Frame(self.root)
        self.dir_label = tk.Label(dir_select, text=self.dir)
        self.dir_label.grid(column=0, row=0, sticky='nesw')
        dir_button = tk.Button(dir_select, text='Change',
                               command=self.change_directory)
        dir_button.grid(column=1, row=0, sticky='nesw')
        dir_select.grid(column=0, row=0, columnspan=2, sticky='nesw')

        # Listbox for all the replays that can be loaded
        replay_selection = tk.Frame(self.root)
        replay_selection.grid_columnconfigure(0, weight=1)  # Adapt to window
        self.replay_box = tk.Listbox(replay_selection, exportselection=False)
        self.replay_box.bind('<<ListboxSelect>>', self.replay_selected)
        self.replay_box.grid(column=0, row=0, sticky='nesw')
        scroll = tk.Scrollbar(replay_selection)
        scroll.grid(column=1, row=0, sticky='nesw')
        scroll.config(command=self.replay_box.yview)
        self.replay_box.config(yscrollcommand=scroll.set)
        replay_selection.grid(column=0, row=1, sticky='nesw')

        # Replay info and edit button
        rep_info = tk.Frame(self.root)
        rep_info.grid_columnconfigure(0, weight=1)  # Adapt to window
        self.info_1 = tk.Label(rep_info)
        self.info_1.grid(column=0, row=0, sticky='nesw')
        self.info_2 = tk.Label(rep_info)
        self.info_2.grid(column=0, row=1, sticky='nesw')
        self.info_3 = tk.Label(rep_info)
        self.info_3.grid(column=0, row=2, sticky='nesw')
        edit = tk.Button(rep_info, text='Edit', command=self.edit_replay)
        edit.grid(column=0, row=3, sticky='nesw')
        rep_info.grid(column=1, row=1, sticky='nesw')

        # Find replays in current directory
        self.load_replays()

        # Start mainloop for GUI
        self.root.mainloop()

    def load_replays(self):
        # Find loadable replays in current directory
        # Each replay consists of a .header and .replay file with the same name
        headers = []
        replays = []
        for file in os.listdir(self.dir):
            if file.endswith('.header'):
                headers.append(file[:-7])
            elif file.endswith('.replay'):
                replays.append(file[:-7])
        files = []
        for h in headers:
            if h in replays:
                files.append(h)
        # Update the filelist
        self.files = files

        # Clear listbox and insert possible replays into it
        self.replay_box.delete(0, 'end')
        self.replay_box.insert('end', *self.files)

    def change_directory(self):
        # Prompt user to change directory. Updates files if changed
        # Dialog will return '' if no directory has been selected, or the
        # selected directory otherwise
        new_dir = filedialog.askdirectory()
        if new_dir:
            if new_dir != self.dir:
                self.dir = new_dir
                self.dir_label.config(text=self.dir)
                self.load_replays()

                # Update config file
                self.config.set_path(self.dir)

                # Remove any replay infos stored or displayed from before
                self.replay_info = {}
                self.info_1.config(text='')
                self.info_2.config(text='')
                self.info_3.config(text='')

    def replay_selected(self, event):
        # If a replay is selected display replay info
        selection = self.replay_box.get(self.replay_box.curselection())
        # Only if a new replay is selected
        if self.selected != selection:
            self.selected = selection
            if selection not in self.replay_info:
                # Load info of replay file if not selected before
                self.replay_info[selection] = Replay(
                    os.path.join(self.dir, selection)).get_race_info()
            # Display replay info on screen
            info = self.replay_info[selection]
            self.info_1.config(text='{} (#{})'.format(info[3], info[4]))
            self.info_2.config(text='{} ({})'.format(info[1], info[2]))
            self.info_3.config(text=info[0])

    def edit_replay(self):
        # Open the edit window for the selected replay
        if self.selected:
            edit = EditGUI(os.path.join(self.dir, self.selected))
            # Hide main window until the edit window is closed
            self.root.withdraw()
            edit.window.wait_window()
            self.root.deiconify()
            self.load_replays()


class EditGUI:
    changed = False
    name_labels = {}
    driver_buttons = {}
    car_buttons = {}

    def __init__(self, filename):
        self.filename = filename

        # Load replay file
        self.replay = Replay(filename)
        self.drivers = self.replay.get_drivers()

        # Create popup window
        self.window = tk.Toplevel()
        self.window.title('Edit Replay')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.grab_set()
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(3, weight=1)

        # Replay info as headline
        info = self.replay.get_race_info()
        headline = tk.Label(
            self.window, text='{} (#{}) - {} ({}) - {}'.format(
                info[3], info[4], info[1], info[2], info[0]))
        headline.grid(column=0, row=0, columnspan=4, sticky='nesw')

        # Create list of drivers with edit buttons
        # Headline for each column
        tk.Label(self.window, text='Name').grid(column=0, row=1, sticky='nesw')
        tk.Label(self.window, text='Driver').grid(column=1, row=1, sticky='nesw')
        tk.Label(self.window, text='Car').grid(column=2, row=1, sticky='nesw')
        tk.Label(self.window, text='Grid').grid(column=3, row=1, sticky='nesw')
        # Individual rows per driver
        i = 2
        for driver in self.drivers:
            id = driver[0]
            name = tk.Label(self.window, text=driver[1])
            name.grid(column=0, row=i, sticky='nesw')
            self.name_labels[id] = name
            d_edit = tk.Button(self.window, text='Edit',
                               command=lambda id=id: self.edit_driver(id))
            d_edit.grid(column=1, row=i, sticky='nesw')
            self.driver_buttons[id] = d_edit
            c_edit = tk.Button(self.window, text='Edit',
                               command=lambda id=id: self.edit_car(id))
            c_edit.grid(column=2, row=i, sticky='nesw')
            self.car_buttons[id] = c_edit
            grid = tk.Label(self.window, text=driver[2])
            grid.grid(column=3, row=i, sticky='nesw')
            i += 1

        # Create save button
        save_button = tk.Button(self.window, text='Save changes', bg='#ACACAC',
                                command=self.save_changes)
        save_button.grid(column=0, row=i, columnspan=4, sticky='nesw')

        # Set changed flag to False
        self.changed = False

    def update_names(self):
        # In case a name has been changed, update all entries in the list
        new_drivers = self.replay.get_drivers()
        if new_drivers != self.drivers:
            self.drivers = new_drivers
            for d in self.drivers:
                id = d[0]
                name = d[1]
                self.name_labels[id].config(text=name)

    def edit_driver(self, id):
        # Open an edit window for the selected driver
        edit = EditDriverGUI(self, self.replay, id)
        edit.window.wait_window()
        self.update_names()

    def edit_car(self, id):
        # Open an edit window for the selected car
        edit = EditCarGUI(self, self.replay, id)
        edit.window.wait_window()
        self.update_names()

    def save_changes(self):
        # Prompt user to select filename for changed replay (and header)
        # Dialog will return '' if no filename has been selected, or the
        # selected filename otherwise
        curr_path, curr_file = os.path.split(self.filename)
        save_location = filedialog.asksaveasfilename(
            defaultextension='.replay',
            filetypes=(('Replay and header files', '*.replay;*.header'),
                       ('All Files', '*.*')),
            initialdir=curr_path,
            initialfile='{}.replay'.format(curr_file))
        if save_location:
            if (save_location.endswith('.replay') or
                    save_location.endswith('.header')):
                # Remove extension (not needed in Replay class)
                save_location = save_location[:-7]
            # Save the replay and header file with the specified filename
            self.replay.save(save_location)

        self.changed = False

    def set_changed(self, event=None):
        # Set changed flag to True
        self.changed = True

    def close_window(self):
        # Check if there have been changes
        # If so, ask if they should be saved
        if self.changed:
            save = messagebox.askyesnocancel(
                'Save changes?', 'Do you want to save your changes?')
            if save is None:  # Cancel selected
                return
            elif save:  # Yes selected
                self.save_changes()
            else:  # No selected
                pass
        self.window.destroy()


class EditDriverGUI:
    # Track if there have been changes
    changed = False
    saved_name = None
    saved_color_suit = None
    saved_color_helmet = None

    # Values for liveries and designs for GUI and replay files
    # Might be incomplete and can change in future updates of the game

    # Suit
    # Values for GUI
    suit_body = ['Female', 'Male']
    suit_design = ['Asymmetric', 'Classic', 'Dragon', 'Honor', 'Oil', 'Roads',
                   'Royal', 'Satelite', 'Sidelines', 'Slick', 'Split',
                   'Stripes']
    # Values for replay file
    suit_driverskin = {'Female': 'driverskin-classic-f',
                       'Male': 'driverskin-classic-m'}
    suit_driverskinlivery = {
        'Female': {
            'Asymmetric': 'driverskinmaterial-asymmetric-f-1',
            'Classic': 'driverskinmaterial-classic-f-0',
            'Dragon': 'driverskinmaterial-arrows-f-2',
            'Honor': 'driverskinmaterial-9-f-1',
            'Oil': 'driverskinmaterial-oil-f-3',
            'Roads': 'driverskinmaterial-7-f-1',
            'Royal': 'driverskinmaterial-diagonals-f-1',
            'Satelite': 'driverskinmaterial-satellite-f-3',
            'Sidelines': 'driverskinmaterial-10-f-1',
            'Slick': 'driverskinmaterial-6-f-1',
            'Split': 'driverskinmaterial-split-f-1',
            'Stripes': 'driverskinmaterial-stripes-f-1'
        },
        'Male': {
            'Asymmetric': 'driverskinmaterial-asymmetric-m-1',
            'Classic': 'driverskinmaterial-classic-m-0',
            'Dragon': 'driverskinmaterial-arrows-m-2',
            'Honor': 'driverskinmaterial-9-m-1',
            'Oil': 'driverskinmaterial-oil-m-3',
            'Roads': 'driverskinmaterial-7-m-1',
            'Royal': 'driverskinmaterial-diagonals-m-1',
            'Satelite': 'driverskinmaterial-satellite-m-3',
            'Sidelines': 'driverskinmaterial-10-m-1',
            'Slick': 'driverskinmaterial-6-m-1',
            'Split': 'driverskinmaterial-split-m-1',
            'Stripes': 'driverskinmaterial-stripes-m-1'
        }
    }
    # Reverse to get the GUI values from the replay value
    inv_driverskinlivery = {}
    for i in suit_driverskinlivery.items():
        for j in i[1].items():
            inv_driverskinlivery[j[1]] = (i[0], j[0])

    # Helmet
    # Values for GUI
    helmet_helmet = ['Classic', 'Modern', 'Ace']
    helmet_design = {
        'Classic': ['Simple', 'Parallel', 'Classic', 'Vintage'],
        'Modern': ['Simple', 'Space', 'Trace', 'Belts', 'Arrow', 'Eyes',
                   'Banner', 'Gradient', 'Jaw', 'Apex'],
        'Ace': ['Simple', 'Layers', 'Abstract', 'Demon', 'Headband', 'Blade']
    }
    # Values for replay file
    helmet_helmet_value = {
        'Classic': 'helmet-0-classic-open-face',
        'Modern': 'helmet-1-modern-full-face',
        'Ace': 'helmet-2-contemporary-full-face'
    }
    helmet_helmetlivery = {
        'Classic': {
            'Simple': 'helmetmaterial-classic-open-face-0',
            'Parallel': 'helmetmaterial-classic-open-face-1',
            'Classic': 'helmetmaterial-classic-open-face-2',
            'Vintage': 'helmetmaterial-classic-open-face-3'
        },
        'Modern': {
            'Simple': 'helmetmaterial-modern-full-face-0',
            'Space': 'helmetmaterial-modern-full-face-1',
            'Trace': 'helmetmaterial-modern-full-face-2',
            'Belts': 'helmetmaterial-modern-full-face-3',
            'Arrow': 'helmetmaterial-modern-full-face-4',
            'Eyes': 'helmetmaterial-modern-full-face-5',
            'Banner': 'helmetmaterial-modern-full-face-6',
            'Gradient': 'helmetmaterial-modern-full-face-7',
            'Jaw': 'helmetmaterial-modern-full-face-8',
            'Apex': 'helmetmaterial-modern-full-face-9'
        },
        'Ace': {
            'Simple': 'helmetmaterial-contemporary-full-face-0',
            'Layers': 'helmetmaterial-contemporary-full-face-1',
            'Abstract': 'helmetmaterial-contemporary-full-face-2',
            'Demon': 'helmetmaterial-contemporary-full-face-3',
            'Headband': 'helmetmaterial-contemporary-full-face-4',
            'Blade': 'helmetmaterial-contemporary-full-face-5'
        }
    }
    # Reverse to get the GUI values from the replay value
    inv_helmetlivery = {}
    for i in helmet_helmetlivery.items():
        for j in i[1].items():
            inv_helmetlivery[j[1]] = (i[0], j[0])

    def __init__(self, parent, replay, id):
        self.parent = parent
        self.replay = replay
        self.id = id

        # Load curent data out of the replay file
        self.driver_info = self.replay.get_driver_info(id)
        racername = self.driver_info['racerName']

        # Create popup window
        self.window = tk.Toplevel()
        self.window.title('Edit Driver')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.grab_set()
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(3, weight=1)

        # racerName as headline
        self.headline = tk.Label(self.window,
                                 text='Edit {}'.format(racername))
        self.headline.grid(column=0, row=0, columnspan=4, sticky='nesw')

        # Edit racerName
        text_name = tk.Label(self.window, text='Name')
        text_name.grid(column=0, row=1, sticky='nesw')
        self.name_field = tk.Entry(self.window)
        self.name_field.insert(0, racername)
        self.name_field.grid(column=1, row=1, columnspan=2, sticky='nesw')

        # Edit driverSkin and driverSkinLivery
        # All designs are available for all bodys => set dropdown values
        text_skin = tk.Label(self.window, text='Skin')
        text_skin.grid(column=0, row=2, sticky='nesw')
        self.body_dd = ttk.Combobox(self.window, values=self.suit_body,
                                    exportselection=False)
        self.body_dd.grid(column=1, row=2, sticky='nesw')
        self.body_dd.bind('<<ComboboxSelected>>', self.set_changed)
        self.suit_design_dd = ttk.Combobox(self.window, values=self.suit_design)
        self.suit_design_dd.grid(column=2, row=2, sticky='nesw')
        self.suit_design_dd.bind('<<ComboboxSelected>>', self.set_changed)
        self.suit_color = ColorPalette(self.window, 3)
        self.suit_color.grid(column=3, row=2, sticky='nesw')

        # Edit helmet and helmetLivery
        # Each helmet has its own set of designs that have to be loaded into
        # the second dropdown menu
        text_helmet = tk.Label(self.window, text='Helmet')
        text_helmet.grid(column=0, row=3, sticky='nesw')
        self.helmet_dd = ttk.Combobox(self.window, values=self.helmet_helmet,
                                      exportselection=False)
        self.helmet_dd.grid(column=1, row=3, sticky='nesw')
        self.helmet_dd.bind('<<ComboboxSelected>>', self.helmet_selected)
        self.helmet_design_dd = ttk.Combobox(self.window, values=[])
        self.helmet_design_dd.grid(column=2, row=3, sticky='nesw')
        self.helmet_design_dd.bind('<<ComboboxSelected>>', self.set_changed)
        self.helmet_color = ColorPalette(self.window, 5)
        self.helmet_color.grid(column=3, row=3, sticky='nesw')

        # Save changes button
        self.save_button = tk.Button(self.window, text='Save changes',
                                     bg='#ACACAC', command=self.save)
        self.save_button.grid(column=0, row=4, columnspan=4, sticky='nesw')

        # Set the selected values to the current values out of the replay file
        self.load_current_values(self.driver_info)

        # Set changed flag to False and remember name value
        self.saved_name = racername
        self.saved_color_suit = self.suit_color.get_colors()
        self.saved_color_helmet = self.helmet_color.get_colors()
        self.changed = False

    def load_current_values(self, driver_info):
        # Track if there have been changes
        changed = False

        # Set the values currently set in the replay file (if possible)
        driverskinlivery = driver_info['driverSkinLivery'][0]
        helmetlivery = driver_info['helmetLivery'][0]
        if driverskinlivery in self.inv_driverskinlivery:
            body_curr, body_design_curr = self.inv_driverskinlivery[
                driverskinlivery]
        else:
            body_curr, body_design_curr = None, None
        if helmetlivery in self.inv_helmetlivery:
            helmet_curr, helmet_design_curr = self.inv_helmetlivery[
                helmetlivery]
        else:
            helmet_curr, helmet_design_curr = None, None

        # Suit body and design
        if body_curr in self.suit_body and body_design_curr in self.suit_design:
            self.body_dd.current(self.suit_body.index(body_curr))
            self.suit_design_dd.current(
                self.suit_design.index(body_design_curr))
        else:
            self.body_dd.current(0)
            self.suit_design_dd.current(0)
        suit_colors = driver_info['driverSkinLivery'][1]
        self.suit_color.set_colors(suit_colors)

        # Helmet and design
        # Set selected helmet first, then update values for design
        if helmet_curr in self.helmet_helmet:
            self.helmet_dd.current(self.helmet_helmet.index(helmet_curr))
            self.helmet_selected()  # Load values for second dropdown box
            if helmet_design_curr in self.helmet_design[helmet_curr]:
                self.helmet_design_dd.current(
                    self.helmet_design[helmet_curr].index(
                        helmet_design_curr))
            else:
                self.helmet_design_dd.current(0)
        else:
            self.helmet_dd.current(0)
            self.helmet_design_dd.current(0)
        helmet_colors = driver_info['helmetLivery']
        helmet_colors = [helmet_colors[1], helmet_colors[2], helmet_colors[3],
                         helmet_colors[4], helmet_colors[5]]
        self.helmet_color.set_colors(helmet_colors)

    def helmet_selected(self, event=None):
        # Executed when the helmet dropdown box is selected
        # Load the correct values in the second dropdown box
        body = self.helmet_dd.get()
        self.helmet_design_dd.config(values=self.helmet_design[body])
        self.helmet_design_dd.current(0)
        self.set_changed()

    def save(self):
        def restore_elements():
            # Restore style of changed elements after (un)successful saving
            self.save_button.config(bg='#ACACAC', text='Save changes')
            self.name_field.config(bg='#FFFFFF')

        driver_info = self.driver_info
        # Get values from GUI elements
        name = self.name_field.get()
        suit = self.body_dd.get()
        suit_design = self.suit_design_dd.get()
        suit_colors = self.suit_color.get_colors()
        helmet = self.helmet_dd.get()
        helmet_design = self.helmet_design_dd.get()
        helmet_colors = self.helmet_color.get_colors()
        # Get values for replay file
        # Add colors to liveries, like in replay file
        driverskinlivery = [self.suit_driverskinlivery[suit][suit_design],
                            suit_colors]
        driverskin = self.suit_driverskin[suit]
        helmetlivery = [self.helmet_helmetlivery[helmet][helmet_design],
                        helmet_colors[0], helmet_colors[1], helmet_colors[2],
                        helmet_colors[3], helmet_colors[4]]
        helmet = self.helmet_helmet_value[helmet]

        # Check if values are valid
        # Name has to be in ascii
        if not all(ord(c) < 128 for c in name):
            # Change color of button and text field to red
            self.save_button.config(bg='#FF0000', text='Invalid input')
            self.name_field.config(bg='#FF0000')
            self.window.after(2000, restore_elements)
            return False

        # Change values in driver info to selected values in the GUI
        driver_info['racerName'] = name
        driver_info['driverSkin'] = driverskin
        driver_info['driverSkinLivery'] = driverskinlivery
        driver_info['helmet'] = helmet
        driver_info['helmetLivery'] = helmetlivery

        # Update values in replay, set changed flag to False and remember values
        self.replay.change_driver_info(self.id, driver_info)
        self.changed = False
        self.saved_name = name
        self.saved_color_suit = self.suit_color.get_colors()
        self.saved_color_helmet = self.helmet_color.get_colors()
        self.parent.set_changed()

        # Change color and text of button
        self.save_button.config(bg='#00FF00', text='Changes saved')
        self.window.after(2000, restore_elements)

        return True

    def set_changed(self, event=None):
        # Set changed flag to True
        self.changed = True

    def close_window(self):
        # Check if there have been changes
        # If so, ask if they should be saved
        if (self.changed or self.saved_name != self.name_field.get() or
                self.saved_color_suit != self.suit_color.get_colors() or
                self.saved_color_helmet != self.helmet_color.get_colors()):
            save = messagebox.askyesnocancel(
                'Save changes?', 'Do you want to save your changes?')
            if save is None:  # Cancel selected
                return
            elif save:  # Yes selected
                saved = self.save()
                # Don't destroy the window if there has been illegal input
                if not saved:
                    return
            else:  # No selected
                pass
        self.window.destroy()


class EditCarGUI:
    # Track if there have been changes
    changed = False
    saved_number = None
    saved_car_color = None

    # Values for liveries and designs for GUI and replay files
    # Might be incomplete and can change in future updates of the game
    # Thanks to Kikwik for helping me gather the design names

    # Car
    # Values for GUI
    car_car = ['Agitator', 'Bonk', 'Conquest', 'Feather', 'Loose Cannon',
               'Mantra', 'Osprey', 'Panther', 'Piccino', 'Vost']
    car_design = {
        'Agitator': ['Factory', 'Blocks', 'Groove', 'Arrow', 'Boulder',
                     'Highway'],
        'Bonk': ['Factory', 'Tour', 'Bonk', 'Duo', 'Escalator', 'Cyclops'],
        'Conquest': ['Factory', 'Myth', 'Demonic', 'Livery 4', 'Livery 5',
                     'Livery 6', 'Livery 7', 'Livery 8'],
        'Feather': ['Factory', 'Classic', 'Prince', 'Vintage', 'Cara', 'Knight',
                    'Livery 7'],
        'Loose Cannon': ['Factory', 'Snake', 'Desert', 'Transform', 'Bumper',
                         'Fine', 'Rear', 'Vintage', 'Livery 9'],
        'Mantra': ['Factory', 'Pro', 'Radiant', 'Ferocce', 'Slick', 'Layers',
                   'Triangle', 'Modern', 'Livery 9'],
        'Osprey': ['Factory', 'Forge', 'Dive', 'Faccia', 'Wind', 'Speed',
                   'Livery 7', 'Livery 8'],
        'Panther': ['Factory', 'Classic', 'Contrast', 'Champion', 'Dagger',
                    'Abstract', 'Livery 7', 'Uncharted', 'Boost'],
        'Piccino': ['Factory', 'Classic', 'Trace', 'Livery 4', 'Livery 5',
                    'Livery 6', 'Livery 7', 'Livery 8', 'Gift'],
        'Vost': ['Factory', 'Stripes', 'Champion', 'Demon', 'Geometric']
    }
    # Values for replay file
    car_vehicle = {
        'Agitator': '4x4-agitator',
        'Bonk': 'eurotruck-geiger',
        'Conquest': 'prototype-conquest',
        'Feather': 'superlights-feather',
        'Loose Cannon': 'trans-am-generic',
        'Mantra': '80s-gp-generic',
        'Osprey': '60s-gp-osprey',
        'Panther': 'gt-panther',
        'Piccino': 'bambino-cup-bambino',
        'Vost': 'rally-vost'
    }
    car_vehiclelivery = {
        'Agitator': {
            'Factory': 'vehiclematerial-4x4-agitator-0',
            'Blocks': 'vehiclematerial-4x4-alligator-1',
            'Groove': 'vehiclematerial-4x4-alligator-2',
            'Arrow': 'vehiclematerial-4x4-alligator-3',
            'Boulder': 'vehiclematerial-4x4-alligator-4',
            'Highway': 'vehiclematerial-4x4-alligator-5'
        },
        'Bonk': {
            'Factory': 'vehiclematerial-eurotruck-geiger-0',
            'Tour': 'vehiclematerial-eurotruck-geiger-1',
            'Bonk': 'vehiclematerial-eurotruck-geiger-2',
            'Duo': 'vehiclematerial-eurotruck-geiger-3',
            'Escalator': 'vehiclematerial-eurotruck-geiger-4',
            'Cyclops': 'vehiclematerial-eurotruck-geiger-5'
        },
        'Conquest': {
            'Factory': 'vehiclematerial-prototype-conquest-0',
            'Myth': 'vehiclematerial-prototype-conquest-1',
            'Demonic': 'vehiclematerial-prototype-conquest-2',
            'Livery 4': 'vehiclematerial-prototype-conquest-3',
            'Livery 5': 'vehiclematerial-prototype-conquest-4',
            'Livery 6': 'vehiclematerial-prototype-conquest-5',
            'Livery 7': 'vehiclematerial-prototype-conquest-6',
            'Livery 8': 'vehiclematerial-prototype-conquest-7',
        },
        'Feather': {
            'Factory': 'vehiclematerial-superlights-feather-0',
            'Classic': 'vehiclematerial-superlights-feather-1',
            'Prince': 'vehiclematerial-superlights-feather-2',
            'Vintage': 'vehiclematerial-superlights-feather-3',
            'Cara': 'vehiclematerial-superlights-feather-4',
            'Knight': 'vehiclematerial-superlights-feather-5',
            'Livery 7': 'vehiclematerial-superlights-feather-6',
        },
        'Loose Cannon': {
            'Factory': 'vehiclematerial-trans-am-generic-0',
            'Snake': 'vehiclematerial-trans-am-generic-1',
            'Desert': 'vehiclematerial-trans-am-generic-2',
            'Transform': 'vehiclematerial-trans-am-generic-3',
            'Bumper': 'vehiclematerial-trans-am-generic-4',
            'Fine': 'vehiclematerial-trans-am-generic-5',
            'Rear': 'vehiclematerial-trans-am-generic-6',
            'Vintage': 'vehiclematerial-trans-am-generic-7',
            'Livery 9': 'vehiclematerial-trans-am-generic-8'
        },
        'Mantra': {
            'Factory': 'vehiclematerial-80s-gp-generic-0',
            'Pro': 'vehiclematerial-80s-gp-generic-1',
            'Radiant': 'vehiclematerial-80s-gp-generic-2',
            'Ferocce': 'vehiclematerial-80s-gp-generic-3',
            'Slick': 'vehiclematerial-80s-gp-generic-4',
            'Layers': 'vehiclematerial-80s-gp-generic-5',
            'Triangle': 'vehiclematerial-80s-gp-generic-6',
            'Modern': 'vehiclematerial-80s-gp-generic-7',
            'Livery 9': 'vehiclematerial-80s-gp-generic-8'
        },
        'Osprey': {
            'Factory': 'vehiclematerial-60s-gp-osprey-0',
            'Forge': 'vehiclematerial-60s-gp-osprey-1',
            'Dive': 'vehiclematerial-60s-gp-osprey-2',
            'Faccia': 'vehiclematerial-60s-gp-osprey-3',
            'Wind': 'vehiclematerial-60s-gp-osprey-4',
            'Speed': 'vehiclematerial-60s-gp-osprey-5',
            'Livery 7': 'vehiclematerial-60s-gp-osprey-6',
            'Livery 8': 'vehiclematerial-60s-gp-osprey-7'
        },
        'Panther': {
            'Factory': 'vehiclematerial-gt-panther-0',
            'Classic': 'vehiclematerial-gt-panther-1',
            'Contrast': 'vehiclematerial-gt-panther-2',
            'Champion': 'vehiclematerial-gt-panther-3',
            'Dagger': 'vehiclematerial-gt-panther-4',
            'Abstract': 'vehiclematerial-gt-panther-5',
            'Livery 7': 'vehiclematerial-gt-panther-6',
            'Uncharted': 'vehiclematerial-gt-panther-7',
            'Boost': 'vehiclematerial-gt-panther-8'
        },
        'Piccino': {
            'Factory': 'vehiclematerial-piccino-cup-0',
            'Classic': 'vehiclematerial-piccino-cup-1',
            'Trace': 'vehiclematerial-piccino-cup-2',
            'Livery 4': 'vehiclematerial-piccino-cup-3',
            'Livery 5': 'vehiclematerial-piccino-cup-4',
            'Livery 6': 'vehiclematerial-piccino-cup-5',
            'Livery 7': 'vehiclematerial-piccino-cup-6',
            'Livery 8': 'vehiclematerial-piccino-cup-7',
            'Gift': 'vehiclematerial-piccino-cup-8'
        },
        'Vost': {
            'Factory': 'vehiclematerial-rally-vost-0',
            'Stripes': 'vehiclematerial-rally-vost-1',
            'Champion': 'vehiclematerial-rally-vost-2',
            'Demon': 'vehiclematerial-rally-vost-3',
            'Geometric': 'vehiclematerial-rally-vost-4'
        }
    }
    # Reverse to get the GUI values from the replay value
    inv_vehiclelivery = {}
    for i in car_vehiclelivery.items():
        for j in i[1].items():
            inv_vehiclelivery[j[1]] = (i[0], j[0])

    def __init__(self, parent, replay, id):
        self.parent = parent
        self.replay = replay
        self.id = id

        # Load current data out of the replay file
        self.car_info = self.replay.get_car_info(id)
        racername = self.car_info['racerName']

        # Create popup window
        self.window = tk.Toplevel()
        self.window.title('Edit Car')
        self.window.protocol('WM_DELETE_WINDOW', self.close_window)
        self.window.grab_set()
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_columnconfigure(1, weight=1)
        self.window.grid_columnconfigure(2, weight=1)
        self.window.grid_columnconfigure(3, weight=1)

        # racerName as headline
        self.headline = tk.Label(self.window,
                                 text='Edit {}'.format(racername))
        self.headline.grid(column=0, row=0, columnspan=4, sticky='nesw')

        # Edit vehicle and vehicleLivery
        # Each car has its own set of designs that have to be loaded into
        # the second dropdown menu
        text_car = tk.Label(self.window, text='Car')
        text_car.grid(column=0, row=1, sticky='nesw')
        self.car_dd = ttk.Combobox(self.window, values=self.car_car,
                                   exportselection=False)
        self.car_dd.grid(column=1, row=1, sticky='nesw')
        self.car_dd.bind('<<ComboboxSelected>>', self.car_selected)
        self.car_design_dd = ttk.Combobox(self.window, values=[])
        self.car_design_dd.grid(column=2, row=1, sticky='nesw')
        self.car_design_dd.bind('<<ComboboxSelected>>', self.set_changed)
        self.car_color = ColorPalette(self.window, 4)
        self.car_color.grid(column=3, row=1, sticky='nesw')

        # Edit car number
        number = self.car_info['vehicleLivery'][2]
        text_number = tk.Label(self.window, text='Number')
        text_number.grid(column=0, row=2, sticky='nesw')
        self.number_field = tk.Entry(self.window)
        self.number_field.insert(0, number)
        self.number_field.grid(column=1, row=2, sticky='nesw')

        # Save changes button
        self.save_button = tk.Button(self.window, text='Save changes',
                                     bg='#ACACAC', command=self.save)
        self.save_button.grid(column=0, row=3, columnspan=4, sticky='nesw')

        # Set the selected values to the current values out of the replay file
        self.load_current_values(self.car_info)

        # Set changed flag to False and remember number and color values
        self.saved_number = number
        self.saved_car_color = self.car_color.get_colors()
        self.changed = False

    def load_current_values(self, car_info):
        # Set the values currently set in the replay file (if possible)
        vehiclelivery = car_info['vehicleLivery'][0]
        if vehiclelivery in self.inv_vehiclelivery:
            vehicle_curr, design_curr = self.inv_vehiclelivery[vehiclelivery]
        else:
            vehicle_curr, design_curr = None, None

        # Car and design
        if vehicle_curr in self.car_car:
            self.car_dd.current(self.car_car.index(vehicle_curr))
            self.car_selected()  # Load values for second dropdown box
            if design_curr in self.car_design[vehicle_curr]:
                self.car_design_dd.current(
                    self.car_design[vehicle_curr].index(design_curr))
            else:
                self.car_design_dd.current(0)
        else:
            self.car_dd.current(0)
            self.car_design_dd.current(0)

        car_colors = car_info['vehicleLivery'][1]
        self.car_color.set_colors(car_colors)

    def car_selected(self, event=None):
        # Executed when the car dropdown box is selected
        # Load the correct values in the second dropdown box
        car = self.car_dd.get()
        self.car_design_dd.config(values=self.car_design[car])
        self.car_design_dd.current(0)

    def save(self):
        def restore_elements():
            # Restore style of changed elements after (un)successful saving
            self.save_button.config(bg='#ACACAC', text='Save changes')
            self.number_field.config(bg='#FFFFFF')

        car_info = self.car_info
        # Get values from GUI elements
        car = self.car_dd.get()
        design = self.car_design_dd.get()
        car_colors = self.car_color.get_colors()
        number = self.number_field.get()

        # Check if values are valid
        # Number has to be between 0 and 99
        if not number.isdecimal() or not 0 <= int(number) <= 99:
            # Change color of button and text field to red
            self.save_button.config(bg='#FF0000', text='Invalid input')
            self.number_field.config(bg='#FF0000')
            self.window.after(2000, restore_elements)
            return False
        number = int(number)

        # Get values for replay file
        # Add colors to liveries, like in replay file
        vehiclelivery = [self.car_vehiclelivery[car][design], car_colors,
                         number]
        vehicle = self.car_vehicle[car]

        # Change values in driver info to selected values in the GUI
        car_info['vehicle'] = vehicle
        car_info['vehicleLivery'] = vehiclelivery

        # Update values in replay, set changed flag to False and remember values
        self.replay.change_car_info(self.id, car_info)
        self.changed = False
        self.saved_number = number
        self.saved_car_color = car_colors
        self.parent.set_changed()

        # Change color and text of button
        self.save_button.config(bg='#00FF00', text='Changes saved')
        self.window.after(2000, restore_elements)

        return True

    def set_changed(self, event=None):
        # Set changed flag to True
        self.changed = True

    def close_window(self):
        # Check if there have been changes
        # If so, ask if they should be saved
        if (self.changed or str(self.saved_number) != self.number_field.get() or
                self.saved_car_color != self.car_color.get_colors()):
            save = messagebox.askyesnocancel(
                'Save changes?', 'Do you want to save your changes?')
            if save is None:  # Cancel selected
                return
            elif save:  # Yes selected
                saved = self.save()
                # Don't destroy the window if there has been illegal input
                if not saved:
                    return
            else:  # No selected
                pass
        self.window.destroy()


class ColorPalette(tk.Frame):
    # Frame containing a specified amount of buttons with color choosers
    def __init__(self, parent, colors=1):
        tk.Frame.__init__(self, parent)
        self.colors = []

        # Always have at least one color, also if input is invalid
        if not isinstance(colors, int) or colors < 1:
            colors = 1

        # Add the color buttons
        for i in range(colors):
            self.grid_columnconfigure(i, weight=1)
            button = tk.Button(self, bg='#FFFFFF', text='   ',
                               command=lambda x=i: self.choose_color(x))
            button.grid(column=i, row=0, sticky='nesw')
            self.colors.append(button)

    def choose_color(self, index):
        # Open a color chooser window and change the color of the button
        color = colorchooser.askcolor(parent=self)[1]
        self.colors[index].config(bg=color)

    def set_colors(self, colors):
        # Set the colors of the buttons to the colors of the given list
        # Only if the right amount of colors is given
        num_buttons = len(self.colors)
        if isinstance(self.colors, list) and num_buttons == len(colors):
            for i in range(len(self.colors)):
                if colors[i].startswith('#'):
                    self.colors[i].config(bg=colors[i])
                else:
                    self.colors[i].config(bg='#{}'.format(colors[i]))

    def get_colors(self):
        # Return a list of the colors selected
        colors = []
        for button in self.colors:
            colors.append(button.cget('bg')[1:])
        return colors


def main():
    GUI()


if __name__ == '__main__':
    main()
