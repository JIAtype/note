TensorFlow的基础操作：

1. 基础张量操作：
- 创建张量：`tf.constant()`, `tf.zeros()`, `tf.ones()`, `tf.random.normal()`
- 数据类型转换：`tf.cast()`
- 设备管理：`tf.device()`

2. 基本运算：
- 矩阵运算：`tf.matmul()`
- 加减乘除：`tf.add()`, `tf.subtract()`, `tf.multiply()`, `tf.divide()`
- 幂运算：`tf.pow()`
- 求和：`tf.reduce_sum()`
- 平均值：`tf.reduce_mean()`

3. 索引和切片：
- 索引：`tensor[0]`, `tensor[0:2]`
- 布尔索引：`tf.boolean_mask()`
- 聚合索引：`tf.gather()`

4. 形状操作：
- 改变形状：`tf.reshape()`
- 增加维度：`tf.expand_dims()`
- 减少维度：`tf.squeeze()`
- 拼接：`tf.concat()`, `tf.stack()`

5. 自动求导（Autograph）：
- 创建梯度：`tf.GradientTape()`
- 计算梯度：`tape.gradient()`
- 停止梯度追踪：`tf.stop_gradient()`

6. 变量管理：
- 创建变量：`tf.Variable()`
- 初始化：`tf.initializers`
- 保存和加载：`tf.train.Checkpoint`

7. 优化器：
- 常用优化器：`tf.keras.optimizers.SGD()`, `tf.keras.optimizers.Adam()`
- 更新参数：`optimizer.apply_gradients()`
- 清除梯度：`optimizer.zero_gradients()`

8. 数据处理：
- 数据加载：`tf.data.Dataset`
- 数据预处理：`tf.data.Dataset.map()`
- 批处理：`tf.data.Dataset.batch()`
- 打乱数据：`tf.data.Dataset.shuffle()`

9. 常用神经网络层：
- 线性层：`tf.keras.layers.Dense()`
- 卷积层：`tf.keras.layers.Conv2D()`
- 池化层：`tf.keras.layers.MaxPooling2D()`
- 批归一化：`tf.keras.layers.BatchNormalization()`
- Dropout：`tf.keras.layers.Dropout()`

10. 损失函数：
- MSE损失：`tf.keras.losses.MeanSquaredError()`
- 交叉熵损失：`tf.keras.losses.CategoricalCrossentropy()`
- 二元交叉熵损失：`tf.keras.losses.BinaryCrossentropy()`

11. 模型构建方式：
- 函数式API：`tf.keras.Model`
- 序贯模型：`tf.keras.Sequential`
- 子类化模型：自定义继承`tf.keras.Model`

12. 训练和评估：
- 编译模型：`model.compile()`
- 训练模型：`model.fit()`
- 评估模型：`model.evaluate()`
- 预测：`model.predict()`

13. 回调函数：
- 保存模型：`tf.keras.callbacks.ModelCheckpoint`
- 早停：`tf.keras.callbacks.EarlyStopping`
- 学习率调整：`tf.keras.callbacks.LearningRateScheduler`

14. 指标：
- 常用指标：`tf.keras.metrics.Accuracy()`, `tf.keras.metrics.MeanSquaredError()`
- 自定义指标：继承`tf.keras.metrics.Metric`

这些是TensorFlow中最基础和常用的操作。TensorFlow 2.x 版本中，由于引入了Eager Execution，使得使用体验更加直观和Pythonic。如果您想深入了解某个具体的操作或概念，我可以为您详细解释。