import os
from PIL import Image
import numpy as np


def png_to_npy(png_path, npy_path):
    try:
        # 打开 PNG 图像
        img = Image.open(png_path)
        # 将图像转换为 NumPy 数组
        img_array = np.array(img)
        # 保存为 .npy 文件
        np.save(npy_path, img_array)
        print(f"已将 {png_path} 转换并保存为 {npy_path}")
    except FileNotFoundError:
        print(f"未找到文件: {png_path}，请检查文件路径。")
    except Exception as e:
        print(f"转换过程中出现错误: {e}")


def batch_png_to_npy(input_folder, output_folder):
    # 如果输出文件夹不存在，则创建它
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有文件
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.png'):
                # 构建 PNG 文件的完整路径
                png_path = os.path.join(root, file)
                # 构建对应的 .npy 文件的完整路径
                relative_path = os.path.relpath(png_path, input_folder)
                npy_file_name = os.path.splitext(relative_path)[0] + '.npy'
                npy_path = os.path.join(output_folder, npy_file_name)
                # 创建 .npy 文件所在的目录
                npy_dir = os.path.dirname(npy_path)
                if not os.path.exists(npy_dir):
                    os.makedirs(npy_dir)
                # 调用转换函数
                png_to_npy(png_path, npy_path)


# 使用示例
input_folder = r'E:\dis(1)\dis\img'
output_folder = r'E:\dis(1)\dis\img\npy'
batch_png_to_npy(input_folder, output_folder)
