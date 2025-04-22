import os
import shutil

# 数据集根目录
data_dir = r"D:\yolo\data_mix_test"
images_dir = os.path.join(data_dir, "images")
labels_dir = os.path.join(data_dir, "labels")

# 创建用于存放要删除标签文件的文件夹
labels_train_del_dir = os.path.join(data_dir, "labels_train_del")
labels_test_del_dir = os.path.join(data_dir, "labels_test_del")
os.makedirs(labels_train_del_dir, exist_ok=True)
os.makedirs(labels_test_del_dir, exist_ok=True)


def check_and_move_labels(label_folder, image_folder, del_folder):
    for root, _, files in os.walk(label_folder):
        for label_file in files:
            if label_file.endswith('.txt'):
                base_name = os.path.splitext(label_file)[0]
                # 假设图片格式为jpg，可按需修改
                image_file = base_name + ".jpg"
                image_path = os.path.join(image_folder, image_file)
                if not os.path.exists(image_path):
                    shutil.move(os.path.join(root, label_file),
                                os.path.join(del_folder, label_file))


# 检查测试集标签
test_images_dir = os.path.join(images_dir, "test")
test_labels_dir = os.path.join(labels_dir, "test")
check_and_move_labels(test_labels_dir, test_images_dir, labels_test_del_dir)

# 检查训练集标签
train_images_dir = os.path.join(images_dir, "train")
train_labels_dir = os.path.join(labels_dir, "train")
check_and_move_labels(train_labels_dir, train_images_dir, labels_train_del_dir)

print("检查完成，无对应图片的标签文件已移动到相应文件夹！")
