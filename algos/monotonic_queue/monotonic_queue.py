"""
Python 单调队列（Monotonic Queue）模板 - 基于 collections.deque

推荐写法：
- 用 deque 当双端队列
- 队列里优先存索引，方便判断元素是否过期
- 每个元素最多进队一次、出队一次，所以总复杂度通常是 O(n)

支持 Python 3.7-3.14，无第三方依赖

核心原理：
- 单调递减队列常用来维护窗口最大值
- 单调递增队列常用来维护窗口最小值
- 题目一旦带“窗口”和“最值”，优先想它
"""

from collections import deque


def max_sliding_window(nums, k):
    """滑动窗口最大值 - O(n)"""
    if not nums or k <= 0:
        return []

    ans = []
    dq = deque()  # 单调递减队列，存索引

    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i + 1 >= k:
            ans.append(nums[dq[0]])

    return ans


def min_sliding_window(nums, k):
    """滑动窗口最小值 - O(n)"""
    if not nums or k <= 0:
        return []

    ans = []
    dq = deque()  # 单调递增队列，存索引

    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        if i + 1 >= k:
            ans.append(nums[dq[0]])

    return ans


def shortest_subarray_at_least_k(nums, k):
    """最短子数组和至少为 k - O(n)"""
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)

    ans = len(nums) + 1
    dq = deque()  # 保持 prefix[dq] 单调递增

    for i, s in enumerate(prefix):
        while dq and s - prefix[dq[0]] >= k:
            ans = min(ans, i - dq.popleft())
        while dq and prefix[dq[-1]] >= s:
            dq.pop()
        dq.append(i)

    return ans if ans <= len(nums) else -1


def constrained_subset_sum(nums, k):
    """受限子序列和最大值 - O(n)"""
    if not nums:
        return 0

    dp = [0] * len(nums)
    dq = deque()  # 保持 dp[dq] 单调递减

    for i, x in enumerate(nums):
        while dq and dq[0] < i - k:
            dq.popleft()
        best = dp[dq[0]] if dq else 0
        dp[i] = x + max(0, best)
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    return max(dp)


if __name__ == '__main__':
    print("=" * 60)
    print("Python 单调队列模板完整示例")
    print("=" * 60)

    print("\n【1. 滑动窗口最大值】")
    print("-" * 60)
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    print(f"{nums}, k=3 -> {max_sliding_window(nums, 3)}")

    print("\n【2. 滑动窗口最小值】")
    print("-" * 60)
    nums = [4, 2, 12, 3, -1, 6]
    print(f"{nums}, k=2 -> {min_sliding_window(nums, 2)}")

    print("\n【3. 最短子数组和至少为 K】")
    print("-" * 60)
    nums = [2, -1, 2]
    print(f"{nums}, k=3 -> {shortest_subarray_at_least_k(nums, 3)}")  # 3

    print("\n【4. 区间 DP 最大值优化】")
    print("-" * 60)
    nums = [10, 2, -10, 5, 20]
    print(f"{nums}, k=2 -> {constrained_subset_sum(nums, 2)}")  # 37

    print("\n【5. 时间复杂度】")
    print("-" * 60)
    print("push / expire - O(1) 摊还")
    print("peek          - O(1)")
    print("单次扫描        - O(n)")

    print("\n【6. 实战提醒】")
    print("-" * 60)
    print("✓ 单调队列优先存索引")
    print("✓ 先踢过期元素，再维护单调性")
    print("✓ 最大值看递减队列，最小值看递增队列")
    print("✓ 前缀和题和 DP 优化也常能套它")
    print("✗ 不要把它误当成普通双指针模板")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
