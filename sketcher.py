import cv2
import os

def main():
    # Get image path
    image_path: str = get_image_path()

    # Apply sketch filter
    sketcher(image_path)

# Function to get image path
def get_image_path() -> str:
    # Initiate infinite loop
    while True:
        # Get image path from user and remove quotes
        image_path: str = input("Enter the path to the image: ").strip('"')

        # Check for input
        if not image_path:
            print("Error: No image path!")
        # Check for valid path input
        elif not os.path.exists(image_path):
            print("Error: Path does not exist!")
        else:
            # Return valid path
            return image_path

# Function to turn image to sketch
def sketcher(image_path) -> None:
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
    print(f"Image sketched and saved as {output_path}")  

if __name__ == "__main__":
    main()