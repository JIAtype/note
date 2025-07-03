import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
import torchvision.transforms as transforms
from torchvision.transforms.functional import resize
import cv2
import os
import matplotlib.pyplot as plt
from PIL import Image
import random
from datetime import datetime
import logging
# numpy: 用于数值计算，例如数组操作。
# torch: PyTorch 深度学习框架的核心库。
# torch.nn: 包含构建神经网络所需的各种模块，如卷积层、池化层等。
# torch.optim: 包含各种优化算法，如 Adam、SGD 等。
# torch.utils.data: 提供用于加载和处理数据的工具，如 DataLoader 和 Dataset。
# torchvision.transforms: 提供图像转换的工具，如缩放、裁剪、归一化等。
# torchvision.transforms.functional: 提供一些函数式的图像变换。
# cv2: OpenCV 库，用于图像处理，如高斯金字塔。
# os: 用于与操作系统交互，如文件和目录操作。
# matplotlib.pyplot: 用于绘制图表和可视化图像。
# PIL (Pillow): 用于图像处理，如读取图像。
# random: 用于生成随机数。
# datetime: 用于处理日期和时间。
# logging: 用于记录日志信息。

# 配置日志记录器
# 用于将日志信息记录到文件 mscdae_model.log 和控制台。日志级别设置为 INFO，表示记录所有信息级别的日志。
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mscdae_model.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 为图像添加椒盐噪声的变换。椒盐噪声是一种常见的图像噪声，它随机地将一些像素设置为白色（盐）或黑色（椒）。
class SaltPepperNoise(object):
    """为图像添加椒盐噪声"""
    def __init__(self, prob=0.05):
        self.prob = prob
        
    def __call__(self, img_tensor):
        # 转换为numpy数组
        img_np = img_tensor.numpy()
        # 添加椒盐噪声
        noise_mask = np.random.random(img_np.shape) < self.prob
        salt_mask = np.random.random(img_np.shape) < 0.5
        # 添加白色像素(salt)
        img_np[noise_mask & salt_mask] = 1.0
        # 添加黑色像素(pepper)
        img_np[noise_mask & ~salt_mask] = 0.0
        # 转回tensor
        return torch.from_numpy(img_np)

# 韦伯定律指出，人眼对亮度的感知与亮度的相对变化有关，而不是绝对变化。这种归一化方法可以减少光照变化对图像的影响。
class NormalizeWeber(object):
    """使用韦伯法则进行光照归一化"""
    def __init__(self, epsilon=1e-6):
        self.epsilon = epsilon
        
    def __call__(self, img_tensor):
        # 计算每个通道的亮度均值
        mean_intensity = torch.mean(img_tensor) + self.epsilon
        # 应用韦伯法则: I_normalized = (I - mean) / mean
        normalized = (img_tensor - mean_intensity) / mean_intensity
        # 将值缩放到[0,1]范围
        min_val = torch.min(normalized)
        max_val = torch.max(normalized)
        normalized = (normalized - min_val) / (max_val - min_val + self.epsilon)
        return normalized

# 高斯金字塔是一系列图像，每一层都是前一层图像的模糊和下采样版本。高斯金字塔可以用于多尺度分析，提取不同尺度的图像特征。
class GaussianPyramid(object):
    """生成图像的高斯金字塔"""
    def __init__(self, levels=3):
        self.levels = levels
        
    def __call__(self, img_tensor):
        # 转换为numpy数组
        img_np = img_tensor.numpy()[0]  # 取第一个通道，假设为灰度图
        pyramid = [img_np]
        
        for i in range(1, self.levels):
            img_np = cv2.pyrDown(img_np)
            pyramid.append(img_np)
            
        # 转回tensor
        pyramid_tensors = [torch.from_numpy(img).unsqueeze(0) for img in pyramid]
        return pyramid_tensors

