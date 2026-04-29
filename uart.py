

def send_hex_data(port, hex_data, baudrate=9600, timeout=1):
    """发送16进制数据到串口"""
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            # 转换数据为字节类型并发送
            if isinstance(hex_data, str):
                message = bytes.fromhex(hex_data.replace(" ", ""))
            elif isinstance(hex_data, list):
                message = bytes(hex_data)
            else:
                message = hex_data

            ser.write(message)
            print(f"已发送: {message.hex().upper()}")
            return True
    except Exception as e:
        print(f"发送错误: {e}")
        return False



import serial
import sys
import msvcrt  # Windows 系统下使用


import serial
import time


def receive(port, baudrate=9600, timeout=0.1):
    """
    接收并解析指定格式的串口数据，返回解析后的十进制坐标值

    数据格式: [0xFF, 数据长度, 数据1, 数据2, ..., 0xFE]
    解析逻辑:
    1. 检测包头 0xFF
    2. 读取数据长度字节
    3. 读取对应长度的数据字节
    4. 验证包尾 0xFE（可选）
    5. 返回十进制数据列表，遇到异常时返回已解析数据

    参数:
        port: 串口号
        baudrate: 波特率，默认 9600
        timeout: 串口读取超时时间，默认 0.1 秒

    返回:
        list: 解析后的十进制数据列表，异常时可能不完整
    """
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            print(f"开始监听 {port} 串口，按 'Ctrl+C' 退出...")
            buffer = bytearray()  # 数据缓冲区

            while True:
                # 读取串口数据并添加到缓冲区
                if ser.in_waiting:
                    data = ser.read(ser.in_waiting)
                    buffer.extend(data)

                # 解析缓冲区中的数据
                parsed_data = _parse_packet(buffer)
                if parsed_data is not None:
                    return parsed_data

                # 降低CPU占用
                time.sleep(0.1)


    except serial.SerialException as e:
        print(f"串口错误: {e}")
        return []
    except KeyboardInterrupt:
        print("\n用户中断，退出程序")
        return []
    except Exception as e:
        print(f"错误: {e}")
        return []


def _parse_packet(buffer):
    """内部函数：解析数据包"""
    len_buffer = len(buffer)

    # 寻找包头 0xFF
    for i in range(len_buffer):
        if buffer[i] == 0xFF:
            # 确保有足够数据读取数据长度
            if i + 1 >= len_buffer:
                break

            data_len = buffer[i + 1]
            expected_len = i + 1 + data_len + 1  # 包头+长度+数据+包尾

            # 检查数据长度是否合理
            if data_len < 0 or data_len > 255:
                print(f"数据异常: 无效数据长度 {data_len}")
                buffer[:i + 2] = b''  # 移除已处理的无效包头
                return []

            # 检查是否有足够数据
            if expected_len > len_buffer:
                break

            # 提取数据部分
            data_bytes = buffer[i + 2:i + 2 + data_len]
            packet_tail = buffer[i + 2 + data_len]

            # 验证包尾（可选，根据需求可跳过验证）
            if packet_tail != 0xFE:
                print(f"数据异常: 包尾错误 (期望 0xFE, 实际 0x{packet_tail:02X})")

            # 转换为十进制并返回
            parsed = [int(b) for b in data_bytes]
            print(f"解析数据: {parsed}")

            # 从缓冲区移除已解析的数据
            del buffer[:i + 2 + data_len + 1]
            return parsed

    return None  # 未解析到有效数据包


def serial_listen(port, baudrate=9600, timeout=0.01):
    """
    纯串口监听：持续接收并打印所有串口数据
    按 Ctrl+C 退出监听
    """
    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser:
            print(f"\n✅ 已开始监听 {port}，波特率：{baudrate}")
            print("ℹ️  实时打印收到的数据，按 Ctrl+C 退出\n")

            while True:
                # 读取所有缓存数据
                if ser.in_waiting > 0:
                    raw_data = ser.read(ser.in_waiting)

                    # 同时打印 十六进制 + 字符串格式
                    hex_str = raw_data.hex(' ').upper()  # 空格分隔
                    try:
                        str_data = raw_data.decode('utf-8', errors='replace')
                    except:
                        str_data = "无法解码"

                    print(f"📥 收到数据 | HEX: {hex_str} | STR: {str_data}")

                time.sleep(0.005)  # 极低延迟，不丢数据

    except serial.SerialException:
        print("❌ 串口打开失败，请检查串口号/权限")
    except KeyboardInterrupt:
        print("\n🛑 停止监听，返回主菜单")
