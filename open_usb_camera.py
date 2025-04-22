import cv2

# 打开默认摄像头
cap = cv2.VideoCapture(0)

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

while True:
    # 逐帧捕获
    ret, frame = cap.read()

    # 如果正确读取帧，ret 为 True
    if not ret:
        print("无法接收帧，退出...")
        break

    # 显示结果帧
    cv2.imshow('Camera', frame)

    # 按 'q' 键退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 完成所有操作后，释放捕获器并关闭所有窗口
cap.release()
cv2.destroyAllWindows()
