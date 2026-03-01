# 平衡树（Balanced Tree）笔试攻略

## 什么是平衡树？

平衡树是一种**自平衡的二叉搜索树**，通过维护树的平衡性来保证操作的高效性。

### 核心性质

1. **二叉搜索树性质**：左子树所有节点 < 根节点 < 右子树所有节点
2. **平衡性**：通过旋转等操作保持树的高度为 O(log n)
3. **动态维护**：插入、删除时自动调整结构保持平衡

### 常见的平衡树类型

| 类型             | 平衡条件    | 实现难度    | 笔试适用性   |
|----------------|---------|---------|---------|
| **二叉搜索树（BST）** | 无平衡保证   | ⭐ 简单    | ❌ 容易退化  |
| **Treap**      | 随机优先级   | ⭐⭐ 中等   | ✅ 推荐    |
| **AVL 树**      | 高度差 ≤ 1 | ⭐⭐⭐ 较难  | ⚠️ 旋转复杂 |
| **红黑树**        | 5 条性质   | ⭐⭐⭐⭐ 困难 | ❌ 不适合笔试 |

### 支持的操作

| 操作                      | 平衡树时间复杂度 | BST 最坏情况 |
|-------------------------|----------|----------|
| `insert`                | O(log n) | O(n)     |
| `delete`                | O(log n) | O(n)     |
| `search`                | O(log n) | O(n)     |
| `min/max`               | O(log n) | O(n)     |
| `predecessor/successor` | O(log n) | O(n)     |

## 平衡树适合解决什么问题？

平衡树特别适合处理以下场景：

1. **动态有序集合**：需要频繁插入、删除并保持有序
    - 例如：维护排行榜、动态中位数
    - 时间复杂度：O(log n) 插入/删除，O(log n) 查询第 k 小

2. **区间查询**：查找某个范围内的元素
    - 例如：查找 [L, R] 范围内的所有元素
    - 时间复杂度：O(log n + k)，k 为结果数量

3. **前驱后继查询**：快速找到比某个值小/大的最近元素
    - 例如：找到小于 x 的最大值、大于 x 的最小值
    - 时间复杂度：O(log n)

4. **动态排名**：查询某个元素的排名或第 k 小元素
    - 例如：实时统计排名变化
    - 时间复杂度：O(log n)（需要维护子树大小）

## 笔试场景建议

### 推荐策略

1. **优先使用 Treap**（树堆）
    - ✅ 代码简洁，容易记忆（约 40 行）
    - ✅ 性能稳定，期望 O(log n)，不会退化
    - ✅ 基于随机优先级，实现简单
    - ✅ 支持所有常用操作

2. **简单场景用 BST**
    - ✅ 代码最短（约 20 行）
    - ⚠️ 仅适用于数据随机或题目保证不退化
    - ❌ 最坏情况退化为链表 O(n)

3. **避免使用红黑树**
    - ❌ 代码量大（100+ 行），容易出错
    - ❌ 5 条性质和 4 种旋转难以记忆
    - ❌ 调试困难，笔试时间不够
    - ✅ 仅在面试官明确要求时使用

## 方案一：Treap（推荐）

### 什么是 Treap？

Treap = Tree + Heap，结合了二叉搜索树和堆的性质：

- **按值（key）维护 BST 性质**：左 < 根 < 右
- **按随机优先级（priority）维护堆性质**：父节点优先级 > 子节点

通过随机优先级，Treap 期望高度为 O(log n)，避免退化。

### 适合速记的 Treap 实现

```python
import random


class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()  # 随机优先级
        self.left = self.right = None


class Treap:
    def __init__(self):
        self.root = None

    def _rotate_right(self, node):
        """右旋 - O(1)"""
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node):
        """左旋 - O(1)"""
        right = node.right
        node.right = right.left
        right.left = node
        return right

    def insert(self, key):
        """插入元素 - O(log n)"""
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
        return node

    def delete(self, key):
        """删除元素 - O(log n)"""
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
        """查找元素 - O(log n)"""
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def min_value(self):
        """查找最小值 - O(log n)"""
        if not self.root:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def max_value(self):
        """查找最大值 - O(log n)"""
        if not self.root:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.key
```

### 使用示例

```python
# 创建 Treap
treap = Treap()

# 插入元素
for x in [5, 3, 7, 1, 9, 4]:
    treap.insert(x)

# 查找
print(treap.search(7))  # True
print(treap.search(6))  # False

# 最小值/最大值
print(treap.min_value())  # 1
print(treap.max_value())  # 9

# 删除
treap.delete(3)
print(treap.search(3))  # False
```

## 方案二：简单 BST（数据随机时可用）

### 为什么 BST 会退化？

二叉搜索树的性能完全依赖于树的**高度**。理想情况下，n 个节点的平衡树高度为 O(log n)，但 BST 没有平衡机制，可能退化为链表。

**退化的根本原因**：插入顺序决定树的结构

#### 退化场景 1：顺序插入

```
插入序列：[1, 2, 3, 4, 5]

结果：退化为右斜链表
    1
     \
      2
       \
        3
         \
          4
           \
            5

高度：O(n)，查找 5 需要 5 次比较
```

#### 退化场景 2：逆序插入

```
插入序列：[5, 4, 3, 2, 1]

结果：退化为左斜链表
        5
       /
      4
     /
    3
   /
  2
 /
1

高度：O(n)，查找 1 需要 5 次比较
```

#### 理想场景：随机插入

```
插入序列：[3, 1, 5, 2, 4]

结果：平衡的树
      3
     / \
    1   5
     \ /
     2 4

高度：O(log n)，查找任意元素最多 3 次比较
```

