import cv2
import os

from tkinter import *
from tkinter import ttk, messagebox, filedialog

class App:
    def __init__(self, root):
        # Create instance variable
        self.root = root

        # Give root window a title
        self.root.title("Sketcher")

        # Create frame for entry field and button
        frame = ttk.Frame(self.root, padding=10)
        frame.grid(column=0, row=0, sticky=(N, S, E, W))

        # Configure rows and columns
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Path entry label
        ttk.Label(frame, text="Enter image path").grid(column=1,row=1)

        # Path entry field
        self.path = StringVar()
        path_entry = ttk.Entry(frame, width=50, textvariable=self.path)
        path_entry.grid(column=1, row=2)

        # Focus cursor in entry field
        path_entry.focus()

        #  Submit button
        submit = ttk.Button(frame, text="Submit", command=self.get_image_path)
        submit.grid(column=1, row=3)

        # Bind return key to get_image_path function
        self.root.bind("<Return>", self.get_image_path)

    # Function to get image path
    def get_image_path(self, *args) -> str:
        # Get image path from user and remove quotes
        image_path = self.path.get().strip('"')

        # Check for input
        if not image_path:
            # Output error message
            print("Error: No image path!")
            messagebox.showerror("Error", "No image path", parent=self.root)
        # Check for valid path input
        elif not os.path.exists(image_path):
            # Output error message
            print("Error: Path does not exist!")
            messagebox.showerror("Error", "Path does not exist!", parent=self.root)
        else:
            # Call sketcher function
            self.sketcher(path=image_path)

    # Function to turn image to sketch
    def sketcher(self, **kwargs):
        # Get image path
        image_path = kwargs["path"]

        # Read image
        image = cv2.imread(image_path)
        
        # Apply grey filter
        grey_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Invert grey image
        invert_img = cv2.bitwise_not(grey_img)

        # Blur inverted-greyed image
        blur_img = cv2.GaussianBlur(invert_img, (21,21),0)

        # Invert blured-inverted-greyed image
        invertedblur = cv2.bitwise_not(blur_img)

        # Turn to image to sketch
        sketch_img = cv2.divide(grey_img, invertedblur, scale=256.0)

        # Save the result
        output_path = "sketch.png"
        cv2.imwrite(output_path, sketch_img)

        # Output Confirmation message
        print(f"Image sketched and saved as {output_path}") 
        messagebox.showinfo("Done!", f"Image sketched and saved as {output_path}", parent=self.root)
 
def main():
    # Create Tk object
    root = Tk(screenName="Sketcher")

    # Create App
    app = App(root)

    # Call mainloop
    root.mainloop()

if __name__ == "__main__":
    main()