"""
红黑树（Red-Black Tree）实现 - 仅供参考

警告：红黑树代码量大（100+ 行），实现复杂，不推荐在笔试中使用！
      笔试推荐使用 Treap（treap.py）

红黑树的 5 条性质：
1. 每个节点是红色或黑色
2. 根节点是黑色
3. 所有叶子节点（NIL）是黑色
4. 红色节点的子节点必须是黑色
5. 从任一节点到其叶子节点的所有路径包含相同数量的黑色节点

重复值处理：
本实现采用"允许重复节点"的方案，重复值会被插入到右子树。
这是最简单的方案，适合作为科普展示。实际应用中可以考虑使用 count 字段。

支持 Python 3.7+
"""


class RBNode:
    """红黑树节点"""

    def __init__(self, key, color='R'):
        self.key = key
        self.color = color  # 'R' 或 'B'
        self.left = None
        self.right = None
        self.parent = None


class RBTree:
    """红黑树实现"""

    def __init__(self):
        # NIL 节点（哨兵节点）
        self.NIL = RBNode(None, 'B')
        self.root = self.NIL

    def _rotate_left(self, x):
        """
        左旋
            x                y
           / \              / \
          A   y     =>     x   C
             / \          / \
            B   C        A   B
        """
        y = x.right
        x.right = y.left

        if y.left != self.NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def _rotate_right(self, y):
        """
        右旋
              y              x
             / \            / \
            x   C   =>     A   y
           / \                / \
          A   B              B   C
        """
        x = y.left
        y.left = x.right

        if x.right != self.NIL:
            x.right.parent = y

        x.parent = y.parent

        if y.parent is None:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        x.right = y
        y.parent = x

    def insert(self, key):
        """
        插入元素
        时间复杂度：O(log n)
        """
        # 创建新节点（默认红色）
        node = RBNode(key, 'R')
        node.left = self.NIL
        node.right = self.NIL

        # BST 插入
        parent = None
        current = self.root

        while current != self.NIL:
            parent = current
            if node.key < current.key:
                current = current.left
            else:
                # 重复元素插入到右子树（简单方案）
                current = current.right

        node.parent = parent

        if parent is None:
            self.root = node
        elif node.key < parent.key:
            parent.left = node
        else:
            parent.right = node

        # 修复红黑树性质
        self._insert_fixup(node)

    def _insert_fixup(self, z):
        """
        插入后修复红黑树性质
        处理 4 种情况
        """
        while z.parent and z.parent.color == 'R':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right  # 叔叔节点

                # 情况 1：叔叔是红色
                if y.color == 'R':
                    z.parent.color = 'B'
                    y.color = 'B'
                    z.parent.parent.color = 'R'
                    z = z.parent.parent
                else:
                    # 情况 2：叔叔是黑色，z 是右子节点
                    if z == z.parent.right:
                        z = z.parent
                        self._rotate_left(z)

                    # 情况 3：叔叔是黑色，z 是左子节点
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self._rotate_right(z.parent.parent)
            else:
                y = z.parent.parent.left  # 叔叔节点

                # 情况 1：叔叔是红色
                if y.color == 'R':
                    z.parent.color = 'B'
                    y.color = 'B'
                    z.parent.parent.color = 'R'
                    z = z.parent.parent
                else:
                    # 情况 2：叔叔是黑色，z 是左子节点
                    if z == z.parent.left:
                        z = z.parent
                        self._rotate_right(z)

                    # 情况 3：叔叔是黑色，z 是右子节点
                    z.parent.color = 'B'
                    z.parent.parent.color = 'R'
                    self._rotate_left(z.parent.parent)

        self.root.color = 'B'

    def search(self, key):
        """
        查找元素
        时间复杂度：O(log n)
        """
        node = self.root
        while node != self.NIL:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def min_value(self):
        """
        查找最小值
        时间复杂度：O(log n)
        """
        if self.root == self.NIL:
            return None
        node = self.root
        while node.left != self.NIL:
            node = node.left
        return node.key

    def max_value(self):
        """
        查找最大值
        时间复杂度：O(log n)
        """
        if self.root == self.NIL:
            return None
        node = self.root
        while node.right != self.NIL:
            node = node.right
        return node.key

    def inorder(self):
        """
        中序遍历（返回有序列表）
        时间复杂度：O(n)
        """
        result = []

        def _inorder(node):
            if node != self.NIL:
                _inorder(node.left)
                result.append(node.key)
                _inorder(node.right)

        _inorder(self.root)
        return result

    def _transplant(self, u, v):
        """用 v 替换 u"""
        if u.parent is None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, node):
        """找到子树的最小节点"""
        while node.left != self.NIL:
            node = node.left
        return node

    def delete(self, key):
        """
        删除元素
        时间复杂度：O(log n)
        注意：删除操作非常复杂，需要处理多种情况
        """
        # 查找要删除的节点
        z = self.root
        while z != self.NIL:
            if key == z.key:
                break
            z = z.left if key < z.key else z.right

        if z == self.NIL:
            return  # 未找到

        y = z
        y_original_color = y.color

        if z.left == self.NIL:
            x = z.right
            self._transplant(z, z.right)
        elif z.right == self.NIL:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y.parent == z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color

        if y_original_color == 'B':
            self._delete_fixup(x)

    def _delete_fixup(self, x):
        """
        删除后修复红黑树性质
        处理 4 种情况（非常复杂）
        """
        while x != self.root and x.color == 'B':
            if x == x.parent.left:
                w = x.parent.right

                # 情况 1：兄弟是红色
                if w.color == 'R':
                    w.color = 'B'
                    x.parent.color = 'R'
                    self._rotate_left(x.parent)
                    w = x.parent.right

                # 情况 2：兄弟是黑色，两个子节点都是黑色
                if w.left.color == 'B' and w.right.color == 'B':
                    w.color = 'R'
                    x = x.parent
                else:
                    # 情况 3：兄弟是黑色，右子节点是黑色
                    if w.right.color == 'B':
                        w.left.color = 'B'
                        w.color = 'R'
                        self._rotate_right(w)
                        w = x.parent.right

                    # 情况 4：兄弟是黑色，右子节点是红色
                    w.color = x.parent.color
                    x.parent.color = 'B'
                    w.right.color = 'B'
                    self._rotate_left(x.parent)
                    x = self.root
            else:
                w = x.parent.left

                if w.color == 'R':
                    w.color = 'B'
                    x.parent.color = 'R'
                    self._rotate_right(x.parent)
                    w = x.parent.left

                if w.right.color == 'B' and w.left.color == 'B':
                    w.color = 'R'
                    x = x.parent
                else:
                    if w.left.color == 'B':
                        w.right.color = 'B'
                        w.color = 'R'
                        self._rotate_left(w)
                        w = x.parent.left

                    w.color = x.parent.color
                    x.parent.color = 'B'
                    w.left.color = 'B'
                    self._rotate_right(x.parent)
                    x = self.root

        x.color = 'B'


