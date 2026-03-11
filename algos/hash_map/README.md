# 哈希表计数与去重笔试攻略

## 什么是哈希表计数与去重？

这里说的不是单独讲哈希表原理，而是笔试里最常见的 **`dict` / `set` 套路**：用哈希表做计数、判重、查位置、分组。

- **`dict`**：适合做频次统计、位置记录、键值映射
- **`set`**：适合做判重、去重、快速查存在
- 平均时间复杂度通常是 **O(1)**，很多暴力双循环都能降到 **O(n)**
- 这类题往往没有复杂数据结构，关键就是第一时间想到“拿空间换时间”

### 支持的操作

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| `x in d` / `x in s` | O(1) 平均 | 判断是否出现过 |
| `d.get(x, 0)` | O(1) 平均 | 计数默认值 |
| `d[x] = v` | O(1) 平均 | 更新映射 |
| `s.add(x)` | O(1) 平均 | 加入集合 |
| `del d[x]` | O(1) 平均 | 删除键 |

## 哈希表计数与去重适合解决什么问题？

1. **频次统计**
    - 例如：出现次数最多的元素、字符计数、Top K 高频元素
    - 时间复杂度：通常 O(n)，明显优于每次都去扫一遍数组

2. **判重与去重**
    - 例如：数组去重、是否存在重复元素、保序去重
    - 时间复杂度：通常 O(n)，优于排序后再慢慢比较的 O(n log n)

3. **查补数 / 查配对**
    - 例如：两数之和、存在差值为 k 的配对
    - 时间复杂度：通常 O(n)，优于 O(n^2) 枚举

4. **记录首次 / 最后一次出现位置**
    - 例如：最长不重复子串、最短覆盖子串的一部分变体
    - 时间复杂度：通常 O(n)

5. **按特征分组**
    - 例如：字母异位词分组、相同签名字符串聚类
    - 时间复杂度：通常 O(n * 构造 key 的代价)

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [Hello 算法：哈希表](https://www.hello-algo.com/chapter_hashing/hash_map/) - 适合先把哈希表的抽象概念、增删查改和时间复杂度过一遍
- [代码随想录：哈希表理论基础](https://programmercarl.com/%E5%93%88%E5%B8%8C%E8%A1%A8%E7%90%86%E8%AE%BA%E5%9F%BA%E7%A1%80.html) - 更偏刷题视角，适合理解数组、`set`、`map` 分别该怎么用
- [代码随想录：哈希表总结篇](https://programmercarl.com/%E5%93%88%E5%B8%8C%E8%A1%A8%E6%80%BB%E7%BB%93.html) - 适合把常见哈希题型串起来看，建立“计数 / 判重 / 映射 / 分组”的题感

## 笔试场景建议

### 推荐策略

1. **优先直接写 `dict` / `set`**
    - ✅ 代码最短
    - ✅ Python 里这就是正解
    - ✅ 绝大多数求职题不需要自己实现哈希表

2. **计数时优先写 `d[x] = d.get(x, 0) + 1`**
    - ✅ 兼容 Python 3.7-3.14
    - ✅ 比先判断 `if x in d` 更顺手

3. **需要保序时，`seen` 和 `ans` 分开维护**
    - ✅ `set` 负责判重
    - ✅ `list` 负责输出顺序
    - ❌ 不要把“去重”和“保序”混成一件事

4. **题目只要求是否存在时，不要多存没必要的信息**
    - ✅ 能存布尔就别存大对象
    - ✅ 能存一次位置就别存全部位置

## 方案一：使用 `dict` / `set`（推荐）

### 频次统计

```python
cnt = {}
for x in nums:
    cnt[x] = cnt.get(x, 0) + 1
```

### 去重保序

```python
seen = set()
ans = []

for x in nums:
    if x not in seen:
        seen.add(x)
        ans.append(x)
```

### 两数之和

```python
pos = {}

for i, x in enumerate(nums):
    need = target - x
    if need in pos:
        return [pos[need], i]
    pos[x] = i
```

## 常见题型速查

### 1. 出现次数统计

```python
cnt = {}
for x in nums:
    cnt[x] = cnt.get(x, 0) + 1

best = None
for x, c in cnt.items():
    if best is None or c > cnt[best]:
        best = x
```

### 2. 保序去重

```python
seen = set()
ans = []

for x in nums:
    if x not in seen:
        seen.add(x)
        ans.append(x)
```

### 3. 两数之和

```python
pos = {}
for i, x in enumerate(nums):
    if target - x in pos:
        return [pos[target - x], i]
    pos[x] = i
```

## 实战技巧总结

✅ **计数优先用 `dict`**：别先排序再数

✅ **判重优先用 `set`**：别每次都在线性查找

✅ **默认值优先用 `get()`**：少写一层分支

✅ **保序去重要双结构**：`seen + ans`

✅ **配对题优先查补数**：常能把 O(n^2) 降成 O(n)

✅ **分组题先想 key**：把复杂对象变成可哈希签名

## 参考资料

- [hash_map_tricks.py](hash_map_tricks.py) - 哈希表计数、去重、两数之和、分组示例
