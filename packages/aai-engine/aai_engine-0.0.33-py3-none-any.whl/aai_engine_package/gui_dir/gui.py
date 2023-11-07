"""GUI for managing the screenshots"""
import argparse
import sys
import os
import tkinter as tk
from tkinter import filedialog as fd
from tkinter.messagebox import askyesnocancel
import yaml

# own imports
from .utils.capture import Capture
from .pages.main_page import MainPage
from .pages.first_run_page import FirstRunPage
from .style.theme import Theme
from aai_engine_package.screenshot_taker import MessageBox


WORKDIR = None
REMEMBER = False
NORMAL_SCREENSHOT = 0
OCR_SCREENSHOT = 1

# Handling of first run and remembering workdir
dirname = os.path.dirname(__file__)
try:
    with open(os.path.join(dirname, "workdir_config.yml"), "r", encoding="utf-8") as config:
        conf = yaml.load(config, yaml.Loader)
        WORKDIR = conf['WORKDIR']
        REMEMBER = conf['REMEMBER']
except:
    print("Something went wrong with the config file. Please check if the file exists and is valid.")


class ApplicationData():
    """Class to keep track of application data and notify the listeners.
    """

    def __init__(self):
        self._directory = ""
        self._observers = []

    @property
    def directory(self):
        """return directory
        """
        return self._directory

    def _observed(func):
        def wrapper(self, value):
            func(self, value)  # call setter function

            # notify all observers (initiate their callbacks)
            for callback in self._observers:
                callback(self._directory)

        return wrapper

    @directory.setter
    @_observed
    def directory(self, value):
        print(f"Setting new directory: {value}")
        self._directory = value

    def bind_to(self, callback):
        """bind to
        """
        self._observers.append(callback)

# END ApplicationData
# --- --- --- --- --- --- --- --- ---
# START GUI


class Toolbar(tk.Frame):
    """Class to manage the toolbar for application level funcitons.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.save_location = WORKDIR
        menubar = tk.Menu(self.parent.master)
        self.parent.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Select directory", command=self.on_open)
        file_menu.add_command(label="New", command=self.on_new)
        file_menu.add_command(label="New OCR", command=self.on_new_ocr)
        file_menu.add_command(label="Refresh", command=self.on_refresh)
        menubar.add_cascade(label="File", menu=file_menu)

    def on_open(self):
        """_summary_
        """
        # Use select dir function from MainApplication
        self.parent.select_dir(self.parent.data)

    def on_new(self):
        """_summary_
        """
        print("save loc: ", self.save_location)
        Capture.screen_capture(self.save_location,
                               update_function_after_edit=self.parent.load_files, screenshot_type=NORMAL_SCREENSHOT)

    def on_new_ocr(self):
        """_summary_
        """
        Capture.screen_capture(self.save_location,
                               update_function_after_edit=self.parent.load_files, screenshot_type=OCR_SCREENSHOT)

    def on_refresh(self):
        """_summary_
        """
        self.save_location = self.save_location


class MainApplication(tk.Frame):
    """Class to group all UI elements.
    """

    def __init__(self, parent, command_line_options, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.master.title("AAI Image manager")
        self.parent = parent
        self.data = ApplicationData()

        parent.tk.call('source', Theme.get_theme_path())
        parent.tk.call("set_theme", "dark")

        if WORKDIR is None or REMEMBER == False:
            print(self.data)
            self.open_first_run_page(self.data)
        else:
            print(self.data)
            self.open_main_page(self.data)


        print("The command line arguments are:")
        for key, value in command_line_options.items():
            print(f"  -Name= {key}, Value= {value}")

        self.data.directory = command_line_options['d']

    def select_dir(self, data):
        """_summary_
        """
        directory = fd.askdirectory(master=self.parent)
        if isinstance(directory, str):
            self.data.directory = directory
            WORKDIR = directory
            ApplicationData.directory = directory

            # Ask if user wants to remember the directory
            confirm = askyesnocancel(
                "Confirm", "Do you want to remember this directory?")
            if confirm is not None:
                if confirm:
                    REMEMBER = True
                else:
                    REMEMBER = False

                # Write to config file
                yaml.dump(
                    {'WORKDIR': WORKDIR, 'REMEMBER': REMEMBER},
                    open(os.path.join(dirname, "workdir_config.yml"),
                         "w", encoding="utf-8")
                )
        else:
            MessageBox.showerror("Error", "Please select a valid directory")

    def get_workdir(self):
        """_summary_
        """
        dirname = os.path.dirname(__file__)

        try:
            with open(os.path.join(dirname, "workdir_config.yml"), "r", encoding="utf-8") as config:
                conf = yaml.load(config, yaml.Loader)
                return conf['WORKDIR']
        except:
            print(
                "Something went wrong with the config file. Please check if the file exists and is valid.")

    def open_first_run_page(self, data):
        self.first_run_page = FirstRunPage(self, data)
        self.first_run_page.pack(expand=1)

    def open_main_page(self, data):
        """_summary_
        """
        self.toolbar = Toolbar(self)
        self.main = MainPage(self, data)

        # main view observes the data
        data.bind_to(self.main.on_data_update)

        self.toolbar.pack(side="top", fill="x")
        self.main.pack(side="right", fill="both", expand=True)

    def load_files(self, directory):
        """_summary_
        """
        self.main._load_files(directory)


def get_args():
    """Parser for the command line options of the GUI

    Returns:
        dict: Dictionary of the command line options
    """
    parser = argparse.ArgumentParser("Arguments for the GUI")

    # Add arguments here:
    if WORKDIR is not None:
        parser.add_argument(
            "-d", metavar="DIRECTORY", type=str,
            help="Enter a directory where the application will look for png images",
            default=WORKDIR  # Use workdir if it got a value
        )
    else:
        # Fall back for when config file is empty
        parser.add_argument(
            "-d", metavar="DIRECTORY", type=str,
            help="Enter a directory where the application will look for png images",
            default=os.path.join(os.path.expanduser('~'), "Pictures")
        )

    return vars(parser.parse_args())


def cli():
    """_summary_
    """
    if len(sys.argv) == 2:
        save_location = sys.argv[1]
        print(os.getcwd(), save_location)
    else:
        print("ERROR: Please provide your desired save location, eg: aai-engine-capture './path/to/location'")
        return
    print("Called aai-engine-capture")
    Capture.screen_capture(save_location)


def test_edit(save_location, param2):
    """Edit stub
    """
    pass


def edit(save_location, haystack):
    """Calls the edit routine
    """
    Capture.screen_capture(save_location, haystack, editing=True)


def main():
    """The main function for the GUI
    """
    args = get_args()
    root = tk.Tk()
    root.geometry("800x495+50+50")
    MainApplication(root, args).pack(side="top", fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
