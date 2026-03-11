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

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [Hello 算法：二叉搜索树](https://www.hello-algo.com/chapter_tree/binary_search_tree/) - 先把最简单 BST 的性质、查找和插入过程看明白，再学平衡化会顺很多
- [Hello 算法：AVL 树](https://www.hello-algo.com/chapter_tree/avl_tree/) - 图示非常直观，适合先把“旋转为什么能保持平衡”看明白
- [洛谷专栏：入门平衡树 Treap](https://www.luogu.com/article/tyvidvb6) - 更偏竞赛和模板视角，适合直接对应到笔试手写代码
- [GeeksforGeeks 中文：红黑树简介](https://www.geeksforgeeks.org/zh-hans/dsa/introduction-to-red-black-tree/) - 适合专门补红黑树的性质、颜色规则和为什么它比 AVL 更常见

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

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各实现类的核心代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| 简单 BST | [bst_simple.py](bst_simple.py) 里的 `BST` 类 | `135.7` | 现场高风险 | 最短，但只适合题目明确不会退化的场景 |
| Treap | [treap.py](treap.py) 里的 `Treap` 类 | `158.5` | 现场高风险 | 推荐，用更高的手写复杂性换稳定性 |
| TreapWithSize（排名扩展） | [treap.py](treap.py) 里的 `TreapWithSize` 类 | `92.6` | 现场高风险 | 只在题目明确需要排名 / 第 k 小时使用 |
| 红黑树 | [rbtree.py](rbtree.py) 里的 `RBTree` 类 | `319.9` | 现场高风险 | 不建议笔试现场硬写 |

这里要特别注意：`TreapWithSize` 的分数低于普通 `Treap`，主要是因为它当前实现的操作集更窄，不代表它更好背。平衡树整体都是高风险模板，推荐 Treap 主要是综合了稳定性和可实现性，而不是因为它分数最低。

## 方案一：Treap（推荐）

### 什么是 Treap？

Treap = Tree + Heap，结合了二叉搜索树和堆的性质：

- **按值（key）维护 BST 性质**：左 < 根 < 右
- **按随机优先级（priority）维护堆性质**：父节点优先级 > 子节点

通过随机优先级，Treap 期望高度为 O(log n)，避免退化。

### 重复值处理方案

**方案一：使用 `count` 字段（推荐）**

在节点中添加 `count` 字段记录重复次数：

- ✅ 空间效率高，相同值只存一个节点
- ✅ 树高度 = O(log 不同值数量)，性能更好
- ✅ 前驱/后继操作不需要改，天然返回"不同的值"
- ✅ 适合"第 k 小的不同值"等常见题型
- ⚠️ 代码稍复杂，需要维护 `count` 字段

**方案二：保留重复节点**

允许重复值作为独立节点存在（插入到右子树）：

- ✅ 代码简单，几乎不用改
- ✅ 逻辑清晰，每个值就是一个节点
- ❌ 空间浪费，大量重复值时树会很大
- ❌ 树高度 = O(log 总元素数量)，性能下降
- ❌ 前驱/后继可能返回相同值，需要额外处理

**笔试建议**：优先使用方案一（`count` 字段），代码量增加不多，但性能和适用性更好。

### 适合速记的 Treap 实现（支持重复值）

```python
import random


class TreapNode:
    def __init__(self, key):
        self.key = key
        self.priority = random.random()  # 随机优先级
        self.count = 1  # 重复值计数
        self.left = self.right = None


class Treap:
    def __init__(self):
        self.root = None

    def _rotate_right(self, node):
        """
        右旋：提升左子节点 - O(1)

        旋转前：              旋转后：
              y                  x
             / \                / \
            x   C      =>      A   y
           / \                    / \
          A   B                  B   C

        作用：当左子节点 x 的优先级高于父节点 y 时，
             通过右旋将 x 提升为新的根节点
        """
        left = node.left
        node.left = left.right
        left.right = node
        return left

    def _rotate_left(self, node):
        """
        左旋：提升右子节点 - O(1)

        旋转前：              旋转后：
            x                  y
           / \                / \
          A   y      =>      x   C
             / \            / \
            B   C          A   B

        作用：当右子节点 y 的优先级高于父节点 x 时，
             通过左旋将 y 提升为新的根节点
        """
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
        else:
            # key == node.key: 重复元素，计数+1
            node.count += 1
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
            # 找到目标节点
            if node.count > 1:
                # 还有重复值，只减计数
                node.count -= 1
                return node

            # count == 1，真正删除节点
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

### 旋转操作示例

假设我们依次插入 5, 3, 7，并且随机优先级分别为 0.5, 0.8, 0.3：

```
步骤 1：插入 5 (优先级 0.5)
    5(0.5)

步骤 2：插入 3 (优先级 0.8)
按 BST 规则，3 应该在 5 的左边：
      5(0.5)
     /
    3(0.8)

但 3 的优先级 0.8 > 5 的优先级 0.5，违反堆性质！
需要右旋：
    3(0.8)          <- 3 提升为根
       \
        5(0.5)

步骤 3：插入 7 (优先级 0.3)
按 BST 规则，7 应该在 5 的右边：
    3(0.8)
       \
        5(0.5)
           \
            7(0.3)

7 的优先级 0.3 < 5 的优先级 0.5，满足堆性质，无需旋转。

最终树结构：
    3(0.8)          <- 优先级最高的在根部
       \
        5(0.5)      <- 满足 BST 性质：3 < 5 < 7
           \        <- 满足堆性质：父节点优先级 > 子节点
            7(0.3)
```

**关键点**：

- **BST 性质**由插入位置保证（左 < 根 < 右）
- **堆性质**由旋转维护（父优先级 > 子优先级）
- 随机优先级使树期望平衡，避免退化

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

### 重复值处理

本实现采用**允许重复节点**的方案：重复值会被插入到右子树，作为独立节点存在。

- ✅ 实现最简单，只需修改一行代码
- ✅ 适合作为科普展示
- ❌ 空间效率低，树会变大
- ❌ 前驱/后继可能返回相同值

**注意**：实际应用中可以考虑使用 `count` 字段（参考 Treap 的实现），但会让已经很复杂的红黑树代码更加复杂。

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
