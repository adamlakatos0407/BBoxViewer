import tkinter as tk
import os
import cv2
import numpy as np

from PIL import ImageTk, Image, ImageDraw
from pathlib import Path

from classes import BBoxData
from dataset import check_data, load_image_and_label, set_new_img_size


class Application(tk.Tk):
    def __init__(self, width, height):
        super().__init__()

        """Window"""
        self.title("BBoxViewer")
        self.geometry(str(width) + "x" + str(height))

        """Frame"""
        self.upper_frame = tk.Frame(self, bg='#4d4d4d')
        self.upper_frame.place(relx=0.02, rely=0.02, relwidth=0.9, relheight=0.05)

        self.img_frame = tk.Frame(self)
        self.img_frame.place(relx=0.02, rely=0.1, relwidth=0.9, relheight=0.9)

        """Canvas"""
        self.img_canvas = tk.Canvas(self.img_frame, bg='#4d4d4d')
        self.img_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)

        """Entry"""
        self.entry = tk.Entry(self.upper_frame, font=20)
        self.entry.place(relx=0.67, rely=0.2, relwidth=0.6, height=20, anchor='n')

        """Buttons"""
        button_names =['ADD FOLDER', 'NEXT_IMG', 'PREV_IMG', 'NEXT_BB', 'PREV_BB']
        button_width = 80
        button_height = 40
        self.buttons = []
        button_x = 0

        """Create buttons"""
        for i, name in enumerate(button_names):
            self.buttons.append(tk.Button(self.upper_frame, text=name, activebackground='gray'))
            self.buttons[i].place(x=button_x, y=0, width=button_width, height=button_height)
            button_x += button_width
        
        """Seting button commands"""
        self.buttons[0]['command'] = self.b_clicked_add_folder
        self.buttons[1]['command'] = self.b_clicked_next_img
        self.buttons[2]['command'] = self.b_clicked_prev_img
        self.buttons[3]['command'] = self.b_clicked_next_bbox
        self.buttons[4]['command'] = self.b_clicked_prev_bbox

        """Data containers"""
        self.img_types = ['.jpg', '.png']
        self.max_img_size = 900
        #self.entry_container: Path
        self.entry_container = Path("D:\\asztal\suli\szakdoga\DATASET\waste\\0_GYHG\\budder")
        self.img_names: list[str]
        self.img_index = 0
        self.bbox_index = 0
        self.BBox_container: BBoxData
        self.img: ImageTk
        self.cv_cont: np.ndarray

    """---- FUNCTIONS -------------------------------------------------------------------------"""
    """Action functions"""
    def b_clicked_add_folder(self) -> None:
        self.entry_container = self.get_entry()
        check_data(self.entry_container)
        self.img_names = self.get_img_src_list(self.entry_container)
        self.set_BBox_data()
        self.load_img()
    
    def b_clicked_next_img(self) -> None:
        if self.img_index < len(self.img_names)-1 : self.img_index += 1
        self.set_BBox_data()
        self.load_img()
        
    def b_clicked_prev_img(self ) -> None:
        if self.img_index > 0 : self.img_index -= 1 
        self.set_BBox_data()
        self.load_img()

    def b_clicked_next_bbox(self) -> None:
        if self.bbox_index < len(self.BBox_container.coco_coords)-1 : self.bbox_index += 1
        self.load_img()

    def b_clicked_prev_bbox(self) -> None:
        if self.bbox_index > 0 : self.bbox_index -= 1
        self.load_img()

    """Getters and Setters"""
    def get_entry(self) -> Path:
        return Path(self.entry.get())

    def get_img_src_list(self, src: Path) -> list[Path]:
        return [Path(file) for file in os.listdir(src) if file[-4:] in self.img_types]

    def set_BBox_data(self) -> None:
        self.bbox_index = 0
        self.BBox_container = load_image_and_label(os.path.join(self.entry_container, self.img_names[self.img_index]))

    def load_img(self):
        self.check_img_size()
        self.BBox_container.set_voc_coords()
        img = cv2.cvtColor(self.BBox_container.img, cv2.COLOR_BGR2RGB)
        self.img = Image.fromarray(img)
        self.draw_bbox()
        self.img = ImageTk.PhotoImage(self.img)
        self.img_canvas.create_image((0, 0), anchor='nw', image=self.img)

    def check_img_size(self) -> None:
        img = self.BBox_container.img
        h, w = img.shape[:2]
        if (w > h and w > self.max_img_size) or (h > w and h > self.max_img_size) or (w == h and h > self.max_img_size):
            self.BBox_container.img = set_new_img_size(img, self.max_img_size, w, h)
        
    # # Functions should be rewritten in dataset.py
    # def set_new_img_size(self, img, w: int, h: int ):
    #     ratio = w / h
    #     if w > h:
    #         new_w = self.max_img_size
    #         new_h = round(self.max_img_size * ratio)
    #     elif w < h:
    #         new_w = round(self.max_img_size * ratio)
    #         new_h = self.max_img_size
    #     elif w == h:
    #         new_w = new_h = self.max_img_size

    #     self.BBox_container.img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    #     self.BBox_container.set_voc_coords()

    def draw_bbox(self):
        colors = [(255, 0, 0), (0, 255, 0), (144, 144, 144), (0, 0, 255)]
        draw = ImageDraw.Draw(self.img)
        coords = self.BBox_container.voc_coords[self.bbox_index]
        draw.rectangle((coords[1], coords[2], coords[3], coords[4]), outline=colors[coords[0]], width=2)