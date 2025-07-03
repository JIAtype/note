# pip install pdf2image
# 安装 pdf2image 和 poppler（后者是 PDF 渲染引擎）

# 安装 Poppler：
# 下载地址：https://github.com/oschwartz10612/poppler-windows/releases
# 解压后，将 bin 文件夹路径添加到系统环境变量 PATH 中。

from pdf2image import convert_from_path
import os

# 设置路径
pdf_path = "input.pdf"  # 替换为你的 PDF 文件路径
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

# 转换 PDF 为图片
images = convert_from_path(pdf_path)
for i, image in enumerate(images):
    image_path = os.path.join(output_folder, f"page_{i + 1}.jpg")
    image.save(image_path, "JPG")
    print(f"Saved: {image_path}")
