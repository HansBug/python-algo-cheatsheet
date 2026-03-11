# 单调栈（Monotonic Stack）笔试攻略

## 什么是单调栈？

单调栈本质上还是**栈**，只是你在入栈时顺手维护“栈内元素单调递增”或“单调递减”，这样就能在线找到某个元素左边或右边第一个更大/更小的位置。

- **单调递增栈**：栈顶到栈底对应值越来越大，常用来找**上一个/下一个更小元素**
- **单调递减栈**：栈顶到栈底对应值越来越小，常用来找**上一个/下一个更大元素**

### 核心性质

1. **每个元素最多进栈一次、出栈一次**：所以总复杂度通常是 O(n)
2. **通常存索引而不是值**：这样既能比较大小，也能顺手算距离和边界
3. **严格还是非严格要先想清楚**：`<`、`<=`、`>`、`>=` 一旦写错，重复值题目很容易翻车
4. **边界题常配合哨兵**：在数组头尾补一个更小/更大的值，代码会短很多

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| `push` | O(1) 摊还 | 当前元素入栈，并顺手维护单调性 |
| `pop` | O(1) 摊还 | 弹出不可能再成为答案的元素 |
| `peek` | O(1) | 查看当前最近候选边界 |
| 单次扫描 | O(n) | 整个数组每个元素最多进出栈一次 |

## 单调栈适合解决什么问题？

单调栈特别适合处理以下场景：

1. **下一个更大 / 更小元素**：找某个元素右边第一个比它大或小的位置
    - 时间复杂度：O(n)，优于双重循环的 O(n^2)

2. **左边最近满足条件的边界**：找左边第一个更大 / 更小元素
    - 时间复杂度：O(n)，适合做边界扩展题

3. **柱状图最大矩形**：求每根柱子能向左右扩到哪里
    - 时间复杂度：O(n)，优于枚举左右边界的 O(n^2)

4. **子数组贡献法**：统计某个元素作为最小值 / 最大值贡献了多少次
    - 例如：子数组最小值之和、子数组范围和
    - 时间复杂度：O(n)，优于枚举所有子数组的 O(n^2)

