'''
心得体会：
快速选择排序
'''

'''
题目：
给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。

请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。

你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。

示例 1:

输入: [3,2,1,5,6,4], k = 2
输出: 5
示例 2:

输入: [3,2,3,1,2,4,5,5,6], k = 4
输出: 4

提示：

1 <= k <= nums.length <= 105
-104 <= nums[i] <= 104
'''

'''
题目要求在 O(n) 的时间复杂度内找到数组中的第 k 个最大元素。

1.  **直接排序**：最直观的方法是对整个数组进行排序，然后返回第 k 个最大的元素。例如，升序排序后，结果是位于索引 `len(nums) - k` 的元素。
标准排序算法（如 Python 内置的 `sort()` 或 `sorted()`）的时间复杂度通常是 O(n log n)，这不满足题目 O(n) 的要求。

2.  **堆（优先队列）**：我们可以使用一个大小为 k 的最小堆。遍历数组，将元素逐个加入堆中。如果堆的大小超过 k，就弹出堆顶（最小）的元素。遍历结束后，堆顶的元素就是我们要求的第 k 个最大元素。
这个方法的时间复杂度是 O(n log k)。当 k 接近 n 时，复杂度也接近 O(n log n)，同样不满足 O(n) 的要求。此外，题目禁止使用 `import`，我们无法导入 `heapq` 模块。

3.  **快速选择算法 (Quickselect)**：这个算法是解决 "选择问题"（在列表中找到第 k 小/大的元素）的经典 O(n) 平均时间复杂度算法。它的思想来源于快速排序，但做了关键的优化。

    *   **快速排序** 的工作方式是：选择一个"枢轴"（pivot）元素，将数组分区，使得所有小于枢轴的元素都在它的一边，所有大于枢轴的元素都在另一边。然后递归地对两边的子数组进行排序。
    *   **快速选择** 的工作方式是：同样选择一个枢轴并进行分区。分区后，枢轴元素就位于其最终排序好的位置上。假设这个位置的索引是 `pivot_index`。我们可以将 `pivot_index` 与我们想找的目标索引（对于第 k 大的元素，目标索引是 `n - k`）进行比较：
        *   如果 `pivot_index` 正好等于 `n - k`，那么我们找到了，枢轴元素就是答案。
        *   如果 `pivot_index` 小于 `n - k`，说明我们想找的元素在枢轴的右边（更大的那部分），我们只需要在右边的子数组中继续寻找。
        *   如果 `pivot_index` 大于 `n - k`，说明我们想找的元素在枢轴的左边（更小的那部分），我们只需要在左边的子数组中继续寻找。

    通过这种方式，我们每次都能排除掉一部分元素，而不需要像快速排序那样对两边都进行递归处理。这使得平均时间复杂度从 O(n log n) 降到了 O(n)。

    *   **时间复杂度**：
        *   **平均情况**: O(n)。每次分区操作是 O(m)（m 为当前子数组大小），而我们期望每次都能将问题规模减半，所以总的计算量是 n + n/2 + n/4 + ... ≈ 2n，即 O(n)。
        *   **最坏情况**: O(n²)。如果我们每次都选到最差的枢轴（比如在已排序数组中总选第一个或最后一个元素），导致每次分区只能排除一个元素。
        在实际应用中，通过随机选择枢轴可以极大地避免最坏情况的发生。由于本题禁止 `import`，我们无法使用 `random` 模块，
        但我们可以采用一个固定的策略（例如选择中间或末尾的元素作为枢轴），这在大多数情况下表现良好。

### 算法设计

我们将实现基于快速选择算法的解决方案。

1.  **主函数 `findKthLargest(nums, k)`**
    *   计算目标索引 `target_index = len(nums) - k`。这是因为我们要找的是第 k **大** 的元素，它等价于升序排序后第 `n-k` **小** 的元素（从0开始计数）。
    *   初始化两个指针 `low` 和 `high`，分别指向数组的开始和结束。
    *   进入一个循环，在 `[low, high]` 范围内执行分区操作。
    *   根据分区后枢轴的最终索引与 `target_index` 的关系，收缩搜索范围 (`low` 或 `high`)，直到找到目标。

2.  **辅助函数 `partition(nums, low, high)`**
    *   这个函数负责对子数组 `nums[low:high+1]`进行分区。
    *   我们选择 `nums[high]` 作为枢轴元素（这是一个简单且常见的策略）。
    *   用一个指针 `i`（从 `low` 开始）来标记小于等于枢轴的区域的右边界。
    *   遍历从 `low` 到 `high-1` 的元素 `j`。如果 `nums[j]` 小于或等于枢轴，就将它与 `nums[i]` 交换，并把 `i` 向右移动一位。
    *   遍历结束后，将枢轴（原来在 `nums[high]`）与 `nums[i]` 交换。这样，枢轴就位于其最终排序位置 `i` 上。
    *   返回枢轴的最终索引 `i`。

### Python 代码实现

```python
class Solution:
    def findKthLargest(self, nums: list[int], k: int) -> int:
        """
        使用快速选择算法找到数组中第 k 个最大的元素。
        时间复杂度: O(n) 平均情况, O(n^2) 最坏情况
        空间复杂度: O(1) (原地修改数组)
        """

        # 数组长度
        n = len(nums)
        # 目标元素的索引（在升序排列的数组中）
        # 第 k 大的元素，相当于第 (n - k) 小的元素 (0-indexed)
        target_index = n - k

        # 初始化搜索区间的左右边界
        low, high = 0, n - 1

        while True:
            # 对当前区间 [low, high] 进行分区，并获取枢轴的最终位置
            pivot_index = self.partition(nums, low, high)

            if pivot_index == target_index:
                # 如果枢轴的位置就是我们的目标位置，我们找到了元素
                return nums[pivot_index]
            elif pivot_index < target_index:
                # 如果枢轴位置在目标左侧，说明目标元素在枢轴的右边
                # 我们需要在右侧子数组中继续寻找
                low = pivot_index + 1
            else: # pivot_index > target_index
                # 如果枢轴位置在目标右侧，说明目标元素在枢轴的左边
                # 我们需要在左侧子数组中继续寻找
                high = pivot_index - 1
    
    def partition(self, nums: list[int], low: int, high: int) -> int:
        """
        分区函数 (Lomuto partition scheme)
        选择 `nums[high]` 作为枢轴，将数组分区，并返回枢轴的最终索引。
        """
        # 选择当前区间的最后一个元素作为枢轴
        pivot = nums[high]
        
        # i 指向小于等于枢轴的区域的下一个位置
        i = low
        
        # 遍历当前区间（不包括枢轴本身）
        for j in range(low, high):
            # 如果当前元素小于或等于枢轴
            if nums[j] <= pivot:
                # 将它交换到 i 的位置
                nums[i], nums[j] = nums[j], nums[i]
                # i 向右移动
                i += 1
        
        # 遍历结束后，i 的位置就是枢轴应该在的位置
        # 将枢轴（原来在 nums[high]）交换到正确的位置
        nums[i], nums[high] = nums[high], nums[i]
        
        # 返回枢轴的最终索引
        return i

# --- 测试用例 ---
solver = Solution()

# 示例 1
nums1 = [3, 2, 1, 5, 6, 4]
k1 = 2
print(f"输入: {nums1}, k = {k1}")
# 预期输出: 5
# 排序后为 [1, 2, 3, 4, 5, 6]，第2大的是 5
output1 = solver.findKthLargest(nums1, k1)
print(f"输出: {output1}")
print("-" * 20)


# 示例 2
nums2 = [3, 2, 3, 1, 2, 4, 5, 5, 6]
k2 = 4
print(f"输入: {nums2}, k = {k2}")
# 预期输出: 4
# 排序后为 [1, 2, 2, 3, 3, 4, 5, 5, 6]，第4大的是 4
output2 = solver.findKthLargest(nums2, k2)
print(f"输出: {output2}")
print("-" * 20)

# 边界情况测试
nums3 = [1]
k3 = 1
print(f"输入: {nums3}, k = {k3}")
output3 = solver.findKthLargest(nums3, k3)
print(f"输出: {output3}")
print("-" * 20)

nums4 = [7, 6, 5, 4, 3, 2, 1]
k4 = 5
print(f"输入: {nums4}, k = {k4}")
output4 = solver.findKthLargest(nums4, k4)
print(f"输出: {output4}")
print("-" * 20)
```
'''

'''
以下是代码
'''
# 使用函数
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        return sorted(nums)[len(nums) - k]

# 常规解法，超出时间限制
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        n = len(nums)
        targetindex= n - k 
        low = 0
        high = n-1

        def partition(nums,high,low):
            pivot = nums[high]
            i = low
            for j in range(low,high):
                if nums[j]<=pivot:
                    nums[i], nums[j] = nums[j], nums[i]
                    i+=1
            nums[i], nums[high] = nums[high], nums[i]
            return i

        while True:
            pivotindex = partition(nums,high,low)
            if pivotindex == targetindex:
                return nums[pivotindex]
            elif pivotindex < targetindex:
                low = pivotindex+1
            else:
                high = pivotindex-1
