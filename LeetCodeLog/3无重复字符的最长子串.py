'''
哈希表
滑动窗口算法
字符串
双指针

根据条件调整左右边界的设定值
字典可以直接查找字符位置
'''

'''
题目：
给定一个字符串 s ，请你找出其中不含有重复字符的 最长 子串 的长度。

示例 1:
输入: s = "abcabcbb"
输出: 3 
解释: 因为无重复字符的最长子串是 "abc"，所以其长度为 3。
示例 2:
输入: s = "bbbbb"
输出: 1
解释: 因为无重复字符的最长子串是 "b"，所以其长度为 1。
示例 3:
输入: s = "pwwkew"
输出: 3
解释: 因为无重复字符的最长子串是 "wke"，所以其长度为 3。
     请注意，你的答案必须是 子串 的长度，"pwke" 是一个子序列，不是子串。
提示：
0 <= s.length <= 5 * 104
s 由英文字母、数字、符号和空格组成
'''

'''
解法：

为了解决 "无重复字符的最长子串" 问题，可以使用滑动窗口算法，这种方法非常高效。以下是详细步骤：

### 步骤 1：理解问题

给定一个字符串 `s`, 需要找出其中不含有重复字符的最长子串的长度。

### 步骤 2：选择方法

最有效的方法是使用滑动窗口算法。这种方法通过维护一个字典（哈希表）来跟踪每个字符的最后一次出现位置。

### 步骤 3：初始化变量

- `char_index_map`: 用于存储每个字符的最后一次出现位置的字典。
- `max_length`: 用于存储目前发现的最长无重复字符子串的长度。
- `left`: 滑动窗口的左边界指针。
- `right`: 滑动窗口的右边界指针。
- `start_index`: 用于记录最长无重复字符子串的开始位置。

通过使用滑动窗口算法并维护一个字典来跟踪每个字符的最后一次出现位置，这种方法可以在 O(n) 时间复杂度内解决问题，非常高效且有效。

'''


'''
以下是代码
'''

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        charindex={}
        maxlen=0
        left=0
        startindex=0

        for right in range(len(s)):
            if s[right] in charindex and charindex[s[right]]>=left:
                left=charindex[s[right]]+1
            charindex[s[right]]=right

            if right-left+1 > maxlen:
                maxlen=right-left+1
                startindex=left
        return maxlen