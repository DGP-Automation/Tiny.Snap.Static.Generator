import os
from PIL import Image
from tkinter import Tk
from tkinter.filedialog import askdirectory

TARGET_RESOLUTION = 250


def resize_images(directory):
    # List all png and jpg images in the directory
    images = [os.path.join(directory, name)
              for name in os.listdir(directory)
              if name.lower().endswith((".png", ".jpg", ".jpeg"))]

    for image_path in images:
        if image_path.endswith(".png"):
            img = Image.open(image_path).convert("RGBA")
        else:
            img = Image.open(image_path).convert("RGB")
        # Check if the shortest side of the image is greater than 400px
        if min(img.size) > TARGET_RESOLUTION:
            print(f"Resizing {image_path}, original size: {img.size}")
            # Calculate the aspect ratio
            aspect_ratio = img.size[0] / img.size[1]
            # If width is the shortest side
            if img.size[0] == min(img.size):
                new_size = (TARGET_RESOLUTION, int(TARGET_RESOLUTION / aspect_ratio))
            # If height is the shortest side
            else:
                new_size = (int(TARGET_RESOLUTION * aspect_ratio), TARGET_RESOLUTION)
            # Resize the image
            img_resized = img.resize(new_size, Image.Resampling.LANCZOS)

            # Save the resized image, overwriting the original image
            img_resized.save(image_path, quality=95, subsampling=0)


def select_directory(title):
    root = Tk()
    root.withdraw()  # Hide the main window
    directory = askdirectory(title=title)  # Show the "Open" dialog box and return the path to the selected directory
    return directory


def main():
    directory = select_directory("Select a directory")
    resize_images(directory)
    print(f"Selected directory: {directory}")


if __name__ == "__main__":
    main()
