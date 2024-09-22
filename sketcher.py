import cv2

# Function to turn image to sketch
def sketcher(image_path):
    # Read image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to open image.")

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
    print(f"Image sketched and saved as {output_path}")  

# Get image path from user
image_path = input("Enter the path to the image: ")

# Apply sketch filter
sketcher(image_path)