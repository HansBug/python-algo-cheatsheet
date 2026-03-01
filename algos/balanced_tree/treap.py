"""
Treap（树堆）实现 - 笔试推荐

核心思想：
- 按值（key）维护二叉搜索树性质
- 按随机优先级（priority）维护堆性质
- 通过随机化避免退化，期望高度 O(log n)

优势：
- 代码简洁（约 40 行核心代码）
- 性能稳定，不会退化
- 容易理解和记忆

支持 Python 3.7+
"""

import random


class TreapNode:
    """Treap 节点"""

    def __init__(self, key):
        self.key = key
        self.priority = random.random()  # 随机优先级
        self.left = None
        self.right = None


class Treap:
    """Treap 实现"""

    def __init__(self):
        self.root = None

    def _rotate_right(self, node):
        """
        右旋：提升左子节点
              y                x
             / \              / \
            x   C    =>      A   y
           / \                  / \
          A   B                B   C
        时间复杂度：O(1)
        """
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node):
        """
        左旋：提升右子节点
            x                  y
           / \                / \
          A   y      =>      x   C
             / \            / \
            B   C          A   B
        时间复杂度：O(1)
        """
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def insert(self, key):
        """
        插入元素
        时间复杂度：期望 O(log n)
        """
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return TreapNode(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
            # 维护堆性质：如果左子节点优先级更高，右旋
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert(node.right, key)
            # 维护堆性质：如果右子节点优先级更高，左旋
            if node.right.priority > node.priority:
                node = self._rotate_left(node)
        # key == node.key: 重复元素，不插入

        return node

    def delete(self, key):
        """
        删除元素
        时间复杂度：期望 O(log n)
        """
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node:
            return None

        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # 找到目标节点，通过旋转将其下沉到叶子节点
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            # 将优先级低的子节点旋转上来
            if node.left.priority > node.right.priority:
                node = self._rotate_right(node)
                node.right = self._delete(node.right, key)
            else:
                node = self._rotate_left(node)
                node.left = self._delete(node.left, key)

        return node

    def search(self, key):
        """
        查找元素
        时间复杂度：期望 O(log n)
        """
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def min_value(self):
        """
        查找最小值
        时间复杂度：期望 O(log n)
        """
        if not self.root:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def max_value(self):
        """
        查找最大值
        时间复杂度：期望 O(log n)
        """
        if not self.root:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.key

    def predecessor(self, key):
        """
        查找前驱（小于 key 的最大值）
        时间复杂度：期望 O(log n)
        """
        node = self.root
        result = None
        while node:
            if node.key < key:
                result = node.key
                node = node.right
            else:
                node = node.left
        return result

    def successor(self, key):
        """
        查找后继（大于 key 的最小值）
        时间复杂度：期望 O(log n)
        """
        node = self.root
        result = None
        while node:
            if node.key > key:
                result = node.key
                node = node.left
            else:
                node = node.right
        return result

    def inorder(self):
        """
        中序遍历（返回有序列表）
        时间复杂度：O(n)
        """
        result = []

        def _inorder(node):
            if not node:
                return
            _inorder(node.left)
            result.append(node.key)
            _inorder(node.right)

        _inorder(self.root)
        return result


class TreapWithSize:
    """带子树大小的 Treap（支持排名查询）"""

    class Node:
        def __init__(self, key):
            self.key = key
            self.priority = random.random()
            self.size = 1  # 子树大小
            self.left = None
            self.right = None

    def __init__(self):
        self.root = None

    def _get_size(self, node):
        return node.size if node else 0

    def _update_size(self, node):
        """更新子树大小"""
        if node:
            node.size = 1 + self._get_size(node.left) + self._get_size(node.right)

    def _rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node
        self._update_size(node)
        self._update_size(left)
        return left

    def _rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node
        self._update_size(node)
        self._update_size(right)
        return right

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node:
            return self.Node(key)

        if key < node.key:
            node.left = self._insert(node.left, key)
            if node.left.priority > node.priority:
                node = self._rotate_right(node)
        elif key > node.key:
            node.right = self._insert(node.right, key)
            if node.right.priority > node.priority:
                node = self._rotate_left(node)

        self._update_size(node)
        return node

    def kth_smallest(self, k):
        """
        查找第 k 小元素（k 从 1 开始）
        时间复杂度：期望 O(log n)
        """
        return self._kth_smallest(self.root, k)

    def _kth_smallest(self, node, k):
        if not node:
            return None

        left_size = self._get_size(node.left)

        if k == left_size + 1:
            return node.key
        elif k <= left_size:
            return self._kth_smallest(node.left, k)
        else:
            return self._kth_smallest(node.right, k - left_size - 1)

    def rank(self, key):
        """
        查询元素的排名（从 1 开始）
        时间复杂度：期望 O(log n)
        """
        return self._rank(self.root, key)

    def _rank(self, node, key):
        if not node:
            return 0

        if key < node.key:
            return self._rank(node.left, key)
        elif key > node.key:
            return 1 + self._get_size(node.left) + self._rank(node.right, key)
        else:
            return self._get_size(node.left) + 1


if __name__ == '__main__':
    # 示例 1：基本操作
    print("=== 示例 1：基本 Treap 操作 ===")
    treap = Treap()

    # 插入元素
    for x in [5, 3, 7, 1, 9, 4, 6]:
        treap.insert(x)

    # 查找
    print(f"查找 7: {treap.search(7)}")  # True
    print(f"查找 8: {treap.search(8)}")  # False

    # 最小值/最大值
    print(f"最小值: {treap.min_value()}")  # 1
    print(f"最大值: {treap.max_value()}")  # 9

    # 中序遍历
    print(f"中序遍历: {treap.inorder()}")  # [1, 3, 4, 5, 6, 7, 9]

    # 示例 2：前驱和后继
    print("\n=== 示例 2：前驱和后继 ===")
    print(f"5 的前驱: {treap.predecessor(5)}")  # 4
    print(f"5 的后继: {treap.successor(5)}")  # 6
    print(f"1 的前驱: {treap.predecessor(1)}")  # None
    print(f"9 的后继: {treap.successor(9)}")  # None

    # 示例 3：删除操作
    print("\n=== 示例 3：删除操作 ===")
    treap.delete(3)
    print(f"删除 3 后: {treap.inorder()}")  # [1, 4, 5, 6, 7, 9]
    print(f"查找 3: {treap.search(3)}")  # False

    treap.delete(5)
    print(f"删除 5 后: {treap.inorder()}")  # [1, 4, 6, 7, 9]

    # 示例 4：顺序插入不会退化
    print("\n=== 示例 4：顺序插入不会退化 ===")
    treap2 = Treap()
    for x in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        treap2.insert(x)

    print(f"顺序插入 [1-10]: {treap2.inorder()}")
    print("注意：由于随机优先级，树不会退化为链表")

    # 示例 5：带排名的 Treap
    print("\n=== 示例 5：带排名的 Treap ===")
    treap_with_size = TreapWithSize()

    for x in [5, 3, 7, 1, 9, 4, 6]:
        treap_with_size.insert(x)

    # 查找第 k 小元素
    print(f"第 1 小: {treap_with_size.kth_smallest(1)}")  # 1
    print(f"第 3 小: {treap_with_size.kth_smallest(3)}")  # 4
    print(f"第 5 小: {treap_with_size.kth_smallest(5)}")  # 6

    # 查询排名
    print(f"元素 5 的排名: {treap_with_size.rank(5)}")  # 4
    print(f"元素 1 的排名: {treap_with_size.rank(1)}")  # 1
    print(f"元素 9 的排名: {treap_with_size.rank(9)}")  # 7

    # 示例 6：区间查询
    print("\n=== 示例 6：区间查询 ===")


    def range_query(treap, L, R):
        """查找 [L, R] 范围内的所有元素"""
        result = []

        def _inorder(node):
            if not node:
                return
            if node.key > L:
                _inorder(node.left)
            if L <= node.key <= R:
                result.append(node.key)
            if node.key < R:
                _inorder(node.right)

        _inorder(treap.root)
        return result


    treap3 = Treap()
    for x in [5, 3, 7, 1, 9, 4, 6, 8]:
        treap3.insert(x)

    print(f"查找 [3, 7] 范围: {range_query(treap3, 3, 7)}")  # [3, 4, 5, 6, 7]
    print(f"查找 [4, 8] 范围: {range_query(treap3, 4, 8)}")  # [4, 5, 6, 7, 8]
