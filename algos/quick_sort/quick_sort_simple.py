"""
Python 快速排序（Quick Sort）模板 - 手写原地版本

推荐写法：
- 用 Lomuto partition，逻辑最短，最适合现场手写
- pivot 固定取右端点，先把基础版写对
- 如果面试官继续追问，再补随机 pivot 或三路快排

支持 Python 3.7-3.14，无第三方依赖

核心原理：
- 选一个 pivot
- 把 <= pivot 的元素放到左边
- 把 pivot 放回正确位置
- 递归排序左右两边
"""


def quick_sort(nums, l=0, r=None):
    """原地快速排序 - 平均 O(n log n)，最坏 O(n^2)"""
    if r is None:
        r = len(nums) - 1
    if l >= r:
        return nums

    pivot = nums[r]
    i = l  # 下一个 <= pivot 的元素该放的位置

    for j in range(l, r):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1

    nums[i], nums[r] = nums[r], nums[i]
    quick_sort(nums, l, i - 1)
    quick_sort(nums, i + 1, r)
    return nums


def partition(nums, l, r):
    """Lomuto partition - O(n)"""
    pivot = nums[r]
    i = l

    for j in range(l, r):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1

    nums[i], nums[r] = nums[r], nums[i]
    return i


def quick_select(nums, k):
    """找第 k 小元素（k 从 0 开始） - 平均 O(n)"""
    l, r = 0, len(nums) - 1

    while l <= r:
        p = partition(nums, l, r)
        if p == k:
            return nums[p]
        if p < k:
            l = p + 1
        else:
            r = p - 1

    raise IndexError("k out of range")


if __name__ == '__main__':
    print("=" * 60)
    print("Python 快速排序模板完整示例")
    print("=" * 60)

    print("\n【1. 原地快排】")
    print("-" * 60)
    nums = [5, 1, 1, 2, 0, 0]
    print(f"排序前: {nums}")
    quick_sort(nums)
    print(f"排序后: {nums}")  # [0, 0, 1, 1, 2, 5]

    print("\n【2. 包含负数和重复值】")
    print("-" * 60)
    nums = [3, -1, 4, -1, 5, 0, 2]
    print(f"排序前: {nums}")
    quick_sort(nums)
    print(f"排序后: {nums}")

    print("\n【3. partition 演示】")
    print("-" * 60)
    nums = [4, 2, 7, 1, 3]
    p = partition(nums, 0, len(nums) - 1)
    print(f"partition 后: {nums}, pivot 位置: {p}")

    print("\n【4. quick select】")
    print("-" * 60)
    nums = [7, 2, 1, 8, 6, 3, 5, 4]
    k = 3
    ans = quick_select(nums[:], k)
    print(f"第 {k + 1} 小元素: {ans}")  # 4

    print("\n【5. 时间复杂度】")
    print("-" * 60)
    print("partition   - O(n)")
    print("quick sort  - 平均 O(n log n), 最坏 O(n^2)")
    print("quick select - 平均 O(n)")

    print("\n【6. 实战提醒】")
    print("-" * 60)
    print("✓ 先写递归边界 if l >= r")
    print("✓ 先把 Lomuto 基础版写对")
    print("✓ i 表示下一个小元素该放的位置")
    print("✓ 题目只要结果时优先用 sorted")
    print("✗ 不要把 Python 内置排序说成快排")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
