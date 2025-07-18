# 根据官方文档，运行和训练 YOLO11 时，需安装以下主要库和版本要求：

1. Python：推荐使用 Python 3.12（不建议用 3.13.1，部分依赖可能不兼容）[(1)](https://docs.ultralytics.com/guides/azureml-quickstart)。
2. Ultralytics 包（含 YOLO11 支持）[(2)](https://docs.ultralytics.com/models/yolo11)[(1)](https://docs.ultralytics.com/guides/azureml-quickstart)。
3. onnx（如需模型导出到 ONNX 格式）[(1)](https://docs.ultralytics.com/guides/azureml-quickstart)。

Windows -> "Anaconda Prompt"安装步骤示例：

```bash
conda create --prefix D:\AI\my_envs\yolo11 python=3.12
conda activate D:\AI\my_envs\yolo11
pip install ultralytics
pip install ultralytics onnx
```
[(1)](https://docs.ultralytics.com/guides/azureml-quickstart)

如需完整依赖，可在 ultralytics 目录下执行：

```bash
pip install -r requirements.txt
```
[(1)](https://docs.ultralytics.com/guides/azureml-quickstart)

主要依赖：
- ultralytics
- onnx

版本要求：
- Python 3.12（推荐）
- Ultralytics 最新版
- onnx 最新稳定版

请根据实际需求选择合适的 Python 版本，避免使用 3.13.1 及以上[(1)](https://docs.ultralytics.com/guides/azureml-quickstart)。

# GPU设置

使用指令`nvidia-smi`查看你的 CUDA 版本，版本向下兼容，12.6的可以用cu118。安装 PyTorch（根据你的 CUDA 版本）。

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

```python
import torch

print(torch.__version__)
print(torch.cuda.is_available())
print(torch.cuda.device_count())
print(torch.version.cuda)
```

显示结果
```
2.7.0+cu118
True
1
11.8
```

```python
pip install -r requirements.txt
```

Windows -> "Anaconda Prompt"
```bash
pip3 install --upgrade labelme

labelme
```

---

尝试[Label Studio](https://labelstud.io/)
官方安装教程[Quick start](https://labelstud.io/guide/quick_start)

(base) C:\Users\splsip258>conda create --prefix D:\my_envs\lable python=3.10

(base) C:\Users\splsip258>conda activate D:\my_envs\lable

(D:\my_envs\lable) C:\Users\splsip258>python -m pip install label-studio

(D:\my_envs\lable) C:\Users\splsip258>label-studio

打开了网站http://localhost:8080/user/login/

登陆后进入网站http://localhost:8080/

得一个一个涂零件，太慢了。

还是用lableme试一试

好像有YOLO专用的版本，会把数据转换成yolo用的格式

(D:\AI\my_envs\yolo11) C:\Users\splssipifmsadmin>pip install labelme2yolo

用命令行把 ./labelme_json 目录下的 JSON 文件转换为 YOLO 格式，并按照 80% 训练集和 20% 验证集的比例进行划分。

labelme2yolo --json_dir ./labelme_json --val_size 0.2

Labelme2YOLOv8 是专门为 YOLOv8 设计的转换工具，支持将 LabelMe 的 JSON 数据集转换为 YOLOv8 格式。

安装：

pip install Labelme2YOLOv8

使用示例：

labelme2yolov8 --json_dir ./labelme_json --val_size 0.2

该工具同样会生成符合 YOLOv8 要求的目录结构和标注文件。

# 实际操作

用labelme标好之后，保存下来json文件，与标注的图片同名。

直接用“labelme2yolo --json_dir ./labelme_json --val_size 0.2”得到了格式正确的数据集。./labelme_json是json文件的位置

然后用官方的代码训练模型

几行就解决了，真的很快很方便。

app.ipynb里的代码也可以下载模型，不用自己再下载模型。
