# 堆（Heap）笔试攻略

## 什么是堆？

堆是一种特殊的**完全二叉树**数据结构，满足堆性质：

- **最小堆（Min Heap）**：父节点的值 ≤ 子节点的值，堆顶是最小元素
- **最大堆（Max Heap）**：父节点的值 ≥ 子节点的值，堆顶是最大元素

### 核心性质

1. **完全二叉树**：除了最后一层，其他层都是满的，最后一层从左到右填充
2. **数组存储**：使用数组实现，索引关系如下：
    - 节点 `i` 的左子节点：`2*i + 1`
    - 节点 `i` 的右子节点：`2*i + 2`
    - 节点 `i` 的父节点：`(i - 1) // 2`
3. **堆顶元素**：始终在索引 0 位置（最小堆的最小值或最大堆的最大值）

### 支持的操作

| 操作        | 时间复杂度    | 说明          |
|-----------|----------|-------------|
| `heapify` | O(n)     | 从数组建堆       |
| `push`    | O(log n) | 插入元素        |
| `pop`     | O(log n) | 弹出堆顶元素      |
| `peek`    | O(1)     | 查看堆顶元素（不弹出） |

## 堆适合解决什么问题？

堆特别适合处理以下场景：

1. **Top K 问题**：找最大/最小的 K 个元素
    - 时间复杂度：O(n log k)，优于排序的 O(n log n)

2. **动态维护最值**：需要频繁插入元素并获取最值
    - 例如：实时获取中位数、滑动窗口最值

3. **优先级队列**：按优先级处理任务
    - 例如：任务调度、Dijkstra 最短路径

4. **合并 K 个有序序列**：使用最小堆高效合并
    - 时间复杂度：O(n log k)

5. **堆排序**：原地排序算法
    - 时间复杂度：O(n log n)，空间复杂度：O(1)

## 笔试场景建议

### 推荐策略

1. **优先使用 `heapq`**（Python 标准库）
    - ✅ 省时省力，代码简洁
    - ✅ 经过优化，性能更好
    - ✅ 大概率比手写实现更快
    - ✅ 不容易出错

2. **手动实现的场景**
    - ❌ 题目明确禁止使用标准库
    - ❌ 需要特殊的堆操作（如修改堆中元素）
    - ❌ 面试官要求手写数据结构

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。`heapq` 按最小可用模板片段测，手写堆按完整 `Heap` 类测。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| `heapq` 标准库 | README 里的最小模板片段 | `0.0` | 很容易手写 | 强烈推荐，复杂度几乎都交给标准库 |
| 手动实现 `Heap` 类 | [heap_manual.py](heap_manual.py) 里的 `Heap` 类 | `65.3` | 现场高风险 | 只在被迫手写数据结构时使用 |

`heapq` 分数几乎为 0 不是工具失灵，而是标准库方案确实把大量手写负担省掉了。

---

## 方案一：使用 heapq（推荐）

### 基本用法

```python
import heapq

# 最小堆
heap = []
heapq.heappush(heap, 3)  # 插入元素
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)

min_val = heapq.heappop(heap)  # 弹出最小值: 1
top = heap[0]  # 查看堆顶: 2

# 从列表建堆 O(n)
nums = [3, 1, 4, 1, 5]
heapq.heapify(nums)  # 原地转换为堆
```

### 最大堆实现

```python
# 方法1: 存储负数
max_heap = []
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -1)
max_val = -heapq.heappop(max_heap)  # 弹出最大值: 3

# 方法2: 存储 (-x, x) 元组（推荐）
max_heap = []
heapq.heappush(max_heap, (-3, 3))
heapq.heappush(max_heap, (-1, 1))
_, max_val = heapq.heappop(max_heap)  # 弹出最大值: 3
```

### 自定义优先级

```python
# 使用 tuple：(优先级, 数据)
heap = []
for x in [3, -5, 2, -1]:
    heapq.heappush(heap, (abs(x), x))  # 按绝对值排序

_, val = heapq.heappop(heap)  # 弹出绝对值最小的: -1
```

### Non-comparable Object 处理技巧

```python
# 问题：当优先级相同时，tuple 会比较下一个元素
# 如果是 list/dict/对象，会报 TypeError

# 解决：插入唯一计数器
heap = []
counter = 0
tasks = [
    (1, {"name": "task_a"}),
    (1, {"name": "task_b"}),  # 优先级相同
]

for priority, task in tasks:
    # 格式: (优先级, 唯一计数器, 对象)
    heapq.heappush(heap, (priority, counter, task))
    counter += 1

priority, _, task = heapq.heappop(heap)  # 不会报错
```

### Top K 问题示例

