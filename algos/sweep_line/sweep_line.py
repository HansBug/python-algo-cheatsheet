"""
Python 扫描线模板 - 把区间问题转成事件排序
支持 Python 3.7-3.14

核心原理：
- 把“进入区间”和“离开区间”拆成事件
- 按坐标顺序扫描，维护当前活跃状态
- 常用于最大重叠数、区间并长度、会议室数量这类题
"""


def max_overlap(intervals):
    """求半开区间 [l, r) 的最大重叠数 - O(n log n)"""
    events = []
    for left, right in intervals:
        events.append((left, 1))
        events.append((right, -1))

    events.sort(key=lambda x: (x[0], x[1]))

    cur = 0
    ans = 0
    for _, delta in events:
        cur += delta
        ans = max(ans, cur)

    return ans


def union_length(intervals):
    """求半开区间 [l, r) 的并长度 - O(n log n)"""
    events = []
    for left, right in intervals:
        if left < right:
            events.append((left, 1))
            events.append((right, -1))

    if not events:
        return 0

    events.sort()
    total = 0
    cur = 0
    prev = events[0][0]

    for x, delta in events:
        if cur > 0:
            total += x - prev
        cur += delta
        prev = x

    return total


def min_meeting_rooms(intervals):
    """最少会议室数量 - O(n log n)"""
    starts = sorted(left for left, _ in intervals)
    ends = sorted(right for _, right in intervals)

    ans = 0
    rooms = 0
    j = 0

    for start in starts:
        while j < len(ends) and ends[j] <= start:
            rooms -= 1
            j += 1
        rooms += 1
        ans = max(ans, rooms)

    return ans


if __name__ == '__main__':
    print("=" * 60)
    print("Python 扫描线模板完整示例")
    print("=" * 60)

    print("\n【1. 最大重叠数】")
    print(max_overlap([(1, 4), (2, 5), (3, 6), (7, 9)]))

    print("\n【2. 区间并长度】")
    print(union_length([(1, 4), (2, 6), (8, 10), (9, 12)]))

    print("\n【3. 最少会议室数量】")
    print(min_meeting_rooms([(0, 30), (5, 10), (15, 20)]))

    print("\n【4. 实战提醒】")
    print("✓ 扫描线先把问题改写成事件")
    print("✓ 排序时要想清楚同点先入还是先出")
    print("✓ 区间覆盖长度通常配合活跃计数")
    print("✗ 边界没统一时最容易错")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
