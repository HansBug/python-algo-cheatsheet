"""
Python 队列（Queue）模板 - list + 头指针

极简暴力写法：
- 入队：q.append(x)
- 出队：x = q[head]; head += 1
- 看队头：q[head]

支持 Python 3.7-3.14，无第三方依赖

核心原理：
- 用 list 存所有元素
- 用 head 指向当前队头
- 这样可以避开 list.pop(0) 的 O(n)
"""


def bfs_dist(graph, start):
    """无权图最短路 - O(V + E)"""
    q = [start]
    head = 0
    dist = {start: 0}

    while head < len(q):
        u = q[head]
        head += 1

        for v in graph.get(u, []):
            if v not in dist:
                dist[v] = dist[u] + 1
                q.append(v)

    return dist


def topo_sort(n, edges):
    """拓扑排序（Kahn）- O(V + E)"""
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


def multi_source_bfs(grid):
    """多源 BFS：求每个点到最近 1 的距离 - O(mn)"""
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    q = []
    head = 0

    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 1:
                dist[i][j] = 0
                q.append((i, j))

    while head < len(q):
        i, j = q[head]
        head += 1

        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and dist[ni][nj] == -1:
                dist[ni][nj] = dist[i][j] + 1
                q.append((ni, nj))

    return dist


if __name__ == '__main__':
    print("=" * 60)
    print("Python list + 头指针 队列操作完整示例")
    print("=" * 60)

    print("\n【1. 基本操作】")
    print("-" * 60)
    q = []
    head = 0
    q.append(3)
    q.append(5)
    q.append(7)
    print(f"入队 3, 5, 7 后: {q[head:]}")  # [3, 5, 7]
    print(f"当前队头: {q[head]}")  # 3
    x = q[head]
    head += 1
    print(f"出队: {x}")  # 3
    print(f"出队后的有效队列: {q[head:]}")  # [5, 7]

    print("\n【2. BFS 最短路】")
    print("-" * 60)
    graph = {
        0: [1, 2],
        1: [3],
        2: [3, 4],
        3: [5],
        4: [5],
        5: []
    }
    print(f"从 0 出发的最短距离: {bfs_dist(graph, 0)}")

    print("\n【3. 拓扑排序】")
    print("-" * 60)
    edges = [(0, 1), (0, 2), (1, 3), (2, 3)]
    print(f"拓扑序: {topo_sort(4, edges)}")  # [0, 1, 2, 3] 或 [0, 2, 1, 3]

    print("\n【4. 多源 BFS】")
    print("-" * 60)
    grid = [
        [0, 0, 1],
        [0, 0, 0],
        [1, 0, 0]
    ]
    dist = multi_source_bfs(grid)
    for row in dist:
        print(row)

    print("\n【5. 轻量回收前缀】")
    print("-" * 60)
    print("如果队列长期复用，可在适当时机切掉前缀废元素：")
    print("if head > 64 and head * 2 >= len(q):")
    print("    q = q[head:]")
    print("    head = 0")

    print("\n【6. 时间复杂度】")
    print("-" * 60)
    print("append(x)       - O(1)")
    print("q[head]         - O(1)")
    print("head += 1       - O(1)")
    print("head == len(q)  - O(1)")
    print("len(q) - head   - O(1)")

    print("\n【7. 实战提醒】")
    print("-" * 60)
    print("✓ 不想 import 时，这个写法很好用")
    print("✓ 判空写 head == len(q)")
    print("✓ 队头写 q[head]")
    print("✗ 不要退回去写 pop(0)")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
