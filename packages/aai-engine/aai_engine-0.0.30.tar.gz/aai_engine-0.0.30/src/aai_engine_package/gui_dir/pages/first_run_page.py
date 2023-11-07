import tkinter as tk
from tkinter import ttk
import os

MIN_WIDTH = 900
MIN_HEIGHT = 550


class FirstRunPage(tk.Frame):
    """Page to select work dir during first run of the application.
    """

    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.data = data
        self.button_width = 10

        self.parent = parent

        self.title = tk.Label(
            self, text="Select a directory to work in", font=("Arial", 20))
        self.title.pack(pady=(50, 50))

        self.work_dir = tk.StringVar()
        self.work_dir.set(os.getcwd())
        self.work_dir_entry = tk.Entry(
            self, textvariable=self.work_dir, width=80)
        self.work_dir_entry.pack(pady=(20, 20))

        self.work_dir_button = ttk.Button(
            self, text="Select",
            command=self._select_dir,
            style='Accent.TButton',
            width=self.button_width
        )
        self.work_dir_button.pack(pady=(20, 20))

    def _select_dir(self):
        """Select a directory to work in.
        """
        # Use select dir function from MainApplication
        self.parent.select_dir(self.data)

        # Open main page
        self.destroy()
        self.parent.open_main_page(self.data)
