'''
心得体会：
ListNode(0, head)创建一个新的链表节点（节点值为0），并将它的 next 指针指向现有的链表头节点 head。
双指针
'''

'''
题目：
给你一个链表，删除链表的倒数第 n 个结点，并且返回链表的头结点。

示例 1：
输入：head = [1,2,3,4,5], n = 2
输出：[1,2,3,5]
示例 2：
输入：head = [1], n = 1
输出：[]
示例 3：
输入：head = [1,2], n = 1
输出：[1]

提示：

链表中结点的数目为 sz
1 <= sz <= 30
0 <= Node.val <= 100
1 <= n <= sz

进阶：你能尝试使用一趟扫描实现吗？
'''

'''
解法：
这是一道经典的“删除链表的倒数第 n 个节点”问题。可以用双指针（快慢指针）实现一趟扫描，避免多次遍历。

## 思路
- 使用两个指针 `fast` 和 `slow`，初始都指向链表头。
- 先让 `fast` 向前移动 `n` 步，确保 `fast` 和 `slow` 之间相隔 `n`。
- 接着同时移动 `fast` 和 `slow`，直到 `fast` 到达链表末尾。
- 此时，`slow` 正好指向待删除节点的前驱，调整指针跳过待删除节点即可。

## 具体实现

```python
# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        dummy = ListNode(0, head)  # 虚拟头节点，方便删除头部
        fast = slow = dummy
        # fast 先向前移动 n+1 步（确保 slow 指向待删除节点的前一个）
        for _ in range(n + 1):
            fast = fast.next
        # 两指针同时移动，直到 fast 到达末尾
        while fast:
            fast = fast.next
            slow = slow.next
        # 删除倒数第 n 个节点
        slow.next = slow.next.next
        return dummy.next
```

## 说明
- 使用虚拟节点 `dummy` 避免头部特殊处理。
- 只用一遍扫描（一次遍历）即可完成操作。

## 示例演示
假设链表为 `[1, 2, 3, 4, 5]`，删除倒数第 2 个节点：

```python
# 构造链表
nodes = [ListNode(i) for i in [1, 2, 3, 4, 5]]
for i in range(4):
    nodes[i].next = nodes[i + 1]
head = nodes[0]

sol = Solution()
new_head = sol.removeNthFromEnd(head, 2)

# 输出删除后的链表
curr = new_head
while curr:
    print(curr.val, end=' ')
# 结果：1 2 3 5
```

---

这是一个经典且高效的解法，符合一趟扫描的进阶要求！
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
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        newhead = ListNode(0, head)
        fast = slow = newhead
        for i in range(n + 1):
            fast = fast.next
        while fast:
            fast = fast.next
            slow = slow.next
        slow.next=slow.next.next
        return newhead.next