**性能对比**：

| 插入顺序  | 树的高度     | 查找时间     | 插入时间     |
|-------|----------|----------|----------|
| 随机    | O(log n) | O(log n) | O(log n) |
| 有序/逆序 | O(n)     | O(n)     | O(n)     |

**何时可以使用 BST**：

✅ 数据是随机打乱的（如洗牌后的数组）
✅ 题目明确说明数据随机分布
✅ 只需要临时存储，数据量小（< 100）

❌ 数据可能有序或接近有序
❌ 数据来自用户输入（可能被恶意构造）
❌ 需要稳定的性能保证

### 适合速记的 BST 实现

```python
class BSTNode:
    def __init__(self, key):
        self.key = key
        self.left = self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key):
        """插入元素 - 平均 O(log n)，最坏 O(n)"""
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
        """查找元素 - 平均 O(log n)，最坏 O(n)"""
        node = self.root
        while node:
            if key == node.key:
                return True
            node = node.left if key < node.key else node.right
        return False

    def min_value(self):
        """查找最小值"""
        if not self.root:
            return None
        node = self.root
        while node.left:
            node = node.left
        return node.key

    def max_value(self):
        """查找最大值"""
        if not self.root:
            return None
        node = self.root
        while node.right:
            node = node.right
        return node.key
```

### 使用示例

```python
bst = BST()
for x in [5, 3, 7, 1, 9, 4]:
    bst.insert(x)

print(bst.search(7))  # True
print(bst.min_value())  # 1
print(bst.max_value())  # 9
```

## 方案三：红黑树（仅供参考）

红黑树是工业级平衡树（C++ STL、Java TreeMap 的底层实现），但**不推荐在笔试中手写**。

### 红黑树的 5 条性质

1. 每个节点是红色或黑色
2. 根节点是黑色
3. 所有叶子节点（NIL）是黑色
4. 红色节点的子节点必须是黑色（不能有连续的红色节点）
5. 从任一节点到其叶子节点的所有路径包含相同数量的黑色节点

### 为什么不适合笔试？

- 插入/删除需要处理 **4 种旋转情况**
- 需要维护 **颜色标记** 和 **多层递归调整**
- 代码量 100+ 行，容易出错
- 调试困难，笔试时间不够

**建议**：如果面试官要求实现红黑树，可以说明 Treap 的优势，或者只实现插入操作。

## 常见题型速查

### 1. 动态维护有序集合

```python
# 使用 Treap 维护动态有序集合
treap = Treap()

# 插入元素
for x in nums:
    treap.insert(x)

# 查找是否存在
if treap.search(target):
    print("Found")

# 获取最小值/最大值
min_val = treap.min_value()
max_val = treap.max_value()
```

### 2. 查找前驱/后继

```python
def predecessor(treap, key):
    """查找小于 key 的最大值"""
    node = treap.root
    result = None
    while node:
        if node.key < key:
            result = node.key
            node = node.right  # 继续向右找更大的
        else:
            node = node.left
    return result


def successor(treap, key):
    """查找大于 key 的最小值"""
    node = treap.root
    result = None
    while node:
        if node.key > key:
            result = node.key
            node = node.left  # 继续向左找更小的
        else:
            node = node.right
    return result
```

### 3. 区间查询

```python
def range_query(treap, L, R):
    """查找 [L, R] 范围内的所有元素"""
    result = []

    def inorder(node):
        if not node:
            return
        if node.key > L:
            inorder(node.left)
        if L <= node.key <= R:
            result.append(node.key)
        if node.key < R:
            inorder(node.right)

    inorder(treap.root)
    return result
```

### 4. 第 K 小元素（需要维护子树大小）

```python
class TreapNodeWithSize:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()
        self.size = 1  # 子树大小
        self.left = self.right = None


def update_size(node):
    """更新子树大小"""
    if node:
        node.size = 1 + (node.left.size if node.left else 0) +
        (node.right.size if node.right else 0)


def kth_smallest(node, k):
    """查找第 k 小元素（k 从 1 开始）"""
    if not node:
        return None

    left_size = node.left.size if node.left else 0

    if k == left_size + 1:
        return node.key
    elif k <= left_size:
        return kth_smallest(node.left, k)
    else:
        return kth_smallest(node.right, k - left_size - 1)
```

## 实战技巧总结

✅ **笔试首选 Treap**：代码简洁（40 行），性能稳定，不会退化

✅ **数据随机时用 BST**：代码最短（20 行），但要确保数据不会导致退化

✅ **避免手写红黑树**：代码量大（100+ 行），容易出错，不适合笔试

✅ **需要排名功能**：在节点中维护 `size` 字段（子树大小）

✅ **旋转操作记忆**：右旋提升左子节点，左旋提升右子节点

✅ **Treap 核心思想**：随机优先级 + 旋转维护堆性质 = 期望平衡

✅ **调试技巧**：先实现中序遍历，验证 BST 性质是否正确

## 参考资料

- [bst_simple.py](bst_simple.py) - 简单二叉搜索树实现（容易退化）
- [treap.py](treap.py) - Treap 完整实现（推荐）
- [rbtree.py](rbtree.py) - 红黑树完整实现（仅供参考）

**推荐阅读顺序**：

1. 先看本 README 了解基本概念和策略
2. 参考 `treap.py` 学习 Treap 实现（笔试推荐）
3. 参考 `bst_simple.py` 了解最简单的 BST（数据随机时可用）
4. 如果面试要求，参考 `rbtree.py` 了解红黑树（不推荐笔试使用）
