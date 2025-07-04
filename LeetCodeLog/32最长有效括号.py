'''
心得体会：

'''

'''
题目：
32. 最长有效括号
给你一个只包含 '(' 和 ')' 的字符串，找出最长有效（格式正确且连续）括号子串的长度。

示例 1：

输入：s = "(()"
输出：2
解释：最长有效括号子串是 "()"
示例 2：

输入：s = ")()())"
输出：4
解释：最长有效括号子串是 "()()"
示例 3：

输入：s = ""
输出：0

提示：

0 <= s.length <= 3 * 104
s[i] 为 '(' 或 ')'
'''

'''
解法：
两个关键点。
1.匹配成功，这个用栈来实现。为了给第2步做准备，我们要在匹配成功时做个记号，这里开辟一个数组，匹配成功时，在'('和")'的索引位置处记为1。
2.最长连续，然后统计数组里面连续1的个数，最长的那个就是结果

'''

'''
以下是代码
'''
class Solution:
    def longestValidParentheses(self, s: str) -> int:
        stack=[]
        maxl=0
        n=len(s)
        tmp=[0]*n
        cur=0

        for i in range(n):
            if s[i]=='(':
                stack.append(i)
            else:
                if stack:
                    j=stack.pop()
                    tmp[i],tmp[j]=1,1
        for num in tmp:
            if num:
                cur+=1
            else:
                maxl=max(cur,maxl)
                cur=0
        maxl=max(cur,maxl)

        return maxl