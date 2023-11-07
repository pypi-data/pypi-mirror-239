from screenshot_taker.normal_screenshot_flow import NormalScreenshot
from screenshot_taker.OCR_screenshot_flow import OcrScreenshot

NORMAL_SCREENSHOT = 0
OCR_SCREENSHOT = 1

class ScreenShotTaker():
    """
    Manager to to manage screenshot selecting process,
    draws the screenshot on a canvas where a region is selected along with
    an offset and matching confidence.
    """
    def __init__(self, master, save_location, update_function_after_edit=None, needle=None, haystack=None, 
                    editing=False, screenshot_type = NORMAL_SCREENSHOT):
        """
        Initialize values and prepare the region pick view
        """
        # bool -> editing mode on(True) or off(False)
        self.editing = editing

        # haystack (= screenshot), type, needle(part of haystack)
        self.haystack = haystack
        self.screenshot_type = screenshot_type
        self.needle = needle

        # master = root window, window title
        self.master = master
        self.master.title("AAI Image Extractor")

        # canvas dimensions
        self.width_canvas, self.height_canvas = self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight() / 2

        if self.screenshot_type == NORMAL_SCREENSHOT:
            print("NORMAL SCREENSHOT FLOW")
            NormalScreenshot(self.needle, self.haystack, self.editing, self.master, 
                                   save_location, update_function_after_edit)
        else:
            print("OCR SCREENSHOT FLOW")
            OcrScreenshot(self.needle, self.haystack, self.editing, self.master,
                                    save_location, update_function_after_edit)