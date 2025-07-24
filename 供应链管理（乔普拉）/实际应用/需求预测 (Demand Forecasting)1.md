*   **问题**: 准确预测未来的产品需求对于库存管理、生产计划和资源分配至关重要。不准确的预测会导致库存积压或缺货。
*   **AI/ML 应用**:
    *   **时间序列预测模型**: 使用如 ARIMA, SARIMA, Prophet (Facebook开源) 等传统统计模型，或更强大的机器学习模型如 LSTM (长短期记忆网络), GRU (门控循环单元) 等深度学习模型来分析历史销售数据、季节性、促销活动、市场趋势等，预测未来需求。
    *   **回归模型**: 使用线性回归、随机森林、梯度提升机 (XGBoost, LightGBM) 等模型，将需求作为目标变量，将价格、广告投入、经济指标、天气等作为特征进行预测。
*   **Python 库**: `pandas`, `numpy` (数据处理), `scikit-learn` (传统ML), `statsmodels` (统计模型), `Prophet`, `TensorFlow`, `PyTorch`, `Keras` (深度学习)。

需求感知与计划 (Demand Sensing & Planning)

*   **问题**: 利用接近实时的数据快速响应需求变化。
*   **AI/ML 应用**:
    *   **实时需求信号提取**: 整合 POS 数据、电商浏览/加购数据、社交媒体趋势、搜索引擎查询量等，使用 ML 模型快速识别需求的短期波动，并调整短期预测和计划。
*   **Python 库**: `pandas`, `numpy`, `scikit-learn`, `nltk`, `statsmodels`。
