"""
Python 离散化模板 - 把稀疏大坐标压成紧凑小坐标
支持 Python 3.7-3.14

核心原理：
- 原始值很大、很稀疏时，直接开数组会浪费空间
- 先排序去重，再把每个值映射成排名
- 常和前缀和、差分、树状数组、线段树一起出现
"""


def compress_values(nums):
    """离散化一组值 - O(n log n)"""
    xs = sorted(set(nums))
    rank = {x: i for i, x in enumerate(xs)}
    return [rank[x] for x in nums], xs, rank


def rank_transform(nums):
    """数组排名映射 - O(n log n)"""
    compressed, _, _ = compress_values(nums)
    return [x + 1 for x in compressed]


def compress_segments(segments):
    """为区间类题目做离散化，额外保留右端点后一位 - O(n log n)"""
    xs = []
    for left, right in segments:
        xs.append(left)
        xs.append(right + 1)

    xs = sorted(set(xs))
    rank = {x: i for i, x in enumerate(xs)}
    mapped = [(rank[left], rank[right + 1]) for left, right in segments]
    return mapped, xs, rank


if __name__ == '__main__':
    print("=" * 60)
    print("Python 离散化模板完整示例")
    print("=" * 60)

    nums = [1000000000, -5, 1000000000, 7, 42]
    compressed, xs, rank = compress_values(nums)

    print("\n【1. 值离散化】")
    print("compressed =", compressed)
    print("xs =", xs)
    print("rank =", rank)

    print("\n【2. 排名映射】")
    print(rank_transform([40, 10, 20, 30, 20]))

    print("\n【3. 区间离散化】")
    print(compress_segments([(1, 10), (5, 20), (100, 1000)]))

    print("\n【4. 实战提醒】")
    print("✓ 值域很大但元素很少时优先想离散化")
    print("✓ 需要还原原值时保留 xs 数组")
    print("✓ 区间差分常要把 right + 1 一起离散化")
    print("✗ 别把原值大小关系映射错")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
