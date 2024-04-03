import subprocess
import os

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
    'chair; window; ceiling; picture; floor; lighting; table; cabinet; curtain; plant; shelving; sink; mirror; stairs; counter; stool; bed; sofa; shower; toilet; TV; clothes; bathtub; blinds; board',
    'cabinet; bed; chair; sofa; table; door; window; bookshelf; picture; counter; desk; curtain; refrigerator; showercurtain; toilet; sink; bathtub'
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

# Process .ply files for each vocab list
for vocab in vocab_lists:
    folder_count = 1  # Reset folder count for each vocab list
    for plyfile in sorted(os.listdir(input_dir)):
        if plyfile.endswith('.ply'):
            full_ply_path = os.path.join(input_dir, plyfile)
            output_dir = os.path.join(output_base_dir, f"{vocab[:10].replace(' ', '_')}_{folder_count}_{plyfile[:-4]}")  # Adjusted output directory to include vocab identifier and remove '.ply' from plyfile name
            os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
            print(f"Processing: {full_ply_path} with vocab: {vocab[:30]}... in {output_dir}")

            try:
                command = create_command(vocab, full_ply_path, output_dir)
                subprocess.run(command, check=True)
                successful_files.append((plyfile, vocab[:10]))  # Adjusted to track which vocab was used
                folder_count += 1  # Increment folder count after successful processing
            except subprocess.CalledProcessError:
                print(f"Failed to process: {full_ply_path}")

# Report success
print("Successfully processed files with their vocab:")
for file, vocab in successful_files:
    print(f"{file} with vocab: {vocab}")
