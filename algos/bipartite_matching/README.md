# 二分图匹配（匈牙利算法）笔试攻略

## 什么是二分图匹配？

**二分图**是一种特殊的图，其顶点可以分为两个互不相交的集合，所有边都连接不同集合中的顶点。**二分图匹配**
是指在二分图中选择一些边，使得任意两条边都不共享顶点。

- **最大匹配**：包含边数最多的匹配
- **完美匹配**：所有顶点都被匹配的匹配（匹配数 = min(左侧顶点数, 右侧顶点数)）

### 核心概念

1. **增广路径**：从左侧未匹配点出发，经过"未匹配边-匹配边-未匹配边..."交替路径，到达右侧未匹配点
2. **匈牙利算法原理**：不断寻找增广路径，每找到一条就能使匹配数 +1
3. **时间复杂度**：O(V × E)，其中 V 是顶点数，E 是边数

### 支持的操作

| 操作     | 时间复杂度    | 说明                    |
|--------|----------|-----------------------|
| 构建图    | O(E)     | 添加所有边                 |
| 求最大匹配  | O(V × E) | 使用 DFS 寻找增广路径         |
| 判断完美匹配 | O(1)     | 检查匹配数是否等于 min(左侧, 右侧) |

## 二分图匹配适合解决什么问题？

二分图匹配特别适合处理以下场景：

1. **任务分配问题**：将 n 个任务分配给 m 个人，每人最多完成一个任务
    - 例如：工作分配、课程安排、资源调度

2. **配对问题**：在两组对象之间建立一对一关系
    - 例如：相亲配对、学生-导师匹配、设备-端口分配

3. **覆盖问题**：最小点覆盖、最大独立集（通过 König 定理转化）
    - 最小点覆盖 = 最大匹配数
    - 最大独立集 = 总顶点数 - 最大匹配数

4. **棋盘问题**：在棋盘上放置棋子，满足特定约束
    - 例如：放置车/象，使其互不攻击

## 笔试场景建议

### 推荐策略

**手动实现匈牙利算法**

- ✅ Python 标准库没有现成的二分图匹配实现
- ✅ 代码简洁（约 20 行），容易记忆
- ✅ 适用于绝大多数笔试题目

## 手动实现匈牙利算法

### 适合速记的匈牙利算法实现

```python
class Hungarian:
    def __init__(self, n, m):
        """
        n: 左侧顶点数（编号 0 到 n-1）
        m: 右侧顶点数（编号 0 到 m-1）
        """
        self.n = n
        self.m = m
        self.graph = [[] for _ in range(n)]  # 邻接表
        self.match = [-1] * m  # match[j] = i 表示右侧 j 匹配到左侧 i

    def add_edge(self, u, v):
        """添加边：左侧 u -> 右侧 v"""
        self.graph[u].append(v)

    def dfs(self, u, visited):
        """DFS 寻找增广路径 - O(E)"""
        for v in self.graph[u]:
            if visited[v]:
                continue
            visited[v] = True

            # 如果 v 未匹配，或者 v 的匹配对象可以找到新的匹配
            if self.match[v] == -1 or self.dfs(self.match[v], visited):
                self.match[v] = u
                return True
        return False

    def max_matching(self):
        """求最大匹配数 - O(V × E)"""
        count = 0
        for i in range(self.n):
            visited = [False] * self.m
            if self.dfs(i, visited):
                count += 1
        return count

    def get_matching(self):
        """返回匹配结果：[(左侧, 右侧), ...]"""
        result = []
        for j in range(self.m):
            if self.match[j] != -1:
                result.append((self.match[j], j))
        return result
```

### 使用示例

```python
# 示例：3 个人，4 个任务
# 人 0 可以做任务 0, 1
# 人 1 可以做任务 1, 2
# 人 2 可以做任务 2, 3

h = Hungarian(3, 4)
h.add_edge(0, 0)
h.add_edge(0, 1)
h.add_edge(1, 1)
h.add_edge(1, 2)
h.add_edge(2, 2)
h.add_edge(2, 3)

print(h.max_matching())  # 输出: 3
print(h.get_matching())  # 输出: [(0, 0), (1, 1), (2, 2)] 或其他等价匹配
```

## 常见题型速查

### 1. 基础匹配问题

```python
# 直接套用模板
h = Hungarian(n, m)
for u, v in edges:
    h.add_edge(u, v)
print(h.max_matching())
```

### 2. 棋盘染色问题

```python
# 将棋盘黑白染色，黑格作为左侧，白格作为右侧
# 例如：8x8 棋盘放置车，使其互不攻击

def solve_chessboard(n, forbidden):
    """
    n: 棋盘大小
    forbidden: 禁止放置的格子列表 [(r, c), ...]
    """
    # 黑格：(r + c) % 2 == 0
    # 白格：(r + c) % 2 == 1

    forbidden_set = set(forbidden)
    black_cells = []
    white_cells = []

    for r in range(n):
        for c in range(n):
            if (r, c) not in forbidden_set:
                if (r + c) % 2 == 0:
                    black_cells.append((r, c))
                else:
                    white_cells.append((r, c))

    # 建图：相邻的黑白格子连边
    h = Hungarian(len(black_cells), len(white_cells))
    for i, (r1, c1) in enumerate(black_cells):
        for j, (r2, c2) in enumerate(white_cells):
            if abs(r1 - r2) + abs(c1 - c2) == 1:  # 相邻
                h.add_edge(i, j)

    return h.max_matching()
```

### 3. 最小点覆盖

```python
# König 定理：二分图的最小点覆盖 = 最大匹配数

def min_vertex_cover(n, m, edges):
    h = Hungarian(n, m)
    for u, v in edges:
        h.add_edge(u, v)
    return h.max_matching()
```

### 4. 最大独立集

```python
# 最大独立集 = 总顶点数 - 最大匹配数

def max_independent_set(n, m, edges):
    h = Hungarian(n, m)
    for u, v in edges:
        h.add_edge(u, v)
    return n + m - h.max_matching()
```

### 5. 判断完美匹配

```python
def has_perfect_matching(n, m, edges):
    if n != m:
        return False

    h = Hungarian(n, m)
    for u, v in edges:
        h.add_edge(u, v)

    return h.max_matching() == n
```

## 实战技巧总结

✅ **建图时注意编号**：左侧从 0 到 n-1，右侧从 0 到 m-1

✅ **visited 数组每次重置**：每次 DFS 都需要新的 visited 数组

✅ **match 数组含义**：`match[j] = i` 表示右侧 j 匹配到左侧 i

✅ **增广路径理解**：找到一条路径后，沿途翻转匹配状态

✅ **棋盘染色技巧**：`(r + c) % 2` 可以将棋盘分为两部分

✅ **König 定理应用**：最小点覆盖 = 最大匹配数（仅适用于二分图）

✅ **时间复杂度估算**：O(V × E)，对于稠密图约为 O(V³)

✅ **空间优化**：如果只需要匹配数，不需要保存完整匹配结果

## 参考资料

- [hungarian.py](hungarian.py) - 匈牙利算法实现
- [examples.py](examples.py) - 常见题型完整示例

**推荐阅读顺序**：

1. 先看本 README 了解基本概念和策略
2. 参考 `hungarian.py` 学习核心实现
3. 查看 `examples.py` 了解实际应用场景
