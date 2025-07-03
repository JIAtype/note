import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision.transforms as transforms
from torch.utils.data import Dataset, DataLoader
import os
from PIL import Image
import numpy as np
import logging
from pathlib import Path

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GaussianPyramid(nn.Module):
    def __init__(self, levels=3):
        super(GaussianPyramid, self).__init__()
        self.levels = levels
        
    def forward(self, x):
        # 生成高斯金字塔
        pyramid = [x]
        current = x
        for _ in range(1, self.levels):
            # 使用平均池化模拟高斯下采样
            current = F.avg_pool2d(current, kernel_size=2, stride=2)
            pyramid.append(current)
        return pyramid

class MultiScaleConvBlock(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(MultiScaleConvBlock, self).__init__()
        # 高斯金字塔
        self.gaussian_pyramid = GaussianPyramid(levels=3)
        
        # 多尺度卷积
        self.conv_layers = nn.ModuleList([
            nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=k, padding=k//2),
                nn.BatchNorm2d(out_channels),
                nn.ReLU(inplace=True)
            ) for k in [1, 3, 5]
        ])
        
        # 计算输出通道数 (3个卷积核尺寸 * 3个金字塔级别 * out_channels)
        self.output_channels = 3 * 3 * out_channels

    def forward(self, x):
        # 获取高斯金字塔
        pyramid_features = self.gaussian_pyramid(x)
        
        # 存储多尺度特征
        multi_scale_features = []
        
        # 在每个金字塔层级应用卷积
        for level in pyramid_features:
            level_features = [conv(level) for conv in self.conv_layers]
            
            #报错
            # 确保所有特征图尺寸一致
            # if level != pyramid_features[0]:
            #     level_features = [F.interpolate(feat, size=pyramid_features[0].shape[2:]) 
            #                     for feat in level_features]
                
            # 另一种修改方式:
            if level.shape != pyramid_features[0].shape:
                level_features = [F.interpolate(feat, size=pyramid_features[0].shape[2:]) 
                                for feat in level_features]

            multi_scale_features.extend(level_features)
        
        # 特征融合
        return torch.cat(multi_scale_features, dim=1)

class MSCDAE(nn.Module):
    def __init__(self, input_channels=1):
        super(MSCDAE, self).__init__()
        
        # 定义每层的通道数
        self.encoder_channels = [input_channels, 16, 32]
        
        # 编码器
        self.encoder_block1 = MultiScaleConvBlock(self.encoder_channels[0], self.encoder_channels[1])
        self.pool1 = nn.MaxPool2d(2, 2)
        self.encoder_block2 = MultiScaleConvBlock(self.encoder_block1.output_channels, self.encoder_channels[2])
        self.pool2 = nn.MaxPool2d(2, 2)
        
        # 获取编码器最终输出通道数
        self.bottleneck_channels = self.encoder_block2.output_channels
        
        # 解码器
        self.upconv1 = nn.ConvTranspose2d(self.bottleneck_channels, 32, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.decoder_block1 = MultiScaleConvBlock(32, 16)
        self.upconv2 = nn.ConvTranspose2d(self.decoder_block1.output_channels, 16, kernel_size=3, stride=2, padding=1, output_padding=1)
        self.decoder_block2 = MultiScaleConvBlock(16, 8)
        self.final_conv = nn.Conv2d(self.decoder_block2.output_channels, input_channels, kernel_size=1)
        
        # 添加Sigmoid激活保证输出在[0,1]范围
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        # 添加噪声 (根据输入强度自适应)
        noise_level = 0.1 * torch.mean(x)
        noise = torch.randn_like(x) * noise_level
        x_noisy = torch.clamp(x + noise, 0, 1)
        
        # 编码
        e1 = self.encoder_block1(x_noisy)
        e1_pool = self.pool1(e1)
        e2 = self.encoder_block2(e1_pool)
        e2_pool = self.pool2(e2)
        
        # 解码
        d1 = self.upconv1(e2_pool)
        d1_block = self.decoder_block1(d1)
        d2 = self.upconv2(d1_block)
        d2_block = self.decoder_block2(d2)
        output = self.final_conv(d2_block)
        
        # 确保输出在[0,1]范围内
        return self.sigmoid(output)

class DefectDataset(Dataset):
    def __init__(self, image_dir, transform=None):
        self.image_dir = Path(image_dir)
        
        # 检查文件夹是否存在
        if not self.image_dir.exists():
            raise FileNotFoundError(f"图像目录 '{image_dir}' 不存在")
        
        # 获取支持的图像文件
        self.images = [f for f in os.listdir(image_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        
        # 检查是否有图像文件
        if len(self.images) == 0:
            raise ValueError(f"图像目录 '{image_dir}' 中没有找到支持的图像文件(.png, .jpg, .jpeg, .bmp)")
        
        self.transform = transform or transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])
        
        logger.info(f"已加载 {len(self.images)} 张图像")

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        img_path = os.path.join(self.image_dir, self.images[idx])
        try:
            image = Image.open(img_path).convert('RGB')  # 确保图像是RGB格式
            image_tensor = self.transform(image)
            return image_tensor
        except Exception as e:
            logger.error(f"加载图像 '{img_path}' 时出错: {e}")
            # 返回一个空白图像作为替代
            return torch.zeros((1, 256, 256))

def train_mscdae(model, train_loader, criterion, optimizer, device, epochs=50, save_path='checkpoints'):
    # 创建保存检查点的目录
    save_dir = Path(save_path)
    save_dir.mkdir(exist_ok=True, parents=True)
    
    best_loss = float('inf')
    model.train()
    
    for epoch in range(epochs):
        total_loss = 0
        for batch_idx, batch in enumerate(train_loader):
            # 将数据移至设备
            batch = batch.to(device)
            
            optimizer.zero_grad()
            
            # 前向传播
            reconstructed = model(batch)
            
            # 计算损失
            loss = criterion(reconstructed, batch)
            
            # 反向传播
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
            # 打印批次进度
            if (batch_idx + 1) % 10 == 0 or (batch_idx + 1) == len(train_loader):
                logger.info(f'Epoch [{epoch+1}/{epochs}], Batch [{batch_idx+1}/{len(train_loader)}], Loss: {loss.item():.4f}')
        
        avg_loss = total_loss / len(train_loader)
        logger.info(f'Epoch [{epoch+1}/{epochs}], Average Loss: {avg_loss:.4f}')
        
        # 保存最佳模型
        if avg_loss < best_loss:
            best_loss = avg_loss
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': best_loss,
            }, save_dir / 'best_model.pth')
            logger.info(f'已保存最佳模型, Loss: {best_loss:.4f}')
        
        # 每10个epoch保存一次检查点
        if (epoch + 1) % 10 == 0:
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'loss': avg_loss,
            }, save_dir / f'checkpoint_epoch_{epoch+1}.pth')

