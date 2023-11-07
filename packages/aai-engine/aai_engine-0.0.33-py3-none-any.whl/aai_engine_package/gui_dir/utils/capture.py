import os
import sys
import tkinter as tk
import tempfile
from tkinter import ttk
from random import choice
from string import digits

# own imports
from ..style.theme import Theme
from aai_engine_package.engine_util import screenshot
from aai_engine_package.screenshot_taker import ScreenShotTaker, NORMAL_SCREENSHOT

class Capture():
    @staticmethod
    def screen_capture(save_location, update_function_after_edit=None, needle=None, editing=False, screenshot_type=NORMAL_SCREENSHOT):
        """main"""
        temp_screenshot = tempfile.NamedTemporaryFile(
            suffix='.png', delete=False)
        temp_screenshot_path = temp_screenshot.name
        if sys.platform == "darwin":
            temp_screenshot_path = temp_screenshot_path.split(".")[
                0] + "_000.png"
        print("TEMP PATH: ", temp_screenshot_path)
        Capture.take_screenshot(temp_screenshot_path)

        root = tk.Tk()
        style = ttk.Style(root)
        root.wm_colormapwindows()

        root.tk.call('source', Theme.get_theme_path())
        root.tk.call("set_theme", "dark")

        if editing:
            print(" - EDIT MODE - ")
            app = ScreenShotTaker(root, save_location, update_function_after_edit=update_function_after_edit, 
                                  needle=needle, haystack=temp_screenshot_path, editing=True)  
                                # When editing from extension
        else:
            print(" - CREATE MODE - ")
            app = ScreenShotTaker(root, save_location, update_function_after_edit=update_function_after_edit,
                                  haystack=temp_screenshot_path, editing=False, screenshot_type=screenshot_type)

        root.mainloop()
        temp_screenshot.close()
        os.unlink(temp_screenshot.name)

    @staticmethod
    def take_screenshot(file_path='my_screenshot.png'):
        """Take a screenshot.
        Args:

        """
        print("Taking screenshot")
        img = screenshot(file_path)
        print("Done")

    @staticmethod
    def take_screenshot_save(save_location):
        """Take a screenshot.
        Args:

        """
        print("Taking screenshot")
        save_path = ''.join([save_location, "/img/aai_",
                            ''.join(choice(digits) for i in range(12)), ".png"])
        img = screenshot(save_path)
        print("Done")
