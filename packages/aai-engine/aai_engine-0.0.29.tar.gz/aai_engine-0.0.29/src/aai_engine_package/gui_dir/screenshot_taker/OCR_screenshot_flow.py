""""OCR screenshot flow"""
from aai_engine_package.engine_util import REGION_PICK_VIEW, OFFSET_PICK_VIEW, NAME_PICK_VIEW

import tkinter
from tkinter import ttk

from random import choice
from string import digits

from PIL import Image, ImageTk
from PIL.PngImagePlugin import PngImageFile, PngInfo

from aai_engine_package.engine_util import locate_all

OCR_MAX_SEPARATION = 75

class OcrScreenshot():
    """
    class to define the flow if working with a OCR screenshot
    """
    def __init__(self, needle, haystack, editing, master, save_location, update_function_after_edit):
        """
        initialise the class
        """
        self.ocr_step1_complete = False
        # coords for rectangle
        self.x = self.y = 0

        # bool -> editing mode on(True) or off(False)
        self.editing = editing
        # master = root window
        self.master = master

        # function to commit the save, haystack save location
        self.update_function_after_edit = update_function_after_edit
        self.save_location = save_location

        # haystack (= screenshot), needle(part of haystack), needle name
        self.haystack = haystack
        self.needle = needle
        self.cropped_png = 'my_cropped.png'

        # # canvas dimensions
        self.width_canvas, self.height_canvas = self.master.winfo_screenwidth() / 2, self.master.winfo_screenheight() / 2

        #implement button and back button + width
        self.button_width = 20
        self.back_button = ttk.Button(self.master, text="Go Back", style='Accent.TButton', width=self.button_width)
        self.button = ttk.Button(self.master, style='Accent.TButton', width=self.button_width)

        if self.editing:
            self.init_canvas_screenshot(self.needle)
            self.view_offset_picker()
        else:
            # file name and save location determination
            self.screenshot_id = ''.join(choice(digits) for i in range(12))
            self.save_path = ''.join(
                [save_location, "/img/aai_", self.screenshot_id, ".png"])
            self.file_name = ''.join(['aai_', self.screenshot_id])
            
            # set default values and initiate first screen
            self.init_canvas_screenshot(self.haystack)

            self.button_confirm__anchor_region_clicked_functionality()
            print("haystack: ", self.haystack)

            self.view = REGION_PICK_VIEW
            self.lower_confidence = 0.5
            self.upper_confidence = 1
            self.confidence_step_size = 0.05

            self.offset_x = 0
            self.offset_y = 0
            
            self.canvas_selection_tool()

        self.button.pack(side=tkinter.BOTTOM, pady=20)

    def init_canvas_screenshot(self, haystack):
        """
        Initialize the canvas to take remaining space on screen, filled with screenshot
        """
        self.canvas = tkinter.Canvas(self.master, width=self.width_canvas, height=self.height_canvas, cursor="cross")
        self.canvas.pack()
        self.canvas.configure(background='black')
        
        self.original_im = Image.open(haystack)
        self.img = self.original_im
        img_width, img_height = self.img.size

        if img_width > self.width_canvas or img_height > self.height_canvas:
            ratio = min(self.width_canvas/img_width, self.height_canvas/img_height)
            img_width = int(img_width*ratio)
            img_height = int(img_height*ratio)
            self.img = self.img.resize(
                (img_width, img_height), Image.ANTIALIAS)

        self.tk_im = ImageTk.PhotoImage(self.img, master=self.master)
        print("needle: ", self.haystack)
        self.screenshot_haystack_set()

    def screenshot_haystack_set(self):
        """
        Function to create the initial screenshot for region confirmation
        """
        self.screenshot = self.canvas.create_image(self.width_canvas/2, self.height_canvas/2, image=self.tk_im)
    


    def first_screen_settings(self):
        """Function to call initial screenshot and let's reselect needle
        """
        print("settings for canvas + width and height")
        self.view = REGION_PICK_VIEW
        self.screenshot_haystack_set()
        self.canvas_selection_tool()



    # button functionalities
    def button_confirm_region_functionality(self):
        """Function to give the button the confirm region functionality
        """
        print("button = confirm region")
        self.button.configure(text="Confirm region", command= self.view_offset_picker)
    
    def button_confirm__anchor_region_clicked_functionality(self):
        """Function to give the button the confirm anchor region functionality
        """
        print("button = confirm anchor region")
        self.button.configure(text="Confirm anchor region", command= self.on_confirm_anchor_region_clicked)
    
    def button_confirm__ocr_region_clicked_functionality(self):
        """Function to give the button the confirm ocr region functionality
        """
        print("button = confirm ocr region")
        self.button.configure(text="Confirm ocr region", command= self.on_confirm_ocr_region_clicked)

    def button_confirm_offset_functionality(self):
        """Function to give the button the confirm offset functionality
        """
        print("button = confirm offset")
        self.button.configure(text="Confirm offset!", command= self.view_confidence_picker)

    def button_confirm_confidence_functionality(self):
        """Function to give the button the confirm confidence functionality
        """
        print("button = confirm confidence")
        self.button.configure(text="Confirm confidence", command=self.view_name_picker)
    
    # back button functionalities
    def back_button_Vissible(self):
        """Function to place the back button on the correct position
        """
        print("adding back button")
        self.back_button.pack(side=tkinter.BOTTOM, pady=(20,0))

    def back_button_on_click(self, new_screen, button_functionality, first_screen= False):
        """Function to navigate to the previous page when clicking back_button
        """
        print("back button clicked")
        self.canvas.delete('all')
        new_screen()
        button_functionality()

        if first_screen:
            self.back_button.forget()



    # functionality to select needle with a rectangle
    def canvas_selection_tool(self):
        """Function to makt it able to select a part of the screenshot
        """
        self.canvas.bind("<ButtonPress-1>", self.on_button_press_rectangle)
        self.canvas.bind("<B1-Motion>", self.on_move_press)

    def on_button_press_rectangle(self, event):
        """ Starts a new rectangle """
        # save mouse drag start position
        self.start_x = event.x
        self.start_y = event.y

        # delete needle
        if self.needle:
            self.canvas.delete(self.needle)
        # creacte first rectangle
        if not self.ocr_step1_complete:
            self.needle = self.canvas.create_rectangle(
                self.x, self.y, 1, 1, fill="", outline="red")
        # create second rectangle
        else:
            self.canvas.create_rectangle(
                self.rect_anchor['x1'], self.rect_anchor['y1'], self.rect_anchor['x2'], self.rect_anchor['y2'], fill="", outline="red")
            self.needle = self.canvas.create_rectangle(
                self.x, self.y, 1, 1, fill="", outline="yellow")
            
    def on_move_press(self, event):
        """ Updates the rectangle to match the current selected region """
        cur_x, cur_y = (event.x, event.y)

        # expand rectangle as you drag the mouse
        self.canvas.coords(self.needle, self.start_x, self.start_y, cur_x, cur_y)
   
   
   
    # functionality for choosing anchor region
    def on_confirm_anchor_region_clicked(self):
        """This function gets called when the anchor region is chosen. It handles the further flow.
        """
        self.ocr_step1_complete = True
        self.button.configure(text="Confirm OCR region",
                              command=self.on_confirm_ocr_region_clicked)

        self.ratio = self.original_im.size[0] / self.img.size[0]
        x1, y1, x2, y2 = self.canvas.coords(self.needle)
        left = x1 * self.ratio
        top = y1 * self.ratio
        right = x2 * self.ratio
        bottom = y2 * self.ratio
        self.cropped = self.original_im.crop((left, top, right, bottom))
        self.cropped.save(self.cropped_png, 'PNG')
        self.tk_cropped = ImageTk.PhotoImage(
            self.cropped, master=self.master)
        self.w, self.h = self.master.winfo_screenwidth(), self.master.winfo_screenheight()


        print(f"Anchor dimensions data = {self.canvas.bbox(self.needle)}")
        x1,y1,x2,y2 = self.canvas.bbox(self.needle)
        self.rect_anchor = {'x1':x1, 'y1':y1,'x2':x2, 'y2':y2 }



    # functionality for confirming ocr region
    def on_confirm_ocr_region_clicked(self):
        """Function gets called when ocr region is chosen by the user. It handles the further flow
        """
        print("OCR REGION CONFIRMED!")
        print(f"Anchor dimensions data = ({self.rect_anchor['x1']}, {self.rect_anchor['y1']}, {self.rect_anchor['x2']}, {self.rect_anchor['y1']}))")
        print(f"OCR dimensions data = {self.canvas.bbox(self.needle)}")
        # Check if boxes are not too far from each other
        width_anchor = abs(self.rect_anchor['x2'] - self.rect_anchor['x1'])
        height_anchor = abs(self.rect_anchor['y2'] - self.rect_anchor['y1'])
        center_x_anchor = min(self.rect_anchor['x1'], self.rect_anchor['x2']) + width_anchor/2
        center_y_anchor = min(self.rect_anchor['y1'], self.rect_anchor['y2']) + height_anchor/2

        x1,y1,x2,y2 = self.canvas.bbox(self.needle)
        width_ocr = abs(x2 - x1)
        height_ocr = abs(y2 - y1)
        center_x = min(x1, x2) + abs(x2 - x1)/2
        center_y = min(y1, y2) + abs(y2 - y1)/2

        distance_x = abs(center_x - center_x_anchor)
        distance_y = abs(center_y - center_y_anchor)

        if (distance_x > (width_anchor/2 + width_ocr/2 + OCR_MAX_SEPARATION)) or (distance_y > (height_anchor/2 + height_ocr/2 + OCR_MAX_SEPARATION)):
            print("The OCR box is too far separated from the anchor!")
            return

        x1,y1,x2,y2 = self.canvas.bbox(self.needle)
        self.ocr_box = (x1,y1,x2,y2)
        self.view_name_picker()



    # functionality for offset picker
    def view_offset_picker(self):
        """
        View to choose the offset to be used,
        saved as offset to center of the selected region
        """
        self.canvas.delete(self.screenshot)
        self.offset_picker_main_settings()

        # cropping screenshot to selected region
        if not self.editing:
            self.ratio = self.original_im.size[0] / self.img.size[0]

            x1, y1, x2, y2 = self.canvas.coords(self.needle)
            left = x1 * self.ratio
            top = y1 * self.ratio
            right = x2 * self.ratio
            bottom = y2 * self.ratio
            self.cropped = self.original_im.crop((left, top, right, bottom))
            self.cropped.save(self.cropped_png, 'PNG')

            self.tk_cropped = ImageTk.PhotoImage(self.cropped, master=self.master)
            self.selected_region = self.canvas.create_image(self.w, self.h, image=self.tk_cropped)

            # center of img
            self.offset_x = self.w
            self.offset_y = self.h
            
            self.drawing_cross_at_center()
            self.canvas.delete(self.needle)

        else:
            print("cropping the screenshot to the selected region")
            self.cropped = self.original_im
            self.cropped.save(self.cropped_png, 'PNG')

            self.tk_cropped = ImageTk.PhotoImage(self.img, master=self.master)
            self.selected_region = self.canvas.create_image(self.w, self.h, image=self.tk_cropped)

            target_image = PngImageFile(self.needle)
            print(target_image.text)
            self.offset_x = float(target_image.text["offset_x"])
            self.offset_y = float(target_image.text["offset_y"])

            self.drawing_cross_at_center()
            # we draw the cross without click event (already offset stored in the image metadata)
            self.drawing_cross_after_click()

            self.canvas.delete(self.needle)

    def offset_picker_main_settings(self):
        """
        Function to initialise the main settings for the ofsset picker screen
        """
        self.view = OFFSET_PICK_VIEW
        self.button_confirm_offset_functionality()
        self.canvas.unbind("<ButtonPress-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        self.canvas.bind("<ButtonPress-1>", self.on_button_press_offset)

        if not self.editing:
            # getting the back button
            self.back_button_Vissible()
            self.back_button.configure(command=lambda: self.back_button_on_click(new_screen= self.first_screen_settings, 
                        button_functionality= self.button_confirm_region_functionality, first_screen=True))

        self.w, self.h = self.master.winfo_screenwidth()/4, self.master.winfo_screenheight()/4
    
    def drawing_cross_at_center(self):
        """Function to draw the default red cross on the screen
        """
        self.cross_h = self.canvas.create_line(
                self.w - 10, self.h, self.w + 10, self.h, fill='red')
        self.cross_v = self.canvas.create_line(
            self.w, self.h - 10, self.w, self.h + 10, fill='red')
    
    def drawing_cross_after_click(self):
        """Function to redraw the cross after a clicking new offset location
        """
        self.canvas.coords(self.cross_h, self.offset_x - 10,
                           self.offset_y, self.offset_x + 10, self.offset_y)
        self.canvas.coords(self.cross_v, self.offset_x,
                           self.offset_y - 10, self.offset_x, self.offset_y + 10)
        
    def on_button_press_offset(self, event):
        """ Draws a cross at the clicked coordinates and saves the offsets """
        self.offset_x = event.x
        self.offset_y = event.y
        self.drawing_cross_after_click()

    def view_offset_picker_settings(self):
        """
        Function to call the initial offset picker screen back
        """
        # forget slidebars and check button
        self.button_check.forget()
        self.scale_lower_confidence.forget()
        self.scale_lower_confidence_label.forget()
        self.scale_upper_confidence.forget()
        self.scale_upper_confidence_label.forget()
        self.scale_confidence_step_size.forget()
        self.scale_confidence_step_size_label.forget()
  
        # initialise offset pick screen
        self.canvas.delete('all')
        self.offset_picker_main_settings()
        self.selected_region = self.canvas.create_image(self.w, self.h, image=self.tk_cropped)
        
        self.drawing_cross_at_center()
        self.drawing_cross_after_click()



    # functionality for cinfidence picker
    def view_confidence_picker(self):
        """
        View showing the confidence picker
        """
        self.view = SIMILARITY_PICK_VIEW
        self.canvas.delete('all')

        self.lower_confidence = 0.5
        self.upper_confidence = 1
        self.confidence_step_size = 0.05

        # button functionality
        self.button_confirm_confidence_functionality()

        # getting check button
        self.button_check = ttk.Button(
            self.master, text="Check", command=self.reset_confidence)
        self.button_check.pack(side=tkinter.BOTTOM, pady=20)
        
        # back button functionality
        self.back_button.configure(command=lambda: self.back_button_on_click(new_screen= self.view_offset_picker_settings, button_functionality= self.button_confirm_offset_functionality))
        
        # getting 3 slide bars to get a numeric value
        self.scale_lower_confidence = ttk.Scale(self.master, from_=0, to=100, orient=tkinter.HORIZONTAL,
                            command=lambda val: (self.set_lower_confidence(val)), length=200)
        self.scale_upper_confidence = ttk.Scale(self.master, from_=0, to=100, orient=tkinter.HORIZONTAL,
                            command=lambda val: (self.set_upper_confidence(val)), length=200)
        self.scale_confidence_step_size = ttk.Scale(self.master, from_=0, to=100, orient=tkinter.HORIZONTAL,
                            command=lambda val: (self.set_confidence_step_size(val)), length=200)

        if not self.editing:
            self.scale_lower_confidence.set(50)
            self.scale_upper_confidence.set(100)
            self.scale_confidence_step_size.set(5)

        else:
            target_image = PngImageFile(self.needle)
            self.scale_lower_confidence.set(
                int(float(target_image.text["lower_confidence"]) * 100))
            self.scale_upper_confidence.set(
                int(float(target_image.text["upper_confidence"]) * 100))
            
        # confidence step size set + label
        self.scale_confidence_step_size.pack(side=tkinter.BOTTOM)
        self.scale_confidence_step_size_label = ttk.Label(self.master, text='Confidence step size',
                  font=('sans-serif', 10))
        self.scale_confidence_step_size_label.pack(side=tkinter.BOTTOM)

        # upper confidence set + label
        self.scale_upper_confidence.pack(side=tkinter.BOTTOM)
        self.scale_upper_confidence_label = ttk.Label(self.master, text='Upper confidence', font=(
            'sans-serif', 10))
        self.scale_upper_confidence_label.pack(side=tkinter.BOTTOM)

        # lower confidence set + label
        self.scale_lower_confidence.pack(side=tkinter.BOTTOM)
        self.scale_lower_confidence_label = ttk.Label(self.master, text='Lower confidence', font=(
            'sans-serif', 10))
        self.scale_lower_confidence.pack(side=tkinter.BOTTOM)

        # screenshot img set
        self.screenshot_haystack_set()

    # def reset_confidence(self):
        """
        Recalculates matching regions
        """
        try:
            for match in self.matches:
                self.canvas.delete(match)
        except AttributeError:
            pass

        self.calculate_all_matches()
        print(self.lower_confidence)
        
    def calculate_all_matches(self):
        """
        Calculates all the matching regions in the taken screenshot, displays these
        regions with red rectangles
        """

        confidence_float = float(self.lower_confidence)
        imloc = locate_all(self.cropped_png, self.haystack,
                           confidence=confidence_float)
        self.matches = []
        self.ratio = self.original_im.size[0] / self.img.size[0]
        for coords in imloc:
            left, top, width, height = coords
            left = left / self.ratio
            top = top / self.ratio
            width = width / self.ratio
            height = height / self.ratio
            match = self.canvas.create_rectangle(
                left, top, left + width, top + height, fill="", outline="red")
            self.matches.append(match)

    # setters for confidence determination bars
    def set_lower_confidence(self, val):
        """setter"""
        self.lower_confidence = float(val) / 100.0

    def set_upper_confidence(self, val):
        """setter"""
        self.upper_confidence = float(val) / 100.0

    def set_confidence_step_size(self, val):
        """setter"""
        self.confidence_step_size = float(val) / 100.0



    # functionality for name picker
    def view_name_picker(self):
        """
        View showing the name picker
        """
        self.view = NAME_PICK_VIEW
        self.canvas.delete('all')
        for widget in self.master.winfo_children():
            widget.destroy()
        self.button = ttk.Button(
            self.master, text="Confirm name", command=self.confirm_name, style='Accent.TButton')
        self.text_box = ttk.Entry(self.master)
        self.text_box.insert(tkinter.END, self.file_name)
        self.button.pack(side=tkinter.BOTTOM, padx=20, pady=20)
        self.text_box.pack(side=tkinter.BOTTOM, pady=(20, 0))
        self.init_canvas_screenshot(self.cropped_png)

    def confirm_name(self):
        """
        Confirm the name and save the selected region to a png
        with the chosen confidence and offsets to the center as metadata

        This metadata can be retrieved through the text field of
        PngImageFile("my_image_meta.png")
        """
        metadata = PngInfo()
        metadata.add_text("offset_x", str(self.offset_x))
        metadata.add_text("offset_y", str(self.offset_y))
        metadata.add_text("lower_confidence", str(self.lower_confidence))
        metadata.add_text("upper_confidence", str(self.upper_confidence))
        metadata.add_text("confidence_step_size", str(self.confidence_step_size))

        self.save_path = ''.join(
            [self.save_location, '/', self.text_box.get().strip(), ".png"])

        print("Save path: ")
        print(self.save_path)

        self.cropped.save(self.save_path, pnginfo=metadata)
        target_image = PngImageFile(self.save_path)
        print(target_image.text)
        self.master.destroy()
        if self.update_function_after_edit:
            self.update_function_after_edit(self.save_location)