"""
Python 前缀和模板 - 一维前缀和与哈希计数
支持 Python 3.7-3.14

核心原理：
- 前缀和把区间和查询从 O(n) 降到 O(1)
- `pre[i]` 表示前 i 个元素的和，区间 [l, r] 的和是 `pre[r + 1] - pre[l]`
- 如果题目变成“子数组和满足条件”，通常要把前缀和和哈希表一起用
"""


def build_prefix(nums):
    """构建前缀和 - O(n)"""
    pre = [0]
    for x in nums:
        pre.append(pre[-1] + x)
    return pre


def range_sum(pre, left, right):
    """查询闭区间 [left, right] 的和 - O(1)"""
    return pre[right + 1] - pre[left]


def subarray_sum_equals_k(nums, k):
    """和为 k 的子数组个数 - O(n)"""
    cnt = {0: 1}
    s = 0
    ans = 0

    for x in nums:
        s += x
        ans += cnt.get(s - k, 0)
        cnt[s] = cnt.get(s, 0) + 1

    return ans


def longest_equal_zero_one(nums):
    """0 和 1 数量相同的最长子数组 - O(n)"""
    first = {0: -1}
    s = 0
    ans = 0

    for i, x in enumerate(nums):
        s += 1 if x == 1 else -1
        if s in first:
            ans = max(ans, i - first[s])
        else:
            first[s] = i

    return ans


if __name__ == '__main__':
    print("=" * 60)
    print("Python 前缀和模板完整示例")
    print("=" * 60)

    nums = [2, 1, 3, 4, 5]
    pre = build_prefix(nums)

    print("\n【1. 构建前缀和】")
    print(pre)

    print("\n【2. 区间和查询】")
    print("sum(nums[1:4]) =", range_sum(pre, 1, 3))

    print("\n【3. 和为 k 的子数组个数】")
    print(subarray_sum_equals_k([1, 1, 1], 2))

    print("\n【4. 0/1 数量相同的最长子数组】")
    print(longest_equal_zero_one([0, 1, 0, 1, 1, 0, 0]))

    print("\n【5. 实战提醒】")
    print("✓ 一维前缀和通常多开一位 0")
    print("✓ 子数组计数题常用 前缀和 + 哈希表")
    print("✓ 闭区间 [l, r] 统一写 pre[r + 1] - pre[l]")
    print("✗ 别把前缀和值和原数组索引混掉")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
