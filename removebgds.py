import os
from rembg import remove
from PIL import Image

# 输入和输出目录
input_dir = "/Users/max/Downloads/unsplash"
output_dir = "/Users/max/Downloads/unsplash_output"

# 支持的图片格式
allowed_extensions = {".jpg", ".jpeg", ".png", ".webp"}

# 创建输出目录
os.makedirs(output_dir, exist_ok=True)

# 遍历输入目录
for filename in os.listdir(input_dir):
    # 检查文件扩展名
    ext = os.path.splitext(filename)[1].lower()
    if ext not in allowed_extensions:
        continue
    
    # 输入输出路径
    input_path = os.path.join(input_dir, filename)
    output_path = os.path.join(output_dir, f"{os.path.splitext(filename)[0]}_output.png")
    
    try:
        # 打开并处理图片
        with open(input_path, "rb") as f_in:
            img_data = f_in.read()
            output_data = remove(img_data)  # 自动抠图
        
        # 保存结果（默认保存为PNG透明背景）
        with open(output_path, "wb") as f_out:
            f_out.write(output_data)
        
        print(f"处理成功: {filename} → {output_path}")
    except Exception as e:
        print(f"处理失败: {filename} - 错误信息: {str(e)}")