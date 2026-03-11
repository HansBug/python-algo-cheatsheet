# 单调队列（Monotonic Queue）笔试攻略

## 什么是单调队列？

单调队列本质上还是**队列 / 双端队列**，只是你在入队时顺手维护“队列内元素单调递增”或“单调递减”，这样就能在滑动窗口里 O(1) 拿到当前最值。

- **单调递减队列**：队头到队尾对应值越来越小，队头就是当前窗口最大值
- **单调递增队列**：队头到队尾对应值越来越大，队头就是当前窗口最小值

### 核心性质

1. **每个元素最多进队一次、出队一次**：所以总复杂度通常是 O(n)
2. **通常存索引而不是值**：这样可以判断元素有没有滑出窗口
3. **队头永远是当前答案候选**：要么是窗口最大值，要么是窗口最小值
4. **大多数题都用 `collections.deque`**：两端弹入弹出都是 O(1)

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| `push` | O(1) 摊还 | 当前元素入队，并弹掉尾部无用元素 |
| `expire` | O(1) 摊还 | 把窗口左边滑出去的元素从队头踢掉 |
| `peek` | O(1) | 查看当前窗口最值对应索引 |
| 单次扫描 | O(n) | 整个数组每个元素最多进出队一次 |

## 单调队列适合解决什么问题？

单调队列特别适合处理以下场景：

1. **滑动窗口最大值 / 最小值**：窗口一边移动，一边要拿最值
    - 时间复杂度：O(n)，优于暴力的 O(nk) 和堆的 O(n log k)

2. **前缀和优化的最短子数组**：找和至少为 `k` 的最短子数组
    - 时间复杂度：O(n)，优于暴力枚举起点终点的 O(n^2)

3. **区间 DP 优化**：状态转移只看最近 `k` 个位置的最大值 / 最小值
    - 例如：`dp[i] = nums[i] + max(dp[j])`
    - 时间复杂度：O(n)，优于每次枚举窗口的 O(nk)

4. **受限滑动窗口**：窗口内既要维护范围，又要快速拿最值
    - 例如：绝对差不超过 `limit` 的最长连续子数组
    - 时间复杂度：O(n)

