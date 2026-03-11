# 离散化笔试攻略

## 什么是离散化？

离散化就是把很大的、很稀疏的值，映射成连续的小整数下标。

- 常见于值域特别大，但实际只出现了很少几个坐标
- 先 `排序 + 去重`
- 再建立 `原值 -> 排名` 的映射
- 这样就能安心开数组、做前缀和、做差分、做树状数组

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| 排序去重 | O(n log n) | 拿到所有出现过的值 |
| 值映射为下标 | O(n) | 通过字典映射 |
| 区间离散化 | O(n log n) | 常保留 `right + 1` |

## 离散化适合解决什么问题？

1. **值域很大但数据很少**
    - 例如：坐标能到 `10^9`，但只有几千个点
    - 时间复杂度：O(n log n)

2. **大坐标上的前缀和 / 差分**
    - 例如：区间覆盖、座位统计、扫描线
    - 时间复杂度：通常 O(n log n)

3. **排名映射**
    - 例如：把原数组映射成相对大小排名
    - 时间复杂度：O(n log n)

4. **树状数组 / 线段树预处理**
    - 例如：需要把原值压成可维护的下标
    - 优势：空间从按值域开，变成按出现数开

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [洛谷题单：前缀和、差分与离散化](https://www.luogu.com.cn/training/200) - 这类技巧题放在一起练很合适，适合先建立离散化的使用场景
- [离散化算法实例讲解 - Dotcpp编程](https://www.dotcpp.com/course/1005) - 讲法比较直接，适合快速理解“排序去重 + 建映射”这套动作
- [博客园：洛谷题单指南-前缀和差分与离散化](https://www.cnblogs.com/hackerchef/p/18336075) - 更偏实战题，适合看离散化和差分如何组合出题

## 笔试场景建议

### 推荐策略

1. **看到值域极大但元素数不多，先想离散化**
    - ✅ 这是最典型信号
    - ✅ 很多空间爆炸题都靠它救

2. **需要还原原值时保留有序数组 `xs`**
    - ✅ `xs[idx]` 就是离散下标对应的原值

3. **区间题别忘了把 `right + 1` 也收进去**
    - ✅ 差分和扫描线里很常见

## 方案一：通用模板（推荐）

```python
xs = sorted(set(nums))
rank = {x: i for i, x in enumerate(xs)}
compressed = [rank[x] for x in nums]
```

## 常见题型速查

### 1. 普通值离散化

```python
xs = sorted(set(nums))
rank = {x: i for i, x in enumerate(xs)}
compressed = [rank[x] for x in nums]
```

### 2. 排名映射

```python
xs = sorted(set(nums))
rank = {x: i + 1 for i, x in enumerate(xs)}
ans = [rank[x] for x in nums]
```

### 3. 区间离散化

```python
xs = []
for left, right in segments:
    xs.append(left)
    xs.append(right + 1)

xs = sorted(set(xs))
rank = {x: i for i, x in enumerate(xs)}
```

## 实战技巧总结

✅ **值域大、数据少时优先想离散化**

✅ **排序去重后再建映射**

✅ **需要还原时保留 `xs`**

✅ **区间差分题常把 `right + 1` 一起压缩**

✅ **离散化保持相对大小关系**：不是乱编号

✅ **常和差分、扫描线、树状数组一起出现**

## 参考资料

- [discretization.py](discretization.py) - 值离散化、排名映射、区间离散化示例
