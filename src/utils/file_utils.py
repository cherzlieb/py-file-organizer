import os
import shutil
import logging
from datetime import datetime

def clean_filename(filename):
    # Replace spaces and underscores with hyphens
    return filename.replace(' ', '-').replace('_', '-')

def organize_files(download_folder, organized_folder, unorganized_folder, file_types, logger):
    try:
        # Create organized and unorganized folders if they don't exist
        for folder in [organized_folder, unorganized_folder]:
            if not os.path.exists(folder):
                os.makedirs(folder)
                print(f"Created folder at {folder}")

        files_moved = 0
        folders_moved = 0

        for item_name in os.listdir(download_folder):
            item_path = os.path.join(download_folder, item_name)

            # Skip the Organized and Unorganized folders
            if item_path in [organized_folder, unorganized_folder]:
                continue

            if os.path.isfile(item_path):
                # Get file creation time and format it
                creation_time = datetime.fromtimestamp(os.path.getctime(item_path))
                date_prefix = creation_time.strftime("%Y-%m-%d-")

                # Clean the filename
                cleaned_name = clean_filename(item_name)
                new_filename = f"{date_prefix}{cleaned_name}"

                # Handle files as before
                file_extension = os.path.splitext(item_name)[1].lower()
                destination_folder = None

                for folder_name, extensions in file_types.items():
                    if file_extension in extensions:
                        destination_folder = os.path.join(organized_folder, folder_name)
                        break

                if destination_folder:
                    try:
                        if not os.path.exists(destination_folder):
                            os.makedirs(destination_folder)

                        destination_path = os.path.join(destination_folder, new_filename)
                        print(f"Moving file: {item_name} -> {destination_folder} as {new_filename}")
                        shutil.move(item_path, destination_path)
                        files_moved += 1
                    except Exception as e:
                        print(f"Error moving file {item_name}: {str(e)}")

            elif os.path.isdir(item_path):
                # Handle folders by moving to Unorganized
                try:
                    destination_path = os.path.join(unorganized_folder, item_name)
                    print(f"Moving folder: {item_name} -> {unorganized_folder}")
                    shutil.move(item_path, destination_path)
                    folders_moved += 1
                except Exception as e:
                    print(f"Error moving folder {item_name}: {str(e)}")

        print(f"\nOrganization complete!")
        print(f"Files moved: {files_moved}")
        print(f"Folders moved to Unorganized: {folders_moved}")

    except Exception as e:
        print(f"Error during organization: {str(e)}")