5. **在线最值维护**：元素持续流入，同时过期旧元素
    - 这类题不一定明写“滑动窗口”，但套路通常一样

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [OI Wiki：单调队列](https://oiwiki.org/ds/monotonous-queue/) - 模板和典型应用都比较系统，适合先建立整体认知
- [labuladong：单调队列解题模板](https://labuladong.online/zh/algo/data-structure/monotonic-queue/) - 更偏滑动窗口题目视角，适合把“过期元素”和“尾部淘汰元素”彻底分清

## 笔试场景建议

### 推荐策略

1. **优先使用 `collections.deque` 存索引**
    - ✅ `append()` / `pop()` / `popleft()` 三件套就够了
    - ✅ 索引天然能处理“过期元素”
    - ✅ 比自己写 `head` 更稳

2. **先处理过期，再维护单调性**
    - ✅ 这是滑动窗口题最稳的写法
    - ✅ 队头代表当前窗口答案，先保证它还活着

3. **最大值和最小值只差一个比较符号**
    - ✅ 最大值：尾部弹掉 `<= 当前值`
    - ✅ 最小值：尾部弹掉 `>= 当前值`

4. **前缀和题别死套滑窗**
    - ✅ 像“最短子数组和至少为 K”这种允许负数的题，要用前缀和 + 单调队列
    - ❌ 直接双指针会错

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| `deque` + 滑动窗口模板 | README 里的窗口最大值模板 | `16.3` | 坑比较多 | 推荐，高频题直接套 |
| 手动封装 `MonoQueue` 类 | README 里的极简类模板 | `13.7` | 坑比较多 | 只有题目不方便 import 时再考虑 |

单调队列比单调栈多一个“元素过期”状态，所以现场更容易漏掉窗口左边界判断。写题时，先想“谁该过期”，再想“谁该被尾部淘汰”。

## 方案一：使用 `collections.deque`（推荐）

### 基本用法

```python
from collections import deque

nums = [1, 3, -1, -3, 5]
k = 3
dq = deque()  # 存索引，保持对应值单调递减

for i, x in enumerate(nums):
    while dq and dq[0] <= i - k:
        dq.popleft()
    while dq and nums[dq[-1]] <= x:
        dq.pop()
    dq.append(i)
```

### 滑动窗口最大值

```python
from collections import deque


def max_sliding_window(nums, k):
    ans = []
    dq = deque()

    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if i + 1 >= k:
            ans.append(nums[dq[0]])

    return ans
```

### 滑动窗口最小值

```python
from collections import deque


def min_sliding_window(nums, k):
    ans = []
    dq = deque()

    for i, x in enumerate(nums):
        while dq and dq[0] <= i - k:
            dq.popleft()
        while dq and nums[dq[-1]] >= x:
            dq.pop()
        dq.append(i)
        if i + 1 >= k:
            ans.append(nums[dq[0]])

    return ans
```

### 最短子数组和至少为 K

```python
from collections import deque


def shortest_subarray(nums, k):
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)

    ans = len(nums) + 1
    dq = deque()  # 保持 prefix[dq] 单调递增

    for i, s in enumerate(prefix):
        while dq and s - prefix[dq[0]] >= k:
            ans = min(ans, i - dq.popleft())
        while dq and prefix[dq[-1]] >= s:
            dq.pop()
        dq.append(i)

    return ans if ans <= len(nums) else -1
```

### 区间 DP 最大值优化

```python
from collections import deque


def constrained_subset_sum(nums, k):
    dp = [0] * len(nums)
    dq = deque()  # 保持 dp[dq] 单调递减

    for i, x in enumerate(nums):
        while dq and dq[0] < i - k:
            dq.popleft()
        best = dp[dq[0]] if dq else 0
        dp[i] = x + max(0, best)
        while dq and dp[dq[-1]] <= dp[i]:
            dq.pop()
        dq.append(i)

    return max(dp)
```

**完整实现和更多示例**：[monotonic_queue.py](monotonic_queue.py)

## 方案二：手动实现单调队列

### 适合速记的单调递减队列实现

```python
class MonoQueue:
    def __init__(self, nums):
        self.nums = nums
        self.q = []
        self.head = 0

    def push(self, i):
        """入队并维护单调递减 - O(1) 摊还"""
        while self.head < len(self.q) and self.nums[self.q[-1]] <= self.nums[i]:
            self.q.pop()
        self.q.append(i)

    def pop(self, left):
        """弹出过期元素 - O(1) 摊还"""
        if self.head < len(self.q) and self.q[self.head] < left:
            self.head += 1

    def peek(self):
        """查看队头索引 - O(1)"""
        return self.q[self.head]
```

### 使用示例

```python
nums = [1, 3, -1, -3, 5, 3, 6, 7]
k = 3
q = MonoQueue(nums)
ans = []

for i in range(len(nums)):
    q.pop(i - k + 1)
    q.push(i)
    if i + 1 >= k:
        ans.append(nums[q.peek()])

print(ans)  # [3, 3, 5, 5, 6, 7]
```

> 实战建议：这类封装更像“帮助你理解”的练习。真到笔试，`deque` 原地写模板通常更稳。

## 常见题型速查

### 1. 滑动窗口最大值

```python
ans = []
dq = deque()

for i, x in enumerate(nums):
    while dq and dq[0] <= i - k:
        dq.popleft()
    while dq and nums[dq[-1]] <= x:
        dq.pop()
    dq.append(i)
    if i + 1 >= k:
        ans.append(nums[dq[0]])
```

### 2. 滑动窗口最小值

```python
ans = []
dq = deque()

for i, x in enumerate(nums):
    while dq and dq[0] <= i - k:
        dq.popleft()
    while dq and nums[dq[-1]] >= x:
        dq.pop()
    dq.append(i)
    if i + 1 >= k:
        ans.append(nums[dq[0]])
```

### 3. 最短子数组和至少为 K

```python
prefix = [0]
for x in nums:
    prefix.append(prefix[-1] + x)

ans = len(nums) + 1
dq = deque()
for i, s in enumerate(prefix):
    while dq and s - prefix[dq[0]] >= k:
        ans = min(ans, i - dq.popleft())
    while dq and prefix[dq[-1]] >= s:
        dq.pop()
    dq.append(i)
```

### 4. 区间 DP 优化

```python
dp = [0] * len(nums)
dq = deque()

for i, x in enumerate(nums):
    while dq and dq[0] < i - k:
        dq.popleft()
    best = dp[dq[0]] if dq else 0
    dp[i] = x + max(0, best)
    while dq and dp[dq[-1]] <= dp[i]:
        dq.pop()
    dq.append(i)
```

## 实战技巧总结

✅ **优先存索引**：窗口题必须知道谁过期了

✅ **先踢过期元素**：队头只要过期，就先别让它继续当答案

✅ **最大值和最小值只改一个符号**：别把整个模板重写一遍

✅ **窗口答案永远看队头**：不要从中间找，那就失去单调队列意义了

✅ **允许负数时优先想前缀和 + 单调队列**：双指针不一定成立

✅ **DP 优化先写出原始转移**：确认“最近 k 个取最大/最小”后再上单调队列

✅ **别把值直接塞进去**：一旦需要判断过期，你还得回头补索引

## 参考资料

- [monotonic_queue.py](monotonic_queue.py) - 单调队列高频模板与完整可运行示例

**推荐阅读顺序**：

1. 先看本 README，把“过期元素”和“尾部淘汰元素”区分开
2. 再看 `monotonic_queue.py`，把滑窗、前缀和、DP 三类题对应起来
3. 刷题时先背窗口最大值模板，其他题基本都从它变形
