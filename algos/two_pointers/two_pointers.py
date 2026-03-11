"""
Python 双指针模板 - 同向双指针与相向双指针
支持 Python 3.7-3.14

核心原理：
- 两个指针按规则移动，避免重复枚举
- 常见写法有相向夹逼、同向滑动、快慢指针
- 很多本来 O(n^2) 的题可以降到 O(n) 或 O(n log n)
"""


def two_sum_sorted(nums, target):
    """有序数组两数之和 - O(n)"""
    left, right = 0, len(nums) - 1

    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return [left, right]
        if s < target:
            left += 1
        else:
            right -= 1

    return []


def remove_duplicates(nums):
    """原地去重，返回新长度 - O(n)"""
    if not nums:
        return 0

    write = 1
    for read in range(1, len(nums)):
        if nums[read] != nums[write - 1]:
            nums[write] = nums[read]
            write += 1

    return write


def move_zeroes(nums):
    """原地把 0 移到末尾 - O(n)"""
    write = 0

    for x in nums:
        if x != 0:
            nums[write] = x
            write += 1

    while write < len(nums):
        nums[write] = 0
        write += 1


def max_area(height):
    """盛最多水的容器 - O(n)"""
    left, right = 0, len(height) - 1
    ans = 0

    while left < right:
        ans = max(ans, (right - left) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return ans


if __name__ == '__main__':
    print("=" * 60)
    print("Python 双指针模板完整示例")
    print("=" * 60)

    print("\n【1. 有序数组两数之和】")
    print(two_sum_sorted([1, 2, 4, 6, 10], 8))

    print("\n【2. 原地去重】")
    nums = [1, 1, 2, 2, 3, 3, 3, 4]
    n = remove_duplicates(nums)
    print(nums[:n])

    print("\n【3. 移动零】")
    nums = [0, 1, 0, 3, 12]
    move_zeroes(nums)
    print(nums)

    print("\n【4. 盛最多水的容器】")
    print(max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]))

    print("\n【5. 实战提醒】")
    print("✓ 有序数组优先想相向双指针")
    print("✓ 原地覆盖题优先想快慢指针")
    print("✓ 指针移动必须有单调依据")
    print("✗ 不要把能 O(n) 的题写成双重循环")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
