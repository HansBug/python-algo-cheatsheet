# 扫描线笔试攻略

## 什么是扫描线？

扫描线的核心思想是：把区间或几何问题，改写成按坐标排序的一系列 **事件**，然后从左到右扫描。

- 常见事件是“进入一个区间”和“离开一个区间”
- 扫描过程中维护当前活跃状态
- 典型输出是最大重叠数、总覆盖长度、最少会议室数量
- 这类题最容易错的不是主思路，而是 **边界和同点事件顺序**

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| 事件排序 | O(n log n) | 通常是主要成本 |
| 单次扫描 | O(n) | 维护活跃计数 |
| 最大重叠 / 并长度 | O(n log n) | 高频题型 |

## 扫描线适合解决什么问题？

1. **区间最大重叠数**
    - 例如：最多同时在线人数、最多重叠会议数
    - 时间复杂度：O(n log n)

2. **区间并长度**
    - 例如：总覆盖长度、被覆盖总时间
    - 时间复杂度：O(n log n)

3. **会议室数量**
    - 例如：最少需要几个会议室
    - 时间复杂度：O(n log n)

4. **大坐标覆盖统计**
    - 例如：配合离散化后做更复杂的覆盖问题
    - 时间复杂度：通常 O(n log n)

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [扫描线算法 - 洛谷专栏](https://www.luogu.com/article/8qqwmlka) - 适合先对扫描线能解决什么问题建立直观认识
- [扫描线入门学习笔记（主要讲解代码实现） - 博客园](https://www.cnblogs.com/InductiveSorting-QYF/p/14066580.html) - 更偏模板实现，适合补“事件 + 离散化 / 数据结构”细节
- [「计算几何」扫描线算法与应用--线段交点问题](https://caleb.ink/posts/91/index.html) - 适合从更抽象的事件驱动角度理解扫描线为什么成立

## 笔试场景建议

### 推荐策略

1. **看到“区间重叠 / 覆盖 / 同时进行”先想扫描线**
    - ✅ 这是高频信号

2. **先统一边界定义**
    - ✅ 闭区间还是半开区间一定先想清楚
    - ❌ 这一步没做好，后面全乱

3. **同一坐标的事件顺序要明确**
    - ✅ 例如半开区间 `[l, r)` 常让离开事件先处理

## 方案一：通用模板（推荐）

```python
events = []
for left, right in intervals:
    events.append((left, 1))
    events.append((right, -1))

events.sort(key=lambda x: (x[0], x[1]))

cur = 0
ans = 0
for _, delta in events:
    cur += delta
    ans = max(ans, cur)
```

## 常见题型速查

### 1. 最大重叠数

```python
events = []
for left, right in intervals:
    events.append((left, 1))
    events.append((right, -1))

events.sort(key=lambda x: (x[0], x[1]))
```

### 2. 区间并长度

```python
events.sort()
total = 0
cur = 0
prev = events[0][0]

for x, delta in events:
    if cur > 0:
        total += x - prev
    cur += delta
    prev = x
```

### 3. 最少会议室数量

```python
starts = sorted(left for left, _ in intervals)
ends = sorted(right for _, right in intervals)
j = 0
rooms = 0
```

## 实战技巧总结

✅ **重叠、覆盖、同时在线先想扫描线**

✅ **先把题目翻译成事件**

✅ **边界定义一定先统一**

✅ **同点先入还是先出要明确**

✅ **总覆盖长度通常维护活跃计数**

✅ **大坐标版本常和离散化一起用**

## 参考资料

- [sweep_line.py](sweep_line.py) - 最大重叠数、区间并长度、会议室数量示例
