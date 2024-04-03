import subprocess
import os
from itertools import cycle  # Importing cycle from itertools

# Initialize directories
input_dir = 'data/input'
output_base_dir = 'data/results'
successful_files = []

# Ensure the output base directory exists
os.makedirs(output_base_dir, exist_ok=True)

# Different vocab lists
vocab_lists = [
    'desk chair; conference chair; desk; filing cabinets; ceiling lights; wall lights; dishwasher; fridge; freezer; lift; plant; extinguisher',
    'window; ceiling; wall; floor',
    'concrete, blockwork; steel; chipboard; brickwork; plasterboard; glazing; render; glazing; carpet tiles; ceramic tiles; vinyl',
    'chair; window; ceiling; picture; floor; lighting; table; cabinet; curtain; plant; shelving; sink; mirror; stairs;  counter; stool; bed; sofa; shower; toilet; TV; clothes; bathtub; blinds; board',
    'cabinet; bed; chair; sofa; table; door; window; bookshelf; picture; counter; desk; curtain; refrigerator; showercurtain; toilet; sink; bathtub',
]

# Function to create command with dynamic vocab and output paths
def create_command(vocab, pcd_path, output_dir):
    return [
        'python', 'zero_shot.py',
        '--byproduct_save', output_dir,
        '--result_save', output_dir,
        '--vocab', vocab,
        '--dataset', 'scannet',
        '--pcd_path', pcd_path
    ]

# Counter for folders
folder_count = 1

# Process .ply files
for plyfile, vocab in zip(sorted(os.listdir(input_dir)), cycle(vocab_lists)):
    if plyfile.endswith('.ply'):
        full_ply_path = os.path.join(input_dir, plyfile)
        output_dir = os.path.join(output_base_dir, f"{folder_count}_{plyfile[:-4]}")  # Removing '.ply' from plyfile name for folder
        os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
        print(f"Processing: {full_ply_path} with vocab: {vocab[:30]}... in {output_dir}")

        try:
            command = create_command(vocab, full_ply_path, output_dir)
            subprocess.run(command, check=True)
            successful_files.append(plyfile)
            folder_count += 1  # Increment folder count after successful processing
        except subprocess.CalledProcessError:
            print(f"Failed to process: {full_ply_path}")

# Report success
print("Successfully processed files:")
for file in successful_files:
    print(file)


