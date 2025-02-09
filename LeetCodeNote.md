    - 数组array
        - 概念
            
            具有相同类型的若干元素
            
            按有序的形式组织起来的一种形式。
            
            作为线性表的实现方式之一，在内存中是 **连续** 存储的，且每个元素占相同大小的内存。
            
            数组通过 **索引** 快速访问每个元素的值。在大多数编程语言中，索引从 0 算起。
            
            C++ 和 Java 中，数组中的元素类型必须保持一致，而 Python 中则可以不同。相比之下，Python 中的数组（称为 list）具有更多的高级功能。
            
        - 283.移动零
            
            给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。
            
            请注意 ，必须在不复制数组的情况下原地对数组进行操作。
            
            ```python
            class Solution(object):
                def moveZeroes(self, nums):
                    """
                    :type nums: List[int]
                    :rtype: None Do not return anything, modify nums in-place instead.
                    """
                    j=0
                    for i in range(0,len(nums)):
                        if nums[i]:
                            nums[j],nums[i]=nums[i],nums[j]
                            j+=1
                        
            ```
            
            ```python
            class Solution(object):
                def moveZeroes(self, nums):
                    """
                    :type nums: List[int]
                    :rtype: None Do not return anything, modify nums in-place instead.
                    """
                    i=0
                    for num in nums:
                        if num != 0 :
                            nums[i]=num
                            i+=1
                    for j in range(i, len(nums)):
                        nums[j] = 0
                    return nums
            ```
            
        - 27.**移除元素**
            
            给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素。元素的顺序可能发生改变。然后返回 nums 中与 val 不同的元素的数量。
            
            假设 nums 中不等于 val 的元素数量为 k，要通过此题，您需要执行以下操作：
            
            更改 nums 数组，使 nums 的前 k 个元素包含不等于 val 的元素。nums 的其余元素和 nums 的大小并不重要。
            返回 k。
            
            ```python
            class Solution(object):
                def removeElement(self, nums, val):
                    """
                    :type nums: List[int]
                    :type val: int
                    :rtype: int
                    """
                    i=0
                    for num in nums:
                        if num != val:
                            nums[i]=num
                            i+=1
                    return i
            ```
            
        - **26.删除排序数组中的重复项**
            
            给你一个 非严格递增排列 的数组 nums ，请你 原地 删除重复出现的元素，使每个元素 只出现一次 ，返回删除后数组的新长度。元素的 相对顺序 应该保持 一致 。然后返回 nums 中唯一元素的个数。
            
            考虑 nums 的唯一元素的数量为 k ，你需要做以下事情确保你的题解可以被通过：
            
            更改数组 nums ，使 nums 的前 k 个元素包含唯一元素，并按照它们最初在 nums 中出现的顺序排列。nums 的其余元素与 nums 的大小不重要。
            返回 k 。
            
            ```python
            class Solution(object):
                def removeDuplicates(self, nums):
                    """
                    :type nums: List[int]
                    :rtype: int
                    """
                    i=1
                    for j in range(1,len(nums)):
                        if nums[j]!=nums[i-1]:
                            nums[i]=nums[j]
                            i+=1
                    return i
            ```
            
        - **80.删除排序数组中的重复项 II**
            
            给你一个有序数组 nums ，请你 原地 删除重复出现的元素，使得出现次数超过两次的元素只出现两次 ，返回删除后数组的新长度。
            
            不要使用额外的数组空间，你必须在 原地 修改输入数组 并在使用 O(1) 额外空间的条件下完成。
            
            ```python
            class Solution:
                def removeDuplicates(self, nums):
                    # 如果数组为空或者长度小于等于2，直接返回
                    if len(nums) <= 2:
                        return len(nums)
                    
                    # 指针j用于标记修改后的数组位置
                    j = 2  # 从第三个元素开始，因为前两个元素是可以保留的
                    
                    for i in range(2, len(nums)):
                        # 如果当前元素不等于 nums[j-2]，说明这个元素是合法的，可以保留
                        if nums[i] != nums[j-2]:
                            nums[j] = nums[i]
                            j += 1
                            
                    # 返回新的数组长度
                    return j
            ```
            
            ```python
            class Solution:
                def removeDuplicates(self, nums):
                    if len(nums) <= 2:
                        return len(nums)
                    
                    # j 是新数组的末尾，初始时为2，因为前两个元素是可以保留的
                    j = 2
                    count = 1  # 从第二个元素开始计数
                    
                    for i in range(2, len(nums)):
                        if nums[i] == nums[i - 1]:
                            count += 1  # 当前元素和前一个元素相同，增加计数
                        else:
                            count = 1  # 当前元素和前一个元素不同，重置计数器
            
                        # 如果 count <= 2，就把元素放到新的位置
                        if count <= 2:
                            nums[j] = nums[i]
                            j += 1  # 移动 j 指针
            
                    return j  # 返回新数组的长度
            ```
            
            由于是保留 k 个相同数字，对于前 k 个数字，我们可以直接保留
            对于后面的任意数字，能够保留的前提是：与当前写入的位置前面的第 k 个元素进行比较，不相同则保留
            
        - **双索引技巧 - 滑动窗口**
            
            定义好滑动窗口，明确边界和初始值非常重要。
            
        - 75.颜色分类
            
            给定一个包含红色、白色和蓝色、共 n 个元素的数组 nums ，原地 对它们进行排序，使得相同颜色的元素相邻，并按照红色、白色、蓝色顺序排列。
            
            我们使用整数 0、 1 和 2 分别表示红色、白色和蓝色。
            
            必须在不使用库内置的 sort 函数的情况下解决这个问题。
            
            **荷兰国旗问题** 的经典变种，目标是将数组中的元素分成三个不同的部分，且按照顺序排列。
            
            题解详细说明[https://leetcode.cn/problems/sort-colors/solutions/437968/yan-se-fen-lei-by-leetcode-solution](https://leetcode.cn/problems/sort-colors/solutions/437968/yan-se-fen-lei-by-leetcode-solution)
            
            ```python
            class Solution(object):
                def sortColors(self, nums):
                    """
                    :type nums: List[int]
                    :rtype: None Do not return anything, modify nums in-place instead.
                    """
                    n=len(nums)-1
                    r=n
                    l=0
                    i=0
                    while i<=r:
                        if nums[i]==0:
                            nums[l],nums[i]=nums[i],nums[l]
                            l+=1
                            i+=1
                        elif nums[i]==2:
                            nums[r],nums[i]=nums[i],nums[r]
                            r-=1
                        else:
                            i+=1
                    return nums      
            ```
            
            ```python
            class Solution:
                def sortColors(self, nums: List[int]) -> None:
                    n = len(nums)
                    ptr = 0
                    for i in range(n):
                        if nums[i] == 0:
                            nums[i], nums[ptr] = nums[ptr], nums[i]
                            ptr += 1
                    for i in range(ptr, n):
                        if nums[i] == 1:
                            nums[i], nums[ptr] = nums[ptr], nums[i]
                            ptr += 1
            ```
            
            ```python
            class Solution:
                def sortColors(self, nums: List[int]) -> None:
                    n = len(nums)
                    p0 = p1 = 0
                    for i in range(n):
                        if nums[i] == 1:
                            nums[i], nums[p1] = nums[p1], nums[i]
                            p1 += 1
                        elif nums[i] == 0:
                            nums[i], nums[p0] = nums[p0], nums[i]
                            if p0 < p1:
                                nums[i], nums[p1] = nums[p1], nums[i]
                            p0 += 1
                            p1 += 1
            ```
            
        - 数组中的第K个最大元素
            
            给定整数数组 nums 和整数 k，请返回数组中第 k 个最大的元素。
            
            请注意，你需要找的是数组排序后的第 k 个最大的元素，而不是第 k 个不同的元素。
            
            你必须设计并实现时间复杂度为 O(n) 的算法解决此问题。
            
            ```python
            class Solution(object):
                def findKthLargest(self, nums, k):
                    """
                    :type nums: List[int]
                    :type k: int
                    :rtype: int
                    """
                    nums.sort()  # 先排序
                    return nums[-k]  # 取倒数第k个元素
            ```
            
            ```python
            class Solution:
                # 采用快速排序方法，分成的数列左边大于右边
                def findKthLargest(self, nums, k):
                    n = len(nums)
                    if (k > n):
                        return
                    index = self.quickSort(nums, 0, n-1, k)
                    return nums[index]
                #快速排序的递归
                def quickSort(self, nums, l, r, k):
                    if l >= r:
                        return l
                    p = self.partition(nums, l, r)
                    if p + 1 == k:
                        return p
                    if p + 1 > k:
                        return self.quickSort(nums, l, p -1, k)
                    else:
                        return self.quickSort(nums, p + 1, r, k)
                #划分区间函数
                def partition(self, nums, l, r):
                    v = nums[l]
                    j = l
                    i = l + 1
                    while i <= r:
                        if nums[i] >= v:
                            nums[j+1],nums[i] = nums[i],nums[j+1]
                            j += 1
                        i += 1
                    nums[l], nums[j] = nums[j], nums[l]
                    return j
            ```
            
        - **合并两个有序数组**
            
            给你两个按 非递减顺序 排列的整数数组 nums1 和 nums2，另有两个整数 m 和 n ，分别表示 nums1 和 nums2 中的元素数目。
            
            请你 合并 nums2 到 nums1 中，使合并后的数组同样按 非递减顺序 排列。
            
            注意：最终，合并后数组不应由函数返回，而是存储在数组 nums1 中。为了应对这种情况，nums1 的初始长度为 m + n，其中前 m 个元素表示应合并的元素，后 n 个元素为 0 ，应忽略。nums2 的长度为 n 。
            
            ```python
            class Solution(object):
                def merge(self, nums1, m, nums2, n):
                    """
                    :type nums1: List[int]
                    :type m: int
                    :type nums2: List[int]
                    :type n: int
                    :rtype: None
                    """
                    # 初始化指针
                    i, j, k = m - 1, n - 1, m + n - 1
            
                    # 从后向前遍历 nums1 和 nums2
                    while i >= 0 and j >= 0:
                        if nums1[i] > nums2[j]:
                            nums1[k] = nums1[i]
                            i -= 1
                        else:
                            nums1[k] = nums2[j]
                            j -= 1
                        k -= 1
            
                    # 如果 nums2 中还有剩余元素，直接复制到 nums1 中
                    while j >= 0:
                        nums1[k] = nums2[j]
                        j -= 1
                        k -= 1
            ```
            
        - 
    
