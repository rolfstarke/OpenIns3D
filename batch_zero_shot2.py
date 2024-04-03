import subprocess
import os

# Initialize input directory
input_dir = 'data/input'

# Different vocab lists
vocab_lists = [
    'desk chair; conference chair; desk; filing cabinets; ceiling lights; wall lights; dishwasher; fridge; freezer; lift; plant; extinguisher',
    'window; ceiling; wall; floor',
    'concrete, blockwork; steel; chipboard; brickwork; plasterboard; glazing; render; glazing; carpet tiles; ceramic tiles; vinyl',
    'chair; window; ceiling; picture; floor; lighting; table; cabinet; curtain; plant; shelving; sink; mirror; stairs; counter; stool; bed; sofa; shower; toilet; TV; clothes; bathtub; blinds; board',
    'cabinet; bed; chair; sofa; table; door; window; bookshelf; picture; counter; desk; curtain; refrigerator; showercurtain; toilet; sink; bathtub'
]

# Function to create command with dynamic vocab and output paths
def create_command(vocab, pcd_path):
    vocab_formatted = vocab.replace('; ', '_').replace(';', '_')  # Replace semicolons with underscores
    output_dir = f"{vocab_formatted[:12]}"  # Use formatted vocab string in output directory path
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    return [
        'python', 'zero_shot.py',
        '--byproduct_save', output_dir,
        '--result_save', output_dir,
        '--vocab', vocab,
        '--dataset', 'scannet',
        '--pcd_path', pcd_path
    ]

successful_files = []

# Process .ply files for each vocab list
for vocab in vocab_lists:
    for plyfile in sorted(os.listdir(input_dir)):
        if plyfile.endswith('.ply'):
            full_ply_path = os.path.join(input_dir, plyfile)
            print(f"Processing: {full_ply_path} with vocab: {vocab[:30]}...")

            try:
                command = create_command(vocab, full_ply_path)
                subprocess.run(command, check=True)
                successful_files.append((plyfile, vocab[:10]))  # Adjusted to track which vocab was used
            except subprocess.CalledProcessError:
                print(f"Failed to process: {full_ply_path}")

# Report success
print("Successfully processed files with their vocab:")
for file, vocab in successful_files:
    print(f"{file} with vocab: {vocab}")
