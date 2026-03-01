"""
Python 堆（Heap）手动实现 - 不使用 heapq

手动实现最小堆，通过 tuple 实现自定义排序
适合笔试场景，代码简洁易记忆
支持 Python 3.7+，无需第三方依赖

核心原理：
- 堆是完全二叉树，使用数组存储
- 索引 i 的节点：左子节点 2*i+1，右子节点 2*i+2，父节点 (i-1)//2
- 最小堆：父节点 <= 子节点
- 最大堆：通过存储 (-x, x) 或 -x 实现
"""


class Heap:
    """
    最小堆实现

    时间复杂度：
    - push: O(log n)
    - pop: O(log n)
    - peek: O(1)
    - heapify: O(n)
    """

    def __init__(self, items=None):
        """
        初始化堆

        参数：
        - items: 可选的初始元素列表，会自动建堆
        """
        self.heap = []
        if items:
            self.heap = items[:]
            self._heapify()

    def _sift_up(self, idx):
        """
        向上调整（上浮）- O(log n)
        用于插入元素后维护堆性质

        原理：将元素与父节点比较，如果违反堆性质则交换，重复直到根节点
        """
        while idx > 0:
            parent = (idx - 1) // 2
            if self.heap[idx] < self.heap[parent]:
                self.heap[idx], self.heap[parent] = self.heap[parent], self.heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx):
        """
        向下调整（下沉）- O(log n)
        用于删除堆顶后维护堆性质

        原理：将元素与子节点比较，选择更小的子节点交换，重复直到叶子节点
        """
        n = len(self.heap)
        while True:
            smallest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            # 找出父节点和两个子节点中最小的
            if left < n and self.heap[left] < self.heap[smallest]:
                smallest = left
            if right < n and self.heap[right] < self.heap[smallest]:
                smallest = right

            # 如果父节点已经是最小的，停止
            if smallest == idx:
                break

            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            idx = smallest

    def _heapify(self):
        """
        从数组建堆 - O(n)

        原理：从最后一个非叶子节点开始，依次向下调整
        比逐个插入 O(n log n) 更高效
        """
        n = len(self.heap)
        # 最后一个非叶子节点的索引是 (n-1-1)//2 = (n-2)//2
        for i in range((n - 2) // 2, -1, -1):
            self._sift_down(i)

    def push(self, item):
        """插入元素 - O(log n)"""
        self.heap.append(item)
        self._sift_up(len(self.heap) - 1)

    def pop(self):
        """弹出堆顶元素 - O(log n)"""
        if not self.heap:
            raise IndexError("pop from empty heap")

        # 将最后一个元素移到堆顶，然后向下调整
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        item = self.heap.pop()

        if self.heap:
            self._sift_down(0)

        return item

    def peek(self):
        """查看堆顶元素（不弹出）- O(1)"""
        if not self.heap:
            raise IndexError("peek from empty heap")
        return self.heap[0]

    def __len__(self):
        """返回堆的大小 - O(1)"""
        return len(self.heap)

    def __bool__(self):
        """判断堆是否为空 - O(1)"""
        return len(self.heap) > 0

    def __repr__(self):
        """返回堆的字符串表示（可方便调试用）"""
        return f"Heap({self.heap})"


if __name__ == '__main__':
    print("=" * 60)
    print("Python 手动堆实现完整示例")
    print("=" * 60)

    # ============ 1. 最小堆基本操作 ============
    print("\n【1. 最小堆基本操作】")
    print("-" * 60)

    # 创建空的最小堆
    min_heap = Heap()

    # push: 插入元素，时间复杂度 O(log n)
    # 原理：将元素添加到数组末尾，然后向上调整（sift up）维护堆性质
    min_heap.push(3)
    min_heap.push(1)
    min_heap.push(2)
    print(f"插入 3, 1, 2 后的堆: {min_heap.heap}")  # 预期: [1, 3, 2]

    # peek: 查看堆顶（不弹出），时间复杂度 O(1)
    top = min_heap.peek()
    print(f"当前堆顶: {top}")  # 预期: 1

    # pop: 弹出最小值，时间复杂度 O(log n)
    # 原理：取出堆顶，将末尾元素移到堆顶，然后向下调整（sift down）
    min_val = min_heap.pop()
    print(f"弹出最小值: {min_val}")  # 预期: 1
    print(f"弹出后的堆: {min_heap.heap}")  # 预期: [2, 3]

    # 从列表建堆，时间复杂度 O(n)
    # 原理：从最后一个非叶子节点开始，依次向下调整，比逐个插入更高效
    nums = [3, 1, 4, 1, 5]
    min_heap = Heap(items=nums)
    print(f"从 [3, 1, 4, 1, 5] 建堆: {min_heap.heap}")  # 预期: [1, 1, 4, 3, 5]

    # ============ 2. 最大堆实现（使用 tuple） ============
    print("\n【2. 最大堆实现（使用 tuple）】")
    print("-" * 60)

    # 方法1: 存储负数
    # 优点：简单直接；缺点：只适用于数值类型
    max_heap = Heap()
    for val in [3, 1, 5, 2]:
        max_heap.push(-val)
    print(f"方法1 - 存储负数: {max_heap.heap}")  # 预期: [-5, -2, -3, -1]
    max_val = -max_heap.pop()
    print(f"弹出最大值: {max_val}")  # 预期: 5

    # 方法2: 存储 (-x, x) 元组（推荐）
    # 优点：保留原始值，便于调试；缺点：占用更多内存
    max_heap = Heap()
    for val in [3, 1, 5, 2]:
        max_heap.push((-val, val))
    print(f"方法2 - 存储元组: {max_heap.heap}")  # 预期: [(-5, 5), (-2, 2), (-3, 3), (-1, 1)]
    _, max_val = max_heap.pop()
    print(f"弹出最大值: {max_val}")  # 预期: 5

    # 从列表建最大堆
    max_heap = Heap(items=[(-x, x) for x in [3, 1, 5, 2]])
    print(f"从列表建最大堆: {max_heap.heap}")  # 预期: [(-5, 5), (-2, 2), (-3, 3), (-1, 1)]

    # ============ 3. 自定义优先级堆 ============
    print("\n【3. 自定义优先级堆】")
    print("-" * 60)

    # 示例1: 按绝对值排序（使用 tuple）
    # 原理：Python tuple 比较时，先比较第一个元素，相同则比较第二个...
    # 格式: (优先级, 数据)
    heap = Heap()
    for x in [3, -5, 2, -1]:
        heap.push((abs(x), x))
    print(f"按绝对值排序的堆: {heap.heap}")  # 预期: [(1, -1), (2, 2), (3, 3), (5, -5)]

    _, val = heap.pop()
    print(f"弹出绝对值最小的: {val}")  # 预期: -1

    # 示例2: 多关键字排序（先按距离，再按坐标）
    heap = Heap()
    points = [(1, 2), (3, 0), (0, 1)]
    for x, y in points:
        dist = x * x + y * y
        heap.push((dist, x, y))
    print(f"按距离排序的点: {heap.heap}")  # 预期: [(1, 0, 1), (5, 1, 2), (9, 3, 0)]

    dist, x, y = heap.pop()
    print(f"最近的点: ({x}, {y}), 距离: {dist}")  # 预期: (0, 1), 距离: 1

    # ============ 4. Non-comparable Object 处理技巧 ============
    print("\n【4. Non-comparable Object 处理技巧】")
    print("-" * 60)
    print("问题：当优先级相同时，tuple 会比较下一个元素")
    print("如果下一个元素是 list/dict/自定义对象，会报错 TypeError")
    print("解决：在优先级和对象之间插入唯一的 int（如入堆顺序）")
    print()

    # 正确做法：插入唯一计数器
    heap = Heap()
    counter = 0
    tasks = [
        (1, {"name": "task_a", "data": [1, 2]}),
        (1, {"name": "task_b", "data": [3, 4]}),  # 优先级相同
        (2, {"name": "task_c", "data": [5, 6]}),
    ]

    for priority, task in tasks:
        # 格式: (优先级, 唯一计数器, 对象)
        # 计数器确保即使优先级相同，也不会比较对象
        heap.push((priority, counter, task))
        counter += 1

    print("入堆顺序: task_a(优先级1), task_b(优先级1), task_c(优先级2)")
    print(f"堆中元素数量: {len(heap)}")  # 预期: 3

    # 弹出元素
    priority, _, task = heap.pop()
    print(f"弹出: {task['name']}, 优先级: {priority}")  # 预期: task_a, 优先级: 1

    priority, _, task = heap.pop()
    print(f"弹出: {task['name']}, 优先级: {priority}")  # 预期: task_b, 优先级: 1

    priority, _, task = heap.pop()
    print(f"弹出: {task['name']}, 优先级: {priority}")  # 预期: task_c, 优先级: 2

    # ============ 5. 堆排序示例 ============
    print("\n【5. 堆排序示例】")
    print("-" * 60)

    # 升序排序：使用最小堆
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    heap = Heap(items=nums)
    sorted_asc = []
    while heap:
        sorted_asc.append(heap.pop())
    print(f"原数组: {nums}")
    print(f"升序排序: {sorted_asc}")  # 预期: [1, 1, 2, 3, 4, 5, 6, 9]

    # 降序排序：使用最大堆（存储负数）
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    heap = Heap(items=[-x for x in nums])
    sorted_desc = []
    while heap:
        sorted_desc.append(-heap.pop())
    print(f"降序排序: {sorted_desc}")  # 预期: [9, 6, 5, 4, 3, 2, 1, 1]

    # ============ 6. Top K 问题 ============
    print("\n【6. Top K 问题】")
    print("-" * 60)

    # 找最大的 k 个元素：维护大小为 k 的最小堆
    # 时间复杂度 O(n log k)，空间复杂度 O(k)
    nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
    k = 3

    # 方法：维护大小为 k 的最小堆，遍历所有元素
    # 如果堆未满或当前元素大于堆顶，则入堆
    heap = Heap()
    for num in nums:
        if len(heap) < k:
            heap.push(num)
        elif num > heap.peek():
            heap.pop()
            heap.push(num)

    top_k = sorted([heap.pop() for _ in range(len(heap))], reverse=True)
    print(f"数组: {nums}")
    print(f"最大的 {k} 个元素: {top_k}")  # 预期: [9, 6, 5]

    # ============ 7. 常用操作汇总 ============
    print("\n【7. 常用操作时间复杂度汇总】")
    print("-" * 60)
    print("push(item)                - O(log n) - 插入元素")
    print("pop()                     - O(log n) - 弹出堆顶")
    print("peek()                    - O(1)     - 查看堆顶")
    print("Heap(items=list)          - O(n)     - 从列表建堆")
    print("堆排序                     - O(n log n) - heapify + 反复 pop")
    print("Top K 问题                 - O(n log k) - 维护大小为 k 的堆")

    # ============ 8. 实战技巧 ============
    print("\n【8. 实战技巧】")
    print("-" * 60)
    print("✓ 最小堆：Heap() 直接使用")
    print("✓ 最大堆：存储 (-x, x) 或 -x")
    print("✓ 自定义排序：使用 (priority, data) 元组")
    print("✓ 避免对象比较：使用 (priority, counter, object)")
    print("✓ 多关键字：使用 (key1, key2, key3, data)")
    print("✓ 从列表建堆：Heap(items=list) 比逐个 push 更快")
    print("✓ Top K 问题：维护大小为 K 的堆，复杂度 O(n log k)")

    # ============ 9. 笔试速记模板 ============
    print("\n【9. 笔试速记模板】")
    print("-" * 60)
    print("核心代码：")
    print()
    print("# 最小堆快速实现")
    print("class Heap:")
    print("    def __init__(self):")
    print("        self.h = []")
    print()
    print("    def push(self, x):")
    print("        self.h.append(x)")
    print("        i = len(self.h) - 1")
    print("        while i > 0:")
    print("            p = (i - 1) // 2")
    print("            if self.h[i] < self.h[p]:")
    print("                self.h[i], self.h[p] = self.h[p], self.h[i]")
    print("                i = p")
    print("            else:")
    print("                break")
    print()
    print("    def pop(self):")
    print("        self.h[0], self.h[-1] = self.h[-1], self.h[0]")
    print("        result = self.h.pop()")
    print("        if self.h:")
    print("            i, n = 0, len(self.h)")
    print("            while True:")
    print("                best = i")
    print("                left, right = 2 * i + 1, 2 * i + 2")
    print("                if left < n and self.h[left] < self.h[best]:")
    print("                    best = left")
    print("                if right < n and self.h[right] < self.h[best]:")
    print("                    best = right")
    print("                if best == i:")
    print("                    break")
    print("                self.h[i], self.h[best] = self.h[best], self.h[i]")
    print("                i = best")
    print("        return result")
    print()
    print("    def peek(self):")
    print("        return self.h[0]")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