```python
# 找最大的 k 个元素：维护大小为 k 的最小堆
nums = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
k = 3

heap = []
for num in nums:
    if len(heap) < k:
        heapq.heappush(heap, num)
    elif num > heap[0]:
        heapq.heappop(heap)
        heapq.heappush(heap, num)

# 结果: [5, 6, 9]
```

**完整实现和更多示例**：[heapq_native.py](heapq_native.py)

---

## 方案二：手动实现堆

### 适合速记的最小堆实现

```python
class Heap:
    def __init__(self):
        self.h = []

    def push(self, x):
        """插入元素 - O(log n)"""
        self.h.append(x)
        i = len(self.h) - 1
        # 向上调整（上浮）
        while i > 0:
            p = (i - 1) // 2  # 父节点索引
            if self.h[i] < self.h[p]:
                self.h[i], self.h[p] = self.h[p], self.h[i]
                i = p
            else:
                break

    def pop(self):
        """弹出堆顶 - O(log n)"""
        # 将最后一个元素移到堆顶
        self.h[0], self.h[-1] = self.h[-1], self.h[0]
        result = self.h.pop()

        if self.h:
            i, n = 0, len(self.h)
            # 向下调整（下沉）
            while True:
                best = i
                left, right = 2 * i + 1, 2 * i + 2
                # 找出父节点和两个子节点中最小的
                if left < n and self.h[left] < self.h[best]:
                    best = left
                if right < n and self.h[right] < self.h[best]:
                    best = right
                if best == i:
                    break
                self.h[i], self.h[best] = self.h[best], self.h[i]
                i = best

        return result

    def peek(self):
        """查看堆顶 - O(1)"""
        return self.h[0]
```

### 使用示例

```python
# 最小堆
heap = Heap()
heap.push(3)
heap.push(1)
heap.push(2)
print(heap.pop())  # 1

# 最大堆：存储负数
max_heap = Heap()
max_heap.push(-3)
max_heap.push(-1)
print(-max_heap.pop())  # 3

# 自定义排序：使用 tuple
heap = Heap()
heap.push((abs(-5), -5))  # 按绝对值排序
heap.push((abs(2), 2))
_, val = heap.pop()  # 弹出绝对值最小的
```

### 从列表建堆（可选）

```python
def heapify(self):
    """从数组建堆 - O(n)"""
    n = len(self.h)
    # 从最后一个非叶子节点开始，依次向下调整
    for i in range((n - 2) // 2, -1, -1):
        self._sift_down(i)
```

**完整实现和更多示例**：[heap_manual.py](heap_manual.py)

---

## 常见题型速查

### 1. Top K 问题

```python
# 找最大的 k 个：维护大小为 k 的最小堆
heap = []
for num in nums:
    if len(heap) < k:
        heapq.heappush(heap, num)
    elif num > heap[0]:
        heapq.heappop(heap)
        heapq.heappush(heap, num)
```

### 2. 合并 K 个有序链表

```python
heap = []
for i, lst in enumerate(lists):
    if lst:
        heapq.heappush(heap, (lst.val, i, lst))

while heap:
    val, i, node = heapq.heappop(heap)
    # 处理节点...
    if node.next:
        heapq.heappush(heap, (node.next.val, i, node.next))
```

### 3. 中位数维护

```python
# 使用两个堆：最大堆存较小的一半，最小堆存较大的一半
max_heap = []  # 存储 -x
min_heap = []


def add_num(num):
    heapq.heappush(max_heap, -num)
    heapq.heappush(min_heap, -heapq.heappop(max_heap))
    if len(min_heap) > len(max_heap):
        heapq.heappush(max_heap, -heapq.heappop(min_heap))


def find_median():
    if len(max_heap) > len(min_heap):
        return -max_heap[0]
    return (-max_heap[0] + min_heap[0]) / 2
```

---

## 实战技巧总结

✅ **最小堆**：直接使用 `heapq` 或 `Heap()`

✅ **最大堆**：存储 `(-x, x)` 或 `-x`

✅ **自定义排序**：使用 `(priority, data)` 元组

✅ **避免对象比较**：使用 `(priority, counter, object)`

✅ **多关键字**：使用 `(key1, key2, key3, data)`

✅ **从列表建堆**：`heapify()` 比逐个 `push` 更快（O(n) vs O(n log n)）

✅ **Top K 问题**：维护大小为 K 的堆，复杂度 O(n log k)

---

## 参考资料

- [heapq_native.py](heapq_native.py) - 使用 heapq 的完整示例
- [heap_manual.py](heap_manual.py) - 手动实现堆的完整代码

**推荐阅读顺序**：

1. 先看本 README 了解基本概念和策略
2. 参考 `heapq_native.py` 学习 heapq 用法
3. 需要手写时，参考 `heap_manual.py` 中的速记模板
