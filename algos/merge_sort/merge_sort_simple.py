"""
Python 归并排序（Merge Sort）模板 - 手写递归版本

推荐写法：
- 用递归拆分区间
- 用一个全局辅助数组反复 merge
- 这是最接近面试现场手写的标准版本

支持 Python 3.7-3.14，无第三方依赖
"""


def merge_sort(nums):
    """归并排序 - O(n log n)，额外空间 O(n)"""
    if len(nums) <= 1:
        return nums

    tmp = [0] * len(nums)

    def sort(l, r):
        if l >= r:
            return

        m = (l + r) // 2
        sort(l, m)
        sort(m + 1, r)

        i, j, k = l, m + 1, l
        while i <= m and j <= r:
            if nums[i] <= nums[j]:
                tmp[k] = nums[i]
                i += 1
            else:
                tmp[k] = nums[j]
                j += 1
            k += 1

        while i <= m:
            tmp[k] = nums[i]
            i += 1
            k += 1

        while j <= r:
            tmp[k] = nums[j]
            j += 1
            k += 1

        nums[l:r + 1] = tmp[l:r + 1]

    sort(0, len(nums) - 1)
    return nums


def count_inversions(nums):
    """统计逆序对数量 - O(n log n)"""
    if len(nums) <= 1:
        return 0

    arr = nums[:]
    tmp = [0] * len(arr)
    cnt = 0

    def sort(l, r):
        nonlocal cnt
        if l >= r:
            return

        m = (l + r) // 2
        sort(l, m)
        sort(m + 1, r)

        i, j, k = l, m + 1, l
        while i <= m and j <= r:
            if arr[i] <= arr[j]:
                tmp[k] = arr[i]
                i += 1
            else:
                tmp[k] = arr[j]
                cnt += m - i + 1
                j += 1
            k += 1

        while i <= m:
            tmp[k] = arr[i]
            i += 1
            k += 1

        while j <= r:
            tmp[k] = arr[j]
            j += 1
            k += 1

        arr[l:r + 1] = tmp[l:r + 1]

    sort(0, len(arr) - 1)
    return cnt


if __name__ == '__main__':
    print("=" * 60)
    print("Python 归并排序模板完整示例")
    print("=" * 60)

    print("\n【1. 普通归并排序】")
    print("-" * 60)
    nums = [5, 1, 1, 2, 0, 0]
    print(f"排序前: {nums}")
    merge_sort(nums)
    print(f"排序后: {nums}")

    print("\n【2. 包含负数和重复值】")
    print("-" * 60)
    nums = [3, -1, 4, -1, 5, 0, 2]
    print(f"排序前: {nums}")
    merge_sort(nums)
    print(f"排序后: {nums}")

    print("\n【3. 逆序对数量】")
    print("-" * 60)
    nums = [7, 5, 6, 4]
    print(f"{nums} -> {count_inversions(nums)}")  # 5

    print("\n【4. 时间复杂度】")
    print("-" * 60)
    print("merge sort - O(n log n)")
    print("extra space - O(n)")

    print("\n【5. 实战提醒】")
    print("-" * 60)
    print("✓ merge 时先比左右两边当前值")
    print("✓ 剩余元素记得补尾巴")
    print("✓ tmp 提前开一次复用")
    print("✓ 逆序对题优先想归并")
    print("✗ 不要每层递归都重新开辅助数组")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