def detect_defects(model, image, device, threshold_factor=2.0):
    # 确保模型在评估模式
    model.eval()
    
    # 将图像移至设备
    image = image.to(device)
    
    with torch.no_grad():
        # 获取重建图像
        reconstructed = model(image.unsqueeze(0)).squeeze(0)
        
        # 计算重建误差
        error_map = torch.abs(image - reconstructed)
        
        # 计算每个通道的误差统计
        if error_map.dim() > 2:  # 多通道图像
            # 转换为灰度误差图
            error_map = torch.mean(error_map, dim=0)
        
        # 设置自适应阈值
        threshold = error_map.mean() + threshold_factor * error_map.std()
        defect_mask = error_map > threshold
        
        # 返回结果
        return {
            'original': image.cpu(),
            'reconstructed': reconstructed.cpu(),
            'error_map': error_map.cpu(),
            'defect_mask': defect_mask.cpu(),
            'threshold': threshold.item()
        }

def load_model(model_path, model, device):
    # 加载模型检查点
    try:
        checkpoint = torch.load(model_path, map_location=device)
        model.load_state_dict(checkpoint['model_state_dict'])
        logger.info(f"模型已从 '{model_path}' 加载, Epoch: {checkpoint['epoch']}, Loss: {checkpoint['loss']:.4f}")
        return True
    except Exception as e:
        logger.error(f"加载模型失败: {e}")
        return False

