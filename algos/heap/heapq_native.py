"""
Python 堆（Heap）模板 - 基于 heapq

heapq 默认是最小堆，通过 tuple 技巧实现最大堆和自定义堆
支持 Python 3.7+，无需第三方依赖

核心原理：
- heapq 实现的是二叉最小堆（binary min-heap）
- 堆是一个完全二叉树，满足父节点 <= 子节点
- 使用数组存储，索引 i 的节点，其左子节点为 2*i+1，右子节点为 2*i+2
- 堆顶元素（最小值）始终在索引 0 位置
"""

import heapq


if __name__ == '__main__':
    print("=" * 60)
    print("Python heapq 堆操作完整示例")
    print("=" * 60)

    # ============ 1. 最小堆基本操作 ============
    print("\n【1. 最小堆基本操作】")
    print("-" * 60)

    # heappush: 插入元素，时间复杂度 O(log n)
    # 原理：将元素添加到数组末尾，然后向上调整（sift up）维护堆性质
    heap = []
    heapq.heappush(heap, 3)
    heapq.heappush(heap, 1)
    heapq.heappush(heap, 2)
    print(f"插入 3, 1, 2 后的堆: {heap}")  # 预期: [1, 3, 2]

    # heappop: 弹出最小值，时间复杂度 O(log n)
    # 原理：取出堆顶，将末尾元素移到堆顶，然后向下调整（sift down）
    min_val = heapq.heappop(heap)
    print(f"弹出最小值: {min_val}")  # 预期: 1
    print(f"弹出后的堆: {heap}")  # 预期: [2, 3]

    # 查看堆顶（不弹出），时间复杂度 O(1)
    top = heap[0]
    print(f"当前堆顶: {top}")  # 预期: 2

    # heapify: 从列表建堆，时间复杂度 O(n)
    # 原理：从最后一个非叶子节点开始，依次向下调整，比逐个插入更高效
    nums = [3, 1, 4, 1, 5]
    heapq.heapify(nums)
    print(f"从 [3, 1, 4, 1, 5] 建堆: {nums}")  # 预期: [1, 1, 4, 3, 5]

    # ============ 2. 最大堆实现 ============
    print("\n【2. 最大堆实现】")
    print("-" * 60)

    # 方法1: 存储负数，时间复杂度与最小堆相同
    # 优点：简单直接；缺点：只适用于数值类型
    max_heap = []
    for val in [3, 1, 5, 2]:
        heapq.heappush(max_heap, -val)
    print(f"方法1 - 存储负数: {max_heap}")  # 预期: [-5, -2, -3, -1]
    max_val = -heapq.heappop(max_heap)
    print(f"弹出最大值: {max_val}")  # 预期: 5

    # 方法2: 存储 (-x, x) 元组（推荐）
    # 优点：保留原始值，便于调试；缺点：占用更多内存
    max_heap = []
    for val in [3, 1, 5, 2]:
        heapq.heappush(max_heap, (-val, val))
    print(f"方法2 - 存储元组: {max_heap}")  # 预期: [(-5, 5), (-2, 2), (-3, 3), (-1, 1)]
    _, max_val = heapq.heappop(max_heap)
    print(f"弹出最大值: {max_val}")  # 预期: 5

    # ============ 3. 自定义优先级堆 ============
    print("\n【3. 自定义优先级堆】")
    print("-" * 60)

    # 示例1: 按绝对值排序
    # 原理：tuple 比较时，先比较第一个元素，相同则比较第二个...
    # 格式: (优先级, 数据)
    heap = []
    for x in [3, -5, 2, -1]:
        heapq.heappush(heap, (abs(x), x))
    print(f"按绝对值排序的堆: {heap}")  # 预期: [(1, -1), (2, 2), (3, 3), (5, -5)]
    _, val = heapq.heappop(heap)
    print(f"弹出绝对值最小的: {val}")  # 预期: -1

    # 示例2: 多关键字排序（先按距离，再按坐标）
    heap = []
    points = [(1, 2), (3, 0), (0, 1)]
    for x, y in points:
        dist = x * x + y * y
        heapq.heappush(heap, (dist, x, y))
    print(f"按距离排序的点: {heap}")  # 预期: [(1, 0, 1), (5, 1, 2), (9, 3, 0)]
    dist, x, y = heapq.heappop(heap)
    print(f"最近的点: ({x}, {y}), 距离: {dist}")  # 预期: (0, 1), 距离: 1

    # ============ 4. Non-comparable Object 处理技巧 ============
    print("\n【4. Non-comparable Object 处理技巧】")
    print("-" * 60)
    print("问题：当优先级相同时，tuple 会比较下一个元素")
    print("如果下一个元素是 list/dict/自定义对象，会报错 TypeError")
    print("解决：在优先级和对象之间插入唯一的 int（如入堆顺序）")
    print()

    # 错误示例（注释掉避免报错）
    # heap = []
    # heapq.heappush(heap, (1, [1, 2]))
    # heapq.heappush(heap, (1, [3, 4]))  # TypeError: '<' not supported between list

    # 正确做法：插入唯一计数器
    heap = []
    counter = 0
    tasks = [
        (1, {"name": "task_a", "data": [1, 2]}),
        (1, {"name": "task_b", "data": [3, 4]}),  # 优先级相同
        (2, {"name": "task_c", "data": [5, 6]}),
    ]

    for priority, task in tasks:
        # 格式: (优先级, 唯一计数器, 对象)
        # 计数器确保即使优先级相同，也不会比较对象
        heapq.heappush(heap, (priority, counter, task))
        counter += 1

    print("入堆顺序: task_a(优先级1), task_b(优先级1), task_c(优先级2)")
    print(f"堆中元素数量: {len(heap)}")  # 预期: 3

    # 弹出元素
    priority, _, task = heapq.heappop(heap)
    print(f"弹出: {task['name']}, 优先级: {priority}")  # 预期: task_a, 优先级: 1

    priority, _, task = heapq.heappop(heap)
    print(f"弹出: {task['name']}, 优先级: {priority}")  # 预期: task_b, 优先级: 1

    priority, _, task = heapq.heappop(heap)
    print(f"弹出: {task['name']}, 优先级: {priority}")  # 预期: task_c, 优先级: 2

    # ============ 5. 常用操作汇总 ============
    print("\n【5. 常用操作时间复杂度汇总】")
    print("-" * 60)
    print("heappush(heap, item)      - O(log n) - 插入元素")
    print("heappop(heap)             - O(log n) - 弹出最小值")
    print("heap[0]                   - O(1)     - 查看堆顶")
    print("heapify(list)             - O(n)     - 从列表建堆")
    print("heappushpop(heap, item)   - O(log n) - 先插入再弹出")
    print("heapreplace(heap, item)   - O(log n) - 先弹出再插入")
    print("nlargest(k, iterable)     - O(n log k) - 返回最大的 k 个元素（列表）")
    print("nsmallest(k, iterable)    - O(n log k) - 返回最小的 k 个元素（列表）")

    # ============ 6. 实战技巧 ============
    print("\n【6. 实战技巧】")
    print("-" * 60)
    print("✓ 最大堆：存储 (-priority, data) 或 -value")
    print("✓ 自定义排序：使用 (priority, data) 元组")
    print("✓ 避免对象比较：使用 (priority, counter, object)")
    print("✓ 多关键字：使用 (key1, key2, key3, data)")
    print("✓ 堆排序：heapify + 反复 heappop，总复杂度 O(n log n)")
    print("✓ Top K 问题：维护大小为 K 的堆，复杂度 O(n log k)")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
