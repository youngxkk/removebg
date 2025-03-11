import os
import io
import numpy as np
from rembg import remove
from PIL import Image

def auto_crop(image):
    """
    根据图片的 alpha 通道自动裁剪出非透明区域（即主体部分）。
    image 应为 RGBA 模式
    """
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    np_image = np.array(image)
    # 获取 alpha 通道
    alpha = np_image[:, :, 3]
    # 找出非透明区域的行和列
    non_empty_columns = np.where(alpha.max(axis=0) > 0)[0]
    non_empty_rows = np.where(alpha.max(axis=1) > 0)[0]
    if non_empty_rows.size and non_empty_columns.size:
        crop_box = (
            int(non_empty_columns[0]),
            int(non_empty_rows[0]),
            int(non_empty_columns[-1] + 1),
            int(non_empty_rows[-1] + 1)
        )
        return image.crop(crop_box)
    return image

# 输入和输出文件夹路径
input_folder = '/Users/max/Downloads/unsplash'
output_folder = '/Users/max/Downloads/unsplash_output'
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历文件夹中所有图片
for filename in os.listdir(input_folder):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_folder, filename)
        # 输出文件以 PNG 格式保存（保证透明通道）
        output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.png')
        
        # 读取图片数据
        with open(input_path, 'rb') as f:
            input_data = f.read()
        
        # 使用 rembg 去除背景
        result_data = remove(input_data)
        
        # 将结果数据转为 PIL Image 对象
        result_image = Image.open(io.BytesIO(result_data))
        
        # 根据 alpha 通道自动裁剪图片，仅保留主体
        cropped_image = auto_crop(result_image)
        
        # 保存最终图片
        cropped_image.save(output_path)
        print(f"处理完成: {filename}")
