import open3d as o3d

# Load the .ply file
pcd = o3d.io.read_point_cloud("room1_model.ply")

# Print the information to inspect structure and data types
print(pcd)
