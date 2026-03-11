# 快速排序（Quick Sort）笔试攻略

## 什么是快速排序？

快速排序是一种经典的**分治排序算法**：先选一个 `pivot`（基准值），把数组分成“左边都不大于它、右边都大于它”两部分，再递归处理左右两边。

- **原地快排**：直接在原数组上交换，空间复杂度通常按递归栈算
- **函数式快排**：写起来更短，但会额外创建列表，面试里一般不算标准手写快排

### 核心性质

1. **分治**：先 partition，再递归排左右两段
2. **平均复杂度优秀**：平均时间复杂度 O(n log n)
3. **最坏情况会退化**：如果 pivot 选得很差，最坏会到 O(n^2)
4. **通常不稳定**：相等元素的相对顺序一般保不住
5. **面试常要求手写 partition**：难点通常不在递归，而在边界和交换逻辑

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| `partition` | O(n) | 把一段区间按 `pivot` 分成左右两边 |
| `quick_sort` 平均 | O(n log n) | 大多数情况下表现很好 |
| `quick_sort` 最坏 | O(n^2) | 近乎有序、pivot 选得差时会退化 |
| 额外空间 | O(log n) 平均 | 主要来自递归栈 |

## 快速排序适合解决什么问题？

快速排序特别适合处理以下场景：

1. **现场手写排序算法**：面试官直接要求你写一个经典排序
    - 时间复杂度：平均 O(n log n)，思路也够经典

2. **需要体现 partition 思维**：很多题不一定真让你完整排序，但会借 partition 出题
    - 例如：快速选择、第 K 大、荷兰国旗问题

3. **原地排序场景**：希望少开额外数组
    - 空间复杂度通常优于归并排序的 O(n)

4. **训练递归 + 双指针 / 单指针边界控制**
    - 快排是很典型的“代码不长，但边界容易写挂”的题

5. **理解比较类排序的平均复杂度**
    - 平均 O(n log n)，是很多工程排序和选择算法讨论的基础

## 笔试场景建议

### 推荐策略

1. **如果题目只是让你“排个序”，优先用 `sorted()` / `.sort()`**
    - ✅ Python 内置排序更稳、更快、更不容易错
    - ✅ 但要注意：**它底层是 Timsort，不是快排**
    - ❌ 如果题目明确要求“手写快排”，那就不能拿它糊过去

2. **如果面试官明确要求写快排，优先写 Lomuto 分区版**
    - ✅ 只有一个 `for` 循环，最好背
    - ✅ `pivot = nums[r]`、`i` 指向下一个该放“小元素”的位置，逻辑直
    - ⚠️ 性能不是最强，但手写成功率高

3. **别一上来追求最优 pivot 策略**
    - ✅ 先把最基础可运行版本写对
    - ✅ 如果面试官继续追问，再补“随机 pivot”“三路快排”
    - ❌ 基础版都没写稳时，先上复杂优化通常只会把自己写乱

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| `sorted()` / `.sort()` | README 里的最小模板片段 | `0.0` | 很容易手写 | 题目只要排序结果时直接用 |
| 手写原地快排 | README 里的 Lomuto 分区模板 | `12.7` | 坑比较多 | 面试官要求写快排时用它 |

`sorted()` 分数几乎为 0 不奇怪，因为复杂度都交给了标准库；真正考你快排时，考点基本都在 `partition` 边界。

## 方案一：直接使用 `sorted()`（只在题目没要求手写快排时）

### 基本用法

```python
nums = [5, 2, 3, 1]
ans = sorted(nums)  # 返回新列表

nums.sort()  # 原地排序
```

### 自定义排序

```python
words = ['pear', 'apple', 'fig', 'banana']
ans = sorted(words, key=len)  # 按长度排序
```

### 倒序排序

```python
nums = [5, 2, 3, 1]
ans = sorted(nums, reverse=True)
```

> 注意：上面这些当然很好用，但它们不是“你手写了快排”。题目明确要求 quick sort 时，还是得自己写。

## 方案二：手写原地快排（推荐面试手写版）

### 适合速记的 Lomuto 分区实现

```python
def quick_sort(nums, l=0, r=None):
    if r is None:
        r = len(nums) - 1
    if l >= r:
        return nums

    pivot = nums[r]
    i = l

    for j in range(l, r):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1

    nums[i], nums[r] = nums[r], nums[i]
    quick_sort(nums, l, i - 1)
    quick_sort(nums, i + 1, r)
    return nums
```

### 使用示例

```python
nums = [5, 1, 1, 2, 0, 0]
quick_sort(nums)
print(nums)  # [0, 0, 1, 1, 2, 5]
```

### 如果担心退化，可补一行随机 pivot

```python
import random

p = random.randint(l, r)
nums[p], nums[r] = nums[r], nums[p]  # 随机选 pivot 再复用同一套 partition
```

这个优化不难，但不建议第一次写模板时就强行塞进去。先把基础版写稳更重要。

**完整实现和更多示例**：[quick_sort_simple.py](quick_sort_simple.py)

## 常见题型速查

### 1. 原地快排

```python
def quick_sort(nums, l=0, r=None):
    if r is None:
        r = len(nums) - 1
    if l >= r:
        return nums

    pivot = nums[r]
    i = l
    for j in range(l, r):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1

    nums[i], nums[r] = nums[r], nums[i]
    quick_sort(nums, l, i - 1)
    quick_sort(nums, i + 1, r)
    return nums
```

### 2. 快速选择第 k 小

```python
def partition(nums, l, r):
    pivot = nums[r]
    i = l
    for j in range(l, r):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1
    nums[i], nums[r] = nums[r], nums[i]
    return i


while l <= r:
    p = partition(nums, l, r)
    if p == k:
        return nums[p]
    if p < k:
        l = p + 1
    else:
        r = p - 1
```

### 3. 数组按 pivot 分两边

```python
pivot = nums[r]
i = l

for j in range(l, r):
    if nums[j] <= pivot:
        nums[i], nums[j] = nums[j], nums[i]
        i += 1

nums[i], nums[r] = nums[r], nums[i]
```

### 4. 三路划分思路

```python
lt, i, gt = l, l, r
pivot = nums[l]

while i <= gt:
    if nums[i] < pivot:
        nums[lt], nums[i] = nums[i], nums[lt]
        lt += 1
        i += 1
    elif nums[i] > pivot:
        nums[gt], nums[i] = nums[i], nums[gt]
        gt -= 1
    else:
        i += 1
```

## 实战技巧总结

✅ **先背会一个最短可运行版本**：面试里先写对，比先写“最优版”重要

✅ **优先写 `pivot = nums[r]` 的 Lomuto 版**：循环短，最好记

✅ **递归边界先写 `if l >= r: return`**：这句最容易漏

✅ **`i` 表示“下一个小元素该放的位置”**：把这个含义想清楚，partition 就不乱

✅ **重复值多时要知道它可能退化**：面试官追问时再补随机 pivot 或三路快排

✅ **题目只要结果时直接 `sorted()`**：别为了秀快排把自己绕进去

✅ **记住 Python 内置排序不是快排**：这是面试里很容易被顺手问到的点

## 参考资料

- [quick_sort_simple.py](quick_sort_simple.py) - 适合面试速记的原地快排模板

**推荐阅读顺序**：

1. 先看本 README，把 `sorted()` 和“手写快排”这两个语境分开
2. 再看 `quick_sort_simple.py`，背住最基础的 partition 模板
3. 需要进阶时，再从 partition 扩展到 quickselect 和三路快排
