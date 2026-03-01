"""
并查集（Union-Find）完整实现（带按秩合并）
支持 Python 3.7-3.14

核心原理：
- 使用数组存储每个节点的父节点
- 路径压缩：查找时将路径上所有节点直接连到根节点
- 按秩合并：合并时将较小的树连到较大的树上，保持树的平衡

按秩合并的优势：
- 保证树的高度尽可能小，理论上性能更优
- 在极端情况下（如链式合并）能避免退化
- 适合数据量特别大（n > 10^5）且对性能敏感的场景

实际笔试建议：
- 大多数情况下，极简版（无按秩合并）已经足够
- 只有在数据量特别大或追求极致性能时才需要按秩合并
- 优先使用 union_find_simple.py 中的极简版
"""


class UnionFind:
    """完整版并查集（带按秩合并）"""

    def __init__(self, n):
        """初始化 n 个独立集合 - O(n)"""
        self.p = list(range(n))  # 父节点数组
        self.r = [0] * n  # 秩（树的高度上界）

    def find(self, x):
        """查找根节点（带路径压缩）- O(α(n)) ≈ O(1)"""
        if self.p[x] != x:
            self.p[x] = self.find(self.p[x])  # 路径压缩
        return self.p[x]

    def union(self, x, y):
        """合并两个集合（按秩合并）- O(α(n)) ≈ O(1)"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False  # 已在同一集合

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
        """判断是否在同一集合 - O(α(n)) ≈ O(1)"""
        return self.find(x) == self.find(y)


if __name__ == '__main__':
    # 示例1：基本使用
    print("=== 示例1：完整版基本使用 ===")
    uf = UnionFind(5)

    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(1, 2)

    print(f"0 和 3 连通: {uf.connected(0, 3)}")  # True
    print(f"0 和 4 连通: {uf.connected(0, 4)}")  # False
    print(f"秩数组: {uf.r}")  # 可以看到树的高度信息

    # 示例2：按秩合并的效果
    print("\n=== 示例2：按秩合并的效果 ===")
    # 链式合并：0->1->2->3->4
    uf2 = UnionFind(5)
    for i in range(4):
        uf2.union(i, i + 1)
    print(f"完整版父节点数组: {uf2.p}")
    print(f"完整版秩数组: {uf2.r}")
