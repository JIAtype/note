'''
心得体会：

'''

'''
题目：
692. 前K个高频单词
中等

给定一个单词列表 words 和一个整数 k ，返回前 k 个出现次数最多的单词。

返回的答案应该按单词出现频率由高到低排序。如果不同的单词有相同出现频率， 按字典顺序 排序。

示例 1：

输入: words = ["i", "love", "leetcode", "i", "love", "coding"], k = 2
输出: ["i", "love"]
解析: "i" 和 "love" 为出现次数最多的两个单词，均为2次。
    注意，按字母顺序 "i" 在 "love" 之前。
示例 2：

输入: ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], k = 4
输出: ["the", "is", "sunny", "day"]
解析: "the", "is", "sunny" 和 "day" 是出现次数最多的四个单词，
    出现次数依次为 4, 3, 2 和 1 次。

注意：
1 <= words.length <= 500
1 <= words[i] <= 10
words[i] 由小写英文字母组成。
k 的取值范围是 [1, 不同 words[i] 的数量]

进阶：尝试以 O(n log k) 时间复杂度和 O(n) 空间复杂度解决。
'''

'''
解法：

'''

'''
以下是代码
'''

# 使用哈希表
class Solution:
    def topKFrequent(self, words: List[str], k: int) -> List[str]:
        
        hash = collections.Counter(words)
        # 使用 collections.Counter 来创建一个计数器对象 hash，它会统计 words 列表中每个单词的出现频率。 
        # Counter 是 collections 模块中的一个类，能够快速地计算可哈希对象的出现次数。
        res = sorted(hash, key=lambda word:(-hash[word], word))
        # key=lambda word:(-hash[word], word) 是一个排序键，表示按照单词的出现频率
        # （使用 -hash[word] 除以负号进行降序排序）以及字母顺序（word 本身进行排序）。
        # 即，如果两个单词的频率相同，它们会按字母序排列。
        return res[:k]
        # 返回结果 res 的前 k 个元素。这就是出现频率最高的前 k 个单词。

# 使用堆
def topKFrequent(self, words: List[str], k: int) -> List[str]:
    freq = {}
    # 这行代码创建一个空字典 `freq`，用于存储每个单词及其对应的出现频率。
    for str in words:
        freq[str] = freq.get(str, 0) + 1
# - 这段代码遍历 `words` 列表中的每个单词。
# - 对于每个单词 `str`，使用 `freq.get(str, 0)` 获取该单词的当前频率（如果该单词不在字典中，则返回默认值 `0`），然后将其增加 `1`，并将更新后的值存回字典 `freq` 中。
# - 这样，循环结束后，字典 `freq` 中存储了每个单词及其对应的频率。

    return heapq.nlargest(k, freq, key = lambda x: (freq.get(x), x))
# - 这行代码使用堆 `heapq.nlargest()` 函数来找出频率最高的前 `k` 个单词。
# - `heapq.nlargest()` 是 Python 的 `heapq` 模块中的一个函数，用于找到 iterable 中的前 `n` 个最大值。
# - 在这个主要行中，`freq` 字典作为输入，其中 `key=lambda x: (freq.get(x), x)` 指定了排序的依据。
#   - `freq.get(x)` 获取单词的频率，用于排序。
#   - `x` 用于在频率相同时，按字母顺序排序。
# - 因此，该行代码最终返回出现频率最高的 `k` 个单词，这些单词在频率相同的情况下按字母顺序排列。
