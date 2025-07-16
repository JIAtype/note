# 在Anaconda Prompt里 指定位置创建虚拟环境

## 每个新项目都要创建新环境！！！

在anaconda prompt里运行
```
conda create --prefix D:\AI\my_envs\nanonets-ocr python=3.10
```
在terminal运行
```
conda activate D:\AI\my_envs\nanonets-ocr
pip install torch torchvision transformers timm pillow
```
### 创建环境到D盘
```
conda create --prefix D:\my_envs\yolo8 python=3.10
```
### 激活环境
```
conda activate D:\my_envs\yolo8
```
### 安装包（例如安装numpy）
```
conda install numpy
```
### 退出环境
```
conda deactivate
```
---

# 检查conda安装

首先，确认conda是否正确安装。在终端或命令提示符中运行：
```
conda --version
```
如果显示版本号，说明conda已安装。

---

# 常见conda指令

```
conda create -n your_env_name python=x.x

conda activate your_env_name

deactivate your_env_name

conda env list

conda list

```

---

# 如果VSCode无法识别conda：

方法1.关闭并重新打开VSCode

方法2.手动选择conda环境

在VSCode中：

- 按F1或Ctrl+Shift+P打开命令面板
- 输入"Python: Select Interpreter"
- 如果列表中显示conda环境，选择它
- 如果没有显示，点击"Enter interpreter path..."并手动定位到您的conda环境

方法3.在settings.json中设置conda路径

在VSCode中打开设置(Ctrl+,)，然后搜索"python.condaPath"，设置为您conda可执行文件的完整路径，例如：

对于Windows:

```
"python.condaPath": "C:\\Users\\用户名\\miniconda3\\Scripts\\conda.exe"
```

对于Mac/Linux:

```
"python.condaPath": "/home/用户名/miniconda3/bin/conda"
```

查看您的conda路径,打开Anaconda Prompt终端，输入指令即可看到。

```
where conda
```

环境设置好后，在VSCode中创建新的终端，conda环境应该能够被正确识别。