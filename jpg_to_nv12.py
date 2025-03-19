import cv2
import numpy as np

# 输入和输出路径
jpg_path = r"C:\Users\n\Pictures\test_taiji_1.jpg"
nv12_path = r"C:\Users\n\Pictures\test_taiji_960x544_1.nv12"

# 读取 JPG 图片
image = cv2.imread(jpg_path)

# 调整大小到 960x544
resized = cv2.resize(image, (960, 544))

# 转换为 YUV420 (NV12) 格式
yuv = cv2.cvtColor(resized, cv2.COLOR_BGR2YUV_I420)

# 提取 Y、U、V 分量
h, w = 544, 960
y_plane = yuv[:h, :w]
u_plane = yuv[h:h + h // 4, :w].reshape(-1)
v_plane = yuv[h + h // 4:, :w].reshape(-1)

# 组合成 NV12 格式（Y + UV 交错存储）
uv_plane = np.zeros((h // 2, w), dtype=np.uint8)
uv_plane[:, 0::2] = u_plane.reshape(h // 2, w // 2)
uv_plane[:, 1::2] = v_plane.reshape(h // 2, w // 2)

# 保存 NV12 文件
with open(nv12_path, 'wb') as f:
    f.write(y_plane.tobytes())
    f.write(uv_plane.tobytes())

print(f"转换完成，NV12 文件已保存到 {nv12_path}")
# 读取 NV12 文件
with open(nv12_path, 'rb') as f:
    y_data = np.frombuffer(f.read(w * h), dtype=np.uint8).reshape(h, w)
    uv_data = np.frombuffer(f.read(w * h // 2), dtype=np.uint8).reshape(h // 2, w)

# 重新构造 U 和 V 平面
u_data = uv_data[:, 0::2].reshape(h // 4, w)
v_data = uv_data[:, 1::2].reshape(h // 4, w)

# 还原 I420 格式
yuv_reconstructed = np.vstack([y_data, u_data, v_data])

# 转换回 BGR 并显示
bgr_image = cv2.cvtColor(yuv_reconstructed, cv2.COLOR_YUV2BGR_I420)
cv2.imshow("NV12 to BGR", bgr_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
