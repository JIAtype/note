查看驱动支持的 CUDA 版本。
```
nvidia-smi
```

查看电脑安装的CUDO版本。查看 CUDA 工具包版本。
```
nvcc --version
```

Uninstall your current PyTorch installation
```
pip uninstall torch torchvision torchaudio
```

if you have CUDA 12.1 installed, you might use:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

After installation, run this Python code to check if CUDA is available:
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device count: {torch.cuda.device_count()}")
if torch.cuda.is_available():
    print(f"Current CUDA device: {torch.cuda.current_device()}")
    print(f"CUDA device name: {torch.cuda.get_device_name()}")

import torch
print(f"torch version: {torch.version.cuda}")
```

ONNX Runtime 的 CUDA 支持需与你的 CUDA 工具包版本（12.1） 对齐，而非驱动版本（驱动通常兼容更高版本）。