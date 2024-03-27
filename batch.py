import subprocess

# Define common parameters
vocab = "chair; window; ceiling; picture; floor; lighting; table; cabinet; curtain; plant; shelving; sink; mirror; stairs; counter; stool; bed; sofa; shower; toilet; TV; clothes; bathtub; blinds; board"
dataset = "mattarport3d"

# Loop through the scene files
for i in range(1, 6):
    pcd_path = f'demo/demo_scene/mattarport3d/mp3d_scene{i}.ply'
    subprocess.run(['python', 'zero_shot.py', '--pcd_path', pcd_path, '--vocab', vocab, '--dataset', dataset])
