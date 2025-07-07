'''
心得体会：
思路得用代码实现才行
注意递归怎么写
'''

'''
题目：
给你一个整数数组 nums，请你将该数组升序排列。

你必须在 不使用任何内置函数 的情况下解决问题，时间复杂度为 O(nlog(n))，并且空间复杂度尽可能小。

示例 1：

输入：nums = [5,2,3,1]
输出：[1,2,3,5]
解释：数组排序后，某些数字的位置没有改变（例如，2 和 3），而其他数字的位置发生了改变（例如，1 和 5）。
示例 2：

输入：nums = [5,1,1,2,0,0]
输出：[0,0,1,1,2,5]
解释：请注意，nums 的值不一定唯一。
 

提示：

1 <= nums.length <= 5 * 104
-5 * 104 <= nums[i] <= 5 * 104
'''

'''
解法：
快排
'''

'''
以下是代码
'''
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def quicksort(l: int, r: int):
            if l >= r:
                return
            pivot = nums[random.randint(l, r)]
            i, j = l, r
            while i <= j:
                while nums[i] < pivot:
                    i += 1
                while nums[j] > pivot:
                    j -= 1
                if i <= j:
                    nums[i], nums[j] = nums[j], nums[i]
                    i += 1
                    j -= 1
            quicksort(l, j)
            quicksort(i, r)
        
        quicksort(0, len(nums) - 1)
        return nums