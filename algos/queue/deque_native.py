"""
Python 队列（Queue）模板 - 基于 collections.deque

推荐写法：
- 入队：append(x)
- 出队：popleft()
- 看队头：q[0]

支持 Python 3.7-3.14，无第三方依赖

核心原理：
- 队列是先进先出（FIFO）
- deque 两端操作都是 O(1)
- 比 list.pop(0) 更快，也比手写 head 更省心
"""

from collections import deque


def bfs_dist(graph, start):
    """无权图最短路 - O(V + E)"""
    q = deque([start])
    dist = {start: 0}

    while q:
        u = q.popleft()
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


def multi_source_bfs(grid):
    """多源 BFS：求每个点到最近 1 的距离 - O(mn)"""
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


if __name__ == '__main__':
    print("=" * 60)
    print("Python deque 队列操作完整示例")
    print("=" * 60)

    print("\n【1. 基本操作】")
    print("-" * 60)
    q = deque()
    q.append(3)
    q.append(5)
    q.append(7)
    print(f"入队 3, 5, 7 后: {list(q)}")  # [3, 5, 7]
    print(f"当前队头: {q[0]}")  # 3
    print(f"出队: {q.popleft()}")  # 3
    print(f"出队后的队列: {list(q)}")  # [5, 7]

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

    print("\n【5. 时间复杂度】")
    print("-" * 60)
    print("append(x)   - O(1)")
    print("popleft()   - O(1)")
    print("q[0]        - O(1)")
    print("not q       - O(1)")
    print("len(q)      - O(1)")

    print("\n【6. 实战提醒】")
    print("-" * 60)
    print("✓ 队列优先用 deque")
    print("✓ BFS 先标记，再入队")
    print("✓ 拓扑排序用入度数组 + 队列")
    print("✗ 不要写 list.pop(0)")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