# 从图像中提取固定大小图像块的变换。图像块提取是许多图像处理任务中的常见步骤，例如目标检测和图像分类。
class PatchExtractor(object):
    """从图像中提取固定大小的图像块"""
    def __init__(self, patch_size=64, stride=32):
        self.patch_size = patch_size
        self.stride = stride
        
    def __call__(self, img_tensor):
        patches = []
        c, h, w = img_tensor.shape
        
        for i in range(0, h - self.patch_size + 1, self.stride):
            for j in range(0, w - self.patch_size + 1, self.stride):
                patch = img_tensor[:, i:i+self.patch_size, j:j+self.patch_size]
                patches.append(patch)
                
        return patches

# 定义了一个用于缺陷检测的数据集。继承自 torch.utils.data.Dataset 类，并实现了 __len__ 和 __getitem__ 方法。__len__ 方法返回数据集的大小，__getitem__ 方法返回给定索引的图像。
class DefectDataset(Dataset):
    """缺陷检测数据集"""
    def __init__(self, image_dir, transform=None, patch_size=64, stride=32):
        self.image_dir = image_dir
        self.transform = transform
        self.patch_extractor = PatchExtractor(patch_size, stride)
        self.image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
    def __len__(self):
        return len(self.image_files)
    
    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.image_files[idx])
        # 读取图像并转换为灰度
        img = Image.open(img_path).convert('L')
        # 转换为tensor
        img_tensor = transforms.ToTensor()(img)
        
        if self.transform:
            img_tensor = self.transform(img_tensor)
            
        return img_tensor

