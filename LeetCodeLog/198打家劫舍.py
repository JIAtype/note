'''
心得体会：

'''

'''
题目：
你是一个专业的小偷，计划偷窃沿街的房屋。每间房内都藏有一定的现金，影响你偷窃的唯一制约因素就是相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警。

给定一个代表每个房屋存放金额的非负整数数组，计算你 不触动警报装置的情况下 ，一夜之内能够偷窃到的最高金额。

示例 1：

输入：[1,2,3,1]
输出：4
解释：偷窃 1 号房屋 (金额 = 1) ，然后偷窃 3 号房屋 (金额 = 3)。
     偷窃到的最高金额 = 1 + 3 = 4 。
示例 2：

输入：[2,7,9,3,1]
输出：12
解释：偷窃 1 号房屋 (金额 = 2), 偷窃 3 号房屋 (金额 = 9)，接着偷窃 5 号房屋 (金额 = 1)。
     偷窃到的最高金额 = 2 + 9 + 1 = 12 。

提示：

1 <= nums.length <= 100
0 <= nums[i] <= 400
'''

'''
解法：


'''

'''
以下是代码
'''
class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0]*(n+1)
        dp[0]=0
        dp[1]=nums[0]
        for i in range(2,n+1):
            dp[i]=max(dp[i-1],nums[i-1]+dp[i-2])
        return dp[n]
    
# 空间复杂度也最低
class Solution:
    def rob(self, nums: List[int]) -> int:
        prev = 0
        curr = 0
        for i in nums:
            prev, curr = curr, max(curr, prev + i)
            #所有的赋值操作都是同时进行的，而不是按顺序逐行执行的。
            # 相当于以下代码
'''
            # 假设 curr 和 prev 最初的值已被初始化
            temp_curr = curr  # 保存当前的 curr 的值，以便之后更新 prev

            # 计算新的 curr 的值
            new_curr = max(temp_curr, prev + i)  # 使用 temp_curr 以确保 prev 的值不受影响

            # 更新 prev 和 curr
            prev = temp_curr  # 更新 prev 为之前的 curr
            curr = new_curr    # 更新 curr 为新计算出的值
'''
        return curr