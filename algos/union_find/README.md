# 并查集（Union-Find）笔试攻略

## 什么是并查集？

并查集是一种用于处理**不相交集合**的数据结构，支持快速合并和查询操作。

### 核心性质

1. **集合划分**：将 n 个元素划分为若干个互不相交的集合
2. **代表元素**：每个集合有一个代表元素（根节点）
3. **路径压缩**：查找时将路径上所有节点直接连到根节点，优化后续查询

### 数组存储方式

使用一维数组 `parent[]` 存储每个节点的父节点：

- 初始时：`parent[i] = i`（每个元素自成一个集合）
- 查找根节点：不断向上查找直到 `parent[i] == i`
- 合并集合：将一个根节点的父节点指向另一个根节点

### 支持的操作

| 操作                | 时间复杂度          | 说明               |
|-------------------|----------------|------------------|
| `__init__(n)`     | O(n)           | 初始化 n 个独立集合      |
| `find(x)`         | O(α(n)) ≈ O(1) | 查找 x 所在集合的根节点    |
| `union(x, y)`     | O(α(n)) ≈ O(1) | 合并 x 和 y 所在的集合   |
| `connected(x, y)` | O(α(n)) ≈ O(1) | 判断 x 和 y 是否在同一集合 |

注：α(n) 是阿克曼函数的反函数，增长极其缓慢，实际应用中可视为常数。

## 并查集适合解决什么问题？

并查集特别适合处理以下场景：

1. **连通性判断**：判断图中两个节点是否连通
    - 时间复杂度：O(α(n)) ≈ O(1)，远优于 DFS/BFS 的 O(n)

2. **动态连通性**：需要频繁添加边并查询连通性
    - 例如：社交网络中的好友关系、网络连接状态

3. **环检测**：判断无向图中是否存在环
    - 添加边时，如果两端点已连通则形成环

4. **最小生成树**：Kruskal 算法的核心数据结构
    - 按边权排序后，用并查集判断是否形成环

