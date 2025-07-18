要快速开始使用 YOLO11 进行本地数据微调（如零件表面瑕疵检测），可参考以下步骤：

1. 准备你的本地数据集，标注好目标（如表面瑕疵）类别和位置，数据格式需符合 YOLO 要求（可用 coco8.yaml 作为参考）[(1)](https://docs.ultralytics.com/models/yolo11)[(2)](https://docs.ultralytics.com/guides/azureml-quickstart)。
2. 安装 Ultralytics 包：

```bash
pip install ultralytics
```
[(1)](https://docs.ultralytics.com/models/yolo11)[(2)](https://docs.ultralytics.com/guides/azureml-quickstart)

3. 在 Python 脚本中加载预训练模型并进行微调，例如：

```python
from ultralytics import YOLO
# 加载 COCO 预训练 YOLO11n 模型
model = YOLO("yolo11n.pt")
# 用本地数据集训练模型，设置训练轮数和图片尺寸
results = model.train(data="你的数据集.yaml", epochs=100, imgsz=640)
```
[(1)](https://docs.ultralytics.com/models/yolo11)[(2)](https://docs.ultralytics.com/guides/azureml-quickstart)

4. 训练完成后，可用模型进行预测和评估：

```python
results = model("你的测试图片.jpg")
results[0].show()
```
[(1)](https://docs.ultralytics.com/models/yolo11)[(2)](https://docs.ultralytics.com/guides/azureml-quickstart)

5. 你也可以使用命令行方式训练和推理：

```bash
yolo train model=yolo11n.pt data=你的数据集.yaml epochs=100 imgsz=640
yolo predict model=yolo11n.pt source=你的测试图片.jpg
```
[(1)](https://docs.ultralytics.com/models/yolo11)[(2)](https://docs.ultralytics.com/guides/azureml-quickstart)

详细文档与更多示例可参考：[YOLO11官方文档](https://docs.ultralytics.com/models/yolo11/)  
数据集格式参考：[数据集配置说明](https://docs.ultralytics.com/datasets/detect/)
[YOLO11 🚀 on AzureML](https://docs.ultralytics.com/guides/azureml-quickstart/)

---

# Fine-tuningYOLO

我来帮你实现用Python和YOLO进行零件表面瑕疵检测的微调方案。基于你的需求，我推荐使用YOLOv8，它对目标检测和分类任务都有很好的支持。

## 完整实现方案

### 1. 环境准备和依赖安装

```python
# requirements.txt
ultralytics>=8.0.0
opencv-python>=4.5.0
numpy>=1.21.0
matplotlib>=3.5.0
Pillow>=8.3.0
torch>=1.11.0
torchvision>=0.12.0
```

### 2. 数据准备和标注格式

```python
import os
import json
import cv2
import numpy as np
from pathlib import Path

class DefectDatasetPreparer:
    def __init__(self, data_root):
        self.data_root = Path(data_root)
        self.classes = {
            0: 'AC_Bright',           # 正常-亮面
            1: 'AC_Half_Bright',      # 正常-半亮面
            2: 'NC_Greyish',          # 缺陷-灰暗
            3: 'NC_Rusty',            # 缺陷-锈蚀
            4: 'NC_Peeled',           # 缺陷-剥落
            5: 'NC_Scaled'            # 缺陷-鳞片状
        }
        
    def create_yolo_structure(self):
        """创建YOLO训练所需的目录结构"""
        dirs = ['images/train', 'images/val', 'images/test',
                'labels/train', 'labels/val', 'labels/test']
        
        for dir_name in dirs:
            (self.data_root / dir_name).mkdir(parents=True, exist_ok=True)
            
    def convert_annotations_to_yolo(self, annotation_file, output_dir):
        """将标注转换为YOLO格式
        假设原始标注格式为COCO或自定义格式
        """
        with open(annotation_file, 'r') as f:
            annotations = json.load(f)
            
        for ann in annotations:
            image_path = ann['image_path']
            image = cv2.imread(image_path)
            h, w = image.shape[:2]
            
            # 转换边界框为YOLO格式 (class_id, x_center, y_center, width, height)
            yolo_labels = []
            for obj in ann['objects']:
                class_id = obj['class_id']
                bbox = obj['bbox']  # [x_min, y_min, x_max, y_max]
                
                # 转换为YOLO格式
                x_center = (bbox[0] + bbox[2]) / 2 / w
                y_center = (bbox[1] + bbox[3]) / 2 / h
                width = (bbox[2] - bbox[0]) / w
                height = (bbox[3] - bbox[1]) / h
                
                yolo_labels.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")
            
            # 保存YOLO格式标注
            label_file = output_dir / f"{Path(image_path).stem}.txt"
            with open(label_file, 'w') as f:
                f.write('\n'.join(yolo_labels))
```

### 3. 数据增强策略

```python
import albumentations as A
from albumentations.pytorch import ToTensorV2

class DefectAugmentation:
    def __init__(self):
        self.train_transform = A.Compose([
            # 几何变换 - 处理零件朝向和位置不固定的问题
            A.RandomRotate90(p=0.5),
            A.Rotate(limit=30, p=0.7),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.3),
            A.ShiftScaleRotate(shift_limit=0.1, scale_limit=0.2, rotate_limit=15, p=0.7),
            
            # 光照变换 - 处理反射和光线问题
            A.RandomBrightnessContrast(brightness_limit=0.3, contrast_limit=0.3, p=0.8),
            A.CLAHE(clip_limit=2.0, tile_grid_size=(8, 8), p=0.5),
            A.RandomGamma(gamma_limit=(80, 120), p=0.5),
            
            # 颜色变换 - 增强对不同表面状态的识别
            A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=20, p=0.6),
            A.RGBShift(r_shift_limit=15, g_shift_limit=15, b_shift_limit=15, p=0.5),
            
            # 噪声和模糊 - 模拟真实环境
            A.GaussNoise(var_limit=(10.0, 50.0), p=0.3),
            A.MotionBlur(blur_limit=3, p=0.3),
            A.GaussianBlur(blur_limit=3, p=0.2),
            
            # 遮挡模拟 - 处理零件堆叠遮挡问题
            A.CoarseDropout(max_holes=3, max_height=50, max_width=50, p=0.3),
            
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
        
        self.val_transform = A.Compose([
            A.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ], bbox_params=A.BboxParams(format='yolo', label_fields=['class_labels']))
```

### 4. YOLO模型微调实现

```python
from ultralytics import YOLO
import torch
import yaml
from pathlib import Path

class DefectYOLOTrainer:
    def __init__(self, data_config_path, model_save_dir):
        self.data_config_path = data_config_path
        self.model_save_dir = Path(model_save_dir)
        self.model_save_dir.mkdir(parents=True, exist_ok=True)
        
    def create_data_config(self, train_path, val_path, test_path, class_names):
        """创建YOLO数据配置文件"""
        config = {
            'path': str(Path(train_path).parent.parent),  # 数据集根目录
            'train': 'images/train',
            'val': 'images/val',
            'test': 'images/test',
            'nc': len(class_names),  # 类别数量
            'names': class_names     # 类别名称
        }
        
        with open(self.data_config_path, 'w') as f:
            yaml.dump(config, f, default_flow_style=False)
            
    def train_model(self, model_size='n', epochs=100, imgsz=640, batch_size=16):
        """训练YOLO模型"""
        # 加载预训练模型
        model = YOLO(f'yolov8{model_size}.pt')
        
        # 训练参数配置
        train_args = {
            'data': self.data_config_path,
            'epochs': epochs,
            'imgsz': imgsz,
            'batch': batch_size,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'workers': 8,
            'project': str(self.model_save_dir),
            'name': 'defect_detection',
            'save': True,
            'save_period': 10,  # 每10个epoch保存一次
            
            # 优化器设置
            'optimizer': 'AdamW',
            'lr0': 0.001,
            'weight_decay': 0.0005,
            
            # 数据增强
            'hsv_h': 0.015,
            'hsv_s': 0.7,
            'hsv_v': 0.4,
            'degrees': 15.0,
            'translate': 0.1,
            'scale': 0.5,
            'shear': 0.0,
            'perspective': 0.0,
            'flipud': 0.5,
            'fliplr': 0.5,
            'mosaic': 1.0,
            'mixup': 0.1,
            
            # 损失函数权重
            'box': 7.5,
            'cls': 0.5,
            'dfl': 1.5,
            
            # 早停和学习率调度
            'patience': 50,
            'cos_lr': True,
        }
        
        # 开始训练
        results = model.train(**train_args)
        
        # 保存最终模型
        best_model_path = self.model_save_dir / 'defect_detection' / 'weights' / 'best.pt'
        final_model_path = self.model_save_dir / 'defect_yolo_final.pt'
        
        if best_model_path.exists():
            import shutil
            shutil.copy2(best_model_path, final_model_path)
            print(f"最佳模型已保存到: {final_model_path}")
            
        return results, final_model_path
    
    def evaluate_model(self, model_path, test_data_path):
        """评估模型性能"""
        model = YOLO(model_path)
        
        # 在测试集上评估
        results = model.val(
            data=self.data_config_path,
            split='test',
            imgsz=640,
            batch=16,
            save_json=True,
            save_hybrid=True
        )
        
        return results
```

### 5. 模型推理和应用

```python
import cv2
import numpy as np
from ultralytics import YOLO

class DefectDetector:
    def __init__(self, model_path, conf_threshold=0.5, iou_threshold=0.45):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # 类别映射
        self.class_names = {
            0: 'AC_Bright',
            1: 'AC_Half_Bright', 
            2: 'NC_Greyish',
            3: 'NC_Rusty',
            4: 'NC_Peeled',
            5: 'NC_Scaled'
        }
        
        # 缺陷类别
        self.defect_classes = {2, 3, 4, 5}
        
    def detect_defects(self, image_path, save_result=True):
        """检测零件表面缺陷"""
        # 推理
        results = self.model(
            image_path,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            save=save_result
        )
        
        # 解析结果
        detections = []
        has_defects = False
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    
                    detection = {
                        'class_id': class_id,
                        'class_name': self.class_names[class_id],
                        'confidence': confidence,
                        'bbox': bbox,
                        'is_defect': class_id in self.defect_classes
                    }
                    
                    detections.append(detection)
                    
                    if class_id in self.defect_classes:
                        has_defects = True
        
        return {
            'image_path': image_path,
            'has_defects': has_defects,
            'detections': detections,
            'total_parts': len(detections),
            'defective_parts': sum(1 for d in detections if d['is_defect'])
        }
    
    def batch_detect(self, image_folder, output_file=None):
        """批量检测"""
        results = []
        image_folder = Path(image_folder)
        
        for image_path in image_folder.glob('*.jpg'):
            result = self.detect_defects(str(image_path))
            results.append(result)
            
        if output_file:
            import json
            with open(output_file, 'w') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
                
        return results
    
    def visualize_results(self, image_path, detections, save_path=None):
        """可视化检测结果"""
        image = cv2.imread(image_path)
        
        for detection in detections:
            bbox = detection['bbox']
            class_name = detection['class_name']
            confidence = detection['confidence']
            is_defect = detection['is_defect']
            
            # 设置颜色：缺陷用红色，正常用绿色
            color = (0, 0, 255) if is_defect else (0, 255, 0)
            
            # 绘制边界框
            cv2.rectangle(image, 
                         (int(bbox[0]), int(bbox[1])), 
                         (int(bbox[2]), int(bbox[3])), 
                         color, 2)
            
            # 添加标签
            label = f"{class_name}: {confidence:.2f}"
            cv2.putText(image, label, 
                       (int(bbox[0]), int(bbox[1]) - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        if save_path:
            cv2.imwrite(save_path, image)
            
        return image
```

### 6. 完整训练流程

```python
def main_training_pipeline():
    """完整的训练流程"""
    
    # 1. 数据准备
    data_root = "path/to/your/dataset"
    preparer = DefectDatasetPreparer(data_root)
    preparer.create_yolo_structure()
    
    # 2. 创建数据配置
    class_names = ['AC_Bright', 'AC_Half_Bright', 'NC_Greyish', 
                   'NC_Rusty', 'NC_Peeled', 'NC_Scaled']
    
    trainer = DefectYOLOTrainer(
        data_config_path="defect_data.yaml",
        model_save_dir="models"
    )
    
    trainer.create_data_config(
        train_path=f"{data_root}/images/train",
        val_path=f"{data_root}/images/val", 
        test_path=f"{data_root}/images/test",
        class_names=class_names
    )
    
    # 3. 训练模型
    print("开始训练模型...")
    results, model_path = trainer.train_model(
        model_size='s',  # 可选: n, s, m, l, x
        epochs=200,
        imgsz=640,
        batch_size=16
    )
    
    # 4. 评估模型
    print("评估模型性能...")
    eval_results = trainer.evaluate_model(model_path, f"{data_root}/images/test")
    
    # 5. 测试推理
    print("测试模型推理...")
    detector = DefectDetector(model_path)
    
    # 单张图片测试
    test_image = "path/to/test/image.jpg"
    detection_result = detector.detect_defects(test_image)
    
    print(f"检测结果: {detection_result}")
    
    return model_path, detector

if __name__ == "__main__":
    model_path, detector = main_training_pipeline()
    print(f"训练完成！模型保存在: {model_path}")
```

### 7. 模型保存和加载

```python
class ModelManager:
    @staticmethod
    def save_model_with_metadata(model_path, metadata):
        """保存模型和元数据"""
        import pickle
        
        model_dir = Path(model_path).parent
        metadata_path = model_dir / "model_metadata.pkl"
        
        with open(metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
            
        print(f"模型元数据已保存到: {metadata_path}")
    
    @staticmethod
    def load_model_with_metadata(model_path):
        """加载模型和元数据"""
        import pickle
        
        model_dir = Path(model_path).parent
        metadata_path = model_dir / "model_metadata.pkl"
        
        detector = DefectDetector(model_path)
        
        metadata = None
        if metadata_path.exists():
            with open(metadata_path, 'rb') as f:
                metadata = pickle.load(f)
                
        return detector, metadata

# 使用示例
metadata = {
    'training_date': '2024-01-01',
    'dataset_size': 10000,
    'classes': ['AC_Bright', 'AC_Half_Bright', 'NC_Greyish', 'NC_Rusty', 'NC_Peeled', 'NC_Scaled'],
    'performance_metrics': {
        'mAP50': 0.85,
        'mAP50-95': 0.72
    }
}

ModelManager.save_model_with_metadata("models/defect_yolo_final.pt", metadata)
```

## 关键要点

1. **数据标注**: 确保准确标注所有类别，特别注意AC和NC的区分
2. **数据增强**: 重点处理光照变化和零件朝向问题
3. **类别平衡**: 由于AC样本较多，考虑使用类别权重或重采样
4. **模型选择**: 建议从YOLOv8s开始，根据精度要求调整模型大小
5. **超参数调优**: 根据验证集表现调整学习率、batch size等参数

这个方案可以有效处理你描述的零件表面瑕疵检测任务，包括处理堆叠遮挡、光照变化等挑战。


---

## 概览

要从头开始实现缺陷检测的**Fine‑tuning**，主要流程包括：

1. **选择预训练框架**（如 Detectron2、MMDetection、YOLOv5/YOLOv8），
2. **准备数据集**（标注、转为 COCO/YOLO 格式），
3. **搭建环境**（安装依赖、克隆仓库），
4. **修改配置文件**（指定类别、冻结层数等），
5. **启动训练**（设置训练参数），
6. **超参数调优**（学习率、Momentum 等）与
7. **模型评估和部署**。

下面将逐步展开每个环节的具体操作和注意事项。

---

## 1. 选择合适的预训练框架

### Detectron2

* Facebook 出品，基于 PyTorch，简洁易用。可直接从 Model Zoo 拉取 Faster R‑CNN、Mask R‑CNN 等检测模型，并对自定义数据微调（fine‑tune）【([Medium][1])】【([Roboflow Blog][2])】。

### MMDetection

* OpenMMLab 生态下的 Detection 工具箱，同样提供丰富的预训练模型和配置继承机制。通过继承 `_base_/models/...` 和 `_base_/datasets/...` 等配置，即可快速适配新数据集【([MMDetection][3])】【([MMDetection][4])】。

### YOLO 系列

* **YOLOv5**：Ultralytics 提供详细教程，数据准备、配置和训练只需数行代码，可快速上手【([Ultralytics Docs][5])】。
* **YOLOv8**：最新研究表明，通过分层解冻（unfreeze）微调可以在新任务上大幅提升 mAP，同时保持 COCO 基准性能不变【([arXiv][6])】。

---

## 2. 数据集准备

1. **收集与标注**：使用 LabelMe、Makesense.ai 或 Roboflow 进行物体边界框（bounding box）标注。
2. **格式转换**：

   * COCO 格式：常见于 Detectron2/MMDetection，需生成 `annotations.json`，键包括 `images`, `annotations`, `categories`【([MMDetection][3])】。
   * YOLO 格式：每张图片对应一个 `.txt` 文件，行格式 `<class_id> <x_center> <y_center> <width> <height>`（归一化坐标）【([DigitalOcean][7])】。
3. **数据划分**：一般按 8:1:1 划分训练/验证/测试集，确保类别分布均匀。

---

## 3. 环境搭建与依赖安装

以 Detectron2 为例：

```bash
# 安装 Detectron2（需匹配 PyTorch 版本）
pip install detectron2 -f \
  https://dl.fbaipublicfiles.com/detectron2/wheels/cu113/torch1.10/index.html
```

以 MMDetection 为例：

```bash
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection
pip install -r requirements/build.txt
pip install -v -e .
```

以 YOLOv5 为例：

```bash
git clone https://github.com/ultralytics/yolov5
cd yolov5
pip install -r requirements.txt
```

以上步骤均在 Python≥3.8、PyTorch≥1.8 环境下进行【([Ultralytics Docs][5], [GitHub][8])】。

---

## 4. 修改配置文件

### Detectron2

* 在示例配置 `configs/COCO-Detection/faster_rcnn_R_50_FPN_1x.yaml` 上：

  1. 修改 `DATASETS.TRAIN`、`DATASETS.TEST` 指向自定义数据集名称；
  2. 调整 `SOLVER.BASE_LR`, `SOLVER.MAX_ITER` 等；
  3. 可通过 `cfg.MODEL.BACKBONE.FREEZE_AT` 决定冻结层级。

### MMDetection

* 编写新配置继承：

  ```yaml
  _base_ = [
    '../_base_/models/faster_rcnn_r50_fpn.py',
    '../_base_/datasets/coco_detection.py',
    '../_base_/schedules/schedule_1x.py',
    '../_base_/default_runtime.py'
  ]
  model = dict(
    roi_head=dict(
      bbox_head=dict(num_classes=你的类别数)
    )
  )
  data = dict(
    train=dict(ann_file='path/to/train.json', img_prefix='train/'),
    val=dict(ann_file='path/to/val.json', img_prefix='val/')
  )
  ```
* 继承避免重复配置，并保证与 Model Zoo 兼容【([MMDetection][3])】。

### YOLOv5/YOLOv8

* 编辑 `data.yaml`：

  ```yaml
  train: path/to/images/train
  val:   path/to/images/val
  nc:    类别数
  names: ['defect1','defect2',...]
  ```
* 选择预训练权重（如 `yolov5s.pt`），并在训练命令中指定冻结层数：

  ```bash
  python train.py --img 640 --batch 16 --epochs 50 \
    --data data.yaml --cfg yolov5s.yaml --weights yolov5s.pt \
    --freeze 10
  ```

  其中 `--freeze` 控制冻结前 N 层，参考最新研究可根据任务需求调整深度【([arXiv][6])】。

---

## 5. 启动训练

* **Detectron2**：

  ```bash
  python tools/train_net.py \
    --config-file configs/YourConfig.yaml \
    --num-gpus 1
  ```
* **MMDetection**：

  ```bash
  ./tools/dist_train.sh \
    configs/your/finetune_config.py 1
  ```
* **YOLOv5**：

  ```bash
  python train.py \
    --data data.yaml --weights yolov5s.pt \
    --epochs 50 --batch-size 16
  ```

训练过程中可实时输出 mAP、loss 曲线，并在验证集上监控性能。

---

## 6. 超参数与调优

* **学习率 (LR)**：一般初始设为 `1e-3`\~`1e-4`，可使用 Warmup 与 LR Scheduler（Step、Cosine）进行动态调整【([arXiv][9])】。
* **Momentum & Weight Decay**：Momentum 建议 0.9 左右，Weight Decay 可尝试 `1e-4`\~`1e-5`，视任务和数据量微调【([arXiv][9])】。
* **冻结策略**：如 YOLOv8 研究所示，逐步解冻（freeze points）可提升细粒度检测性能，同时避免遗忘原模型能力【([arXiv][6])】。

---

## 7. 模型评估与部署

1. **评估**：使用 COCO API 计算 AP、mAP、Recall 等指标；
2. **导出权重**：Detectron2 可导出 `.pth`，MMDetection 同理；YOLOv5 支持导出 ONNX/ TorchScript；
3. **部署**：

   * 云端服务（Flask/GPU）；
   * 边缘端（TensorRT、OpenVINO）；
   * 集成到 ROS/工业流水线。

---

通过上述步骤，你即可从零开始完成基于预训练模型的缺陷检测 Fine‑tuning。根据项目需求，灵活选择框架和超参数，并在训练中不断迭代优化。祝你早日实现高精度、实时的缺陷检测系统！

[1]: https://medium.com/the-owl/guide-to-fine-tuning-a-pre-trained-model-for-object-detection-tasks-with-faster-rcnn-using-e2e7e190105b?utm_source=chatgpt.com "Guide to fine-tuning a Pre-trained model for Object Detection tasks ..."
[2]: https://blog.roboflow.com/how-to-train-detectron2/?utm_source=chatgpt.com "How to Train Detectron2 on Custom Object Detection Data"
[3]: https://mmdetection.readthedocs.io/en/v2.9.0/tutorials/finetune.html?utm_source=chatgpt.com "Tutorial 7: Finetuning Models - MMDetection's documentation!"
[4]: https://mmdetection.readthedocs.io/en/latest/user_guides/train.html?utm_source=chatgpt.com "Train predefined models on standard datasets"
[5]: https://docs.ultralytics.com/yolov5/tutorials/train_custom_data/?utm_source=chatgpt.com "Train YOLOv5 on Custom Data - Ultralytics YOLO Docs"
[6]: https://arxiv.org/abs/2505.01016?utm_source=chatgpt.com "Fine-Tuning Without Forgetting: Adaptation of YOLOv8 Preserves COCO Performance"
[7]: https://www.digitalocean.com/community/tutorials/train-yolov5-custom-data?utm_source=chatgpt.com "How to Train YOLO v5 on a Custom Dataset | DigitalOcean"
[8]: https://github.com/open-mmlab/mmdetection?utm_source=chatgpt.com "open-mmlab/mmdetection: OpenMMLab Detection Toolbox ... - GitHub"
[9]: https://arxiv.org/abs/2002.11770?utm_source=chatgpt.com "Rethinking the Hyperparameters for Fine-tuning"


---

使用YOLO11（YOLOv11）是个很好的选择！YOLO11是最新版本，性能更优秀。让我为你提供完整的环境配置和代码实现。

## 环境配置

### 1. Python版本要求
```bash
# 推荐使用 Python 3.8-3.11
python --version  # 确保是 3.8+ 版本
```

### 2. 安装依赖
```bash
# 创建虚拟环境（推荐）
conda create -n yolo11_defect python=3.10
conda activate yolo11_defect

# 或使用 venv
python -m venv yolo11_env
source yolo11_env/bin/activate  # Linux/Mac
# yolo11_env\Scripts\activate  # Windows

# 安装核心依赖
pip install ultralytics>=8.3.0  # YOLO11 需要最新版本
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118  # CUDA版本
# 如果没有GPU，使用CPU版本：
# pip install torch torchvision torchaudio

# 其他依赖
pip install opencv-python>=4.8.0
pip install numpy>=1.24.0
pip install matplotlib>=3.7.0
pip install Pillow>=10.0.0
pip install albumentations>=1.3.0
pip install pandas>=2.0.0
pip install seaborn>=0.12.0
pip install tqdm>=4.65.0
```

### 3. 验证安装
```python
import ultralytics
print(f"Ultralytics version: {ultralytics.__version__}")

from ultralytics import YOLO
# 这会自动下载YOLO11模型
model = YOLO('yolo11n.pt')
print("YOLO11 安装成功！")
```

## YOLO11 专用代码实现

### 1. YOLO11 训练器（更新版本）

```python
from ultralytics import YOLO
import torch
import yaml
from pathlib import Path
import json

class YOLO11DefectTrainer:
    def __init__(self, data_config_path, model_save_dir):
        self.data_config_path = data_config_path
        self.model_save_dir = Path(model_save_dir)
        self.model_save_dir.mkdir(parents=True, exist_ok=True)
        
        # YOLO11 可用的模型尺寸
        self.available_models = {
            'n': 'yolo11n.pt',      # Nano - 最快
            's': 'yolo11s.pt',      # Small - 平衡
            'm': 'yolo11m.pt',      # Medium - 更好精度
            'l': 'yolo11l.pt',      # Large - 高精度
            'x': 'yolo11x.pt'       # Extra Large - 最高精度
        }
        
    def create_data_config(self, train_path, val_path, test_path, class_names):
        """创建YOLO11数据配置文件"""
        config = {
            'path': str(Path(train_path).parent.parent),
            'train': 'images/train',
            'val': 'images/val', 
            'test': 'images/test',
            'nc': len(class_names),
            'names': class_names
        }
        
        with open(self.data_config_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)
            
    def train_model(self, model_size='s', epochs=200, imgsz=640, batch_size=16):
        """使用YOLO11训练模型"""
        
        # 加载YOLO11预训练模型
        model_name = self.available_models.get(model_size, 'yolo11s.pt')
        print(f"加载YOLO11模型: {model_name}")
        model = YOLO(model_name)
        
        # YOLO11 优化的训练参数
        train_args = {
            'data': self.data_config_path,
            'epochs': epochs,
            'imgsz': imgsz,
            'batch': batch_size,
            'device': 'cuda' if torch.cuda.is_available() else 'cpu',
            'workers': 8,
            'project': str(self.model_save_dir),
            'name': 'yolo11_defect_detection',
            'save': True,
            'save_period': 10,
            'cache': True,  # 缓存数据集以加速训练
            
            # YOLO11 优化器设置
            'optimizer': 'auto',  # YOLO11 自动选择最佳优化器
            'lr0': 0.01,          # 初始学习率
            'lrf': 0.01,          # 最终学习率 (lr0 * lrf)
            'momentum': 0.937,
            'weight_decay': 0.0005,
            'warmup_epochs': 3.0,
            'warmup_momentum': 0.8,
            'warmup_bias_lr': 0.1,
            
            # YOLO11 数据增强（更先进）
            'hsv_h': 0.015,
            'hsv_s': 0.7,
            'hsv_v': 0.4,
            'degrees': 0.0,       # 旋转角度
            'translate': 0.1,     # 平移
            'scale': 0.5,         # 缩放
            'shear': 0.0,         # 剪切
            'perspective': 0.0,   # 透视变换
            'flipud': 0.0,        # 上下翻转
            'fliplr': 0.5,        # 左右翻转
            'bgr': 0.0,           # BGR通道翻转
            'mosaic': 1.0,        # Mosaic增强
            'mixup': 0.0,         # Mixup增强
            'copy_paste': 0.0,    # Copy-paste增强
            
            # YOLO11 损失函数权重
            'box': 7.5,           # 边界框损失权重
            'cls': 0.5,           # 分类损失权重
            'dfl': 1.5,           # DFL损失权重
            
            # 训练策略
            'patience': 100,      # 早停耐心值
            'close_mosaic': 10,   # 最后N个epoch关闭mosaic
            'amp': True,          # 自动混合精度
            'fraction': 1.0,      # 使用数据集的比例
            'profile': False,     # 性能分析
            'freeze': None,       # 冻结层数
            
            # 验证设置
            'val': True,
            'split': 'val',
            'save_json': True,
            'save_hybrid': True,
            'conf': 0.001,        # 验证时的置信度阈值
            'iou': 0.6,           # 验证时的IoU阈值
            'max_det': 300,       # 最大检测数量
            'half': False,        # 半精度验证
            'dnn': False,         # 使用OpenCV DNN
            'plots': True,        # 保存训练图表
        }
        
        print("开始YOLO11训练...")
        print(f"使用设备: {train_args['device']}")
        print(f"批次大小: {batch_size}")
        print(f"图像尺寸: {imgsz}")
        
        # 开始训练
        results = model.train(**train_args)
        
        # 保存最终模型
        best_model_path = self.model_save_dir / 'yolo11_defect_detection' / 'weights' / 'best.pt'
        final_model_path = self.model_save_dir / 'yolo11_defect_final.pt'
        
        if best_model_path.exists():
            import shutil
            shutil.copy2(best_model_path, final_model_path)
            print(f"✅ 最佳YOLO11模型已保存到: {final_model_path}")
            
        return results, final_model_path
    
    def validate_model(self, model_path):
        """验证YOLO11模型"""
        model = YOLO(model_path)
        
        # YOLO11 验证参数
        val_results = model.val(
            data=self.data_config_path,
            imgsz=640,
            batch=16,
            conf=0.001,
            iou=0.6,
            max_det=300,
            half=False,
            device='cuda' if torch.cuda.is_available() else 'cpu',
            dnn=False,
            plots=True,
            save_json=True,
            save_hybrid=True,
            verbose=True
        )
        
        return val_results
```

### 2. YOLO11 检测器

```python
import cv2
import numpy as np
from ultralytics import YOLO
from pathlib import Path
import json

class YOLO11DefectDetector:
    def __init__(self, model_path, conf_threshold=0.5, iou_threshold=0.45):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold
        
        # 类别映射
        self.class_names = {
            0: 'AC_Bright',
            1: 'AC_Half_Bright', 
            2: 'NC_Greyish',
            3: 'NC_Rusty',
            4: 'NC_Peeled',
            5: 'NC_Scaled'
        }
        
        # 缺陷类别
        self.defect_classes = {2, 3, 4, 5}
        
    def detect_defects(self, image_path, save_result=True, save_dir="runs/detect"):
        """使用YOLO11检测零件表面缺陷"""
        
        # YOLO11 推理参数
        results = self.model(
            image_path,
            conf=self.conf_threshold,
            iou=self.iou_threshold,
            max_det=300,
            device='cuda' if torch.cuda.is_available() else 'cpu',
            half=False,
            augment=False,  # TTA (Test Time Augmentation)
            agnostic_nms=False,
            retina_masks=False,
            save=save_result,
            save_dir=save_dir,
            save_txt=True,
            save_conf=True,
            show_labels=True,
            show_conf=True,
            show_boxes=True,
            line_width=2
        )
        
        # 解析YOLO11结果
        detections = []
        has_defects = False
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    class_id = int(box.cls[0])
                    confidence = float(box.conf[0])
                    bbox = box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    
                    detection = {
                        'class_id': class_id,
                        'class_name': self.class_names.get(class_id, f'Unknown_{class_id}'),
                        'confidence': confidence,
                        'bbox': bbox,
                        'is_defect': class_id in self.defect_classes,
                        'area': (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                    }
                    
                    detections.append(detection)
                    
                    if class_id in self.defect_classes:
                        has_defects = True
        
        # 计算统计信息
        defective_parts = [d for d in detections if d['is_defect']]
        normal_parts = [d for d in detections if not d['is_defect']]
        
        return {
            'image_path': image_path,
            'has_defects': has_defects,
            'detections': detections,
            'total_parts': len(detections),
            'defective_parts': len(defective_parts),
            'normal_parts': len(normal_parts),
            'defect_ratio': len(defective_parts) / len(detections) if detections else 0,
            'confidence_stats': {
                'avg_confidence': np.mean([d['confidence'] for d in detections]) if detections else 0,
                'min_confidence': min([d['confidence'] for d in detections]) if detections else 0,
                'max_confidence': max([d['confidence'] for d in detections]) if detections else 0
            }
        }
    
    def batch_detect(self, image_folder, output_file=None, progress_callback=None):
        """批量检测"""
        results = []
        image_folder = Path(image_folder)
        
        # 支持的图像格式
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.webp']
        image_files = []
        for ext in image_extensions:
            image_files.extend(image_folder.glob(ext))
            image_files.extend(image_folder.glob(ext.upper()))
        
        print(f"找到 {len(image_files)} 张图片")
        
        for i, image_path in enumerate(image_files):
            try:
                result = self.detect_defects(str(image_path), save_result=False)
                results.append(result)
                
                if progress_callback:
                    progress_callback(i + 1, len(image_files))
                else:
                    print(f"处理进度: {i+1}/{len(image_files)} - {image_path.name}")
                    
            except Exception as e:
                print(f"处理图片 {image_path} 时出错: {e}")
                
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
                
        return results
    
    def export_model(self, export_format='onnx', optimize=True):
        """导出YOLO11模型为其他格式"""
        export_formats = ['onnx', 'torchscript', 'tensorflow', 'tflite', 'edgetpu', 'coreml']
        
        if export_format not in export_formats:
            raise ValueError(f"不支持的导出格式: {export_format}")
            
        print(f"导出YOLO11模型为 {export_format} 格式...")
        
        export_path = self.model.export(
            format=export_format,
            imgsz=640,
            keras=False,
            optimize=optimize,
            half=False,
            int8=False,
            dynamic=False,
            simplify=True,
            opset=None,
            workspace=4,
            nms=False
        )
        
        print(f"✅ 模型已导出到: {export_path}")
        return export_path
```

### 3. 完整的YOLO11训练流程

```python
def main_yolo11_pipeline():
    """完整的YOLO11训练和部署流程"""
    
    # 1. 数据准备
    data_root = "path/to/your/dataset"
    
    # 2. 创建训练器
    trainer = YOLO11DefectTrainer(
        data_config_path="yolo11_defect_data.yaml",
        model_save_dir="yolo11_models"
    )
    
    # 3. 配置数据
    class_names = ['AC_Bright', 'AC_Half_Bright', 'NC_Greyish', 
                   'NC_Rusty', 'NC_Peeled', 'NC_Scaled']
    
    trainer.create_data_config(
        train_path=f"{data_root}/images/train",
        val_path=f"{data_root}/images/val", 
        test_path=f"{data_root}/images/test",
        class_names=class_names
    )
    
    # 4. 训练YOLO11模型
    print("🚀 开始YOLO11训练...")
    results, model_path = trainer.train_model(
        model_size='s',  # 推荐从's'开始
        epochs=200,
        imgsz=640,
        batch_size=16
    )
    
    # 5. 验证模型
    print("📊 验证YOLO11模型...")
    val_results = trainer.validate_model(model_path)
    
    # 6. 创建检测器
    print("🔍 创建YOLO11检测器...")
    detector = YOLO11DefectDetector(model_path)
    
    # 7. 测试检测
    test_image = "path/to/test/image.jpg"
    if Path(test_image).exists():
        detection_result = detector.detect_defects(test_image)
        print(f"检测结果: {detection_result}")
    
    # 8. 导出模型（可选）
    print("📦 导出YOLO11模型...")
    onnx_path = detector.export_model('onnx')
    
    return model_path, detector

if __name__ == "__main__":
    model_path, detector = main_yolo11_pipeline()
    print(f"✅ YOLO11训练完成！模型保存在: {model_path}")
```

### 4. 性能监控和可视化

```python
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class YOLO11Monitor:
    def __init__(self, results_dir):
        self.results_dir = Path(results_dir)
        
    def plot_training_curves(self):
        """绘制YOLO11训练曲线"""
        results_csv = self.results_dir / "results.csv"
        
        if not results_csv.exists():
            print("未找到训练结果文件")
            return
            
        import pandas as pd
        df = pd.read_csv(results_csv)
        
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('YOLO11 Training Results', fontsize=16)
        
        # 损失曲线
        axes[0, 0].plot(df['epoch'], df['train/box_loss'], label='Box Loss')
        axes[0, 0].plot(df['epoch'], df['train/cls_loss'], label='Class Loss')
        axes[0, 0].plot(df['epoch'], df['train/dfl_loss'], label='DFL Loss')
        axes[0, 0].set_title('Training Losses')
        axes[0, 0].set_xlabel('Epoch')
        axes[0, 0].set_ylabel('Loss')
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # mAP曲线
        axes[0, 1].plot(df['epoch'], df['metrics/mAP50(B)'], label='mAP@0.5')
        axes[0, 1].plot(df['epoch'], df['metrics/mAP50-95(B)'], label='mAP@0.5:0.95')
        axes[0, 1].set_title('Validation mAP')
        axes[0, 1].set_xlabel('Epoch')
        axes[0, 1].set_ylabel('mAP')
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # 精确率和召回率
        axes[1, 0].plot(df['epoch'], df['metrics/precision(B)'], label='Precision')
        axes[1, 0].plot(df['epoch'], df['metrics/recall(B)'], label='Recall')
        axes[1, 0].set_title('Precision & Recall')
        axes[1, 0].set_xlabel('Epoch')
        axes[1, 0].set_ylabel('Score')
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # 学习率
        axes[1, 1].plot(df['epoch'], df['lr/pg0'], label='Learning Rate')
        axes[1, 1].set_title('Learning Rate')
        axes[1, 1].set_xlabel('Epoch')
        axes[1, 1].set_ylabel('LR')
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.savefig(self.results_dir / 'training_curves.png', dpi=300, bbox_inches='tight')
        plt.show()
```

## YOLO11 vs YOLO8 主要优势

1. **更好的精度**: YOLO11在相同模型尺寸下精度更高
2. **更快的推理速度**: 优化的网络结构
3. **更强的泛化能力**: 改进的训练策略
4. **更好的小目标检测**: 对你的零件堆叠场景更有利
5. **自动优化器选择**: 训练更稳定

## 推荐配置

- **开发环境**: Python 3.10 + CUDA 11.8
- **模型选择**: 从YOLO11s开始，根据精度要求调整
- **训练策略**: 使用更长的训练周期（200+ epochs）
- **数据增强**: YOLO11内置的增强策略已经很强大

这样你就可以使用最新的YOLO11来训练你的零件缺陷检测模型了！
