# 滑动窗口笔试攻略

## 什么是滑动窗口？

滑动窗口本质上是在数组或字符串上维护一个 **连续区间**，让左右边界按规则移动。

- **固定窗口**：窗口长度固定，常见于“长度为 k 的子数组”
- **可变窗口**：窗口长度不固定，常见于“最长 / 最短满足条件的连续段”
- 每个元素通常最多进窗口一次、出窗口一次，所以常见复杂度是 **O(n)**
- 它和双指针很像，但更强调 **连续区间维护**

### 支持的操作

| 模式 | 时间复杂度 | 典型场景 |
|------|------------|----------|
| 固定长度窗口 | O(n) | 长度为 k 的最大和 |
| 可变长度窗口 | O(n) | 最短覆盖、最长不重复子串 |
| 计数窗口 | O(n) | 字符出现次数约束 |

## 滑动窗口适合解决什么问题？

1. **固定长度子数组 / 子串**
    - 例如：长度为 k 的最大和
    - 时间复杂度：O(n)

2. **最短满足条件的连续子数组**
    - 例如：和至少为 target 的最短子数组
    - 时间复杂度：O(n)

3. **最长不含重复字符的子串**
    - 例如：最长无重复子串
    - 时间复杂度：O(n)

4. **连续区间统计**
    - 例如：最多包含 K 种字符、窗口内字符频次限制
    - 时间复杂度：通常 O(n)

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [滑动窗口的一些总结](https://hit9.dev/post/sliding-window) - 对窗口成立条件、收缩时机和常见坑点总结得很清楚，适合先建立题感
- [滑动窗口算法（sliding window algorithm）](https://xiaoyuhen.com/blog/2019-03-12-sliding-window-algorithm/) - 例子很典型，固定窗口和可变窗口都讲到了，适合对照模板看
- [代码随想录：双指针总结篇](https://programmercarl.com/%E5%8F%8C%E6%8C%87%E9%92%88%E6%80%BB%E7%BB%93.html) - 滑动窗口本质上也是双指针套路的一种，适合补充整体框架

## 笔试场景建议

### 推荐策略

1. **出现“连续子数组 / 子串”先想窗口**
    - ✅ 这是最高频信号
    - ✅ 常能把 O(n^2) 降到 O(n)

2. **固定窗口写成“加一个、减一个”**
    - ✅ 不要每次重新算整段

3. **可变窗口写成“右扩左缩”**
    - ✅ `right` 扩大候选区间
    - ✅ 条件满足时尝试 `left` 收缩

## 方案一：通用模板（推荐）

### 固定窗口

```python
window = sum(nums[:k])
ans = window

for i in range(k, len(nums)):
    window += nums[i] - nums[i - k]
    ans = max(ans, window)
```

### 可变窗口

```python
left = 0
s = 0

for right, x in enumerate(nums):
    s += x
    while s >= target:
        # 更新答案
        s -= nums[left]
        left += 1
```

## 常见题型速查

### 1. 固定窗口最大和

```python
window = sum(nums[:k])
ans = window

for i in range(k, len(nums)):
    window += nums[i] - nums[i - k]
    ans = max(ans, window)
```

### 2. 最短满足条件的连续子数组

```python
left = 0
s = 0
ans = len(nums) + 1

for right, x in enumerate(nums):
    s += x
    while s >= target:
        ans = min(ans, right - left + 1)
        s -= nums[left]
        left += 1
```

### 3. 最长无重复子串

```python
last = {}
left = 0
ans = 0

for right, ch in enumerate(s):
    if ch in last and last[ch] >= left:
        left = last[ch] + 1
    last[ch] = right
    ans = max(ans, right - left + 1)
```

## 实战技巧总结

✅ **连续段问题优先想窗口**

✅ **固定窗口别重复求和**：直接滚动更新

✅ **可变窗口常写 `for right in ...` + `while ...`**

✅ **维护窗口状态时要先想增量更新**

✅ **答案更新时机很重要**：扩完更，还是缩前更，要想清楚

✅ **含负数的窗口题未必还能直接双指针**：别套错

## 参考资料

- [sliding_window.py](sliding_window.py) - 固定窗口、可变窗口、最长无重复子串示例
