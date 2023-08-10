import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk

class ImageViewerApp:
    def __init__(self, root, image_pairs, output_folder):
        self.root = root
        # setting window size
        width = 1920
        height = 1080
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        self.image_pairs = image_pairs
        self.output_folder = output_folder
        self.current_index = 0

        self.load_images()

        self.canvas = tk.Canvas(self.root, width=width, height=height*0.9)
        self.canvas.pack()

        self.original_label = tk.Label(self.root, text="Original Image")
        self.original_label.pack(side=tk.LEFT)

        self.processed_label = tk.Label(self.root, text="Processed Image")
        self.processed_label.pack(side=tk.RIGHT)

        self.previous_button = tk.Button(self.root, text="Previous [q]", command=self.show_previous)
        self.previous_button.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.root, text="Next[w]", command=self.show_next)
        self.next_button.pack(side=tk.RIGHT)

        self.move_original_button = tk.Button(self.root, text="Move Original[1]", command=self.move_original)
        self.move_original_button.pack(side=tk.LEFT)

        self.move_processed_button = tk.Button(self.root, text="Move Processed[2]", command=self.move_processed)
        self.move_processed_button.pack(side=tk.RIGHT)

        self.root.bind('1', self.move_original)
        self.root.bind('2', self.move_processed)
        self.root.bind('w', self.show_next)
        self.root.bind('q', self.show_previous)

        self.show_images()

    def load_images(self):
        self.loaded_images = []
        for pair in self.image_pairs:
            original_image = Image.open(pair[0])
            processed_image = Image.open(pair[1])
            self.loaded_images.append((original_image, processed_image))

    def show_images(self):
        original_image, processed_image = self.loaded_images[self.current_index]
        width, height = original_image.size
        aspect = width/height
        if aspect < 1: # Tall
            size = (1050*aspect, 1050)
        if aspect > 1: # Wide
            size = (950, 950*aspect)
        original_image.thumbnail(size)
        processed_image.thumbnail(size)

        self.original_tkimage = ImageTk.PhotoImage(original_image)
        self.processed_tkimage = ImageTk.PhotoImage(processed_image)

        self.canvas.create_image(0, self.root.winfo_screenheight()/2, image=self.original_tkimage, anchor=tk.W)
        self.canvas.create_image(1920, self.root.winfo_screenheight()/2, image=self.processed_tkimage, anchor=tk.E)

    def show_previous(self, event=None):
        if self.current_index > 0:
            self.current_index -= 1
            self.show_images()

    def show_next(self, event=None):
        if self.current_index < len(self.image_pairs) - 1:
            self.current_index += 1
            self.show_images()

    def move_original(self, event=None):
        self.move_image(self.image_pairs[self.current_index][0])

    def move_processed(self, event=None):
        self.move_image(self.image_pairs[self.current_index][1])

    def move_image(self, source_path):
        filename = os.path.basename(source_path)
        destination_path = os.path.join(self.output_folder, filename)
        shutil.copy(source_path, destination_path)
        print(f"Moved {filename} to {self.output_folder}")

# Provide your image pairs and output folder here
root_folder = r'C:\Users\ham\Pictures\Michael Family Photos'
ls = os.listdir(fr'{root_folder}\original')
processed = [fr'{root_folder}\processed\{i}' for i in ls]
original = [fr'{root_folder}\original\{i}' for i in ls]
image_pairs = [(fr'{root_folder}\original\{i}',fr'{root_folder}\processed\{i}') for i in ls]
output_folder = fr"{root_folder}\final"

root = tk.Tk()
app = ImageViewerApp(root, image_pairs, output_folder)
root.mainloop()
