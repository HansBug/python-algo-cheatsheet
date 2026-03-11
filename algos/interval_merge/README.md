# 区间合并笔试攻略

## 什么是区间合并？

区间合并的核心套路很简单：**先排序，再线性扫描**。

- 合并题通常按 **左端点排序**
- 当前区间能接上，就更新右端点
- 接不上，就开一个新区间
- 很多区间题本质上都是这一个套路的变体

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| 合并重叠区间 | O(n log n) | 排序是主要成本 |
| 插入新区间 | O(n log n) | 常可转成合并问题 |
| 删除最少区间 | O(n log n) | 常配合贪心按右端点排序 |

## 区间合并适合解决什么问题？

1. **合并重叠区间**
    - 例如：区间去重、日程整理
    - 时间复杂度：O(n log n)

2. **插入新区间**
    - 例如：往已排序区间里插一个新区间并合并
    - 时间复杂度：O(n) 到 O(n log n)

3. **区间选择**
    - 例如：最少删除几个区间使其互不重叠
    - 时间复杂度：O(n log n)

4. **日程安排类问题**
    - 例如：会议合并、区间冲突检测
    - 时间复杂度：通常 O(n log n)

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [代码随想录：贪心算法总结篇](https://programmercarl.com/%E8%B4%AA%E5%BF%83%E7%AE%97%E6%B3%95%E6%80%BB%E7%BB%93%E7%AF%87.html) - 适合先建立“区间题很多时候是排序 + 贪心”的整体认识
- [代码随想录：本周小结！（贪心算法系列四）](https://programmercarl.com/%E5%91%A8%E6%80%BB%E7%BB%93/20201224%E8%B4%AA%E5%BF%83%E5%91%A8%E6%9C%AB%E6%80%BB%E7%BB%93.html) - 专门把无重叠区间、合并区间这类题串起来讲，和笔试非常贴
- [图算法：拓扑排序-区间合并问题](https://sherryuuer.github.io/techs/algo/merge-intervals.html) - 讲法比较直白，适合快速回顾排序后线性扫描这套模板

## 笔试场景建议

### 推荐策略

1. **区间题先问自己要不要排序**
    - ✅ 这是第一反应
    - ✅ 大多数情况下答案是要

2. **合并题按左端点排**
    - ✅ 方便和当前答案最后一段比较

3. **选择最多不重叠区间按右端点排**
    - ✅ 这是经典贪心
    - ❌ 不要把不同区间题的排序规则混着用

## 方案一：通用模板（推荐）

```python
intervals.sort()
ans = [intervals[0][:]]

for left, right in intervals[1:]:
    if left <= ans[-1][1]:
        ans[-1][1] = max(ans[-1][1], right)
    else:
        ans.append([left, right])
```

## 常见题型速查

### 1. 合并重叠区间

```python
intervals.sort()
ans = [intervals[0][:]]

for left, right in intervals[1:]:
    if left <= ans[-1][1]:
        ans[-1][1] = max(ans[-1][1], right)
    else:
        ans.append([left, right])
```

### 2. 插入新区间

```python
intervals.append(new_interval)
intervals.sort()
# 后面直接套合并模板
```

### 3. 最少删除重叠区间

```python
intervals.sort(key=lambda x: x[1])
keep = 1
end = intervals[0][1]

for left, right in intervals[1:]:
    if left >= end:
        keep += 1
        end = right
```

## 实战技巧总结

✅ **区间题先排序**

✅ **合并题通常按左端点排**

✅ **选择题通常按右端点排**

✅ **先统一闭区间还是半开区间**

✅ **答案列表最后一段常是当前比较对象**

✅ **别在未排序状态下直接分类讨论**

## 参考资料

- [interval_merge.py](interval_merge.py) - 区间合并、插入区间、删除重叠区间示例
