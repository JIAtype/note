总结Pandas和Numpy在数据清洗与分析中的主要功能和用法：

1. 数据读取与写入：
```python
# Pandas读取数据
df = pd.read_csv('data.csv')           # CSV文件
df = pd.read_excel('data.xlsx')        # Excel文件
df = pd.read_json('data.json')         # JSON文件

# 写入数据
df.to_csv('output.csv', index=False)   # CSV文件
df.to_excel('output.xlsx')             # Excel文件
df.to_json('output.json')              # JSON文件
```

2. 数据查看与基本信息：
```python
# 查看数据
df.head()         # 查看前几行
df.tail()         # 查看后几行
df.describe()     # 数据统计信息
df.info()         # 数据信息

# 查看特定列
df['column_name']     # 单列
df[['col1', 'col2']]  # 多列
```

3. 数据清洗：
```python
# 处理缺失值
df.isnull()              # 检查缺失值
df.dropna()             # 删除缺失值
df.fillna(value)        # 填充缺失值
df.interpolate()        # 插值填充

# 数据类型转换
df.astype({'col1': 'float', 'col2': 'int'})
pd.to_datetime(df['date_col'])
pd.to_numeric(df['num_col'], errors='coerce')

# 重复值处理
df.duplicated()         # 检查重复
df.drop_duplicates()    # 删除重复

# 异常值处理
df[df['col'] > threshold]   # 筛选异常值
df['col'].clip(lower, upper)  # 限制值范围
```

4. 数据转换：
```python
# 日期处理
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month

# 分类数据编码
pd.get_dummies(df['category'])  # one-hot编码
df['category'].astype('category')  # 转换为分类类型

# 数据标准化
(df - df.mean()) / df.std()  # Z-score标准化
(df - df.min()) / (df.max() - df.min())  # Min-Max标准化
```

5. 数据筛选与过滤：
```python
# 条件筛选
df[df['col1'] > 10]              # 单条件
df[(df['col1'] > 10) & (df['col2'] < 20)]  # 多条件
df.query('col1 > 10 and col2 < 20')       # query方法

# 分组筛选
df.groupby('category').filter(lambda x: len(x) > 10)
```

6. 数据聚合：
```python
# 基本聚合
df.groupby('category').mean()    # 按类别求平均
df.groupby('category').sum()     # 按类别求和
df.groupby('category').agg(['mean', 'sum', 'count'])  # 多个聚合函数

# 自定义聚合
df.groupby('category').agg(custom_func=lambda x: x.max() - x.min())
```

7. 数据合并：
```python
# 合并数据
pd.concat([df1, df2], axis=0)    # 垂直合并
pd.concat([df1, df2], axis=1)    # 水平合并

# 合并DataFrame
pd.merge(df1, df2, on='key')     # 内连接
pd.merge(df1, df2, on='key', how='left')  # 左连接
pd.merge(df1, df2, on='key', how='right') # 右连接
pd.merge(df1, df2, on='key', how='outer') # 外连接
```

8. 数据排序：
```python
df.sort_values('col1')           # 单列排序
df.sort_values(['col1', 'col2']) # 多列排序
df.sort_values('col1', ascending=False)  # 降序
```

9. 数据采样：
```python
df.sample(n=10)         # 随机抽取10行
df.sample(frac=0.1)     # 抽取10%的数据
df.sample(n=10, replace=True)  # 有放回抽样
```

10. 数据可视化：
```python
# Pandas内置可视化
df.plot(kind='line')    # 线图
df.plot(kind='bar')     # 柱状图
df.plot(kind='hist')    # 直方图
df.plot(kind='scatter', x='col1', y='col2')  # 散点图

# Numpy可视化
plt.plot(np.arange(10), np.random.randn(10))  # 线图
plt.bar(np.arange(5), np.random.randn(5))     # 柱状图
plt.hist(np.random.randn(1000), bins=30)      # 直方图
```

11. Numpy高级操作：
```python
# 数组操作
np.concatenate([arr1, arr2])     # 数组拼接
np.split(arr, 3)                 # 数组分割
np.reshape(arr, (3, 4))          # 改变形状

# 数学运算
np.mean(arr)                     # 平均值
np.std(arr)                      # 标准差
np.percentile(arr, 50)           # 中位数

# 随机数
np.random.randn(100)             # 标准正态分布
np.random.randint(0, 10, size=10)  # 随机整数
np.random.choice(arr, size=5)      # 随机选择
```

12. 时间序列分析：
```python
# 重采样
df.resample('M').mean()          # 按月重采样
df.resample('W').sum()           # 按周重采样

# 滚动窗口
df.rolling(window=3).mean()      # 滚动平均
df.expanding().mean()            # 扩展窗口

# 时差计算
df['date'].diff()                # 时间差
df['value'].diff()               # 值差
```

13. 数据验证：
```python
# 数据质量检查
df.duplicated().sum()            # 重复值数量
df.isnull().sum()                # 缺失值数量
df.nunique()                     # 唯一值数量

# 数据分布检查
df['col'].value_counts()         # 值计数
df['col'].describe()             # 统计描述
```

14. 数据转换：
```python
# 数据重塑
df.pivot(index='row', columns='col', values='value')  # 枢纽表
df.melt(id_vars=['col1'], value_vars=['col2', 'col3'])  # 熔化

# 数据映射
df['col'].map({'old': 'new'})     # 值映射
df.replace({'old': 'new'})        # 替换值
```

15. 性能优化：
```python
# 使用向量化操作
df['new_col'] = df['col1'] + df['col2']  # 向量化
df['new_col'] = np.where(df['col'] > 0, 1, 0)  # 向量化条件

# 使用inplace参数
df.dropna(inplace=True)          # 直接修改
df.rename(columns={'old': 'new'}, inplace=True)
```

注意事项：
1. 处理大数据集时注意内存使用
2. 使用向量化操作提高性能
3. 数据清洗时注意数据类型转换
4. 处理缺失值时要根据业务场景选择合适的方法
5. 时间序列分析时注意时间戳的格式
6. 数据聚合时考虑性能影响
7. 数据可视化时注意选择合适的图表类型
8. 数据转换时注意数据的一致性

这些是Pandas和Numpy中最常用的数据清洗与分析操作。根据具体应用场景，可以组合使用这些功能来完成复杂的数据处理任务。