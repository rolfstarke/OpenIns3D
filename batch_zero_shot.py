"""
Zero-shot inference Script for OpenIns3D

Author: Zhening Huang (zh340@cam.ac.uk)
"""

import torch
from openins3d.lookup import *
from openins3d.snap import *
from openins3d.build_lookup_dict import *
import pyviz3d.visualizer as viz
import argparse
import sys
sys.path.append("./ODISE")
from openins3d.utils import save_visulization_3d, generate_detection_results
from openins3d.mask3d import get_model, load_mesh, prepare_data, map_output_to_pointcloud, save_colorized_mesh, prepare_data_pcd
import datetime


for plyfile in os.listdir('data/input/'):

    def get_args():
        
        '''Command line arguments.'''

        parser = argparse.ArgumentParser(
            description='OpenIns3D')

        #parser.add_argument('--pcd_path', default="demo_scene/replica/frl_apartment_1_mesh.ply", type=str, help='the path of the colored point cloud')
        parser.add_argument('--img_size', default=[1000,1000], help='size of snap images')
        parser.add_argument('--MPM_checkpoint', default="checkpoints/scannet200_val.ckpt", type=str, help='the path of MPM_checkpoint')
        parser.add_argument('--vocab', default="cabinet; bed; chair; sofa; table; door; window; bookshelf; picture; counter; desk; curtain; refrigerator; showercurtain; toilet; sink; bathtub", help= "simliar to ODISE, this is in format 'a1,a2;b1,b2', where a1,a2 are synonyms vocabularies for the first class")
        parser.add_argument('--result_save', default="data/results", type=str, help='Where to save the pcd results')
        parser.add_argument('--dataset', default="mattarport3d", type=str, help='where to save the pcd results')
        parser.add_argument('--byproduct_save', default = "data/results", type=str, help='Where to save the byproduct, including snap images, masks, and lookup_dict')
        args = parser.parse_args()
        return args

    if __name__ == "__main__":
        
        v = viz.Visualizer()
        timestamp = datetime.datetime.now().strftime("%Y%m%d")
        # load all args
        args = get_args()   

        scene_id = os.path.splitext(plyfile)[0]
        height, width = args.img_size[0], args.img_size[1] 
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        snap_save_path = f"{args.byproduct_save}/{timestamp}_{scene_id}/snap/"
        lookup_save_path = f"{args.byproduct_save}/{timestamp}_{scene_id}/Lookup_dict/"
        result_save_path_2d = f"{args.byproduct_save}/{timestamp}_{scene_id}/result_vis_2d/"
        result_save_path_3d = f"{args.byproduct_save}/{timestamp}_{scene_id}/result_vis_3d/"
        result_mask_save_path = f"{args.result_save}/{timestamp}_{scene_id}/"
        string_list = args.vocab.split(';')

        CLASS_LABELS = [s.strip() for s in string_list]
        VALID_CLASS_IDS = np.arange(1, len(CLASS_LABELS) + 1).tolist()


        print("start to load models>>>>>>>>>>>>>>>>>>>>>>>>")
        # mask proposal module
        model = get_model(args.MPM_checkpoint)
        # model = torch.nn.DataParallel(model)
        model.eval()
        model.to(device) 
        odise_model = load_2d_model(args.vocab)

        print(f"finish loading models; start to process {scene_id}>>>>>>>>>>>>>>>>>>>>>>>>")

        # snap module
        print("snap:")
        pointcloud_file = f"data/input/{plyfile}"
        print(pointcloud_file)
        scene_id1 = ""
        # load mattarport3d as pcd
        pcd, _ = read_plymesh(pointcloud_file)
        xyz, rgb = pcd[:,:3], pcd[:,8:11]
        scan_pc = torch.from_numpy(np.hstack([xyz, rgb]))
        adjust_camera = [2, 0.1, 0.3]  
        image_generation_pcd(scan_pc, height, width, scene_id1, snap_save_path, adjust_camera=adjust_camera)

        print("mask:")
        # mask module
        mesh = load_mesh(pointcloud_file)
        data, _, _, features, _, inverse_map = prepare_data(mesh, device)
        with torch.no_grad():
            outputs = model(data, raw_coordinates=features)
        binary_mask = map_output_to_pointcloud(mesh, outputs, inverse_map, confidence_threshold = 0.8)

        print("build lookup dictionaries:")
        # build_lookup_dict
        build_lookup_dict_one_scene(odise_model, scene_id1, snap_save_path, lookup_save_path)
        print("mask2pixel lookup:")
        # mask2pixel lookup
        mask2pixel_lookup, _ = mask_classfication(binary_mask, scan_pc, adjust_camera, scene_id1, height, width, snap_save_path, lookup_save_path, result_mask_save_path, CLASS_LABELS, VALID_CLASS_IDS)

        # save and visulizize the results
        detection_results, detected_label_id = generate_detection_results(mask2pixel_lookup, binary_mask, CLASS_LABELS, VALID_CLASS_IDS)
        # save results in image
        save_results_2d(scan_pc, height, width, scene_id1, result_save_path_2d, adjust_camera, detection_results)
        save_visulization_3d(scan_pc.cpu().numpy(), args.vocab, binary_mask, detection_results[0], detected_label_id, scene_id, result_save_path_3d, save_ply = False)