if __name__ == '__main__':
    print("=" * 60)
    print("警告：红黑树实现复杂，不推荐在笔试中使用！")
    print("推荐使用 Treap（见 treap.py）")
    print("=" * 60)

    # 示例 1：基本操作
    print("\n=== 示例 1：基本操作 ===")
    rbt = RBTree()

    # 插入元素
    for x in [7, 3, 18, 10, 22, 8, 11, 26]:
        rbt.insert(x)

    # 查找
    print(f"查找 10: {rbt.search(10)}")  # True
    print(f"查找 15: {rbt.search(15)}")  # False

    # 最小值/最大值
    print(f"最小值: {rbt.min_value()}")  # 3
    print(f"最大值: {rbt.max_value()}")  # 26

    # 中序遍历
    print(f"中序遍历: {rbt.inorder()}")  # [3, 7, 8, 10, 11, 18, 22, 26]

    # 示例 2：顺序插入不会退化
    print("\n=== 示例 2：顺序插入不会退化 ===")
    rbt2 = RBTree()
    for x in range(1, 11):
        rbt2.insert(x)

    print(f"顺序插入 [1-10]: {rbt2.inorder()}")
    print("红黑树通过旋转和重新着色保持平衡")

    # 示例 3：删除操作
    print("\n=== 示例 3：删除操作 ===")
    rbt3 = RBTree()
    for x in [7, 3, 18, 10, 22, 8, 11, 26]:
        rbt3.insert(x)

    print(f"删除前: {rbt3.inorder()}")
    rbt3.delete(18)
    print(f"删除 18 后: {rbt3.inorder()}")
    rbt3.delete(11)
    print(f"删除 11 后: {rbt3.inorder()}")

    # 示例 4：重复值处理
    print("\n=== 示例 4：重复值处理 ===")
    rbt4 = RBTree()

    # 插入重复值
    for x in [5, 3, 7, 3, 5, 3]:
        rbt4.insert(x)

    print(f"插入 [5, 3, 7, 3, 5, 3]")
    print(f"中序遍历: {rbt4.inorder()}")  # [3, 3, 3, 5, 5, 7]
    print("注意：重复值被插入到右子树，会在中序遍历中出现多次")

    # 删除重复值
    rbt4.delete(3)
    print(f"\n删除一个 3 后:")
    print(f"中序遍历: {rbt4.inorder()}")  # [3, 3, 5, 5, 7]

    rbt4.delete(3)
    rbt4.delete(3)
    print(f"\n再删除两个 3 后:")
    print(f"中序遍历: {rbt4.inorder()}")  # [5, 5, 7]
    print(f"查找 3: {rbt4.search(3)}")  # False

    # 示例 5：性能对比说明
    print("\n=== 示例 5：为什么不推荐在笔试中使用红黑树？ ===")
    print("1. 代码量大：本文件 300+ 行，Treap 只需 100 行")
    print("2. 实现复杂：需要处理 8 种旋转情况（插入 4 种 + 删除 4 种）")
    print("3. 容易出错：颜色维护、NIL 节点处理、父指针更新等")
    print("4. 调试困难：笔试时间不够排查问题")
    print("\n推荐方案：")
    print("- 笔试首选：Treap（代码简洁，性能稳定）")
    print("- 数据随机：简单 BST（代码最短）")
    print("- 工业应用：红黑树（C++ STL、Java TreeMap 的选择）")
