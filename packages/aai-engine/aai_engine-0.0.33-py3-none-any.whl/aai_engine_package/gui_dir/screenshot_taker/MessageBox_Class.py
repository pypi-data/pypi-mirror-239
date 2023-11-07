import tkinter
from tkinter import ttk

class MessageBox():
    """A message box class
    """
    def __init__(self, parent_class, parent, title, message, dim):
        self.parent_class = parent_class
        self.parent = parent
        self.top = tkinter.Toplevel(self.parent)
        self.top.geometry(f"{dim[0]}x{dim[1]}")
        self.top.transient(self.parent)

        self.top.title(title)
        self.frame0 = ttk.Frame(self.top)
        self.top.l1 = ttk.Label(self.frame0, text=message)
        self.top.l1.pack(pady=30)
        self.frame0.pack()
        self.top.grab_set()
        self.top.f1 = ttk.Frame(self.top)
        button = ttk.Button(self.top, text="OK", command=self.destroy_widget)
        button.pack(side=tkinter.BOTTOM, padx = 10, pady = 20)
        self.top.f1.pack()

    def destroy_widget(self):
        """setter for value
        """
        self.top.destroy()