import cv2
import os

# 图片文件夹路径
image_folder = r"D:\yolo\datasets_train_test_ld\images\train"
# 输出视频文件路径
video_name = 'output_video.mp4'

# 获取图片文件列表
images = [img for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]


# 按文件名中的数字部分从小到大排序
def extract_number(filename):
    # 提取文件名中的数字部分
    import re
    numbers = re.findall(r'\d+', filename)
    return int(numbers[0]) if numbers else float('inf')


images = sorted(images, key=extract_number)

# 读取第一张图片以获取尺寸
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

# 定义视频编码器和创建VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc, 10, (width, height))

# 遍历图片列表并写入视频
for image in images:
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    # 调整图片尺寸为统一大小
    frame = cv2.resize(frame, (width, height))
    video.write(frame)

# 释放资源
video.release()
cv2.destroyAllWindows()

print(f"视频已保存为 {video_name}")
