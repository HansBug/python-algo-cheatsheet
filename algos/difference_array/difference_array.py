"""
Python 差分模板 - 批量区间加减
支持 Python 3.7-3.14

核心原理：
- `diff[i]` 记录当前位置相对前一个位置的变化量
- 区间 [l, r] 加上 val，只需要做 `diff[l] += val`、`diff[r + 1] -= val`
- 最后跑一遍前缀和就能还原原数组
"""


def range_add(length, updates):
    """批量区间加法 - O(n + m)"""
    diff = [0] * (length + 1)

    for left, right, val in updates:
        diff[left] += val
        if right + 1 < length:
            diff[right + 1] -= val

    ans = [0] * length
    cur = 0
    for i in range(length):
        cur += diff[i]
        ans[i] = cur

    return ans


def corp_flight_bookings(bookings, n):
    """航班预订统计 - O(n + m)"""
    updates = []
    for first, last, seats in bookings:
        updates.append((first - 1, last - 1, seats))
    return range_add(n, updates)


def car_pooling(trips, capacity):
    """拼车是否超载 - O(max_position + n)"""
    if not trips:
        return True

    max_pos = 0
    for _, _, to in trips:
        max_pos = max(max_pos, to)

    diff = [0] * (max_pos + 1)
    for num, start, end in trips:
        diff[start] += num
        if end < len(diff):
            diff[end] -= num

    cur = 0
    for x in diff:
        cur += x
        if cur > capacity:
            return False

    return True


if __name__ == '__main__':
    print("=" * 60)
    print("Python 差分模板完整示例")
    print("=" * 60)

    print("\n【1. 批量区间加法】")
    print(range_add(5, [(1, 3, 2), (2, 4, 3), (0, 2, -2)]))

    print("\n【2. 航班预订统计】")
    print(corp_flight_bookings([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5))

    print("\n【3. 拼车】")
    print(car_pooling([[2, 1, 5], [3, 3, 7]], 4))
    print(car_pooling([[2, 1, 5], [3, 3, 7]], 5))

    print("\n【4. 实战提醒】")
    print("✓ 多次区间加减优先想差分")
    print("✓ 最后一定要还原一次前缀和")
    print("✓ 区间定义要先统一成闭区间还是左闭右开")
    print("✗ 别每次更新都真的去改整段")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