def main():
    # 设备选择
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"使用设备: {device}")
    
    # 设置参数
    image_dir = 'images'
    batch_size = 16
    epochs = 50
    learning_rate = 0.001
    
    try:
        # 数据集和数据加载器
        dataset = DefectDataset(image_dir)
        
        # 划分训练集和验证集 (80% 训练, 20% 验证)
        train_size = int(0.8 * len(dataset))
        val_size = len(dataset) - train_size
        train_dataset, val_dataset = torch.utils.data.random_split(dataset, [train_size, val_size])
        
        train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
        val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
        
        logger.info(f"训练集: {train_size} 样本, 验证集: {val_size} 样本")
        
        # 模型初始化
        model = MSCDAE().to(device)
        logger.info(f"初始化模型: {model.__class__.__name__}")
        
        # 损失函数和优化器
        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)
        
        # 训练
        logger.info("开始训练...")
        train_mscdae(model, train_loader, criterion, optimizer, device, epochs=epochs)
        
        # 保存最终模型
        torch.save({
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
        }, 'final_mscdae_model.pth')
        logger.info("训练完成，模型已保存")
        
        # 在验证集上评估
        logger.info("在验证集上评估...")
        model.eval()
        val_loss = 0
        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(device)
                reconstructed = model(batch)
                loss = criterion(reconstructed, batch)
                val_loss += loss.item()
        
        avg_val_loss = val_loss / len(val_loader)
        logger.info(f"验证集平均损失: {avg_val_loss:.4f}")

    except Exception as e:
        logger.error(f"发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()

# 执行
# python mscdae_v1_3.py

import torch
import torchvision.transforms as transforms
from PIL import Image
import os
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import logging
import argparse
import cv2
import matplotlib.pyplot as plt

# 导入模型 (确保路径正确，能够导入之前定义的MSCDAE类)
from mscdae_v1_3 import MSCDAE, load_model

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为 SimHei
plt.rcParams['axes.unicode_minus'] = False    # 解决负号显示问题

def load_and_preprocess_image(image_path, transform=None):
    """加载并预处理单张图像"""
    if transform is None:
        transform = transforms.Compose([
            transforms.Grayscale(),
            transforms.Resize((256, 256)),
            transforms.ToTensor()
        ])
    
    try:
        image = Image.open(image_path).convert('RGB')
        tensor = transform(image)
        return tensor, image
    except Exception as e:
        logger.error(f"加载图像 '{image_path}' 失败: {e}")
        return None, None

def visualize_results(results, save_path=None):
    """可视化检测结果"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 原始图像
    axes[0, 0].imshow(results['original'].permute(1, 2, 0).cpu().numpy())
    axes[0, 0].set_title('原始图像')
    axes[0, 0].axis('off')
    
    # 重建图像
    axes[0, 1].imshow(results['reconstructed'].permute(1, 2, 0).cpu().numpy())
    axes[0, 1].set_title('重建图像')
    axes[0, 1].axis('off')
    
    # 误差图
    error_map = results['error_map'].cpu().numpy()
    im = axes[1, 0].imshow(error_map, cmap='jet')
    axes[1, 0].set_title(f'重建误差 (均值: {error_map.mean():.4f})')
    axes[1, 0].axis('off')
    fig.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
    
    # 缺陷掩码
    axes[1, 1].imshow(results['defect_mask'].cpu().numpy(), cmap='gray')
    axes[1, 1].set_title(f'缺陷掩码 (阈值: {results["threshold"]:.4f})')
    axes[1, 1].axis('off')
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path)
        logger.info(f"结果已保存至 {save_path}")
    
    plt.show()

def apply_defect_mask(original_image, defect_mask, color=(0, 0, 255), alpha=0.5):
    """在原始图像上应用缺陷掩码，突出显示缺陷区域"""
    # 将原始图像转换为NumPy数组
    if isinstance(original_image, torch.Tensor):
        # 如果是张量，转换为NumPy数组并确保通道顺序正确(C,H,W -> H,W,C)
        original_np = original_image.permute(1, 2, 0).cpu().numpy()
    elif isinstance(original_image, Image.Image):
        # 如果是PIL图像，转换为NumPy数组
        original_np = np.array(original_image)
    else:
        original_np = original_image
    
    # 确保值范围在0-1之间
    if original_np.max() <= 1.0:
        original_np = (original_np * 255).astype(np.uint8)
    
    # 创建RGB图像(如果是灰度图)
    if len(original_np.shape) == 2 or original_np.shape[2] == 1:
        original_np = cv2.cvtColor(original_np, cv2.COLOR_GRAY2BGR)
    
    # 创建与原图相同大小的掩码图像
    mask_np = cv2.resize(defect_mask.cpu().numpy().astype(np.uint8) * 255, 
                         (original_np.shape[1], original_np.shape[0]))
    
    # 创建一个彩色覆盖图
    overlay = original_np.copy()
    overlay[mask_np > 0] = color
    
    # 将覆盖图与原图混合
    highlighted = cv2.addWeighted(overlay, alpha, original_np, 1 - alpha, 0)
    
    return highlighted

def test_single_image(model, image_path, device, threshold_factor=2.0, save_dir=None):
    """测试单张图像并可视化结果"""
    # 加载并预处理图像
    image_tensor, original_image = load_and_preprocess_image(image_path)
    if image_tensor is None:
        return
    
    # 检测缺陷
    results = detect_defects(model, image_tensor, device, threshold_factor)
    
    # 可视化结果
    if save_dir:
        save_path = os.path.join(save_dir, f"{Path(image_path).stem}_results.png")
    else:
        save_path = None
    
    visualize_results(results, save_path)
    
    # 在原始图像上标记缺陷
    highlighted_image = apply_defect_mask(original_image, results['defect_mask'])
    
    if save_dir:
        highlight_path = os.path.join(save_dir, f"{Path(image_path).stem}_highlighted.png")
        cv2.imwrite(highlight_path, cv2.cvtColor(highlighted_image, cv2.COLOR_RGB2BGR))
        logger.info(f"标记的图像已保存至 {highlight_path}")
    
    plt.figure(figsize=(8, 8))
    plt.imshow(highlighted_image)
    plt.title("标记的缺陷")
    plt.axis('off')
    plt.show()
    
    return results

def detect_defects(model, image, device, threshold_factor=2.0):
    """检测图像中的缺陷"""
    # 确保模型在评估模式
    model.eval()
    
    # 将图像移至设备
    image = image.to(device)
    
    with torch.no_grad():
        # 获取重建图像
        reconstructed = model(image.unsqueeze(0)).squeeze(0)
        
        # 计算重建误差
        error_map = torch.abs(image - reconstructed)
        
        # 计算每个通道的误差统计
        if error_map.dim() > 2:  # 多通道图像
            # 转换为灰度误差图
            error_map = torch.mean(error_map, dim=0)
        
        # 设置自适应阈值
        threshold = error_map.mean() + threshold_factor * error_map.std()
        defect_mask = error_map > threshold
        
        # 返回结果
        return {
            'original': image.cpu(),
            'reconstructed': reconstructed.cpu(),
            'error_map': error_map.cpu(),
            'defect_mask': defect_mask.cpu(),
            'threshold': threshold.item()
        }

def test_batch_images(model, image_dir, device, threshold_factor=2.0, save_dir=None):
    """测试文件夹中的所有图像"""
    # 确保保存目录存在
    if save_dir:
        os.makedirs(save_dir, exist_ok=True)
    
    # 获取所有图像文件
    image_files = [f for f in os.listdir(image_dir) 
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    
    if not image_files:
        logger.error(f"目录 '{image_dir}' 中没有找到图像文件")
        return
    
    logger.info(f"找到 {len(image_files)} 个图像文件")
    
    # 对每个图像进行测试
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        logger.info(f"处理图像: {image_path}")
        try:
            test_single_image(model, image_path, device, threshold_factor, save_dir)
        except Exception as e:
            logger.error(f"处理图像 '{image_path}' 时出错: {e}")
            import traceback
            traceback.print_exc()

def main():
    parser = argparse.ArgumentParser(description='测试缺陷检测模型')
    parser.add_argument('--model_path', type=str, default='final_mscdae_model.pth',
                        help='模型权重文件路径')
    parser.add_argument('--data_dir', type=str, default='data',
                        help='包含测试图像的目录')
    parser.add_argument('--single_image', type=str, default=None,
                        help='单张图像的路径（可选）')
    parser.add_argument('--threshold', type=float, default=2.0,
                        help='缺陷检测阈值因子（默认：标准差的2倍）')
    parser.add_argument('--output_dir', type=str, default='results',
                        help='保存结果的目录')
    args = parser.parse_args()
    
    # 选择设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    logger.info(f"使用设备: {device}")
    
    # 初始化模型
    model = MSCDAE().to(device)
    
    # 加载模型权重
    if not os.path.exists(args.model_path):
        logger.error(f"模型文件 '{args.model_path}' 不存在")
        return
    
    checkpoint = torch.load(args.model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    logger.info(f"已加载模型 '{args.model_path}'")
    
    # 创建输出目录
    if args.output_dir:
        os.makedirs(args.output_dir, exist_ok=True)
    
    # 测试模型
    if args.single_image:
        if os.path.exists(args.single_image):
            logger.info(f"测试单张图像: {args.single_image}")
            test_single_image(model, args.single_image, device, args.threshold, args.output_dir)
        else:
            logger.error(f"图像文件 '{args.single_image}' 不存在")
    else:
        if os.path.exists(args.data_dir):
            logger.info(f"测试目录中的所有图像: {args.data_dir}")
            test_batch_images(model, args.data_dir, device, args.threshold, args.output_dir)
        else:
            logger.error(f"数据目录 '{args.data_dir}' 不存在")

if __name__ == '__main__':
    main()

# 模型名
# final_mscdae_model
# 测试数据保存在
# data
# 结果保存在
# results

# 测试整个数据目录中的图像
# python mscdae_v1_3_test.py --model_path final_mscdae_model.pth --data_dir data --output_dir results

# 测试单张图像
# python mscdae_v1_3_test.py --model_path final_mscdae_model.pth --single_image data/test_image.jpg --output_dir results

# 调整缺陷检测阈值
# python mscdae_v1_3_test.py --data_dir data --threshold 1.5  # 降低阈值，检测更多潜在缺陷