5. **等价类划分**：将元素按等价关系分组
    - 例如：字符串相似度分组、账号合并

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [OI Wiki：并查集](https://oiwiki.org/ds/dsu/) - 模板、优化和应用场景都比较系统，适合先打整体基础
- [labuladong：Union-Find 并查集详解](https://labuladong.online/zh/algo/data-structure/union-find/) - 更偏题目视角，适合把路径压缩和连通性问题结合起来理解
- [C 语言中文网：并查集（Union-Find）算法详解](https://c.biancheng.net/view/olbfcce.html) - 讲法更偏入门，适合补“为什么这样合并”的直觉

## 笔试场景建议

### 推荐策略

1. **优先使用极简版**（无按秩合并）
    - ✅ 代码最短，最容易记忆（10 行左右）
    - ✅ 性能足够好，笔试题数据量下无明显差异
    - ✅ 不容易写错

2. **完整版的使用场景**（带按秩合并）
    - 数据量特别大（n > 10^5）且对性能敏感
    - 题目明确要求最优时间复杂度
    - 有充足时间且追求完美实现

### 记忆技巧

并查集的核心就三个操作，记住这个口诀：

- **初始化**：`self.p = list(range(n))` - 每个元素指向自己
- **查找根**：`if self.p[x] != x: self.p[x] = self.find(self.p[x])` - 递归查找并压缩路径
- **合并集**：`self.p[self.find(x)] = self.find(y)` - 将一个根指向另一个根

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对对应实现类的核心代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| 极简版并查集 | [union_find_simple.py](union_find_simple.py) 里的 `UnionFind` 类 | `9.7` | 正常可写 | 推荐，路径压缩已经足够能打 |
| 按秩合并版并查集 | [union_find_basic.py](union_find_basic.py) 里的 `UnionFind` 类 | `18.3` | 现场高风险 | 只有特别在意极限性能时再上 |

按秩合并确实更完整，但从面试手写体感上看，复杂性已经明显上去了，性价比并不高。

## 方案一：极简版实现（推荐）

```python
class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.p[rx] = ry
            return True  # 合并成功
        return False  # 已在同一集合

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

## 方案二：按秩合并版

### 什么时候需要按秩合并？

按秩合并是一种优化技术，通过维护树的高度信息来保持树的平衡：

**按秩合并的好处：**

- 保证树的高度尽可能小，理论上性能更优
- 在极端情况下（如链式合并 0→1→2→3→...）能避免树退化
- 适合数据量特别大（n > 10^5）且对性能敏感的场景

**实际笔试建议：**

- 大多数情况下，极简版已经足够（路径压缩已经提供了接近 O(1) 的性能）
- 只有在数据量特别大或追求极致性能时才需要按秩合并
- 按秩合并会增加代码复杂度和记忆难度，性价比不高

### 完整版代码

```python
class UnionFind:
    def __init__(self, n):
        self.p = list(range(n))  # 父节点数组
        self.r = [0] * n  # 秩（树的高度上界）

    def find(self, x):
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])
        return self.p[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False

        # 按秩合并：小树连到大树
        if self.r[rx] < self.r[ry]:
            self.p[rx] = ry
        elif self.r[rx] > self.r[ry]:
            self.p[ry] = rx
        else:
            self.p[ry] = rx
            self.r[rx] += 1  # 只有秩相同时才增加
        return True

    def connected(self, x, y):
        return self.find(x) == self.find(y)
```

### 按秩合并的原理

- **秩（rank）**：表示树的高度上界
- **合并规则**：将秩小的树连到秩大的树上
- **秩的更新**：只有两棵秩相同的树合并时，新树的秩才会增加 1

这样可以保证树的高度始终保持在 O(log n) 级别。

## 常见题型速查

### 1. 判断图的连通性

```python
# 给定 n 个节点和边列表，判断图是否连通
uf = UnionFind(n)
for x, y in edges:
    uf.union(x, y)

# 方法1：检查是否只有一个连通分量
is_connected = len(set(uf.find(i) for i in range(n))) == 1

# 方法2：检查是否所有节点都连到同一个根
root = uf.find(0)
is_connected = all(uf.find(i) == root for i in range(n))
```

### 2. 检测无向图中的环

```python
# 添加边时，如果两端点已连通则形成环
uf = UnionFind(n)
for x, y in edges:
    if not uf.union(x, y):
        print(f"发现环: 边 ({x}, {y})")
        break
```

### 3. 统计连通分量数量

```python
# 处理完所有边后，统计不同的根节点数
uf = UnionFind(n)
for x, y in edges:
    uf.union(x, y)

components = len(set(uf.find(i) for i in range(n)))
```

### 4. 账号合并（等价类问题）

```python
# 例如：[[email1, email2], [email2, email3]] 表示这些邮箱属于同一账号
uf = UnionFind(len(all_emails))
email_to_id = {email: i for i, email in enumerate(all_emails)}

for account in accounts:
    first_id = email_to_id[account[0]]
    for email in account[1:]:
        uf.union(first_id, email_to_id[email])

# 按根节点分组
groups = {}
for email, idx in email_to_id.items():
    root = uf.find(idx)
    if root not in groups:
        groups[root] = []
    groups[root].append(email)
```

### 5. 最小生成树（Kruskal 算法）

```python
# 按边权排序，贪心选择不形成环的边
edges.sort(key=lambda e: e[2])  # 按权重排序
uf = UnionFind(n)
mst_weight = 0

for u, v, weight in edges:
    if uf.union(u, v):  # 不形成环
        mst_weight += weight
```

### 6. 岛屿数量（二维网格）

```python
# 将二维坐标映射到一维索引
def get_id(i, j):
    return i * cols + j


uf = UnionFind(rows * cols)
for i in range(rows):
    for j in range(cols):
        if grid[i][j] == '1':
            # 与右边和下边的陆地合并
            for di, dj in [(0, 1), (1, 0)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == '1':
                    uf.union(get_id(i, j), get_id(ni, nj))

# 统计陆地的连通分量数
islands = len(set(uf.find(get_id(i, j))
                  for i in range(rows)
                  for j in range(cols)
                  if grid[i][j] == '1'))
```

## 实战技巧总结

✅ **极简版足够用**：笔试中 99% 的情况用极简版即可，代码短不易错

✅ **路径压缩是核心**：`self.p[x] = self.find(self.p[x])` 这一行是性能关键

✅ **union 返回布尔值**：返回是否成功合并，方便检测环和统计操作次数

✅ **二维网格映射**：`id = i * cols + j` 将二维坐标转为一维索引

✅ **统计连通分量**：`len(set(uf.find(i) for i in range(n)))`

✅ **初始化技巧**：`self.p = list(range(n))` 比循环赋值更简洁

## 参考资料

- [union_find_simple.py](union_find_simple.py) - 极简版实现及完整使用示例（推荐）
- [union_find_basic.py](union_find_basic.py) - 完整版实现（带按秩合并）及迭代版 find

**推荐阅读顺序**：

1. 先看本 README 了解并查集的概念和应用场景
2. 记住极简版的 10 行代码实现
3. 参考常见题型速查，了解如何套用模板
4. 查看 `union_find_simple.py` 中的完整示例代码
5. 如需了解按秩合并，参考 `union_find_basic.py`
