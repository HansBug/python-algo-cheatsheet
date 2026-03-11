"""
Python 贪心模板 - 每步做当前最优选择
支持 Python 3.7-3.14

核心原理：
- 贪心不是固定模板，而是“局部最优推动全局最优”的思路
- 常见信号：要求最少步数、最多数量、最小代价、能否完成
- 真正的难点是证明选择策略，而不是代码本身
"""


def can_jump(nums):
    """跳跃游戏 - O(n)"""
    farthest = 0
    for i, step in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + step)
    return True


def jump(nums):
    """跳跃游戏 II，最少跳跃次数 - O(n)"""
    steps = 0
    end = 0
    farthest = 0

    for i in range(len(nums) - 1):
        farthest = max(farthest, i + nums[i])
        if i == end:
            steps += 1
            end = farthest

    return steps


def max_non_overlapping(intervals):
    """最多选择多少个互不重叠区间 - O(n log n)"""
    intervals = sorted(intervals, key=lambda x: x[1])
    ans = 0
    end = float('-inf')

    for left, right in intervals:
        if left >= end:
            ans += 1
            end = right

    return ans


if __name__ == '__main__':
    print("=" * 60)
    print("Python 贪心模板完整示例")
    print("=" * 60)

    print("\n【1. 是否能跳到终点】")
    print(can_jump([2, 3, 1, 1, 4]))
    print(can_jump([3, 2, 1, 0, 4]))

    print("\n【2. 最少跳跃次数】")
    print(jump([2, 3, 1, 1, 4]))

    print("\n【3. 最多不重叠区间】")
    print(max_non_overlapping([[1, 2], [2, 3], [3, 4], [1, 3]]))

    print("\n【4. 实战提醒】")
    print("✓ 贪心题先想每一步该选谁")
    print("✓ 区间选择题常按右端点排序")
    print("✓ 能否到达 / 最少步数这类题常能线性扫")
    print("✗ 没证明前别把搜索题硬写成贪心")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
