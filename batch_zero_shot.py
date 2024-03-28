import subprocess
import os

# Specify the directory containing the .ply files
input_dir = 'data/input'
# Specify the base command without the file-dependent argument
base_command = [
    'python', 'zero_shot.py',
    '--byproduct_save', 'data/byproduct/',
    '--result_save', 'data/results/',
    '--vocab', 'chair; window; ceiling; picture; floor; lighting; table; cabinet; curtain; plant; shelving; sink; mirror; stairs; counter; stool; bed; sofa; shower; toilet; TV; clothes; bathtub; blinds; board',
    '--dataset', 'mattarport3d'
]

# Loop through all .ply files in the input directory
for plyfile in os.listdir(input_dir):
    full_ply_path = os.path.join(input_dir, plyfile)
    print(f"Processing: {full_ply_path}")

    # Run the command with the current .ply file path
    subprocess.run(base_command + ['--pcd_path', full_ply_path])

print("All files have been processed.")