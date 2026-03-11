# 贪心笔试攻略

## 什么是贪心？

贪心不是某个固定数据结构，而是一种策略：**每一步都做当前看起来最优的选择**，希望最终得到全局最优。

- 常见目标：最少步数、最多数量、最小代价、是否可行
- 代码通常很短
- 真正难点是 **为什么这样选不会错**
- 面试里经常会问你“这个贪心为什么成立”

### 支持的操作

| 场景 | 常见复杂度 | 说明 |
|------|------------|------|
| 线性贪心 | O(n) | 例如跳跃游戏 |
| 排序后贪心 | O(n log n) | 例如区间选择、分配问题 |
| 堆优化贪心 | O(n log n) | 例如带动态最值维护的贪心 |

## 贪心适合解决什么问题？

1. **可达性 / 最少步数**
    - 例如：跳跃游戏、最少跳跃次数
    - 时间复杂度：通常 O(n)

2. **区间选择**
    - 例如：最多选择多少个互不重叠区间
    - 时间复杂度：O(n log n)

3. **排序后按规则选**
    - 例如：分发饼干、安排会议、最小箭数射气球
    - 时间复杂度：通常 O(n log n)

4. **局部最优能自然延伸到整体**
    - 例如：总是选当前最早结束的区间
    - 优势：代码极短，实战很香

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [Hello 算法：贪心算法](https://www.hello-algo.com/chapter_greedy/greedy_algorithm/) - 适合先把贪心的定义、直觉和适用前提过一遍
- [代码随想录：贪心算法总结篇](https://programmercarl.com/%E8%B4%AA%E5%BF%83%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93%E7%AF%87.html) - 更偏求职题套路，适合建立“什么时候该怀疑是贪心”的题感
- [代码随想录：本周小结！（贪心算法系列四）](https://programmercarl.com/%E5%91%A8%E6%80%BB%E7%BB%93/20201224%E8%B4%AA%E5%BF%83%E5%91%A8%E6%9C%AB%E6%80%BB%E7%BB%93.html) - 区间贪心讲得很集中，适合补最常见的面试场景

## 笔试场景建议

### 推荐策略

1. **看到“最少 / 最多 / 能否完成”，先问能不能贪**
    - ✅ 这是高频信号
    - ❌ 但不能因为看起来简单就盲写

2. **先想选择规则，再想如何证明**
    - ✅ 面试里经常会追问证明

3. **区间贪心优先记住“按右端点排序”**
    - ✅ 这是最高频模板之一

## 方案一：通用模板（推荐）

### 线性贪心

```python
farthest = 0
for i, step in enumerate(nums):
    if i > farthest:
        return False
    farthest = max(farthest, i + step)
```

### 排序后贪心

```python
intervals.sort(key=lambda x: x[1])
ans = 0
end = float('-inf')

for left, right in intervals:
    if left >= end:
        ans += 1
        end = right
```

## 常见题型速查

### 1. 跳跃游戏

```python
farthest = 0
for i, step in enumerate(nums):
    if i > farthest:
        return False
    farthest = max(farthest, i + step)
return True
```

### 2. 最少跳跃次数

```python
steps = 0
end = 0
farthest = 0

for i in range(len(nums) - 1):
    farthest = max(farthest, i + nums[i])
    if i == end:
        steps += 1
        end = farthest
```

### 3. 最多不重叠区间

```python
intervals.sort(key=lambda x: x[1])
ans = 0
end = float('-inf')

for left, right in intervals:
    if left >= end:
        ans += 1
        end = right
```

## 实战技巧总结

✅ **先想选择规则，再想证明**

✅ **看到“最少 / 最多 / 是否可行”先试贪心**

✅ **区间选择优先记右端点排序**

✅ **能线性扫解决时别上 DP**

✅ **局部最优必须能推出全局最优**：这点说不清就危险

✅ **贪心代码短，但证明往往是面试重点**

## 参考资料

- [greedy.py](greedy.py) - 跳跃游戏、最少跳跃次数、区间贪心示例
