"""
二分图匹配 - 匈牙利算法基础实现
适用于 Python 3.7+

核心原理：
1. 通过 DFS 寻找增广路径
2. 每找到一条增广路径，匹配数 +1
3. 时间复杂度：O(V × E)
"""


class Hungarian:
    def __init__(self, n, m):
        """
        初始化二分图
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
        """
        DFS 寻找增广路径
        u: 当前左侧顶点
        visited: 本轮 DFS 中右侧顶点的访问状态
        返回：是否找到增广路径
        """
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
        """
        求最大匹配数
        时间复杂度：O(V × E)
        """
        count = 0
        for i in range(self.n):
            visited = [False] * self.m  # 每次 DFS 都需要新的 visited
            if self.dfs(i, visited):
                count += 1
        return count

    def get_matching(self):
        """
        返回匹配结果
        返回：[(左侧顶点, 右侧顶点), ...]
        """
        result = []
        for j in range(self.m):
            if self.match[j] != -1:
                result.append((self.match[j], j))
        return result


if __name__ == '__main__':
    # 示例 1：基础匹配问题
    print("=== 示例 1：任务分配 ===")
    # 3 个人，4 个任务
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

    max_match = h.max_matching()
    print(f"最大匹配数: {max_match}")
    print(f"匹配结果: {h.get_matching()}")

    # 示例 2：完美匹配判断
    print("\n=== 示例 2：完美匹配判断 ===")
    h2 = Hungarian(3, 3)
    h2.add_edge(0, 0)
    h2.add_edge(0, 1)
    h2.add_edge(1, 1)
    h2.add_edge(1, 2)
    h2.add_edge(2, 0)
    h2.add_edge(2, 2)

    max_match2 = h2.max_matching()
    is_perfect = max_match2 == min(3, 3)
    print(f"最大匹配数: {max_match2}")
    print(f"是否完美匹配: {is_perfect}")
    print(f"匹配结果: {h2.get_matching()}")

    # 示例 3：最小点覆盖（König 定理）
    print("\n=== 示例 3：最小点覆盖 ===")
    # 构建一个简单的二分图
    h3 = Hungarian(4, 4)
    edges = [(0, 0), (0, 1), (1, 1), (2, 2), (3, 2), (3, 3)]
    for u, v in edges:
        h3.add_edge(u, v)

    max_match3 = h3.max_matching()
    print(f"边列表: {edges}")
    print(f"最大匹配数: {max_match3}")
    print(f"最小点覆盖: {max_match3}")  # König 定理

    # 示例 4：最大独立集
    print("\n=== 示例 4：最大独立集 ===")
    n, m = 4, 4
    h4 = Hungarian(n, m)
    for u, v in edges:
        h4.add_edge(u, v)

    max_match4 = h4.max_matching()
    max_independent = n + m - max_match4
    print(f"总顶点数: {n + m}")
    print(f"最大匹配数: {max_match4}")
    print(f"最大独立集: {max_independent}")
