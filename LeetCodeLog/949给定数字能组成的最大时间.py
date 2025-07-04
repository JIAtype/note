'''
心得体会：
排列组合问题
生成所有排列的方式
1.itertools.product 是 Python 的 itertools 模块中的一个函数，用于生成多个可迭代对象的笛卡尔积（Cartesian Product）。这意味着它可以生成所有可能的组合，其中每个组合由各个可迭代对象中的元素组成。
2.列表推导式：使用三个 for 子句来生成所有可能的组合。

for循环中用continue可以跳过此次循环，结合for，continue和else可以print“没有遇到跳过条件”
'''

'''
题目：

给定一个由 4 位数字组成的数组，返回可以设置的符合 24 小时制的最大时间。

24 小时格式为 "HH:MM" ，其中 HH 在 00 到 23 之间，MM 在 00 到 59 之间。最小的 24 小时制时间是 00:00 ，而最大的是 23:59 。从 00:00 （午夜）开始算起，过得越久，时间越大。

以长度为 5 的字符串，按 "HH:MM" 格式返回答案。如果不能确定有效时间，则返回空字符串。
'''

'''
解法：
要解决这个问题，可以通过以下步骤来找到符合 24 小时制的最大时间：

1. **生成所有可能的组合**：
   - 从给定的 4 位数字数组 `arr` 中生成所有可能的两位数字组合，以表示小时和分钟。
   - 每个组合都需要满足 24 小时制的限制，即小时在 00 到 23 之间，分钟在 00 到 59 之间。

2. **过滤有效时间**：
   - 检查每个组合是否符合 24 小时制的有效时间。
   - 如果组合有效，则将其添加到结果列表中。

3. **找到最大时间**：
   - 从结果列表中找到最大的有效时间。

以下是具体的实现代码：

```python
'''
def largestTimeFromDigits(arr):
    max_time = -1

    # 遍历所有可能的组合
    for h1, h2, m1, m2 in itertools.product(range(10), repeat=4):
        if h1 == 0 or h2 == 0 or m1 == 0 or m2 == 0:
            continue

        # 尝试组合成小时和分钟
        h = h1 * 10 + h2
        m = m1 * 10 + m2

        # 检查是否符合 24 小时制
        if h >= 24 or m >= 60:
            continue

        # 如果满足条件，则更新最大时间
        current_time = h * 60 + m
        max_time = max(max_time, current_time)

    # 如果找到有效时间，则返回以 "HH:MM" 格式的字符串，如果没有找到，则返回空字符串
    if max_time == -1:
        return ""
    else:
        hours = max_time // 60
        minutes = max_time % 60
        return f"{hours:02d}:{minutes:02d}"

# 测试示例
arr = [1, 2, 3, 4]
print(largestTimeFromDigits(arr))  # 输出："23:41"

arr = [5, 5, 5, 5]
print(largestTimeFromDigits(arr))  # 输出：""

arr = [0, 0, 0, 0]
print(largestTimeFromDigits(arr))  # 输出："00:00"

arr = [0, 0, 1, 0]
print(largestTimeFromDigits(arr))  # 输出："10:00"
'''
```

在这个实现中，使用 `itertools.product` 生成所有可能的两位数字组合，并检查这些组合是否符合 24 小时制的有效时间。最后，如果找到有效时间，则返回以 "HH:MM" 格式的字符串，如果没有找到，则返回空字符串。
'''

'''
以下是代码
'''
class Solution:
    def largestTimeFromDigits(self, arr: List[int]) -> str:
        maxtime = -1
        for h1 in range(4):
            for h2 in range(4):
                if h1 == h2:
                    continue
                for m1 in range(4):
                    if m1 == h1 or m1 == h2:
                        continue
                    m2 = 6-h1-h2-m1
                    h = arr[h1]*10+arr[h2]
                    m = arr[m1]*10+arr[m2]

                    if h < 24 and m<60:
                        currenttime = h*60+m
                        maxtime=max(maxtime,currenttime)

        if maxtime == -1:
            return ""
        else:
            hours = maxtime//60
            minutes = maxtime%60
            return f"{hours:02d}:{minutes:02d}"