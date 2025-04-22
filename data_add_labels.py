import os
import shutil

# 数据集根目录
data_root = r"D:\yolo\data_mix_test"

# 定义各目录路径
images_train_dir = os.path.join(data_root, "images", "train")
images_test_dir = os.path.join(data_root, "images", "test")
labels_train_dir = os.path.join(data_root, "labels", "train")
labels_test_dir = os.path.join(data_root, "labels", "test")
extra_labels_dir = os.path.join(data_root, "labelss")

# 确保 labels 下的 train 和 test 目录存在
os.makedirs(labels_train_dir, exist_ok=True)
os.makedirs(labels_test_dir, exist_ok=True)


def check_and_process_labels(image_dir, label_dir):
    for image_file in os.listdir(image_dir):
        # 提取图片文件名（不含扩展名）
        base_name = os.path.splitext(image_file)[0]
        # 构建对应的标签文件名
        label_file = f"{base_name}.txt"
        # 构建当前标签文件路径
        current_label_path = os.path.join(label_dir, label_file)

        if not os.path.exists(current_label_path):
            # 尝试从备用标签目录查找
            extra_label_path = os.path.join(extra_labels_dir, label_file)
            if os.path.exists(extra_label_path):
                # 若找到，复制到对应的标签目录
                shutil.copy(extra_label_path, current_label_path)
            else:
                # 若未找到，打印缺失信息
                print(f"{os.path.basename(label_dir)} 中 {label_file} 缺失")


# 检查训练集图片对应的标签
check_and_process_labels(images_train_dir, labels_train_dir)

# 检查测试集图片对应的标签
check_and_process_labels(images_test_dir, labels_test_dir)

print("检查完成。")
