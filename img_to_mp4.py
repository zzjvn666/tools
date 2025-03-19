import cv2
import os

# 图片文件夹路径
image_folder = r"D:\yolo\data\images\test"
# 输出视频文件路径
video_name = 'output_video.mp4'

# 获取图片文件列表并按文件名排序
images = [img for img in os.listdir(image_folder) if img.endswith(('.png', '.jpg', '.jpeg'))]
images.sort()

# 读取第一张图片以获取尺寸
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

# 定义视频编码器和创建VideoWriter对象
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter(video_name, fourcc,60, (width, height))

# 遍历图片列表并写入视频
for image in images:
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    video.write(frame)

# 释放资源
video.release()
cv2.destroyAllWindows()

print(f"视频已保存为 {video_name}")