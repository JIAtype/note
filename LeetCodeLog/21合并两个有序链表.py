'''
心得体会：

链表名默认指向头节点
'''

'''
题目：
将两个升序链表合并为一个新的 升序 链表并返回。新链表是通过拼接给定的两个链表的所有节点组成的。 

示例 1：
输入：l1 = [1,2,4], l2 = [1,3,4]
输出：[1,1,2,3,4,4]
示例 2：

输入：l1 = [], l2 = []
输出：[]
示例 3：

输入：l1 = [], l2 = [0]
输出：[0]

提示：
两个链表的节点数目范围是 [0, 50]
-100 <= Node.val <= 100
l1 和 l2 均按 非递减顺序 排列
'''

'''
解法：
好的！这个问题是典型的“合并两个升序链表”。可以采用迭代或递归的方法将两个链表合并成一个新的升序链表。

## 方法一：迭代实现
思路：
- 创建一个哑节点（虚拟头节点） `dummy` ，用来方便操作
- 设置两个指针 `l1` 和 `l2`，分别指向两个链表的头
- 比较 `l1` 和 `l2` 当前指向的节点值，将较小的节点链接到合并链表末尾，然后移动对应的指针
- 当某一链表遍历完后，将剩余的链表拼接到新链表后面

【代码实现】：
```python
# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        dummy = ListNode(0)  # 虚拟头节点
        current = dummy

        # 比较两个链表的节点值，逐个连接较小的节点
        while l1 and l2:
            if l1.val <= l2.val:
                current.next = l1
                l1 = l1.next
            else:
                current.next = l2
                l2 = l2.next
            current = current.next

        # 连接未遍历完的链表
        if l1:
            current.next = l1
        elif l2:
            current.next = l2

        return dummy.next
```

## 方法二：递归实现
思路：
- 如果 `l1` 为空，直接返回 `l2`
- 如果 `l2` 为空，直接返回 `l1`
- 比较 `l1.val` 和 `l2.val`：
  - 如果 `l1.val <= l2.val`，那么 `l1` 的节点就加入结果，将 `l1.next` 递归合并剩余部分
  - 反之，将 `l2` 连接到结果，递归合并剩余部分

【代码实现】：
```python
class Solution:
    def mergeTwoLists(self, l1: ListNode, l2: ListNode) -> ListNode:
        if not l1:
            return l2
        if not l2:
            return l1
        
        if l1.val <= l2.val:
            l1.next = self.mergeTwoLists(l1.next, l2)
            return l1
        else:
            l2.next = self.mergeTwoLists(l1, l2.next)
            return l2
```

## 示例
假设：
```python
# 构造链表 l1: [1, 2, 4]
l1 = ListNode(1, ListNode(2, ListNode(4)))

# 构造链表 l2: [1, 3, 4]
l2 = ListNode(1, ListNode(3, ListNode(4)))

sol = Solution()
result = sol.mergeTwoLists(l1, l2)

# 打印结果
curr = result
while curr:
    print(curr.val, end=' ')
# 输出：1 1 2 3 4 4
```

这两种方法都可以高效解决问题，可以根据自己的偏好选择实现方式！
'''

'''
以下是代码
'''

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        cur = dum = ListNode(0)
        while list1 and list2:
            if list1.val < list2.val:
                cur.next = list1
                list1 = list1.next
            else:
                cur.next = list2
                list2 = list2.next
            cur = cur.next
        if list1:
            cur.next = list1
        elif list2:
            cur.next = list2
        return dum.next
    
    # 满分

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        if not list1:
            return list2
        if not list2:
            return list1
        
        if list1.val <= list2.val:
            list1.next = self.mergeTwoLists(list1.next, list2)
            return list1
        else:
            list2.next = self.mergeTwoLists(list1, list2.next)
            return list2