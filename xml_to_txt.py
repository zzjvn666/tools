import os
import xml.etree.ElementTree as ET

def convert(size, box):
    """
    将边界框坐标转换为归一化的中心坐标和宽高
    :param size: 图像的宽度和高度 (width, height)
    :param box: 边界框的坐标 (xmin, xmax, ymin, ymax)
    :return: 归一化后的中心坐标和宽高 (x_center, y_center, width, height)
    """
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)

def convert_xml_to_yolo(xml_path, output_path, classes):
    """
    将XML文件转换为YOLO格式的TXT文件
    :param xml_path: XML文件的路径
    :param output_path: 输出TXT文件的路径
    :param classes: 类别列表
    """
    tree = ET.parse(xml_path)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    with open(output_path, 'w') as out_file:
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text),
                 float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            bb = convert((w, h), b)
            out_file.write(f"{cls_id} {' '.join(map(str, bb))}\n")

def batch_convert_xml_to_yolo(xml_dir, output_dir, classes):
    """
    批量将XML文件转换为YOLO格式的TXT文件
    :param xml_dir: XML文件所在的目录
    :param output_dir: 输出TXT文件的目录
    :param classes: 类别列表
    """
    os.makedirs(output_dir, exist_ok=True)
    for xml_file in os.listdir(xml_dir):
        if xml_file.endswith('.xml'):
            xml_path = os.path.join(xml_dir, xml_file)
            txt_file = os.path.splitext(xml_file)[0] + '.txt'
            output_path = os.path.join(output_dir, txt_file)
            convert_xml_to_yolo(xml_path, output_path, classes)

# 示例使用
if __name__ == "__main__":
    # 定义类别列表
    classes = ["lines","batteries","qrcode","park"]
    # XML文件所在的目录
    xml_dir = r'D:\yolo\datasets_park\Annotations'
    # 输出TXT文件的目录
    output_dir = r'D:\yolo\datasets_park\labels'
    batch_convert_xml_to_yolo(xml_dir, output_dir, classes)