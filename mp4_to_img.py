import cv2
import os


def video_to_frames(video_file, output_folder):
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 打开视频文件
    cap = cv2.VideoCapture(video_file)

    # 初始化帧计数器
    count = 0

    # 读取视频中的帧
    while True:
        # 读取一帧
        ret, frame = cap.read()

        # 如果读取帧失败，则跳出循环
        if not ret:
            break

        # 每隔100帧保存一次图片
        if count % 100 == 0:
            # 定义输出图片的文件名
            filename = f"{output_folder}/frame_{count}.png"
            # 保存帧为PNG图片
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")

        # 增加帧计数器
        count += 1

    # 释放视频捕获对象
    cap.release()


if __name__ == "__main__":
    # 视频文件的路径
    video_file_path = r"C:\Users\crz\Downloads\QQ2025126-20460.mp4"
    # 输出图片的文件夹路径
    output_folder_path = 'output_frames'

    # 调用函数
    video_to_frames(video_file_path, output_folder_path)
