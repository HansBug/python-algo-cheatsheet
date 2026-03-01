"""
二分图匹配 - 常见题型完整示例
适用于 Python 3.7+

包含以下题型：
1. 基础任务分配
2. 棋盘染色问题
3. 最小点覆盖
4. 最大独立集
5. 完美匹配判断
"""


class Hungarian:
    """匈牙利算法实现"""

    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.graph = [[] for _ in range(n)]
        self.match = [-1] * m

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def dfs(self, u, visited):
        for v in self.graph[u]:
            if visited[v]:
                continue
            visited[v] = True
            if self.match[v] == -1 or self.dfs(self.match[v], visited):
                self.match[v] = u
                return True
        return False

    def max_matching(self):
        count = 0
        for i in range(self.n):
            visited = [False] * self.m
            if self.dfs(i, visited):
                count += 1
        return count

    def get_matching(self):
        result = []
        for j in range(self.m):
            if self.match[j] != -1:
                result.append((self.match[j], j))
        return result


# ============ 题型 1：基础任务分配 ============

def solve_task_assignment(n_workers, n_tasks, can_do):
    """
    任务分配问题
    n_workers: 工人数量
    n_tasks: 任务数量
    can_do: can_do[i] 是工人 i 可以完成的任务列表
    返回：最大可完成的任务数
    """
    h = Hungarian(n_workers, n_tasks)
    for worker, tasks in enumerate(can_do):
        for task in tasks:
            h.add_edge(worker, task)
    return h.max_matching()


# ============ 题型 2：棋盘染色问题 ============

def solve_chessboard_placement(n, forbidden):
    """
    在 n×n 棋盘上放置最多的车，使其互不攻击
    forbidden: 禁止放置的格子列表 [(r, c), ...]

    思路：将棋盘黑白染色，黑格和白格分别作为二分图的两侧
    相邻的黑白格子之间连边，求最大匹配
    """
    forbidden_set = set(forbidden)
    black_cells = []
    white_cells = []

    # 黑白染色
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
            # 判断是否相邻（上下左右）
            if abs(r1 - r2) + abs(c1 - c2) == 1:
                h.add_edge(i, j)

    return h.max_matching()


def solve_chessboard_domino(n, m, forbidden):
    """
    在 n×m 棋盘上放置最多的多米诺骨牌（1×2）
    forbidden: 禁止放置的格子列表 [(r, c), ...]

    思路：每个多米诺骨牌覆盖一个黑格和一个白格
    问题等价于求最大匹配
    """
    forbidden_set = set(forbidden)
    black_cells = []
    white_cells = []

    for r in range(n):
        for c in range(m):
            if (r, c) not in forbidden_set:
                if (r + c) % 2 == 0:
                    black_cells.append((r, c))
                else:
                    white_cells.append((r, c))

    h = Hungarian(len(black_cells), len(white_cells))
    for i, (r1, c1) in enumerate(black_cells):
        for j, (r2, c2) in enumerate(white_cells):
            if abs(r1 - r2) + abs(c1 - c2) == 1:
                h.add_edge(i, j)

    return h.max_matching()


# ============ 题型 3：最小点覆盖 ============

def min_vertex_cover(n, m, edges):
    """
    最小点覆盖问题（König 定理）
    n: 左侧顶点数
    m: 右侧顶点数
    edges: 边列表 [(u, v), ...]
    返回：最小点覆盖数

    König 定理：二分图的最小点覆盖 = 最大匹配数
    """
    h = Hungarian(n, m)
    for u, v in edges:
        h.add_edge(u, v)
    return h.max_matching()


# ============ 题型 4：最大独立集 ============

def max_independent_set(n, m, edges):
    """
    最大独立集问题
    n: 左侧顶点数
    m: 右侧顶点数
    edges: 边列表 [(u, v), ...]
    返回：最大独立集大小

    定理：最大独立集 = 总顶点数 - 最大匹配数
    """
    h = Hungarian(n, m)
    for u, v in edges:
        h.add_edge(u, v)
    return n + m - h.max_matching()


# ============ 题型 5：完美匹配判断 ============

