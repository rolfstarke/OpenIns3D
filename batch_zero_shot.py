import subprocess
import os

# Initialize directories and base command
input_dir = 'data/input'
successful_files = []

base_command = [
    'python', 'zero_shot.py',
    '--byproduct_save', 'data/results/',
    '--result_save', 'data/results/',
    '--vocab', 'chair; window; ceiling; wall, floor; table; curtain; extinguisher; carpet',
    #'--vocab', 'extinguisher,  wall',
    '--dataset', 'scannet'
]

# Process .ply files
for plyfile in os.listdir(input_dir):
    if plyfile.endswith('.ply'):
        full_ply_path = os.path.join(input_dir, plyfile)
        print(f"Processing: {full_ply_path}")
        try:
            subprocess.run(base_command + ['--pcd_path', full_ply_path], check=True)
            successful_files.append(plyfile)
        except subprocess.CalledProcessError:
            print(f"Failed to process: {full_ply_path}")

# Report success
print("Successfully processed files:")
for file in successful_files:
    print(file)




