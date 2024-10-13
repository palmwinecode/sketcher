import cv2
import os

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class App:
    def __init__(self, root):
        # Create instance variable
        self.root = root

        # Create frame for entry field and button
        frame = ttk.Frame(self.root)
        frame.grid(column=0, row=0)

        # Configure rows and columns
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Heading label
        tk.Label(frame, text="Select image path", font=("Helvetica", 12, "bold"), pady=10).grid(column=0,row=0, columnspan=3, sticky=("NW"))

        # Path entry field
        self.image_path = tk.StringVar()
        self.path_entry = ttk.Entry(frame, width=50, textvariable=self.image_path)
        self.path_entry.grid(column=0, row=1, columnspan=3, sticky=("NSEW"))

        # Focus cursor in entry field
        self.path_entry.focus()
        
        # Path selection button
        self.path_btn = ttk.Button(frame, text="Path", command=self.select_image_path)
        self.path_btn.grid(column=3, row=1, sticky="NSWE")

        # Submit button
        submit = ttk.Button(frame, text="Sketch", command=self.get_image_path)
        submit.grid(column=0, row=2, columnspan=4, pady=5, sticky="NSEW")

        # Bind return key to get_image_path function
        self.root.bind("<Return>", self.get_image_path)

    # Function to select image path
    def select_image_path(self, *args) -> None:
        # Select image path
        image_path = filedialog.askopenfilename(title="Select image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        # Clear entry field
        self.path_entry.delete(0, tk.END)

        # Insert image path in entry field 
        self.path_entry.insert(0, image_path)

    # Function to get image path
    def get_image_path(self, *args) -> str:
        # Get image path from user and remove quotes
        image_path = self.image_path.get().strip('"')

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

        # Ask user for save name
        output_path = filedialog.asksaveasfilename(title="Save sketch", filetypes=[("Image files", "*.png;")])
        
        # print(output_path)
        # Did user cancel save dialog?
        if not output_path:
            return

        # Add extension
        output_path = output_path + ".png"

        # Get file name
        _, file_name = os.path.split(output_path)

        # Save file
        cv2.imwrite(output_path, sketch_img)

        # Output Confirmation message
        print(f"Saved to {output_path} as {file_name}") 
        messagebox.showinfo("Sketched!", f"Saved to {output_path} as {file_name}", parent=self.root)
 
def main():
    # Create Tk object
    root = tk.Tk()

    # Give root window a title
    root.title("Sketcher")

    # Window dimensions
    root.geometry("450x150")

    # Make window non-resizable
    root.resizable(False, False)

    # Instantiate App
    App(root)

    # Call mainloop
    root.mainloop()

if __name__ == "__main__":
    main()