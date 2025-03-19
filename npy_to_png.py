import os
import numpy as np
from PIL import Image


def npy_to_mono16_png(npy_file_path, output_image_path):
    # 加载 .npy 文件
    data = np.load(npy_file_path)

    # 检查数据类型
    if data.dtype == np.uint8:
        mode = 'L'
    elif data.dtype == np.uint16:
        mode = 'I;16'
    else:
        # 如果数据类型不是 uint8 或 uint16，尝试进行转换
        if data.min() >= 0 and data.max() <= 255:
            data = data.astype(np.uint8)
            mode = 'L'
        elif data.min() >= 0 and data.max() <= 65535:
            data = data.astype(np.uint16)
            mode = 'I;16'
        else:
            print(f"不支持的数据范围，无法无损转换: 数据范围为 [{data.min()}, {data.max()}]")
            return

    # 创建 PIL 图像对象
    img = Image.fromarray(data, mode=mode)

    # 保存为无损的 .png 图像
    img.save(output_image_path, 'PNG', compress_level=0)
    print(f"图片已保存至 {output_image_path}")


def batch_convert_npy_to_mono16_png(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.npy'):
                npy_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(npy_file_path, input_folder)
                output_image_path = os.path.join(output_folder, os.path.splitext(relative_path)[0] + '.png')
                output_dir = os.path.dirname(output_image_path)
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                npy_to_mono16_png(npy_file_path, output_image_path)


# 使用示例
input_folder = r'E:\dis(1)\dis'
output_folder = r'E:\dis(1)\dis\img'
batch_convert_npy_to_mono16_png(input_folder, output_folder)
