import os
import random
import shutil

# 数据集根目录
data_dir = r"D:\yolo\data_pink\datasets"
images_dir = os.path.join(data_dir, "images")
labels_dir = os.path.join(data_dir, "labels")

# 在 images 和 labels 文件夹下创建 train 和 test 文件夹
train_images_dir = os.path.join(images_dir, "train")
train_labels_dir = os.path.join(labels_dir, "train")
test_images_dir = os.path.join(images_dir, "test")
test_labels_dir = os.path.join(labels_dir, "test")

for dir_path in [train_images_dir, train_labels_dir, test_images_dir, test_labels_dir]:
    os.makedirs(dir_path, exist_ok=True)

# 获取所有图片文件名
image_files = os.listdir(images_dir)
# 过滤掉子文件夹
image_files = [f for f in image_files if os.path.isfile(os.path.join(images_dir, f))]
random.shuffle(image_files)

# 划分训练集和测试集
split_ratio = 0.8
train_size = int(len(image_files) * split_ratio)
train_files = image_files[:train_size]
test_files = image_files[train_size:]

# 移动训练集文件
for image_file in train_files:
    image_path = os.path.join(images_dir, image_file)
    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join(labels_dir, label_file)

    shutil.move(image_path, os.path.join(train_images_dir, image_file))
    if os.path.exists(label_path):
        shutil.move(label_path, os.path.join(train_labels_dir, label_file))

# 移动测试集文件
for image_file in test_files:
    image_path = os.path.join(images_dir, image_file)
    label_file = os.path.splitext(image_file)[0] + ".txt"
    label_path = os.path.join(labels_dir, label_file)

    shutil.move(image_path, os.path.join(test_images_dir, image_file))
    if os.path.exists(label_path):
        shutil.move(label_path, os.path.join(test_labels_dir, label_file))

print("数据划分完成！")
