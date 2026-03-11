# 双指针笔试攻略

## 什么是双指针？

双指针就是维护两个位置，根据题目的单调性一起移动，避免无意义的重复枚举。

- **相向双指针**：常见于有序数组、夹逼最值问题
- **同向双指针**：常见于原地去重、快慢指针覆盖
- **快慢指针**：本质也是双指针，常见于链表和数组原地修改
- 关键不是“两个指针”本身，而是 **移动规则必须有依据**

### 支持的操作

| 模式 | 时间复杂度 | 典型场景 |
|------|------------|----------|
| 相向夹逼 | O(n) | 两数之和、盛水问题 |
| 同向覆盖 | O(n) | 去重、移动零、删除元素 |
| 快慢指针 | O(n) | 环检测、链表中点 |

## 双指针适合解决什么问题？

1. **有序数组配对**
    - 例如：两数之和、三数之和外层框架
    - 时间复杂度：O(n)，优于 O(n^2)

2. **原地删除 / 去重**
    - 例如：删除重复元素、移动零、删除指定值
    - 时间复杂度：O(n)

3. **区间夹逼最优值**
    - 例如：盛最多水的容器
    - 时间复杂度：O(n)

4. **链表快慢指针**
    - 例如：找中点、判环
    - 时间复杂度：O(n)，空间 O(1)

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [代码随想录：双指针总结篇](https://programmercarl.com/%E5%8F%8C%E6%8C%87%E9%92%88%E6%80%BB%E7%BB%93.html) - 很适合求职刷题，把数组、链表、字符串上的双指针套路都串起来了
- [代码随想录：字符串总结篇](https://programmercarl.com/%E5%AD%97%E7%AC%A6%E4%B8%B2%E6%80%BB%E7%BB%93.html) - 适合补字符串里的双指针和原地处理技巧
- [Hello 算法：数组](https://www.hello-algo.com/chapter_array_and_linkedlist/array/) - 更偏基础数据结构视角，适合回头补数组遍历和原地操作的底层直觉

## 笔试场景建议

### 推荐策略

1. **先找单调性，再决定指针怎么动**
    - ✅ 能证明“某一侧一定没必要保留”时，才适合双指针
    - ❌ 没单调性时硬写双指针，通常会错

2. **有序数组优先想相向双指针**
    - ✅ 代码短
    - ✅ 现场容易写稳

3. **原地覆盖题优先想快慢指针**
    - ✅ `read` 负责扫，`write` 负责写
    - ✅ 不需要额外数组

## 方案一：通用模板（推荐）

### 相向双指针

```python
left, right = 0, len(nums) - 1

while left < right:
    s = nums[left] + nums[right]
    if s == target:
        return [left, right]
    if s < target:
        left += 1
    else:
        right -= 1
```

### 同向双指针

```python
write = 0
for x in nums:
    if x != 0:
        nums[write] = x
        write += 1
```

## 常见题型速查

### 1. 有序数组两数之和

```python
left, right = 0, len(nums) - 1
while left < right:
    s = nums[left] + nums[right]
    if s == target:
        return [left, right]
    if s < target:
        left += 1
    else:
        right -= 1
```

### 2. 原地去重

```python
write = 1
for read in range(1, len(nums)):
    if nums[read] != nums[write - 1]:
        nums[write] = nums[read]
        write += 1
```

### 3. 移动零

```python
write = 0
for x in nums:
    if x != 0:
        nums[write] = x
        write += 1

while write < len(nums):
    nums[write] = 0
    write += 1
```

## 实战技巧总结

✅ **先确认单调性**：这是双指针能成立的前提

✅ **有序数组优先想夹逼**

✅ **原地修改优先想 `read / write`**

✅ **返回长度和返回数组要分清**

✅ **指针移动规则写死在 while / for 里**：别到处散落

✅ **三数之和常是排序 + 外层枚举 + 内层双指针**

## 参考资料

- [two_pointers.py](two_pointers.py) - 相向双指针、快慢指针、原地覆盖示例
