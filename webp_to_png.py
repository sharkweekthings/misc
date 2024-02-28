import os
from PIL import Image
import shutil  # Import shutil for file moving operations

def convert_webp_to_png(folder_path):
    # List to store the paths of the converted PNG files
    png_files = []

    # Path for the 'webp' folder within the specified folder_path
    webp_folder_path = os.path.join(folder_path, "webp")

    # Check if the 'webp' folder exists, if not, create it
    if not os.path.exists(webp_folder_path):
        os.makedirs(webp_folder_path)

    # Loop through all files in the specified folder
    for file_name in os.listdir(folder_path):
        # Check if the file is a WEBP file
        if file_name.lower().endswith('.webp'):
            # Construct full file path
            webp_path = os.path.join(folder_path, file_name)
            # Create PNG path by replacing the file extension
            png_path = webp_path.rsplit('.', 1)[0] + '.png'

            # Open the webp image file
            with Image.open(webp_path) as image:
                # Save as PNG
                image.save(png_path, 'PNG')
                png_files.append(png_path)

            # Move the original .webp file to the 'webp' folder
            shutil.move(webp_path, webp_folder_path)

    # Return the list of converted PNG files
    return png_files

# Specify the folder that should be converted
folder_path = 'C:/Users/'  # Update this to your specific folder path
converted_png_files = convert_webp_to_png(folder_path)
converted_png_files