def has_perfect_matching(n, m, edges):
    """
    判断是否存在完美匹配
    n: 左侧顶点数
    m: 右侧顶点数
    edges: 边列表 [(u, v), ...]
    返回：是否存在完美匹配
    """
    if n != m:
        return False

    h = Hungarian(n, m)
    for u, v in edges:
        h.add_edge(u, v)

    return h.max_matching() == n


# ============ 题型 6：相亲配对问题 ============

def solve_dating_matching(boys, girls, preferences):
    """
    相亲配对问题
    boys: 男生列表
    girls: 女生列表
    preferences: preferences[i] 是男生 i 喜欢的女生列表
    返回：最大配对数和配对结果
    """
    n_boys = len(boys)
    n_girls = len(girls)

    h = Hungarian(n_boys, n_girls)
    for boy_id, girl_ids in enumerate(preferences):
        for girl_id in girl_ids:
            h.add_edge(boy_id, girl_id)

    max_match = h.max_matching()
    matching = h.get_matching()

    # 转换为实际名字
    result = []
    for boy_id, girl_id in matching:
        result.append((boys[boy_id], girls[girl_id]))

    return max_match, result


if __name__ == '__main__':
    print("=" * 50)
    print("题型 1：基础任务分配")
    print("=" * 50)
    # 3 个工人，4 个任务
    can_do = [
        [0, 1],  # 工人 0 可以做任务 0, 1
        [1, 2],  # 工人 1 可以做任务 1, 2
        [2, 3]  # 工人 2 可以做任务 2, 3
    ]
    result = solve_task_assignment(3, 4, can_do)
    print(f"最大可完成任务数: {result}")

    print("\n" + "=" * 50)
    print("题型 2：棋盘染色问题 - 放置车")
    print("=" * 50)
    # 4×4 棋盘，禁止在 (1, 1) 和 (2, 2) 放置
    forbidden = [(1, 1), (2, 2)]
    result = solve_chessboard_placement(4, forbidden)
    print(f"最多可放置的车数量: {result}")

    print("\n" + "=" * 50)
    print("题型 2：棋盘染色问题 - 放置多米诺骨牌")
    print("=" * 50)
    # 3×4 棋盘，禁止在 (0, 0) 和 (2, 3) 放置
    forbidden = [(0, 0), (2, 3)]
    result = solve_chessboard_domino(3, 4, forbidden)
    print(f"最多可放置的多米诺骨牌数量: {result}")

    print("\n" + "=" * 50)
    print("题型 3：最小点覆盖")
    print("=" * 50)
    edges = [(0, 0), (0, 1), (1, 1), (2, 2), (3, 2), (3, 3)]
    result = min_vertex_cover(4, 4, edges)
    print(f"边列表: {edges}")
    print(f"最小点覆盖: {result}")

    print("\n" + "=" * 50)
    print("题型 4：最大独立集")
    print("=" * 50)
    result = max_independent_set(4, 4, edges)
    print(f"边列表: {edges}")
    print(f"最大独立集: {result}")

    print("\n" + "=" * 50)
    print("题型 5：完美匹配判断")
    print("=" * 50)
    # 测试 1：存在完美匹配
    edges1 = [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 2)]
    result1 = has_perfect_matching(3, 3, edges1)
    print(f"边列表: {edges1}")
    print(f"是否存在完美匹配: {result1}")

    # 测试 2：不存在完美匹配
    edges2 = [(0, 0), (1, 0)]
    result2 = has_perfect_matching(3, 3, edges2)
    print(f"\n边列表: {edges2}")
    print(f"是否存在完美匹配: {result2}")

    print("\n" + "=" * 50)
    print("题型 6：相亲配对问题")
    print("=" * 50)
    boys = ["张三", "李四", "王五"]
    girls = ["小红", "小明", "小芳"]
    preferences = [
        [0, 1],  # 张三喜欢小红、小明
        [1, 2],  # 李四喜欢小明、小芳
        [0, 2]  # 王五喜欢小红、小芳
    ]
    max_match, matching = solve_dating_matching(boys, girls, preferences)
    print(f"最大配对数: {max_match}")
    print(f"配对结果: {matching}")
