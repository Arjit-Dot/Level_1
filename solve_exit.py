import os
import shutil

# Configuration
source_prefix = "Clue-"
destination_dir = "Exit1"
total_tiles = 64

# Ensure the destination exists
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

print(f"Initiating reconstruction sequence for {destination_dir}...")

for i in range(1, total_tiles + 1):
    # Construct paths
    folder_name = f"{source_prefix}{i}"
    source_folder_path = os.path.join(os.getcwd(), folder_name)
    
    # Locate the image file inside the Clue folder
    try:
        files = [f for f in os.listdir(source_folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        
        if files:
            source_file = os.path.join(source_folder_path, files[0])
            dest_file = os.path.join(destination_dir, f"tile_{i}.jpg")
            
            # Execute relocation
            shutil.copy2(source_file, dest_file)
            print(f"Uploaded: {folder_name} -> tile_{i}.jpg")
        else:
            print(f"Warning: No data packet found in {folder_name}")
            
    except FileNotFoundError:
        print(f"Critical Error: {folder_name} is missing from the directory.")

print("\nReconstruction complete. Verify the monitor interface.")
