"""
Python 区间合并模板 - 排序后线性扫描
支持 Python 3.7-3.14

核心原理：
- 先按左端点排序
- 当前区间能接上就合并，接不上就开新区间
- 这类题的关键通常不是数据结构，而是先统一区间顺序
"""


def merge_intervals(intervals):
    """合并重叠区间 - O(n log n)"""
    if not intervals:
        return []

    intervals = sorted(intervals)
    ans = [intervals[0][:]]

    for left, right in intervals[1:]:
        if left <= ans[-1][1]:
            ans[-1][1] = max(ans[-1][1], right)
        else:
            ans.append([left, right])

    return ans


def insert_interval(intervals, new_interval):
    """插入并合并新区间 - O(n) 到 O(n log n)"""
    return merge_intervals(intervals + [new_interval])


def erase_overlap_intervals(intervals):
    """最少删除多少区间才能不重叠 - O(n log n)"""
    if not intervals:
        return 0

    intervals = sorted(intervals, key=lambda x: x[1])
    keep = 1
    end = intervals[0][1]

    for left, right in intervals[1:]:
        if left >= end:
            keep += 1
            end = right

    return len(intervals) - keep


if __name__ == '__main__':
    print("=" * 60)
    print("Python 区间合并模板完整示例")
    print("=" * 60)

    print("\n【1. 合并重叠区间】")
    print(merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]))

    print("\n【2. 插入新区间】")
    print(insert_interval([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 9]))

    print("\n【3. 最少删除区间数】")
    print(erase_overlap_intervals([[1, 2], [2, 3], [3, 4], [1, 3]]))

    print("\n【4. 实战提醒】")
    print("✓ 区间题先问自己要不要排序")
    print("✓ 合并题通常按左端点排")
    print("✓ 选最多不重叠区间通常按右端点排")
    print("✗ 别在未排序状态下直接扫")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
