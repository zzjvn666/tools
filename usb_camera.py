import cv2


def get_supported_resolutions_fps(camera_index):
    cap = cv2.VideoCapture(camera_index)
    supported_resolutions_fps = []
    common_resolutions = [
        (640, 480), (800, 600), (1024, 768), (1280, 720), (1280, 1024), (1920, 1080)
    ]
    for width, height in common_resolutions:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps > 0:
            supported_resolutions_fps.append((width, height, fps))
    cap.release()
    return supported_resolutions_fps


def main():
    camera_index = 0
    supported_resolutions_fps = get_supported_resolutions_fps(camera_index)
    print("支持的分辨率和帧率:")
    for i, (width, height, fps) in enumerate(supported_resolutions_fps):
        print(f"{i + 1}. 分辨率: {width}x{height}, 帧率: {fps}")

    choice = int(input("请输入你要选择的序号: ")) - 1
    if 0 <= choice < len(supported_resolutions_fps):
        width, height, fps = supported_resolutions_fps[choice]
        cap = cv2.VideoCapture(camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FPS, fps)

        while True:
            ret, frame = cap.read()
            if ret:
                cv2.imshow('USB Camera', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("无效的选择")


if __name__ == "__main__":
    main()