# 卷积去噪自编码器 (CDAE) 模型。CDAE 是一种无监督学习模型，它通过学习重建输入数据来提取数据的特征。CDAE 由一个编码器和一个解码器组成。编码器将输入数据压缩成一个低维的表示，解码器将低维表示重建为原始数据。
class ConvolutionalDenoisingAutoencoder(nn.Module):
    """卷积去噪自编码器模型"""
    def __init__(self, input_channels=1):
        super(ConvolutionalDenoisingAutoencoder, self).__init__()
        
        # 编码器
        self.encoder = nn.Sequential(
            nn.Conv2d(input_channels, 32, kernel_size=3, stride=1, padding=1),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1),
            nn.ReLU(True),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.ReLU(True)
        )
        
        # 解码器
        self.decoder = nn.Sequential(
            nn.ConvTranspose2d(128, 64, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(True),
            nn.ConvTranspose2d(64, 32, kernel_size=3, stride=2, padding=1, output_padding=1),
            nn.ReLU(True),
            nn.Conv2d(32, input_channels, kernel_size=3, stride=1, padding=1),
            nn.Sigmoid()  # 输出范围在[0,1]
        )
        
    def forward(self, x):
        x = self.encoder(x)
        x = self.decoder(x)
        return x

# 多尺度卷积去噪自编码器 (MSCDAE) 模型。MSCDAE 是一种用于表面缺陷检测的无监督学习模型。它使用多个 CDAE 模型来提取不同尺度的图像特征，并通过融合这些特征来提高检测的准确性。
# __init__: 构造函数，初始化 MSCDAE 模型的参数，包括金字塔层数、图像块大小、步长、批大小、训练周期数、学习率、噪声概率、阈值参数和设备。
# train: 训练模型。该方法首先对图像进行预处理，包括缩放、光照归一化和添加椒盐噪声。然后，它为每个金字塔层级训练一个 CDAE 模型。在训练过程中，该方法计算每个图像块的重建误差，并使用这些误差来更新 CDAE 模型的参数。
# save_model: 保存模型和统计信息。
# load_model: 加载已保存的模型和统计信息。
# detect: 检测图像中的缺陷。该方法首先对图像进行预处理，包括缩放和光照归一化。然后，它使用训练好的 MSCDAE 模型来提取图像的特征，并计算每个像素的重建误差。最后，该方法使用一个阈值来分割缺陷区域。
# test_batch_images: 批量测试图像并统计结果。
class MSCDAE:
    """多尺度卷积去噪自编码器"""
    def __init__(self, levels=3, patch_size=64, stride=32, batch_size=32, epochs=50, learning_rate=0.001,
                 noise_prob=0.05, gamma=3.0, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.levels = levels
        self.patch_size = patch_size
        self.stride = stride
        self.batch_size = batch_size
        self.epochs = epochs
        self.learning_rate = learning_rate
        self.noise_prob = noise_prob
        self.gamma = gamma  # 阈值参数
        self.device = device
        
        # 为每个金字塔层级创建一个CDAE模型
        self.models = [ConvolutionalDenoisingAutoencoder().to(self.device) for _ in range(levels)]
        self.optimizers = [optim.Adam(model.parameters(), lr=learning_rate) for model in self.models]
        self.criterion = nn.MSELoss()
        
        # 存储每个层级的重建误差统计
        self.error_stats = [{'mean': None, 'std': None, 'threshold': None} for _ in range(levels)]
        
        logger.info(f"初始化MSCDAE模型: 金字塔层级={levels}, 设备={device}")
        
    def train(self, image_dir):
        """训练模型"""
        logger.info(f"开始训练: 图像目录={image_dir}")
        
        # 数据预处理和变换
        transform = transforms.Compose([
            transforms.Resize((256, 256)),  # 调整为固定大小
            NormalizeWeber(),  # 光照归一化
        ])
        
        noise_transform = transforms.Compose([
            SaltPepperNoise(prob=self.noise_prob)  # 添加椒盐噪声
        ])
        
        # 创建数据集
        dataset = DefectDataset(image_dir, transform=transform, patch_size=self.patch_size, stride=self.stride)
        dataloader = DataLoader(dataset, batch_size=1, shuffle=True)  # 每次加载一张图像
        
        # 对每个金字塔层级训练一个CDAE模型
        for level in range(self.levels):
            logger.info(f"训练金字塔层级 {level + 1}/{self.levels}")
            model = self.models[level]
            optimizer = self.optimizers[level]
            model.train()
            
            all_errors = []  # 收集所有重建误差
            
            for epoch in range(self.epochs):
                epoch_loss = 0.0
                batch_count = 0
                
                for i, img in enumerate(dataloader):
                    # 缩放到当前金字塔层级
                    scale_factor = 0.5 ** level
                    scaled_size = (int(img.shape[2] * scale_factor), int(img.shape[3] * scale_factor))
                    scaled_img = resize(img, scaled_size)
                    
                    # 提取图像块
                    patches = []
                    for h in range(0, scaled_img.shape[2] - self.patch_size + 1, self.stride):
                        for w in range(0, scaled_img.shape[3] - self.patch_size + 1, self.stride):
                            patch = scaled_img[:, :, h:h+self.patch_size, w:w+self.patch_size]
                            patches.append(patch)
                    
                    if not patches:
                        continue
                    
                    # 将图像块组合成一个批次
                    batch = torch.cat(patches, dim=0).to(self.device)
                    
                    # 添加噪声
                    noisy_batch = torch.stack([noise_transform(patch.squeeze(0)).unsqueeze(0) for patch in patches], dim=0).to(self.device)
                    
                    # 训练步骤
                    optimizer.zero_grad()
                    outputs = model(noisy_batch)
                    loss = self.criterion(outputs, batch)
                    loss.backward()
                    optimizer.step()
                    
                    # 收集重建误差用于统计
                    with torch.no_grad():
                        for j in range(batch.size(0)):
                            clean_patch = batch[j].unsqueeze(0)
                            noisy_patch = noisy_batch[j].unsqueeze(0)
                            output = model(noisy_patch)
                            error = torch.mean((output - clean_patch) ** 2).item()
                            all_errors.append(error)
                    
                    epoch_loss += loss.item() * batch.size(0)
                    batch_count += batch.size(0)
                
                # 输出每个epoch的训练损失
                avg_loss = epoch_loss / batch_count if batch_count > 0 else 0
                logger.info(f"  Epoch {epoch+1}/{self.epochs}, Loss: {avg_loss:.6f}")
            
            # 计算重建误差的统计信息
            if all_errors:
                mean_error = np.mean(all_errors)
                std_error = np.std(all_errors)
                threshold = mean_error + self.gamma * std_error
                
                self.error_stats[level] = {
                    'mean': mean_error,
                    'std': std_error,
                    'threshold': threshold
                }
                
                logger.info(f"层级 {level + 1} 统计: Mean={mean_error:.6f}, Std={std_error:.6f}, Threshold={threshold:.6f}")
        
        logger.info("训练完成")
        return self
    
    def save_model(self, save_dir):
        """保存模型和统计信息"""
        os.makedirs(save_dir, exist_ok=True)
        
        # 保存模型参数
        for level, model in enumerate(self.models):
            torch.save(model.state_dict(), os.path.join(save_dir, f"model_level_{level}.pth"))
        
        # 保存重建误差统计信息
        np.save(os.path.join(save_dir, "error_stats.npy"), self.error_stats)
        
        # 保存配置信息
        config = {
            'levels': self.levels,
            'patch_size': self.patch_size,
            'stride': self.stride,
            'gamma': self.gamma
        }
        np.save(os.path.join(save_dir, "config.npy"), config)
        
        logger.info(f"模型保存至: {save_dir}")
    
    def load_model(self, save_dir):
        """加载已保存的模型和统计信息"""
        # 加载模型参数
        for level in range(self.levels):
            self.models[level].load_state_dict(torch.load(os.path.join(save_dir, f"model_level_{level}.pth"), map_location=self.device))
        
        # 加载重建误差统计信息
        self.error_stats = np.load(os.path.join(save_dir, "error_stats.npy"), allow_pickle=True).tolist()
        
        # 加载配置信息
        config = np.load(os.path.join(save_dir, "config.npy"), allow_pickle=True).item()
        self.levels = config['levels']
        self.patch_size = config['patch_size']
        self.stride = config['stride']
        self.gamma = config['gamma']
        
        logger.info(f"从 {save_dir} 加载模型")
        return self
    
    def detect(self, image_path, output_dir=None):
        """检测图像中的缺陷"""
        logger.info(f"检测图像: {image_path}")
        
        # 数据预处理
        transform = transforms.Compose([
            transforms.Resize((256, 256)),  # 调整为固定大小
            NormalizeWeber(),  # 光照归一化
        ])
        
        # 读取图像
        img = Image.open(image_path).convert('L')
        img_tensor = transform(transforms.ToTensor()(img)).unsqueeze(0)  # [1, 1, H, W]
        
        # 保存原始图像用于可视化
        original_img = img_tensor.clone()
        
        # 对每个金字塔层级进行缺陷检测
        residual_maps = []
        segmentation_maps = []
        
        for level in range(self.levels):
            logger.info(f"处理金字塔层级 {level + 1}/{self.levels}")
            model = self.models[level]
            model.eval()
            
            # 缩放到当前金字塔层级
            scale_factor = 0.5 ** level
            scaled_size = (int(img_tensor.shape[2] * scale_factor), int(img_tensor.shape[3] * scale_factor))
            scaled_img = resize(img_tensor, scaled_size)
            
            # 创建空的残差图
            residual_map = torch.zeros((1, 1, scaled_img.shape[2], scaled_img.shape[3])).to(self.device)
            count_map = torch.zeros((1, 1, scaled_img.shape[2], scaled_img.shape[3])).to(self.device)
            
            # 滑动窗口提取图像块并计算重建误差
            with torch.no_grad():
                for h in range(0, scaled_img.shape[2] - self.patch_size + 1, self.stride):
                    for w in range(0, scaled_img.shape[3] - self.patch_size + 1, self.stride):
                        patch = scaled_img[:, :, h:h+self.patch_size, w:w+self.patch_size].to(self.device)
                        output = model(patch)
                        
                        # 计算重建残差
                        error = (output - patch) ** 2
                        
                        # 更新残差图和计数图
                        residual_map[:, :, h:h+self.patch_size, w:w+self.patch_size] += error
                        count_map[:, :, h:h+self.patch_size, w:w+self.patch_size] += 1
            
            # 处理计数为0的位置
            count_map[count_map == 0] = 1
            # 计算平均残差
            residual_map = residual_map / count_map
            
            # 调整残差图到原始大小
            residual_map_full = resize(residual_map, (img_tensor.shape[2], img_tensor.shape[3]))
            residual_maps.append(residual_map_full)
            
            # 应用阈值进行缺陷分割
            threshold = self.error_stats[level]['threshold']
            segmentation_map = (residual_map_full > threshold).float()
            segmentation_maps.append(segmentation_map)
        
        # 融合不同层级的分割结果
        # 使用逻辑运算：相邻层使用AND，最终结果使用OR
        final_segmentation = torch.zeros_like(segmentation_maps[0])
        
        # 如果只有一个层级，直接使用该层级的分割图
        if self.levels == 1:
            final_segmentation = segmentation_maps[0]
        else:
            # 首先对相邻层级进行AND运算
            and_results = []
            for i in range(self.levels - 1):
                and_result = segmentation_maps[i] * segmentation_maps[i + 1]  # 逻辑AND
                and_results.append(and_result)
            
            # 然后对AND结果进行OR运算
            for and_result in and_results:
                final_segmentation = torch.max(final_segmentation, and_result)  # 逻辑OR
        
        # 计算统计信息
        defect_ratio = torch.sum(final_segmentation) / (final_segmentation.shape[2] * final_segmentation.shape[3])
        defect_ratio = defect_ratio.item()
        
        # 判断是否为NC产品
        is_nc = defect_ratio > 0.01  # 如果缺陷像素比例>1%，则判断为NC产品
        
        result = {
            'is_nc': is_nc,
            'defect_ratio': defect_ratio,
            'segmentation': final_segmentation.cpu().numpy()
        }
        
        # 如果指定了输出目录，则保存可视化结果
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
            # 保存原始图像
            original_np = original_img.squeeze().cpu().numpy()
            plt.figure(figsize=(10, 10))
            plt.imshow(original_np, cmap='gray')
            plt.title("Original Image")
            plt.savefig(os.path.join(output_dir, "original.png"))
            plt.close()
            
            # 保存残差图
            for i, residual_map in enumerate(residual_maps):
                residual_np = residual_map.squeeze().cpu().numpy()
                plt.figure(figsize=(10, 10))
                plt.imshow(residual_np, cmap='jet')
                plt.colorbar()
                plt.title(f"Residual Map - Level {i+1}")
                plt.savefig(os.path.join(output_dir, f"residual_level_{i+1}.png"))
                plt.close()
            
            # 保存分割图
            for i, segmentation_map in enumerate(segmentation_maps):
                segmentation_np = segmentation_map.squeeze().cpu().numpy()
                plt.figure(figsize=(10, 10))
                plt.imshow(segmentation_np, cmap='gray')
                plt.title(f"Segmentation - Level {i+1}")
                plt.savefig(os.path.join(output_dir, f"segmentation_level_{i+1}.png"))
                plt.close()
            
            # 保存最终分割结果
            final_np = final_segmentation.squeeze().cpu().numpy()
            plt.figure(figsize=(10, 10))
            plt.imshow(final_np, cmap='gray')
            plt.title(f"Final Segmentation (NC: {is_nc}, Defect Ratio: {defect_ratio:.6f})")
            plt.savefig(os.path.join(output_dir, "final_segmentation.png"))
            plt.close()
            
            # 在原始图像上标注缺陷区域
            original_rgb = np.stack([original_np, original_np, original_np], axis=2)
            overlay = original_rgb.copy()
            overlay[final_np > 0, 0] = 1.0  # 红色标注缺陷
            overlay[final_np > 0, 1:] = 0.0
            
            plt.figure(figsize=(10, 10))
            plt.imshow(overlay)
            plt.title(f"Defect Overlay (NC: {is_nc}, Defect Ratio: {defect_ratio:.6f})")
            plt.savefig(os.path.join(output_dir, "defect_overlay.png"))
            plt.close()
        
        logger.info(f"检测结果: {'NC' if is_nc else 'AC'}, 缺陷比例: {defect_ratio:.6f}")
        return result
    
    def test_batch_images(self, image_dir, output_dir=None, threshold=0.01):
        """批量测试图像并统计结果"""
        logger.info(f"批量测试图像: {image_dir}")
        
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # 获取目录中的所有图像
        image_files = [f for f in os.listdir(image_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
        
        results = []
        nc_count = 0
        
        for image_file in image_files:
            image_path = os.path.join(image_dir, image_file)
            
            # 为每个图像创建输出子目录
            if output_dir:
                image_output_dir = os.path.join(output_dir, os.path.splitext(image_file)[0])
                os.makedirs(image_output_dir, exist_ok=True)
            else:
                image_output_dir = None
            
            # 检测缺陷
            result = self.detect(image_path, image_output_dir)
            
            # 统计结果
            if result['is_nc']:
                nc_count += 1
            
            results.append({
                'image': image_file,
                'is_nc': result['is_nc'],
                'defect_ratio': result['defect_ratio']
            })
        
        # 计算NC产品比例
        nc_ratio = nc_count / len(image_files) if image_files else 0
        
        # 保存汇总结果
        summary = {
            'total_images': len(image_files),
            'nc_count': nc_count,
            'nc_ratio': nc_ratio,
            'threshold': threshold,
            'results': results
        }
        
        if output_dir:
            # 保存汇总报告
            with open(os.path.join(output_dir, "summary_report.txt"), "w") as f:
                f.write(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"图像总数: {len(image_files)}\n")
                f.write(f"NC产品数量: {nc_count}\n")
                f.write(f"NC产品比例: {nc_ratio:.4f}\n")
                f.write(f"缺陷阈值: {threshold}\n\n")
                f.write("详细结果:\n")
                for result in results:
                    f.write(f"图像: {result['image']}, 结果: {'NC' if result['is_nc'] else 'AC'}, 缺陷比例: {result['defect_ratio']:.6f}\n")
            
            # 保存汇总图表
            if results:
                defect_ratios = [r['defect_ratio'] for r in results]
                plt.figure(figsize=(12, 6))
                plt.bar(range(len(defect_ratios)), defect_ratios)
                plt.axhline(y=threshold, color='r', linestyle='-', label=f'Threshold ({threshold})')
                plt.xlabel("Image Index")
                plt.ylabel("Defect Ratio")
                plt.title("Defect Ratio for Each Image")
                plt.legend()
                plt.savefig(os.path.join(output_dir, "defect_ratios.png"))
                plt.close()
        
        logger.info(f"批量测试完成: 总数={len(image_files)}, NC数量={nc_count}, NC比例={nc_ratio:.4f}")
        return summary

# 使用示例
def run_demo():
    # 创建目录结构
    os.makedirs("data/ac_samples", exist_ok=True)
    os.makedirs("data/test_samples", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("results", exist_ok=True)
    
    # 初始化模型
    model = MSCDAE(levels=3, patch_size=64, stride=32, batch_size=32, epochs=30, learning_rate=0.001, noise_prob=0.05, gamma=3.0)
    
    # 训练模型（假设ac_samples目录包含无缺陷样本）
    model.train("data/ac_samples")
    
    # 保存模型
    model.save_model("models/mscdae_model")
    
    # 在测试样本上进行检测
    model.test_batch_images("data/test_samples", "results/test_results")

if __name__ == "__main__":
    # 运行演示示例
    run_demo()