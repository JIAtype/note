'''
心得体会：

'''

'''
题目：
给你单链表的头节点 head ，请你反转链表，并返回反转后的链表。
 
示例 1：

输入：head = [1,2,3,4,5]
输出：[5,4,3,2,1]
示例 2：

输入：head = [1,2]
输出：[2,1]
示例 3：

输入：head = []
输出：[]
 
提示：

链表中节点的数目范围是 [0, 5000]
-5000 <= Node.val <= 5000
 
进阶：链表可以选用迭代或递归方式完成反转。你能否用两种方法解决这道题？
'''

'''
解法：
当然可以！这是经典的反转链表问题，可以使用**迭代方法**和**递归方法**分别实现。

---

## 方法一：迭代

思路：
- 使用三个指针：`prev`（前一个节点），`curr`（当前节点），`next_node`（下一个节点）
- 遍历链表：
  - 暂存`curr`的下一个节点到`next_node`
  - 将`curr.next`指向`prev`
  - 向后移动`prev`和`curr`
- 最终`prev`即为反转链表的头节点

【代码实现】：
```python
# 定义链表节点
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev = None
        curr = head
        while curr:
            next_node = curr.next  # 暂存下一节点
            curr.next = prev       # 反转指针
            prev = curr            # 前移prev
            curr = next_node       # 继续遍历
        return prev
```

---

## 方法二：递归

思路：
- 递归地反转子链表，只需处理`head.next`
- 最底层返回头节点，然后逐层反转

【代码实现】：
```python
class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head or not head.next:
            return head
        new_head = self.reverseList(head.next)
        head.next.next = head
        head.next = None
        return new_head
```

---

## 测试示例
假设链表为 `[1, 2, 3, 4, 5]`，可构造链表并测试：

```python
# 构造链表
nodes = [ListNode(i) for i in range(1, 6)]
for i in range(4):
    nodes[i].next = nodes[i+1]
head = nodes[0]

# 迭代反转
sol = Solution()
reversed_head_iter = sol.reverseList(head)
# 打印反转后链表
curr = reversed_head_iter
while curr:
    print(curr.val, end=' ')
    curr = curr.next
# 输出: 5 4 3 2 1

# 递归反转
# 需要重新构造链表，因为前面被反转过
head = nodes[0]
reversed_head_rec = sol.reverseList(head)
curr = reversed_head_rec
while curr:
    print(curr.val, end=' ')
    curr = curr.next
# 输出: 1 2 3 4 5
```

---

## 总结：
两种方法都可以实现链表的反转，迭代方式更直观，递归方式则简洁优雅，实际选用看个人偏好和平衡考虑。
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
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr:
            nextnode = curr.next
            curr.next = prev
            prev = curr
            curr = nextnode
        return prev