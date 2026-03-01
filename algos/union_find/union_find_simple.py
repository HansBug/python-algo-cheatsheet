"""
并查集（Union-Find）极简版实现
支持 Python 3.7-3.14

核心原理：
- 使用数组存储每个节点的父节点
- 路径压缩：查找时将路径上所有节点直接连到根节点

这是最容易记忆的版本，只有 10 行核心代码！
"""


class UnionFind:
    """极简版并查集 - 最容易记忆"""

    def __init__(self, n):
        """初始化 n 个独立集合 - O(n)"""
        self.p = list(range(n))

    def find(self, x):
        """查找根节点（带路径压缩）- O(α(n)) ≈ O(1)"""
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])  # 路径压缩
        return self.p[x]

    def union(self, x, y):
        """合并两个集合 - O(α(n)) ≈ O(1)"""
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.p[rx] = ry
            return True  # 合并成功
        return False  # 已在同一集合

    def connected(self, x, y):
        """判断是否在同一集合 - O(α(n)) ≈ O(1)"""
        return self.find(x) == self.find(y)


if __name__ == '__main__':
    # 示例1：基本使用
    print("=== 示例1：基本使用 ===")
    uf = UnionFind(5)

    # 合并集合
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(1, 2)

    # 查询连通性
    print(f"0 和 3 连通: {uf.connected(0, 3)}")  # True
    print(f"0 和 4 连通: {uf.connected(0, 4)}")  # False

    # 示例2：检测环（无向图）
    print("\n=== 示例2：检测环 ===")
    uf2 = UnionFind(4)
    edges = [(0, 1), (1, 2), (2, 3), (3, 0)]

    has_cycle = False
    for x, y in edges:
        if not uf2.union(x, y):
            has_cycle = True
            print(f"发现环: 边 ({x}, {y})")
            break

    # 示例3：岛屿数量问题
    print("\n=== 示例3：岛屿数量 ===")
    grid = [
        ['1', '1', '0', '0', '0'],
        ['1', '1', '0', '0', '0'],
        ['0', '0', '1', '0', '0'],
        ['0', '0', '0', '1', '1']
    ]
    rows, cols = len(grid), len(grid[0])


    def get_id(i, j):
        return i * cols + j


    uf3 = UnionFind(rows * cols)
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == '1':
                # 与右边和下边的陆地合并
                for di, dj in [(0, 1), (1, 0)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] == '1':
                        uf3.union(get_id(i, j), get_id(ni, nj))

    # 统计陆地的连通分量数
    islands = len(set(uf3.find(get_id(i, j))
                      for i in range(rows)
                      for j in range(cols)
                      if grid[i][j] == '1'))
    print(f"岛屿数量: {islands}")  # 3
