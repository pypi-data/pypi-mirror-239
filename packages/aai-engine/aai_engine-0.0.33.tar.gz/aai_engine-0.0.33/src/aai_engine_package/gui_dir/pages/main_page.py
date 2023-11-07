import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel
import os
import glob
from PIL.PngImagePlugin import PngImageFile

# own imports
from aai_engine_package.screenshot_taker import MessageBox
from ..utils.capture import Capture


MIN_WIDTH = 900
MIN_HEIGHT = 550
SHOW_IMAGE_PADDING = 300


class MainPage(tk.Frame):
    """Class to manage the main view of the application.
    """

    def __init__(self, parent, data, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.parent = parent
        self.data = data
        self.button_width = 10

        # Create the paned window and the main frame
        self.paned_window = tk.PanedWindow(self, orient=tk.HORIZONTAL)
        self.main_frame = tk.Frame(self.paned_window)

        # Create the frame for the label and the listbox
        self.label_listbox_frame = tk.Frame(self.paned_window)

        # Create the label and pack it into the label_listbox_frame
        self.label = tk.Label(self.label_listbox_frame, text="Screenshots",
                              bg="gray25", fg="white", font=("Arial", 12))
        self.label.pack(fill=tk.X)

        # Create the listbox and pack it into the label_listbox_frame
        self.lst = tk.Listbox(self.label_listbox_frame, width=20)
        self.lst.bind("<<ListboxSelect>>", self._show_img)
        self.lst.pack(fill=tk.BOTH, expand=1)

        # Add the label_listbox_frame and the main frame to the paned window
        self.paned_window.add(self.label_listbox_frame)
        self.paned_window.add(self.main_frame)

        # Pack the paned window into the frame
        self.paned_window.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # Create the label for displaying the image and pack it into the main frame
        self.show_img = tk.Label(self.main_frame, text="")
        self.show_img.pack()

        # Create the canvas and pack it into the main frame
        self.canvas = tk.Canvas(self.main_frame)
        self.canvas.pack()

        # Create the edit button and pack it into the main frame
        edit_button = ttk.Button(
            self.main_frame,
            text="Edit",
            command=self._edit_img,
            style='Accent.TButton',
            width=self.button_width
        )
        edit_button.pack(pady=(25, 50), side=tk.BOTTOM)

        # Create the delete button and pack it into the main frame
        delete_button = ttk.Button(
            self.main_frame,
            text="Delete",
            command=self._delete_img,
            style='Accent.TButton',
            width=self.button_width
        )
        delete_button.pack(pady=(25, 0), side=tk.BOTTOM)

        directory = self.parent.get_workdir()
        print("directory: ", directory)
        self._load_files(directory)

    # Observes application data (mainly current directory)
    def on_data_update(self, directory):
        """_summary_

        Args:
            directory (_type_): _description_
        """
        # Check if directory is valid
        if os.path.isdir(directory):
            self._load_files(directory)
        else:
            print(f"{directory} is not a valid directory!")

    def _load_files(self, directory):
        """_summary_

        Args:
            directory (_type_): _description_
        """
        self.lst.delete(0, tk.END)  # clear previously opened folder list
        imgs = glob.glob(os.path.join(directory, '*.png'))
        for img in imgs:
            # get the filename without the directory path
            img_name = os.path.basename(img)
            self.lst.insert(tk.END, img_name)

        if self.lst.size() > 0:
            self.lst.selection_set(0)  # select first item of the list to show
            self._show_img(None)  # show to selected item

    def _delete_img(self):
        """On click function for the deletion of an image
        """
        selec = self.lst.curselection()
        filename = os.path.join(self.data.directory, self.lst.get(selec))
        answer = askyesnocancel(
            "Deleting image", f"Are you sure you want to delete {filename}?")
        if answer:
            os.remove(filename)
            print(f"Deleted image: {filename}")
            # Refresh the current directory
            self.on_data_update(self.data._directory)

    def _edit_img(self):
        """_summary_
        """
        selec = self.lst.curselection()
        try:
            filename = os.path.join(self.data.directory, self.lst.get(selec))
            print(f"Edit image: {filename}")
            img = PngImageFile(filename)
            img_keys = list(img.text.keys())
            if ('offset_x' not in img_keys) or ('offset_y' not in img_keys) or ('upper_confidence' not in img_keys) or ('lower_confidence' not in img_keys):
                print("  -The image does not contain the right metadata!")
                return

            if 'ocr_box_relative' in img.text:
                MessageBox(
                    self, self.parent,
                    "GUI - Message",
                    "You cannot edit OCR images because the OCR box could be placed outside the needle image!\nPlease create a new OCR image instead. (File -> new OCR)",
                    (650, 170)
                )
            else:
                Capture.screen_capture(
                    self.data.directory, update_function_after_edit=self._load_files, needle=filename, editing=True)
        except Exception as ex:
            print("Image could not be edited!")

    def process_ocr_box(self, ocr_box):
        """Processes the ocr_box metadata into readable information

        Args:
            ocr_box (str): ocr_box metadata

        Returns:
            str: The processed metadata
        """
        info = ocr_box[1:-1].split(',')
        result = "This is an OCR image. It has an OCR box attached to it, where you can perform OCR operations.\n"
        result += "The OCR box is drawn at the given offset, seen from the top left of the image \n"
        result += "The following metadata of the OCR box is available: \n"
        result += f"Offset=({info[0]},{info[1]}) - width: {info[2]}, height: {info[3]})"
        return result

    def _show_img(self, event):
        """_summary_

        Args:
            event (_type_): _description_
        """
        try:
            selec = self.lst.curselection()
            filename = os.path.join(self.data.directory, self.lst.get(selec))

            img = tk.PhotoImage(file=filename)
            metadata = PngImageFile(filename).text
            if 'ocr_box_relative' in metadata.keys():
                self.show_img.configure(
                    text=self.process_ocr_box(metadata['ocr_box_relative']))
            else:
                self.show_img.configure(text="")
            width, height = img.width(), img.height()
            print(f"Currently showing: {filename}")
            self.canvas.image = img
            self.canvas.config(width=width, height=height)
            self.canvas.create_image((width/2), (height/2), image=img)
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

            # Adjust screensize to image dimensions
            height = img.height()
            width = img.width()
            # Height setting:
            if (height + SHOW_IMAGE_PADDING) > MIN_HEIGHT:
                height += SHOW_IMAGE_PADDING
                if height > self.parent.parent.winfo_screenheight():
                    height = self.parent.parent.winfo_screenheight()
            else:
                height = MIN_HEIGHT
            # Width setting:
            if (width + SHOW_IMAGE_PADDING) > MIN_WIDTH:
                width += SHOW_IMAGE_PADDING
                if width > self.parent.parent.winfo_screenwidth():
                    width = self.parent.parent.winfo_screenwidth()
            else:
                width = MIN_WIDTH
            self.parent.parent.geometry(f"{str(width)}x{str(height)}")
            print(f"New window dimensions: ({str(width)},{str(height)})")

        except Exception as ex:
            print(ex)
            self.canvas.delete("all")
            print("Image could not be shown!")
