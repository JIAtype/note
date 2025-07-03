'''
心得体会：
暴力循环是n^2的复杂度
'''

'''
题目：
给定一个整数数组 nums 和一个整数目标值 target，请你在该数组中找出 和为目标值 target  的那 两个 整数，并返回它们的数组下标。

你可以假设每种输入只会对应一个答案，并且你不能使用两次相同的元素。

你可以按任意顺序返回答案。

示例 1：

输入：nums = [2,7,11,15], target = 9
输出：[0,1]
解释：因为 nums[0] + nums[1] == 9 ，返回 [0, 1] 。
示例 2：

输入：nums = [3,2,4], target = 6
输出：[1,2]
示例 3：

输入：nums = [3,3], target = 6
输出：[0,1]
 

提示：

2 <= nums.length <= 104
-109 <= nums[i] <= 109
-109 <= target <= 109
只会存在一个有效答案
'''

'''
最优解法：
使用哈希表（字典）来实现时间复杂度为 O(n) 的算法。这种方法通过一遍遍历数组，在遍历过程中快速查找是否存在另一个数，使两者之和等于目标值。

【思路】：
- 遍历数组，同时将元素存入字典（元素值 -> 索引）
- 对每个元素，计算其差值（`target - nums[i]`），并立即在字典中查找
- 如果找到差值对应的元素索引，直接返回

【代码示例】：
```python
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], i]
            num_to_index[num] = i
```

【复杂度分析】：
- 时间复杂度：O(n)，因为只遍历数组一次，字典查找时间为O(1)
- 空间复杂度：O(n)，字典存储所有元素

【总结】：
这种方法在大部分情况下比双重循环快得多，尤其是数组较长时，性能明显提升。
'''

'''
以下是代码
'''
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(0,len(nums)):
            for j in range(i+1,len(nums)):
                if nums[i]+nums[j]==target:
                    return [i,j]