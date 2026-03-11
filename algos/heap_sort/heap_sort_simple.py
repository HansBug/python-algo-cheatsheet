"""
Python 堆排序（Heap Sort）模板 - 手写原地版本

推荐写法：
- 用最大堆做升序排序
- 核心是 sift_down
- 先建堆，再不断把堆顶交换到末尾

支持 Python 3.7-3.14，无第三方依赖
"""


def heap_sort(nums):
    """堆排序 - O(n log n)，额外空间 O(1)"""
    n = len(nums)

    def sift_down(i, end):
        while True:
            best = i
            left = 2 * i + 1
            right = left + 1

            if left < end and nums[left] > nums[best]:
                best = left
            if right < end and nums[right] > nums[best]:
                best = right
            if best == i:
                return

            nums[i], nums[best] = nums[best], nums[i]
            i = best

    for i in range((n - 2) // 2, -1, -1):
        sift_down(i, n)

    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)

    return nums


if __name__ == '__main__':
    print("=" * 60)
    print("Python 堆排序模板完整示例")
    print("=" * 60)

    print("\n【1. 原地堆排序】")
    print("-" * 60)
    nums = [5, 1, 1, 2, 0, 0]
    print(f"排序前: {nums}")
    heap_sort(nums)
    print(f"排序后: {nums}")

    print("\n【2. 包含负数和重复值】")
    print("-" * 60)
    nums = [3, -1, 4, -1, 5, 0, 2]
    print(f"排序前: {nums}")
    heap_sort(nums)
    print(f"排序后: {nums}")

    print("\n【3. 时间复杂度】")
    print("-" * 60)
    print("build heap - O(n)")
    print("heap sort  - O(n log n)")
    print("extra space - O(1)")

    print("\n【4. 实战提醒】")
    print("-" * 60)
    print("✓ 先建最大堆")
    print("✓ 再把堆顶换到数组末尾")
    print("✓ sift_down 是核心")
    print("✓ end 表示当前堆的右边界开区间")
    print("✗ 不要把 heapq 当成手写堆排序答案")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
