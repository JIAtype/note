池化层pooling
降维减少数据维度，保留关键特征

reshape层
调整张量的维度形状，不改变数据本身，只改变数据的组织形式

output层
输出网络的最终结果，适配具体任务需求
二分类用sigmoid，输出0-1概率
多分类用softmax，输出概率分布

dropout层
防止过拟合

batch normalization层
加速训练，稳定数值