5. **温度 / 股票跨度这类最近更大元素题**：本质就是“最近边界”
    - 时间复杂度：O(n)，模板高度统一

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [OI Wiki：单调栈](https://oiwiki.org/ds/monotonous-stack/) - 模板、思路和常见应用都比较全，适合系统打底
- [labuladong：单调栈解题模板](https://labuladong.online/zh/algo/data-structure/monotonic-stack/) - 更偏刷题视角，适合把“下一个更大元素”这类套路彻底吃透

## 笔试场景建议

### 推荐策略

1. **直接用 `list` 存索引**
    - ✅ 最短最好记，`append()` / `pop()` / `[-1]` 就够了
    - ✅ 既能比较值，也能算距离和边界
    - ✅ 绝大多数题都不需要额外封装

2. **先确定你要的是“大于/小于”，再确定“严格/非严格”**
    - ✅ 重复值题最容易死在这里
    - ✅ 写代码前先在草稿上定好 `while` 条件，能少 debug 很多

3. **边界题优先考虑哨兵写法**
    - ✅ 柱状图、子数组贡献这类题会明显更顺
    - ✅ 少写一堆扫尾逻辑

4. **除非题目强制要类接口，否则别额外包一层**
    - ✅ 单调栈本来就是题内模板，原地写最快
    - ❌ 为了“优雅”封装成通用类，现场反而更容易写乱

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| `list` + 单次扫描模板 | README 里的下一个更大元素模板 | `5.9` | 很容易手写 | 推荐，先把模板背熟 |
| 手动封装 `MonoStack` 类 | README 里的极简类模板 | `10.2` | 正常可写 | 只在题目强制要类接口时再写 |

单调栈不难，但它的坑不在语法，而在**比较符号和边界定义**。这类题写挂，大多不是因为不会用栈，而是条件写反了。

## 方案一：直接使用 `list`（推荐）

### 基本用法

```python
nums = [2, 1, 2, 4, 3]
st = []  # 存索引，保持 nums[st] 单调递减
ans = [-1] * len(nums)

for i, x in enumerate(nums):
    while st and nums[st[-1]] < x:
        ans[st.pop()] = x
    st.append(i)
```

### 下一个更大元素

```python
def next_greater(nums):
    ans = [-1] * len(nums)
    st = []  # 单调递减栈，存索引

    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            ans[st.pop()] = x
        st.append(i)

    return ans
```

### 左边第一个更小元素

```python
def previous_less_index(nums):
    ans = [-1] * len(nums)
    st = []  # 单调递增栈，存索引

    for i, x in enumerate(nums):
        while st and nums[st[-1]] >= x:
            st.pop()
        ans[i] = st[-1] if st else -1
        st.append(i)

    return ans
```

### 每日温度

```python
def daily_temperatures(t):
    ans = [0] * len(t)
    st = []  # 单调递减栈，存还没等到更高温度的索引

    for i, x in enumerate(t):
        while st and t[st[-1]] < x:
            j = st.pop()
            ans[j] = i - j
        st.append(i)

    return ans
```

### 柱状图最大矩形

```python
def largest_rectangle_area(heights):
    ans = 0
    st = []

    for i, h in enumerate(heights + [0]):  # 尾部补哨兵，统一结算
        while st and heights[st[-1]] >= h:
            height = heights[st.pop()]
            left = st[-1] if st else -1
            ans = max(ans, height * (i - left - 1))
        st.append(i)

    return ans
```

**完整实现和更多示例**：[monotonic_stack.py](monotonic_stack.py)

## 方案二：手动实现单调栈

### 适合速记的单调递增栈实现

```python
class MonoStack:
    def __init__(self, nums):
        self.nums = nums
        self.st = []

    def push(self, i):
        """入栈并维护单调递增 - O(1) 摊还"""
        while self.st and self.nums[self.st[-1]] >= self.nums[i]:
            self.st.pop()
        self.st.append(i)

    def pop(self):
        """弹出栈顶 - O(1) 摊还"""
        return self.st.pop()

    def peek(self):
        """查看栈顶索引 - O(1)"""
        return self.st[-1]

    def empty(self):
        """判空 - O(1)"""
        return not self.st
```

### 使用示例

```python
nums = [3, 7, 4, 2, 5]
st = MonoStack(nums)
left = [-1] * len(nums)

for i in range(len(nums)):
    st.push(i)
    if len(st.st) >= 2:
        left[i] = st.st[-2]

print(left)  # [-1, 0, 0, -1, 3]
```

> 实战建议：这个类只是为了方便你记忆“维护单调性”这件事。真到笔试里，直接写 `st = []` 通常更快。

## 常见题型速查

### 1. 下一个更大元素

```python
ans = [-1] * len(nums)
st = []

for i, x in enumerate(nums):
    while st and nums[st[-1]] < x:
        ans[st.pop()] = x
    st.append(i)

return ans
```

### 2. 每日温度

```python
ans = [0] * len(t)
st = []

for i, x in enumerate(t):
    while st and t[st[-1]] < x:
        j = st.pop()
        ans[j] = i - j
    st.append(i)

return ans
```

### 3. 柱状图最大矩形

```python
ans = 0
st = []

for i, h in enumerate(heights + [0]):
    while st and heights[st[-1]] >= h:
        height = heights[st.pop()]
        left = st[-1] if st else -1
        ans = max(ans, height * (i - left - 1))
    st.append(i)

return ans
```

### 4. 子数组最小值之和

```python
left = [-1] * len(nums)
right = [len(nums)] * len(nums)
st = []

for i, x in enumerate(nums):
    while st and nums[st[-1]] > x:
        st.pop()
    left[i] = st[-1] if st else -1
    st.append(i)

st = []
for i in range(len(nums) - 1, -1, -1):
    while st and nums[st[-1]] >= nums[i]:
        st.pop()
    right[i] = st[-1] if st else len(nums)
    st.append(i)
```

## 实战技巧总结

✅ **优先存索引**：用索引而不是值，距离、边界、去重都更好处理

✅ **先想清单调方向**：找更大就维护递减栈，找更小就维护递增栈

✅ **重复值只选一边吃掉**：一边用严格比较，另一边用非严格比较

✅ **边界题加哨兵**：特别是柱状图和贡献法，能省掉扫尾逻辑

✅ **弹栈时顺手结算答案**：很多题答案就出在“谁把谁弹掉”这一刻

✅ **不要把值和索引混着存**：模板会变乱，重复值时也更容易出错

✅ **不会就先画出栈变化**：这类题调试最有效的办法就是看每一步谁进谁出

## 参考资料

- [monotonic_stack.py](monotonic_stack.py) - 单调栈高频模板与完整可运行示例

**推荐阅读顺序**：

1. 先看本 README，把“单调方向”和“严格/非严格”搞清楚
2. 再看 `monotonic_stack.py`，把几个高频题型对应起来
3. 刷题时优先套“下一个更大元素”或“边界扩展”模板
