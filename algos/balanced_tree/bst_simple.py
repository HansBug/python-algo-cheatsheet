"""
简单二叉搜索树（BST）实现

适用场景：
- 数据随机分布，不会导致树退化
- 题目保证数据不会导致最坏情况
- 需要最简洁的代码实现

注意：最坏情况下会退化为链表，时间复杂度 O(n)

支持 Python 3.7+
"""


class BSTNode:
    """二叉搜索树节点"""

    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


class BST:
    """简单二叉搜索树实现"""

    def __init__(self):
        self.root = None

    def insert(self, key):
        """
        插入元素
        时间复杂度：平均 O(log n)，最坏 O(n)
        """
        if not self.root:
            self.root = BSTNode(key)
            return

        node = self.root
        while True:
            if key < node.key:
                if not node.left:
                    node.left = BSTNode(key)
                    break
                node = node.left
            elif key > node.key:
                if not node.right:
                    node.right = BSTNode(key)
                    break
                node = node.right
            else:
                break  # 重复元素，不插入

    def search(self, key):
        """
        查找元素
        时间复杂度：平均 O(log n)，最坏 O(n)
        """
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def delete(self, key):
        """
        删除元素
        时间复杂度：平均 O(log n)，最坏 O(n)
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
            # 找到目标节点
            if not node.left:
                return node.right
            if not node.right:
                return node.left

            # 有两个子节点：找右子树的最小值替换
            min_node = node.right
            while min_node.left:
                min_node = min_node.left

            node.key = min_node.key
            node.right = self._delete(node.right, min_node.key)

        return node

    def min_value(self):
        """
        查找最小值
        时间复杂度：平均 O(log n)，最坏 O(n)
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
        时间复杂度：平均 O(log n)，最坏 O(n)
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
        时间复杂度：平均 O(log n)，最坏 O(n)
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
        时间复杂度：平均 O(log n)，最坏 O(n)
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


if __name__ == '__main__':
    # 示例 1：基本操作
    print("=== 示例 1：基本操作 ===")
    bst = BST()

    # 插入元素
    for x in [5, 3, 7, 1, 9, 4, 6]:
        bst.insert(x)

    # 查找
    print(f"查找 7: {bst.search(7)}")  # True
    print(f"查找 8: {bst.search(8)}")  # False

    # 最小值/最大值
    print(f"最小值: {bst.min_value()}")  # 1
    print(f"最大值: {bst.max_value()}")  # 9

    # 中序遍历（有序输出）
    print(f"中序遍历: {bst.inorder()}")  # [1, 3, 4, 5, 6, 7, 9]

    # 示例 2：前驱和后继
    print("\n=== 示例 2：前驱和后继 ===")
    print(f"5 的前驱: {bst.predecessor(5)}")  # 4
    print(f"5 的后继: {bst.successor(5)}")  # 6
    print(f"1 的前驱: {bst.predecessor(1)}")  # None
    print(f"9 的后继: {bst.successor(9)}")  # None

    # 示例 3：删除操作
    print("\n=== 示例 3：删除操作 ===")
    bst.delete(3)
    print(f"删除 3 后: {bst.inorder()}")  # [1, 4, 5, 6, 7, 9]
    print(f"查找 3: {bst.search(3)}")  # False

    bst.delete(5)
    print(f"删除 5 后: {bst.inorder()}")  # [1, 4, 6, 7, 9]

    # 示例 4：退化情况演示
    print("\n=== 示例 4：退化情况演示 ===")
    bst_degenerate = BST()
    # 按顺序插入会导致退化为链表
    for x in [1, 2, 3, 4, 5]:
        bst_degenerate.insert(x)

    print(f"顺序插入 [1,2,3,4,5]: {bst_degenerate.inorder()}")
    print("注意：此时树已退化为链表，查找性能降为 O(n)")

    # 示例 5：区间查询
    print("\n=== 示例 5：区间查询 ===")


    def range_query(bst, L, R):
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

        _inorder(bst.root)
        return result


    bst2 = BST()
    for x in [5, 3, 7, 1, 9, 4, 6, 8]:
        bst2.insert(x)

    print(f"查找 [3, 7] 范围: {range_query(bst2, 3, 7)}")  # [3, 4, 5, 6, 7]
    print(f"查找 [4, 8] 范围: {range_query(bst2, 4, 8)}")  # [4, 5, 6, 7, 8]
