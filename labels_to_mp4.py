import cv2
import os
import numpy as np
from tqdm import tqdm

# 定义函数来绘制边界框
def draw_bounding_boxes(image, boxes):
    height, width, _ = image.shape
    for box in boxes:
        class_id = int(box[0])
        x_center = float(box[1]) * width
        y_center = float(box[2]) * height
        box_width = float(box[3]) * width
        box_height = float(box[4]) * height

        x = int(x_center - box_width / 2)
        y = int(y_center - box_height / 2)
        w = int(box_width)
        h = int(box_height)

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, str(class_id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image


# 定义函数来处理数据集
def process_dataset(labels_folder, images_folder, output_path):
    images = []
    for filename in tqdm(os.listdir(images_folder)):
        if filename.endswith('.png'):
            image_path = os.path.join(images_folder, filename)
            label_path = os.path.join(labels_folder, filename.replace('.png', '.txt'))

            image = cv2.imread(image_path)
            boxes = []
            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        box = line.strip().split()
                        boxes.append(box)

            image_with_boxes = draw_bounding_boxes(image, boxes)
            images.append(image_with_boxes)

    # 保存为 MP4 视频
    if images:
        height, width, _ = images[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

        for img in images:
            out.write(img)

        out.release()


if __name__ == "__main__":
    while True:
        labels_folder = input("请输入 labels 文件夹的路径: ")
        if os.path.isdir(labels_folder):
            break
        else:
            print("输入的 labels 文件夹路径无效，请重新输入。")

    while True:
        images_folder = input("请输入 images 文件夹的路径: ")
        if os.path.isdir(images_folder):
            break
        else:
            print("输入的 images 文件夹路径无效，请重新输入。")

    while True:
        output_path = input("请输入输出视频文件的路径（例如：output.mp4）: ")
        if output_path.endswith('.mp4'):
            break
        else:
            print("输出文件的扩展名必须为 .mp4，请重新输入。")

    process_dataset(labels_folder, images_folder, output_path)