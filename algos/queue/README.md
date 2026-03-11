# 队列（Queue）笔试攻略

## 什么是队列？

队列是一种**先进先出（FIFO, First In First Out）**的数据结构，最先进去的元素最先出来。

在 Python 里，队列常见有两种靠谱写法：

- **推荐方案**：`collections.deque`
- **极简暴力方案**：`list + 头指针`

### 核心性质

1. **先进先出**：先入队的元素会先出队
2. **一头进，一头出**：通常在尾部入队、头部出队
3. **别直接用 `pop(0)`**：那是 O(n)，数据一大直接炸
4. **`deque` 最稳**：代码短、性能稳、最不容易写错
5. **`list + 头指针` 也能打**：不想 import 时很好用，但要自己维护 `head`

### 支持的操作

| 操作      | `deque` 时间复杂度 | `list + 头指针` 时间复杂度 | 说明 |
|---------|----------------|----------------------|----|
| `push`  | O(1)           | O(1)                 | 入队 |
| `pop`   | O(1)           | O(1) 摊还            | 出队 |
| `front` | O(1)           | O(1)                 | 查看队头 |
| `empty` | O(1)           | O(1)                 | 判断是否为空 |
| `size`  | O(1)           | O(1)                 | 获取当前大小 |

## 队列适合解决什么问题？

队列特别适合处理以下场景：

1. **BFS 广度优先搜索**：按层扩展节点
    - 例如：图最短路、树层序遍历、网格最短步数
    - 时间复杂度：O(V + E) 或 O(mn)

2. **拓扑排序**：维护当前入度为 0 的点
    - 例如：课程表、依赖调度、DAG 处理
    - 时间复杂度：O(V + E)

3. **多源 BFS**：多个起点同时扩散
    - 例如：最近 0、腐烂橘子、火势蔓延
    - 时间复杂度：O(mn)

4. **任务调度 / 模拟题**：按到达顺序处理元素
    - 例如：打印队列、轮转调度、消息处理
    - 时间复杂度：通常是 O(n)

5. **层级处理问题**：天然按“第几层”推进
    - 例如：二叉树层序遍历、最短跳数问题
    - 优势：写法直观，不容易乱

## 笔试场景建议

### 推荐策略

1. **优先使用 `collections.deque`**
    - ✅ 标准库现成，直接能用
    - ✅ `append()` / `popleft()` / `q[0]` 就够了
    - ✅ 本地实测略快于 `list + 头指针`
    - ✅ 不需要自己维护 `head`

2. **不想 import 时，用 `list + 头指针`**
    - ✅ 代码也很短，思路很直接
    - ✅ BFS、拓扑排序这类“一路进一路出”的题完全够用
    - ⚠️ 长时间复用同一个队列时，前面弹掉的元素还留在列表里
    - ⚠️ 需要自己写 `head == len(q)` 这种判空逻辑

3. **不要用 `list.pop(0)`**
    - ❌ 出队是 O(n)
    - ❌ 数据一大直接慢几个数量级
    - ❌ 看着简单，实战最坑

### 本地对比（Python 3.11.5，仅供参考）

下面是本地跑出来的简单 benchmark：

| 方案 | 核心写法行数 | 20 万次先入队再出队 | 30 万次交替入队/出队 | 结论 |
|------|------------|------------------|-------------------|------|
| `deque` | 约 5 行 | `0.0096s` | `0.0105s` | 最稳，推荐 |
| `list + 头指针` | 约 7 行 | `0.0124s` | `0.0160s` | 也能打，不想 import 时可用 |
| `list.pop(0)` | 约 4 行 | `13.5s` | 未测 | 别用 |

结论很直接：

- **笔试优先 `deque`**
- **不想 import 就用 `list + 头指针`**
- **别碰 `pop(0)`**

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| `collections.deque` | README 里的最小模板片段 | `0.0` | 很容易手写 | 推荐，核心状态只有队列本身 |
| `list + 头指针` | README 里的最小模板片段 | `0.0` | 很容易手写 | 也很轻，但要额外维护 `head` |

这两个基础模板都很容易手写。推荐 `deque` 的原因主要不是分数差距，而是它少一个 `head` 状态，现场更不容易写乱。

## 方案一：使用 `collections.deque`（推荐）

### 基本用法

```python
from collections import deque

q = deque()

q.append(3)        # 入队
q.append(5)
front = q[0]       # 看队头: 3
x = q.popleft()    # 出队: 3
empty = not q      # 判空
size = len(q)      # 当前大小
```

### BFS 最短路

