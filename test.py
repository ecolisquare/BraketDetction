from element import *
import matplotlib.pyplot as plt
from utils import *
from infoextraction import *
import numpy as np
import os
from plot_geo import *

from config import *

def process_json_files(folder_path, output_foler):
    # 检查文件夹是否存在
    if not os.path.isdir(folder_path):
        print(f"路径 {folder_path} 不存在或不是一个文件夹。")
        return
    
    # 遍历文件夹中的每个文件
    for filename in os.listdir(folder_path):
        # 检查文件是否是JSON文件
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_foler, name)
            print(f"正在处理文件: {file_path}")
            
            # 打开并读取JSON文件内容
            try:
                process_json_data(file_path, output_path)  # 对数据进行操作
            except json.JSONDecodeError as e:
                print(f"解析JSON文件 {file_path} 时出错: {e}")
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")

def process_json_data(json_path, output_path):
    segmentation_config=SegmentationConfig()
    segmentation_config.line_image_path = os.path.join(output_path, "line.png")
    segmentation_config.poly_image_dir = os.path.join(output_path, "poly_image")
    segmentation_config.poly_info_dir = os.path.join(output_path, "poly_info")
    segmentation_config.res_image_path = os.path.join(output_path, "res.png")

    try:
        os.makedirs(segmentation_config.poly_image_dir, exist_ok=True)
        os.makedirs(segmentation_config.poly_info_dir, exist_ok=True)
    except Exception as e:
        print(f"创建文件夹时出错: {e}")

    if segmentation_config.verbose:
        print("读取json文件")
    #文件中线段元素的读取和根据颜色过滤
    elements,ori_segments=readJson(json_path)
    if segmentation_config.verbose:
        print("json文件读取完毕")
    #将线进行适当扩张
    segments=expandFixedLength(ori_segments,segmentation_config.line_expand_length)

    #找出所有包含角隅孔圆弧的基本环
    ppolys, new_segments, point_map,star_pos_map,cornor_holes=findClosedPolys_via_BFS(elements,segments,segmentation_config)

    #结构化输出每个肘板信息
    print("正在输出结构化信息...")
    polys_info = []
    print("正在输出结构化信息...")
    for i, poly in enumerate(ppolys):
        res = outputPolyInfo(poly, new_segments, segmentation_config, point_map, i, star_pos_map, cornor_holes)
        if res is not None:
            polys_info.append(res)

    print("结构化信息输出完毕，保存于:", segmentation_config.poly_info_dir)

    outputRes(new_segments, point_map, polys_info, segmentation_config.res_image_path,segmentation_config.draw_intersections,segmentation_config.draw_segments,segmentation_config.line_image_drawPolys)



folder_path = "/home/user10/code/BraketDetection/data/split"
output_foler = "/home/user10/code/BraketDetection/output"
process_json_files(folder_path, output_foler)