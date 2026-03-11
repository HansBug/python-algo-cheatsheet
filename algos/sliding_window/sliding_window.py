"""
Python 滑动窗口模板 - 固定窗口与可变窗口
支持 Python 3.7-3.14

核心原理：
- 用一个连续区间维护当前答案
- 右指针负责扩张，左指针负责收缩
- 每个元素通常最多进窗口一次、出窗口一次，所以总复杂度常是 O(n)
"""


def max_window_sum(nums, k):
    """固定窗口最大和 - O(n)"""
    if not nums or k <= 0 or k > len(nums):
        return 0

    window = sum(nums[:k])
    ans = window

    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        ans = max(ans, window)

    return ans


def min_subarray_len(target, nums):
    """和至少为 target 的最短子数组 - O(n)"""
    left = 0
    s = 0
    ans = len(nums) + 1

    for right, x in enumerate(nums):
        s += x
        while s >= target:
            ans = min(ans, right - left + 1)
            s -= nums[left]
            left += 1

    return ans if ans <= len(nums) else 0


def length_of_longest_substring(s):
    """无重复字符的最长子串 - O(n)"""
    last = {}
    left = 0
    ans = 0

    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        ans = max(ans, right - left + 1)

    return ans


if __name__ == '__main__':
    print("=" * 60)
    print("Python 滑动窗口模板完整示例")
    print("=" * 60)

    print("\n【1. 固定窗口最大和】")
    print(max_window_sum([1, 4, 2, 10, 23, 3, 1, 0, 20], 4))

    print("\n【2. 和至少为 target 的最短子数组】")
    print(min_subarray_len(7, [2, 3, 1, 2, 4, 3]))

    print("\n【3. 无重复字符的最长子串】")
    print(length_of_longest_substring("abcabcbb"))

    print("\n【4. 实战提醒】")
    print("✓ 连续子数组 / 子串优先想窗口")
    print("✓ 固定长度窗口常用加一个减一个")
    print("✓ 可变窗口常写成 right 扩、left 缩")
    print("✗ 窗口题别忘了维护答案更新时机")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
