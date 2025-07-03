'''
心得体会：
矩阵 排序
'''

'''
题目：
以数组 intervals 表示若干个区间的集合，其中单个区间为 intervals[i] = [starti, endi] 。请你合并所有重叠的区间，并返回 一个不重叠的区间数组，该数组需恰好覆盖输入中的所有区间 。

示例 1：

输入：intervals = [[1,3],[2,6],[8,10],[15,18]]
输出：[[1,6],[8,10],[15,18]]
解释：区间 [1,3] 和 [2,6] 重叠, 将它们合并为 [1,6].
示例 2：

输入：intervals = [[1,4],[4,5]]
输出：[[1,5]]
解释：区间 [1,4] 和 [4,5] 可被视为重叠区间。

提示：

1 <= intervals.length <= 104
intervals[i].length == 2
0 <= starti <= endi <= 104
'''

'''
解法：
你描述的问题是一个经典的“区间合并”问题（Merge Intervals）。具体思路如下：

### 思路总结
1. **排序**：先按起始位置 `start` 对所有区间进行排序。这样相邻的区间更容易检测重叠。
2. **合并**：遍历排序后的区间，如果当前区间的起点 `start` 在上一个区间的结束点 `end` 之内（或重叠），则合并这两个区间，更新结束点为较大值。
3. **结果**：保存合并后的区间到结果数组。

---

### 代码实现
```python
from typing import List

class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        # 按起始值排序
        intervals.sort(key=lambda x: x[0])
        
        merged = []
        for interval in intervals:
            # 如果结果数组为空，直接加入
            if not merged:
                merged.append(interval)
            else:
                # 比较当前区间与最后一个合并区间的关系
                last = merged[-1]
                if interval[0] <= last[1]:
                    # 有重叠，合并
                    last[1] = max(last[1], interval[1])
                else:
                    # 无重叠，加入新区间
                    merged.append(interval)
        return merged
```

### 详细说明
- `intervals.sort(key=lambda x: x[0])`：按照每个区间的起点由小到大排序。
- 遍历每个区间：
  - 如果 `merged` 为空，直接加入这个区间。
  - 如果当前区间的起点 `interval[0]` 小于或等于刚加入的最后一个区间的结束点 `last[1]`，说明两个区间有重叠：
    - 更新结束点为两个区间的最大结束点。
  - 否则，说明没有重叠，加入新的区间。

---

### 示例
```python
intervals = [[1,3],[2,6],[8,10],[15,18]]
solution = Solution()
print(solution.merge(intervals))
# 输出：[[1,6],[8,10],[15,18]]
```

这个方案时间复杂度为 `O(n log n)`（由于排序），空间复杂度为 `O(n)`（存储合并区间）。

如果你还需要更详细的解释或者其他实现方式，随时告诉我！
'''

'''
以下是代码
'''
class Solution:
    def merge(self, intervals: List[List[int]]) -> List[List[int]]:
        intervals.sort(key=lambda x: x[0])
        result=[]
        for interval in intervals:
            if not result:
                result.append(interval)
            else:
                last=result[-1]
                if interval[0]<=last[1]:
                    last[1]=max(last[1], interval[1])
                else:
                    result.append(interval)
        return result