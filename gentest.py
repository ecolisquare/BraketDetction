from element import *
import matplotlib.pyplot as plt
from utils import *
from infoextraction import *
import numpy as np
import os
from plot_geo import *
from draw_dxf import *
from config import *


            

def process_json_files(folder_path, output_foler, dxf_path):
    # 检查文件夹是否存在
    if not os.path.isdir(folder_path):
        print(f"路径 {folder_path} 不存在或不是一个文件夹。")
        return
    
    all_bbox = []
    all_classi = []
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
                bboxs, classi_res = process_json_data(file_path, output_path)  # 对数据进行操作
                all_bbox.extend(bboxs)
                all_classi.extend(classi_res)
            except json.JSONDecodeError as e:
                print(f"解析JSON文件 {file_path} 时出错: {e}")
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {e}")
    
    # 将所有检测结果画到一张图纸上
    try:
        draw_rectangle_in_dxf(dxf_path, folder_path, all_bbox, all_classi)
    except Exception as e:
        print(f"绘制dxf文件到 {folder_path} 时出错: {e}")

def process_json_data(json_path, output_path):
    segmentation_config=SegmentationConfig()
    segmentation_config.json_path = json_path
    segmentation_config.line_image_path = os.path.join(output_path, "line.png")
    segmentation_config.poly_image_dir = os.path.join(output_path, "poly_image")
    segmentation_config.poly_info_dir = os.path.join(output_path, "poly_info")
    segmentation_config.res_image_path = os.path.join(output_path, "res.png")
    segmentation_config.dxf_output_folder = os.path.join(output_path)

    try:
        # os.makedirs(segmentation_config.poly_image_dir, exist_ok=True)
        os.makedirs(segmentation_config.poly_info_dir, exist_ok=True)
    except Exception as e:
        print(f"创建文件夹时出错: {e}")

    if segmentation_config.verbose:
        print("读取json文件")
    #文件中线段元素的读取和根据颜色过滤
    elements,segments,ori_segments,stiffeners=readJson(json_path,segmentation_config)
    #将线进行适当扩张
    
    texts ,dimensions=findAllTextsAndDimensions(elements)
    ori_dimensions=dimensions
    dimensions=processDimensions(dimensions)
    texts=processTexts(texts)
    if segmentation_config.verbose:
        print("json文件读取完毕")
    

    #找出所有包含角隅孔圆弧的基本环
    ppolys, new_segments, point_map,star_pos_map,cornor_holes,text_map=findClosedPolys_via_BFS(elements,texts,dimensions,segments,segmentation_config)
    # output_training_data(ppolys, training_data_output_folder, name)

    # output_training_img(ppolys, new_segments, training_img_output_folder, name)
    #结构化输出每个肘板信息
    polys_info = []
    classi_res = []
    print("正在输出结构化信息...")
    for i, poly in enumerate(ppolys):
        try:
            res = outputPolyInfo(poly, ori_segments, segmentation_config, point_map, i, star_pos_map, cornor_holes,texts,dimensions,text_map,stiffeners)
        except Exception as e:
            res=None
            print(e)
        if res is not None:
            polys_info.append(res[0])
            classi_res.append(res[1])

    print("结构化信息输出完毕，保存于:", segmentation_config.poly_info_dir)

    outputRes(new_segments, point_map, polys_info, segmentation_config.res_image_path,segmentation_config.draw_intersections,segmentation_config.draw_segments,segmentation_config.line_image_drawPolys)

    #将检测到的肘板标注在原本的dxf文件中
    bboxs = []
    for poly_refs in polys_info:
        max_x = float('-inf')
        min_x = float('inf')
        max_y = float('-inf')
        min_y = float('inf')
        for seg in poly_refs:
            # 提取起点和终点的横纵坐标
            x_coords = [seg.start_point[0], seg.end_point[0]]
            y_coords = [seg.start_point[1], seg.end_point[1]]

            # 更新最大最小值
            max_x = max(max_x, *x_coords)
            min_x = min(min_x, *x_coords)
            max_y = max(max_y, *y_coords)
            min_y = min(min_y, *y_coords)

        bbox = [[min_x, min_y], [max_x, max_y]]
        bboxs.append(bbox)
    
    try:
        dxf_path = os.path.splitext(segmentation_config.json_path)[0] + '.dxf'
        dxf_output_folder = segmentation_config.dxf_output_folder
        draw_rectangle_in_dxf(dxf_path, dxf_output_folder, bboxs, classi_res)
    except Exception as e:
        print("子图dxf生成错误:", e)
    
    return bboxs, classi_res


if __name__ == '__main__':
    folder_path = "/home/user10/code/BraketDetection/test2"
    output_folder = "./output"
    dxf_path = "/home/user10/code/BraketDetection/test2/all.dxf"
    process_json_files(folder_path, output_folder, dxf_path)
