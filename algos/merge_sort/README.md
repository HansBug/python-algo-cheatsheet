# 归并排序（Merge Sort）笔试攻略

## 什么是归并排序？

归并排序是一种经典的**分治排序算法**：先把数组递归拆成左右两半，分别排好序，再把两段有序数组合并起来。

- **自顶向下归并**：递归拆分，再合并，最常见也最好理解
- **自底向上归并**：按区间长度迭代合并，不用递归，但现场手写通常不如递归版顺

### 核心性质

1. **分治**：先分，再治，最后 merge
2. **稳定排序**：相等元素的相对顺序能保住
3. **时间复杂度稳定**：无论最好最坏，都是 O(n log n)
4. **需要额外数组**：标准写法通常要 O(n) 辅助空间
5. **面试考点主要在 merge 过程**：左右指针推进和收尾最容易写错

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| `merge` | O(n) | 合并两段有序区间 |
| `merge_sort` | O(n log n) | 拆分 + 合并 |
| 额外空间 | O(n) | 标准模板需要辅助数组 |

## 归并排序适合解决什么问题？

归并排序特别适合处理以下场景：

1. **面试要求手写稳定排序**
    - 时间复杂度：稳定 O(n log n)，比快排更稳

2. **排序同时统计信息**
    - 例如：逆序对数量、区间和计数、小和问题
    - merge 阶段天然适合做这种“跨左右区间”的统计

3. **链表排序**
    - 链表不适合随机访问，归并排序通常比快排更自然

4. **对最坏复杂度敏感**
    - 不像快排会退化到 O(n^2)

5. **需要稳定性**
    - 相等元素顺序不能乱时，归并排序比快排更合适

## 笔试场景建议

### 推荐策略

1. **如果题目只是让你排序，优先用 `sorted()` / `.sort()`**
    - ✅ Python 内置排序更稳、更快
    - ✅ 但注意：**它也不是你手写了归并排序**

2. **如果面试官明确要求写归并排序，优先写递归 + 辅助数组版**
    - ✅ 最容易理解，也最好背
    - ✅ 核心只有“递归拆分”和“merge 两段有序数组”
    - ⚠️ 不要现场再发明花哨优化

3. **如果题目和“逆序对 / 区间统计”有关，优先想归并**
    - ✅ 这类题很多就是 merge 阶段顺手统计
    - ✅ 比硬上树状数组、平衡树更稳

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| `sorted()` / `.sort()` | README 里的最小模板片段 | `0.0` | 很容易手写 | 题目只要结果时直接用 |
| 手写归并排序 | README 里的递归 + merge 模板 | `37.5` | 现场高风险 | 面试官要求手写排序时可选它 |

归并排序的难点不在思想，而在 `merge` 时的左右指针和收尾逻辑。代码往往不长，但很容易少拷一个尾巴。

## 方案一：直接使用 `sorted()`（只在题目没要求手写归并时）

### 基本用法

```python
nums = [5, 2, 3, 1]
ans = sorted(nums)

nums.sort()
```

## 方案二：手写归并排序（推荐面试手写版）

### 适合速记的递归实现

```python
def merge_sort(nums):
    tmp = [0] * len(nums)

    def sort(l, r):
        if l >= r:
            return

        m = (l + r) // 2
        sort(l, m)
        sort(m + 1, r)

        i, j, k = l, m + 1, l
        while i <= m and j <= r:
            if nums[i] <= nums[j]:
                tmp[k] = nums[i]
                i += 1
            else:
                tmp[k] = nums[j]
                j += 1
            k += 1

        while i <= m:
            tmp[k] = nums[i]
            i += 1
            k += 1

        while j <= r:
            tmp[k] = nums[j]
            j += 1
            k += 1

        nums[l:r + 1] = tmp[l:r + 1]

    sort(0, len(nums) - 1)
    return nums
```

### 使用示例

```python
nums = [5, 1, 1, 2, 0, 0]
merge_sort(nums)
print(nums)  # [0, 0, 1, 1, 2, 5]
```

### 逆序对统计思路

```python
# 在 merge 时，如果 nums[i] > nums[j]
# 说明 nums[i..m] 都比 nums[j] 大
# 逆序对数量直接加 m - i + 1
```

**完整实现和更多示例**：[merge_sort_simple.py](merge_sort_simple.py)

## 常见题型速查

### 1. 普通归并排序

```python
tmp = [0] * len(nums)

def sort(l, r):
    if l >= r:
        return

    m = (l + r) // 2
    sort(l, m)
    sort(m + 1, r)

    i, j, k = l, m + 1, l
    while i <= m and j <= r:
        if nums[i] <= nums[j]:
            tmp[k] = nums[i]
            i += 1
        else:
            tmp[k] = nums[j]
            j += 1
        k += 1

    while i <= m:
        tmp[k] = nums[i]
        i += 1
        k += 1

    while j <= r:
        tmp[k] = nums[j]
        j += 1
        k += 1

    nums[l:r + 1] = tmp[l:r + 1]
```

### 2. 逆序对数量

```python
cnt = 0

while i <= m and j <= r:
    if nums[i] <= nums[j]:
        tmp[k] = nums[i]
        i += 1
    else:
        tmp[k] = nums[j]
        cnt += m - i + 1
        j += 1
    k += 1
```

### 3. 两个有序数组合并

```python
i = j = 0
res = []

while i < len(a) and j < len(b):
    if a[i] <= b[j]:
        res.append(a[i])
        i += 1
    else:
        res.append(b[j])
        j += 1

res.extend(a[i:])
res.extend(b[j:])
```

## 实战技巧总结

✅ **先背 merge 流程**：左右指针推进、剩余部分补尾巴

✅ **递归边界先写 `if l >= r: return`**

✅ **`tmp` 提前开一次**：不要每层递归都新建数组

✅ **统计逆序对时优先想归并**

✅ **需要稳定排序时优先想归并而不是快排**

✅ **题目只要结果时直接用 `sorted()`**

## 参考资料

- [merge_sort_simple.py](merge_sort_simple.py) - 适合面试速记的归并排序模板

**推荐阅读顺序**：

1. 先看本 README，把 merge 过程背熟
2. 再看 `merge_sort_simple.py`，理解辅助数组怎么复用
3. 需要进阶时，再把逆序对等题型套到 merge 阶段
