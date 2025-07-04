'''
心得体会：
巧用python
'''

'''
题目：
在一条单行道上，有 n 辆车开往同一目的地。目的地是几英里以外的 target 。

给定两个整数数组 position 和 speed ，长度都是 n ，其中 position[i] 是第 i 辆车的位置， speed[i] 是第 i 辆车的速度(单位是英里/小时)。

一辆车永远不会超过前面的另一辆车，但它可以追上去，并以较慢车的速度在另一辆车旁边行驶。

车队 是指并排行驶的一辆或几辆汽车。车队的速度是车队中 最慢 的车的速度。

即便一辆车在 target 才赶上了一个车队，它们仍然会被视作是同一个车队。

返回到达目的地的车队数量 。

示例 1：

输入：target = 12, position = [10,8,0,5,3], speed = [2,4,1,1,3]

输出：3

解释：

从 10（速度为 2）和 8（速度为 4）开始的车会组成一个车队，它们在 12 相遇。车队在 target 形成。
从 0（速度为 1）开始的车不会追上其它任何车，所以它自己是一个车队。
从 5（速度为 1） 和 3（速度为 3）开始的车组成一个车队，在 6 相遇。车队以速度 1 移动直到它到达 target。
示例 2：

输入：target = 10, position = [3], speed = [3]

输出：1

解释：

只有一辆车，因此只有一个车队。
示例 3：

输入：target = 100, position = [0,2,4], speed = [4,2,1]

输出：1

解释：

从 0（速度为 4） 和 2（速度为 2）开始的车组成一个车队，在 4 相遇。从 4 开始的车（速度为 1）移动到了 5。
然后，在 4（速度为 2）的车队和在 5（速度为 1）的车成为一个车队，在 6 相遇。车队以速度 1 移动直到它到达 target。

提示：

n == position.length == speed.length
1 <= n <= 105
0 < target <= 106
0 <= position[i] < target
position 中每个值都 不同
0 < speed[i] <= 106
'''

'''
解法：
如果一辆车到目标的时间大于或等于前一辆车的时间，则它会追上前车或组成车队。
如果当前车辆到目标的时间 <= 前面车辆到目标的时间，那么它会追上前面的车，成为同一车队。
否则，它自己形成一个新的车队。

首先对这些车辆按照它们的起始位置降序排序
用 (target - position) / speed 计算出每辆车在不受其余车的影响时，行驶到终点需要的时间。

'''

'''
以下是代码
'''
class Solution:
    def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
        n = len(position)
        if n <= 1:
            return n
        # 将车辆按位置降序排序（离目标更近的车辆先处理）
        # 必须加reverse，如果不加，position=0的项开始，maxt一开始就会是最大的，结果始终返回1
        cars = sorted(zip(position, speed), reverse=True)
        # 计算每辆车到目标的时间
        times = [(target - p) / s for p, s in cars]
        fleet_count = 0
        max_time = 0
        for t in times:
            if t > max_time:
                fleet_count += 1
                max_time = t
        return fleet_count