def send_coordinate_data(coordinates, port="COM11",baudrate=9600, x_first=True):
    """
    打包坐标数据并通过串口发送，支持多种输入格式和坐标顺序自定义

    参数:
        port: 串口号 (如 '/dev/ttyUSB0' 或 'COM3')
        coordinates: 坐标数据，可以是单个坐标或多个坐标，格式支持：
                    - 单个坐标：[x, y], (x, y), x, y
                    - 多个坐标：[[x1, y1], [x2, y2]], [(x1, y1), (x2, y2)], (x1, y1, x2, y2)
        baudrate: 波特率，默认 9600
        x_first: 坐标顺序，True表示(x, y)，False表示(y, x)，默认True

    返回:
        bool: 发送是否成功
    """
    try:
        # 统一转换为列表格式处理
        if not isinstance(coordinates, (list, tuple)):
            # 处理单个坐标的非列表/元组输入 (如 coords=300, 400)
            coordinates = [coordinates]

        # 解析坐标数据
        parsed_coords = []
        for coord in coordinates:
            # 处理单个坐标的多种格式
            if isinstance(coord, (int, float)):
                # 处理形如 coords=300, 400 的输入
                if len(parsed_coords) == 0:
                    parsed_coords.append(coord)
                else:
                    # 组合成 (x, y)
                    x = parsed_coords.pop()
                    y = coord
                    parsed_coords.append((x, y) if x_first else (y, x))
            elif isinstance(coord, (list, tuple)):
                # 处理列表/元组格式的坐标
                if len(coord) == 2:
                    x, y = coord
                    parsed_coords.append((x, y) if x_first else (y, x))
                elif len(coord) % 2 == 0:
                    # 处理连续坐标数据 (如 (x1, y1, x2, y2))
                    for i in range(0, len(coord), 2):
                        x = coord[i]
                        y = coord[i + 1]
                        parsed_coords.append((x, y) if x_first else (y, x))
                else:
                    raise ValueError("坐标数据长度必须为偶数")
            else:
                raise ValueError("不支持的坐标格式")

        # 计算数据长度 (每个坐标占2字节)
        data_length = len(parsed_coords) * 2

        # 构建数据包
        packet = [0xFF, data_length]  # 包头 + 数据长度

        # 添加坐标数据
        for x, y in parsed_coords:
            packet.append(int(x) & 0xFF)  # x坐标低8位
            packet.append(int(y) & 0xFF)  # y坐标低8位

        packet.append(0xFE)  # 包尾

        # 打印发送的数据包（可选）
        hex_packet = [f"0x{b:02X}" for b in packet]
        print(f"发送数据包: {' '.join(hex_packet)}")

        # 打开串口并发送数据
        with serial.Serial(port, baudrate, timeout=1) as ser:
            # 等待串口就绪
            time.sleep(0.1)
            # 发送数据
            sent = ser.write(packet)
            # 验证发送字节数
            return sent == len(packet)

    except serial.SerialException as e:
        print(f"串口错误: {e}")
        return False
    except Exception as e:
        print(f"发送错误: {e}")
        return False

if __name__ == "__main__":
    PORT = 'COM11'  # 修改为你的串口
    print("\n=== 串口交互菜单 ===")
    print("1. 接收数据")
    print("2. 发送数据")
    print("0. 退出程序")

    while True:
        try:
            choice = input("\n请选择功能 (0-2): ")

            if choice == '0':
                print("程序退出")
                break

            elif choice == '1':
                print("\n--- 接收模式 ---")

                print("按 Ctrl+C 退出接收模式")
                try:
                    while True:

                        data = receive("COM11")
                        if data:
                            print(f"接收到数据: {data}")
                except KeyboardInterrupt:
                    print("\n返回主菜单")

            elif choice == '2':
                print("\n--- 发送模式 ---")
                send_success = send_hex_data(PORT, [0xFF, 0x04, 0x8B, 0xAE, 0xB6,0x70,0xFE]) # 异常情况
                if send_success:
                    print(f"发送成功")
                else:
                    print("发送失败")
            elif choice == '3':
                print("\n--- 纯串口监听模式 ---")
                serial_listen(PORT)  # 直接调用纯监听函数
            else:
                print("无效选择，请输入 0-2")

        except Exception as e:
            print(f"操作错误: {e}")