```python
from collections import deque


def bfs_dist(graph, start):
    q = deque([start])
    dist = {start: 0}

    while q:
        u = q.popleft()
        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    return dist
```

### 拓扑排序

```python
from collections import deque


def topo_sort(n, edges):
    g = [[] for _ in range(n)]
    indeg = [0] * n

    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1

    q = deque(i for i in range(n) if indeg[i] == 0)
    order = []

    while q:
        u = q.popleft()
        order.append(u)
        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return order if len(order) == n else []
```

### 多源 BFS

```python
from collections import deque


def multi_source_bfs(grid):
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = deque()

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                dist[i][j] = 0
                q.append((i, j))

    while q:
        i, j = q.popleft()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and dist[ni][nj] == -1:
                dist[ni][nj] = dist[i][j] + 1
                q.append((ni, nj))

    return dist
```

**完整实现和更多示例**：[deque_native.py](deque_native.py)

## 方案二：`list + 头指针`

### 基本用法

```python
q = []
head = 0

q.append(3)         # 入队
q.append(5)
front = q[head]     # 看队头: 3
x = q[head]         # 出队值: 3
head += 1           # 出队
empty = head == len(q)
size = len(q) - head
```

### BFS 最短路

```python
def bfs_dist(graph, start):
    q = [start]
    head = 0
    dist = {start: 0}

    while head < len(q):
        u = q[head]
        head += 1

        for v in graph[u]:
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    return dist
```

### 轻量回收前缀（可选）

```python
# 长时间复用同一个队列时，可选地把前面废掉的部分切掉
if head > 64 and head * 2 >= len(q):
    q = q[head:]
    head = 0
```

这几行不是必须的，但如果队列生命周期很长，这么写更稳一点。

### 拓扑排序

```python
def topo_sort(n, edges):
    g = [[] for _ in range(n)]
    indeg = [0] * n

    for u, v in edges:
        g[u].append(v)
        indeg[v] += 1

    q = [i for i in range(n) if indeg[i] == 0]
    head = 0
    order = []

    while head < len(q):
        u = q[head]
        head += 1
        order.append(u)

        for v in g[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return order if len(order) == n else []
```

**完整实现和更多示例**：[list_head.py](list_head.py)

## 常见题型速查

### 1. BFS 最短路

```python
q = deque([start])
dist = {start: 0}

while q:
    u = q.popleft()
    for v in graph[u]:
        if v not in dist:
            dist[v] = dist[u] + 1
            q.append(v)
```

### 2. 多源 BFS

```python
q = deque(sources)
for x, y in sources:
    dist[x][y] = 0

while q:
    x, y = q.popleft()
    for dx, dy in dirs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < rows and 0 <= ny < cols and dist[nx][ny] == -1:
            dist[nx][ny] = dist[x][y] + 1
            q.append((nx, ny))
```

### 3. 拓扑排序

```python
q = deque(i for i in range(n) if indeg[i] == 0)
order = []

while q:
    u = q.popleft()
    order.append(u)
    for v in g[u]:
        indeg[v] -= 1
        if indeg[v] == 0:
            q.append(v)
```

### 4. 二叉树层序遍历

```python
q = deque([root])
ans = []

while q:
    level = []
    for _ in range(len(q)):
        node = q.popleft()
        level.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    ans.append(level)
```

### 5. `list + 头指针` BFS 模板

```python
q = [start]
head = 0

while head < len(q):
    u = q[head]
    head += 1
    for v in graph[u]:
        if v not in seen:
            seen.add(v)
            q.append(v)
```

## 实战技巧总结

✅ **优先用 `deque`**：`append()` + `popleft()` 最顺手

✅ **不想 import 再用 `list + 头指针`**：`q.append(x)`、`q[head]`、`head += 1`

✅ **`list + 头指针` 判空**：写 `head == len(q)`，别写成 `not q`

✅ **BFS 先标记再入队**：避免同一个点被重复加入

✅ **拓扑排序核心**：维护入度数组 + 队列

✅ **层序遍历按 `len(q)` 分层**：一层一层处理最稳

✅ **不要用 `pop(0)`**：这玩意会把 O(n) 隐藏得很深

## 参考资料

- [deque_native.py](deque_native.py) - 使用 `collections.deque` 的完整示例
- [list_head.py](list_head.py) - 使用 `list + 头指针` 的完整示例

**推荐阅读顺序**：

1. 先看本 README，记住推荐顺序：`deque` > `list + 头指针` > `pop(0)` 别用
2. 再看 `deque_native.py`，把 BFS 和拓扑排序模板吃透
3. 如果你更习惯裸写法，再看 `list_head.py`
