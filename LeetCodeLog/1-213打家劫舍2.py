'''
动态规划
根据约束条件设定边界
然后设置符合要求的状态转移方程

利用list的index直接读数据
注意for循环（i，j）的范围是从i到j-1
正数第一个是[0]
倒数第一个是[-1]
'''

'''
题目：
你是一个专业的小偷，计划偷窃沿街的房屋，每间房内都藏有一定的现金。这个地方所有的房屋都 围成一圈 ，这意味着第一个房屋和最后一个房屋是紧挨着的。同时，相邻的房屋装有相互连通的防盗系统，如果两间相邻的房屋在同一晚上被小偷闯入，系统会自动报警 。

给定一个代表每个房屋存放金额的非负整数数组，计算你 在不触动警报装置的情况下 ，今晚能够偷窃到的最高金额。

示例 1：

输入：nums = [2,3,2]
输出：3
解释：你不能先偷窃 1 号房屋（金额 = 2），然后偷窃 3 号房屋（金额 = 2）, 因为他们是相邻的。
示例 2：

输入：nums = [1,2,3,1]
输出：4
解释：你可以先偷窃 1 号房屋（金额 = 1），然后偷窃 3 号房屋（金额 = 3）。
     偷窃到的最高金额 = 1 + 3 = 4 。
示例 3：

输入：nums = [1,2,3]
输出：3
 

提示：

1 <= nums.length <= 100
0 <= nums[i] <= 1000
'''

'''
解法：
### 问题背景
你面临的是一个名为“打家劫舍 II”的问题，描述如下：

- 有一个环形的房屋群，每个房屋都有一个金额。
- 你可以偷窃这些房屋，但不能同时窃取相邻两个房屋。
- 你需要找到不触动防盗系统的情况下，可以窃取到的最高金额。

### 解决方案
为了解决这个问题，我们可以分成两个子问题：

1. **不包括第一个房屋**：计算从第二个房屋开始到最后一个房屋的最大金额。
2. **不包括最后一个房屋**：计算从第一个房屋开始到倒数第二个房屋的最大金额。

然后，我们从这两种情况中选择较大的一个作为答案。

### 详细推演

#### Step 1: 初始化状态

假设我们有一个房屋列表 `nums`，我们定义两个动态规划数组：

- `dp_exclude_first`：用于存放不包括第一个房屋时，可以得到的最高金额。
- `dp_exclude_last`：用于存放不包括最后一个房屋时，可以得到的最高金额。

#### Step 2: 状态转移方程

1. **不包括第一个房屋**

   - 如果不包括第一个房屋，当前位置的最大金额可以来自两种情况：
     - **情况 1**：不包含当前位置房屋时的最大金额，即 `dp_exclude_first[i-1]`。
     - **情况 2**：包含当前位置房屋时的最大金额，即 `dp_exclude_first[i-2] + nums[i]`。

   - 最终，我们选择这两种情况中的最大值，即 `max(dp_exclude_first[i-1], dp_exclude_first[i-2] + nums[i])`。

2. **不包括最后一个房屋**

   - 如果不包括最后一个房屋，当前位置的最大金额可以来自两种情况：
     - **情况 1**：不包含当前位置房屋时的最大金额，即 `dp_exclude_last[i-1]`。
     - **情况 2**：包含当前位置房屋时的最大金额，即 `dp_exclude_last[i-2] + nums[-i-1]`。注意这里是倒数第二个元素。

   - 最终，我们选择这两种情况中的最大值，即 `max(dp_exclude_last[i-1], dp_exclude_last[i-2] + nums[-i-1])`。

#### Step 3: 初始化和循环

1. **初始化状态**

   ```python
   dp_exclude_first =  * len(nums)#存储不包括第一个房屋，当前位置的最大金额
   dp_exclude_last =  * len(nums)#存储不包括最后一个房屋，当前位置的最大金额
   dp_exclude_first[1] = nums[1]#正数第二个元素
   dp_exclude_last[1] = nums[-2]#倒数第二个元素
   ```

2. **循环计算**

   ```python
   for i in range(2, len(nums)):
       dp_exclude_first[i] = max(dp_exclude_first[i-1], dp_exclude_first[i-2] + nums[i])
   for i in range(2, len(nums)):
       dp_exclude_last[i] = max(dp_exclude_last[i-1], dp_exclude_last[i-2] + nums[-i-1])
   ```

#### Step 4: 返回结果

最终，我们返回这两种情况中的最大值，即：

```python
return max(dp_exclude_first[-1], dp_exclude_last[-1])
```

### 示例推演

假设我们有一个房屋列表 `nums = [2, 7, 9, 3, 1]`。

1. **不包括第一个房屋**
   - `dp_exclude_first` 初始化：
     ```python
     dp_exclude_first = [0, 7, 10, 13]
     ```
   - 循环计算：
     ```python
     dp_exclude_first[3] = max(dp_exclude_first[2], dp_exclude_first[1] + nums[3]) = max(10, 10 + 3) = max(10,13) =13
     dp_exclude_first[4] = max(dp_exclude_first[3], dp_exclude_first[2] + nums[4])= max(13,10+1)=max(13,11)=13
     ```
   
2. **不包括最后一个房屋**

   - `dp_exclude_last` 初始化：
     ```python
     dp_exclude_last=[0,3,10,13]
     ```
   - 循环计算：
     ```python
     dp_exclude_last[3]=max(dp_exclude_last[2],dp_exclude_last[1]+nums[-3])=max(10,10+9)=max(10,19)=19
     dp_exclude_last[4]=max(dp_exclude_last[3],dp_exclude_last[2]+nums[-4])=max(19,10+7)=max(19,17)=19
     ```
   
3. **返回结果**

最终，我们返回这两种情况中的最大值，即：

```python
return max(dp_exclude_first[-1], dp_exclude_last[-1])=max(13,19)=19
```

因此，在这个例子中，最高的不触动防盗系统的情况下，可以窃取到的金额是 `19`。

通过这种方式，我们可以有效地解决涉及多个状态和决策结果的复杂问题。
'''

'''
以下是代码
'''

class Solution:
    def rob(self, nums: List[int]) -> int:
        # 如果没有房屋，直接返回 0
        if not nums:
            return 0

        # 如果只有一个房屋，直接返回这个房屋的金额
        if len(nums) == 1:
            return nums[0]

        # 不包括第一个房屋的最大金额
        n = len(nums)
        dp_exclude_first = [0] * n
        dp_exclude_first[1] = nums[1]
        
        for i in range(2, len(nums)):
            dp_exclude_first[i] = max(dp_exclude_first[i-1], dp_exclude_first[i-2] + nums[i])

        # 不包括最后一个房屋的最大金额
        dp_exclude_last = [0] * len(nums)
        dp_exclude_last[1] = nums[-2]
        
        for i in range(2, len(nums)):
            dp_exclude_last[i] = max(dp_exclude_last[i-1], dp_exclude_last[i-2] + nums[-i-1])

        # 返回两种情况中的最大值
        return max(dp_exclude_first[-1], dp_exclude_last[-1])
        