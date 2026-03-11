# 堆排序（Heap Sort）笔试攻略

## 什么是堆排序？

堆排序本质上是“先建堆，再不断把堆顶换到数组末尾”的排序算法。对升序排序来说，通常建**最大堆**，这样每次都能把当前最大值放到末尾。

- **最大堆排序升序**：堆顶最大，每轮把最大值放到右边
- **最小堆排序降序**：思路对称，但面试里最常写的是最大堆版

### 核心性质

1. **基于堆**：核心就是 `heapify` 和 `sift_down`
2. **原地排序**：空间复杂度 O(1)
3. **时间复杂度稳定**：最好、平均、最坏都是 O(n log n)
4. **不稳定**：相等元素顺序通常保不住
5. **面试主要难点在下沉调整**：索引和边界容易写错

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| 建堆 | O(n) | 从最后一个非叶子结点开始下沉 |
| 单次取最大值 | O(log n) | 交换堆顶和末尾，再下沉 |
| `heap_sort` | O(n log n) | 原地完成排序 |
| 额外空间 | O(1) | 不算输入数组本身 |

## 堆排序适合解决什么问题？

堆排序特别适合处理以下场景：

1. **面试要求手写原地排序**
    - 时间复杂度：稳定 O(n log n)，额外空间 O(1)

2. **想体现对堆结构的理解**
    - 和单纯调 `heapq` 不一样，堆排序要求你自己写下沉逻辑

3. **最坏复杂度不能退化**
    - 不像快排会掉到 O(n^2)

4. **空间受限**
    - 比归并排序更省空间

5. **Top K / 优先队列思维的延伸**
    - 学会堆排序后，建堆和下沉这套操作会更熟

## 笔试场景建议

### 推荐策略

1. **如果题目只是让你排序，还是优先用 `sorted()` / `.sort()`**
    - ✅ Python 内置排序更稳
    - ❌ 但题目明确要求手写堆排序时，不能直接拿它代替

2. **如果要求手写堆排序，优先背“最大堆升序模板”**
    - ✅ 面试里最常见
    - ✅ 核心只要记住 `left = 2*i + 1`
    - ✅ 先建堆，再从后往前交换

3. **别把 `heapq` 当成堆排序答案**
    - ✅ `heapq` 能帮助你理解堆
    - ❌ 但它默认最小堆，而且大多数“手写堆排序”语境下还是要你自己写 `sift_down`

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| `sorted()` / `.sort()` | README 里的最小模板片段 | `0.0` | 很容易手写 | 题目只要结果时直接用 |
| 手写堆排序 | README 里的最大堆模板 | `24.9` | 现场高风险 | 面试官要求写堆排序时用它 |

堆排序的难点不在外层循环，而在 `sift_down`。一旦左右孩子索引和“谁是当前最大”写乱，后面全错。

## 方案一：直接使用 `sorted()`（只在题目没要求手写堆排序时）

### 基本用法

```python
nums = [5, 2, 3, 1]
ans = sorted(nums)

nums.sort()
```

## 方案二：手写堆排序（推荐面试手写版）

### 适合速记的最大堆实现

```python
def heap_sort(nums):
    n = len(nums)

    def sift_down(i, end):
        while True:
            best = i
            left = 2 * i + 1
            right = left + 1

            if left < end and nums[left] > nums[best]:
                best = left
            if right < end and nums[right] > nums[best]:
                best = right
            if best == i:
                return

            nums[i], nums[best] = nums[best], nums[i]
            i = best

    for i in range((n - 2) // 2, -1, -1):
        sift_down(i, n)

    for end in range(n - 1, 0, -1):
        nums[0], nums[end] = nums[end], nums[0]
        sift_down(0, end)

    return nums
```

### 使用示例

```python
nums = [5, 1, 1, 2, 0, 0]
heap_sort(nums)
print(nums)  # [0, 0, 1, 1, 2, 5]
```

### 和 `heapq` 的关系

```python
# heapq 更适合 Top K、优先队列
# 真要手写堆排序，重点还是自己会写 sift_down
```

**完整实现和更多示例**：[heap_sort_simple.py](heap_sort_simple.py)

## 常见题型速查

### 1. 原地堆排序

```python
for i in range((n - 2) // 2, -1, -1):
    sift_down(i, n)

for end in range(n - 1, 0, -1):
    nums[0], nums[end] = nums[end], nums[0]
    sift_down(0, end)
```

### 2. 下沉调整

```python
best = i
left = 2 * i + 1
right = left + 1

if left < end and nums[left] > nums[best]:
    best = left
if right < end and nums[right] > nums[best]:
    best = right
if best == i:
    return

nums[i], nums[best] = nums[best], nums[i]
i = best
```

### 3. 从数组建最大堆

```python
for i in range((n - 2) // 2, -1, -1):
    sift_down(i, n)
```

## 实战技巧总结

✅ **先背最大堆升序模板**：这是面试里最常用的版本

✅ **记住左孩子公式 `2*i + 1`**

✅ **建堆从最后一个非叶子节点开始**

✅ **每轮先交换堆顶和末尾，再缩小堆范围**

✅ **`sift_down` 是核心**：外层流程不会，通常还是因为这个没写稳

✅ **题目只要结果时直接 `sorted()`**

## 参考资料

- [heap_sort_simple.py](heap_sort_simple.py) - 适合面试速记的堆排序模板

**推荐阅读顺序**：

1. 先看本 README，把建堆和下沉流程理清
2. 再看 `heap_sort_simple.py`，背住最大堆模板
3. 如果还想补强，再回头看 [heap/README.md](../heap/README.md) 里的堆基础
