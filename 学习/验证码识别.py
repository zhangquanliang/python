import os
import pytesseract
from PIL import Image
from collections import defaultdict

# tesseract.exe所在的文件路径
# pytesseract.pytesseract.tesseract_cmd = 'C://Program Files (x86)/Tesseract-OCR/tesseract.exe'


# 获取图片中像素点数量最多的像素
def get_threshold(image):
    pixel_dict = defaultdict(int)

    # 像素及该像素出现次数的字典
    rows, cols = image.size
    for i in range(rows):
        for j in range(cols):
            pixel = image.getpixel((i, j))
            pixel_dict[pixel] += 1

    count_max = max(pixel_dict.values())  # 获取像素出现出多的次数
    pixel_dict_reverse = {v: k for k, v in pixel_dict.items()}
    threshold = pixel_dict_reverse[count_max]  # 获取出现次数最多的像素点

    return threshold


# 按照阈值进行二值化处理
# threshold: 像素阈值
def get_bin_table(threshold):
    # 获取灰度转二值的映射table
    table = []
    for i in range(256):
        rate = 0.1  # 在threshold的适当范围内进行处理
        if threshold * (1 - rate) <= i <= threshold * (1 + rate):
            table.append(1)
        else:
            table.append(0)
    return table


# 去掉二值化处理后的图片中的噪声点
def cut_noise(image):
    rows, cols = image.size  # 图片的宽度和高度
    change_pos = []  # 记录噪声点位置

    # 遍历图片中的每个点，除掉边缘
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            # pixel_set用来记录该店附近的黑色像素的数量
            pixel_set = []
            # 取该点的邻域为以该点为中心的九宫格
            for m in range(i - 1, i + 2):
                for n in range(j - 1, j + 2):
                    if image.getpixel((m, n)) != 1:  # 1为白色,0位黑色
                        pixel_set.append(image.getpixel((m, n)))

            # 如果该位置的九宫内的黑色数量小于等于4，则判断为噪声
            if len(pixel_set) <= 4:
                change_pos.append((i, j))

    # 对相应位置进行像素修改，将噪声处的像素置为1（白色）
    for pos in change_pos:
        image.putpixel(pos, 1)

    return image  # 返回修改后的图片


# 识别图片中的数字加字母
# 传入参数为图片路径，返回结果为：识别结果
def OCR_lmj(img_path):
    image = Image.open(img_path)  # 打开图片文件
    imgry = image.convert('L')  # 转化为灰度图

    # 获取图片中的出现次数最多的像素，即为该图片的背景
    max_pixel = get_threshold(imgry)

    # 将图片进行二值化处理
    table = get_bin_table(threshold=max_pixel)
    out = imgry.point(table, '1')

    # 去掉图片中的噪声（孤立点）
    out = cut_noise(out)

    #保存图片
    out.save('2.jpg')

    # 仅识别图片中的数字
    # text = pytesseract.image_to_string(out, config='digits')
    # 识别图片中的数字和字母
    text = pytesseract.image_to_string(out)
    print(text)
    # 去掉识别结果中的特殊字符
    exclude_char_list = ' .:\\|\'\"?![],()~@#$%^&*_+-={};<>/¥'
    text = ''.join([x for x in text if x not in exclude_char_list])
    # print(text)

    return text


def main():
    # 识别指定文件目录下的图片

    # 单张图片识别
    image_path = '1.jpg'
    OCR_lmj(image_path)


if __name__ == '__main__':
    main()
