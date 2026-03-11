# 栈（Stack）笔试攻略

## 什么是栈？

栈是一种**后进先出（LIFO, Last In First Out）**的数据结构，最后放进去的元素最先出来。

在 Python 里，栈这玩意**直接用 `list` 就够了**：

- 入栈：`append(x)`
- 出栈：`pop()`
- 看栈顶：`s[-1]`

### 核心性质

1. **后进先出**：最后压进去的元素会最先弹出来
2. **只操作一端**：所有操作都在尾部完成，代码最短也最快
3. **原生 list 足够快**：`append()` 和 `pop()` 在尾部是摊还 O(1)
4. **别碰头部操作**：`insert(0)` 和 `pop(0)` 是 O(n)，笔试里纯属给自己找麻烦

### 支持的操作

| 操作      | 时间复杂度   | 说明                |
|---------|---------|-------------------|
| `push`  | O(1) 摊还 | `s.append(x)` 入栈   |
| `pop`   | O(1) 摊还 | `s.pop()` 出栈      |
| `peek`  | O(1)    | `s[-1]` 查看栈顶     |
| `empty` | O(1)    | `not s` 判断是否为空 |
| `size`  | O(1)    | `len(s)` 获取元素个数 |

## 栈适合解决什么问题？

栈特别适合处理以下场景：

1. **括号匹配**：判断括号是否合法、是否成对出现
    - 时间复杂度：O(n)，一次扫描就够了

2. **表达式求值**：处理中缀表达式、逆波兰表达式、基本计算器
    - 时间复杂度：O(n)，边扫边算

3. **相邻消除 / 撤销操作**：维护“最近一个还没处理掉的元素”
    - 例如：相邻重复字符消除、模拟撤销
    - 时间复杂度：O(n)，优于反复删除的 O(n^2)

4. **迭代版 DFS**：用栈手动模拟递归调用
    - 例如：图遍历、树遍历、Flood Fill
    - 优势：避免递归深度限制，逻辑也更可控

5. **单调栈题型**：找下一个更大/更小元素、柱状图面积等
    - 时间复杂度：通常是 O(n)，优于暴力的 O(n^2)

## 推荐学习资料

如果你想系统学习这个算法，建议按下面顺序看这些中文资料：

- [Hello 算法：栈](https://www.hello-algo.com/chapter_stack_and_queue/stack/) - 图示很直观，适合先把栈的定义、基本操作和底层实现过一遍
- [数据结构电子讲义：栈和队列的概念与实现](https://www.xmut-lby.work/ds-book/03/1.implementation.html) - 更偏教材风格，适合补顺序栈、链栈这些实现细节
- [labuladong：队列实现栈以及栈实现队列](https://labuladong.online/zh/algo/data-structure/stack-queue/) - 更偏面试题视角，适合把基础结构和题目套路连起来

## 笔试场景建议

### 推荐策略

1. **直接用 `list`**
    - ✅ 最短、最好记、最快上手
    - ✅ `append()`、`pop()`、`[-1]` 足够覆盖绝大多数题目
    - ✅ 不需要任何额外封装

2. **所有操作都放在尾部**
    - ✅ `append()` / `pop()` 是摊还 O(1)
    - ✅ 写法最顺手，不容易出错
    - ❌ 不要用 `insert(0)` / `pop(0)`，那是 O(n)

3. **除非题目强制要求类接口，否则别额外包一层**
    - ✅ `st = []` 比 `Stack()` 更省代码
    - ✅ 少一层封装，出错点更少
    - ❌ 包装得太花反而拖慢你

## 复杂性速览

说明：以下分数由 `python -m tools.interview_complexity` 对各方案的核心模板代码测得。分数越低，越适合现场手写。

| 方案 | 核心代码口径 | 复杂性分数 | 等级 | 面试建议 |
|------|-------------|----------|------|---------|
| 直接使用 `list` | README 里的最小模板片段 | `0.0` | 很容易手写 | 推荐，几乎没有额外模板负担 |
| 手动实现 `Stack` 类 | README 里的类接口模板 | `3.4` | 很容易手写 | 只有题目强制要类接口时再写 |

两种写法都不难，但 `list` 方案少一层封装，笔试里更顺手也更稳。

## 方案一：直接使用 list（推荐）

### 基本用法

```python
# 栈 = list
st = []

st.append(3)      # 入栈
st.append(5)
top = st[-1]      # 看栈顶: 5
x = st.pop()      # 出栈: 5
empty = not st    # 判空
size = len(st)    # 当前大小
```

### 括号匹配

```python
def is_valid(s):
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []

    for ch in s:
        if ch in '([{':
            st.append(ch)
        elif not st or st.pop() != pairs[ch]:
            return False

    return not st
```

### 逆波兰表达式

```python
def eval_rpn(tokens):
    st = []

    for token in tokens:
        if token not in '+-*/':
            st.append(int(token))
            continue

        b = st.pop()
        a = st.pop()

        if token == '+':
            st.append(a + b)
        elif token == '-':
            st.append(a - b)
        elif token == '*':
            st.append(a * b)
        else:
            st.append(int(a / b))  # 向 0 截断

    return st[-1]
```

### 迭代版 DFS

```python
def dfs(graph, start):
    st = [start]
    seen = {start}
    order = []

    while st:
        u = st.pop()
        order.append(u)

        # 逆序入栈，遍历顺序更接近递归写法
        for v in reversed(graph[u]):
            if v not in seen:
                seen.add(v)
                st.append(v)

    return order
```

### 单调栈基础模板

```python
def next_greater(nums):
    ans = [-1] * len(nums)
    st = []  # 存索引，保持对应值单调递减

    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            ans[st.pop()] = x
        st.append(i)

    return ans
```

**完整实现和更多示例**：[stack_list.py](stack_list.py)

## 方案二：手动实现栈（只在题目强制要求类接口时使用）

### 适合速记的栈实现

```python
class Stack:
    def __init__(self):
        self.s = []

    def push(self, x):
        """入栈 - O(1) 摊还"""
        self.s.append(x)

    def pop(self):
        """出栈 - O(1) 摊还"""
        return self.s.pop()

    def peek(self):
        """查看栈顶 - O(1)"""
        return self.s[-1]

    def empty(self):
        """判空 - O(1)"""
        return not self.s
```

### 使用示例

```python
st = Stack()
st.push(1)
st.push(2)
print(st.peek())   # 2
print(st.pop())    # 2
print(st.empty())  # False
```

> 实战建议：上面这个类只是给“题目强制要类接口”的场景准备的。正常笔试，直接写 `st = []` 就行。

## 常见题型速查

### 1. 括号匹配

```python
st = []
pairs = {')': '(', ']': '[', '}': '{'}

for ch in s:
    if ch in '([{':
        st.append(ch)
    elif not st or st.pop() != pairs[ch]:
        return False

return not st
```

### 2. 逆波兰表达式

```python
st = []
for token in tokens:
    if token not in '+-*/':
        st.append(int(token))
        continue

    b = st.pop()
    a = st.pop()
    if token == '+':
        st.append(a + b)
    elif token == '-':
        st.append(a - b)
    elif token == '*':
        st.append(a * b)
    else:
        st.append(int(a / b))
```

### 3. 相邻重复字符消除

```python
st = []
for ch in s:
    if st and st[-1] == ch:
        st.pop()
    else:
        st.append(ch)

return ''.join(st)
```

### 4. 下一个更大元素

```python
ans = [-1] * len(nums)
st = []

for i, x in enumerate(nums):
    while st and nums[st[-1]] < x:
        ans[st.pop()] = x
    st.append(i)

return ans
```

### 5. 迭代 DFS

```python
st = [start]
seen = {start}

while st:
    u = st.pop()
    # 处理节点 u

    for v in reversed(graph[u]):
        if v not in seen:
            seen.add(v)
            st.append(v)
```

## 实战技巧总结

✅ **栈就用 `list`**：别为了栈专门引 `deque`

✅ **入栈 / 出栈 / 栈顶**：记住 `append()`、`pop()`、`s[-1]`

✅ **先判空再看栈顶**：写 `if st and st[-1] == ...`

✅ **别碰头部操作**：`pop(0)` 和 `insert(0)` 都是 O(n)

✅ **单调栈通常存索引**：这样既能拿值，也能算距离

✅ **模拟递归时逆序入栈**：更容易和递归遍历顺序对齐

✅ **字符串消除题直接存字符**：别额外搞节点对象

## 参考资料

- [stack_list.py](stack_list.py) - 使用 `list` 实现栈的完整示例

**推荐阅读顺序**：

1. 先看本 README，记住 `append()` / `pop()` / `[-1]`
2. 再看 `stack_list.py`，熟悉几个最常见题型
3. 真到笔试里，优先直接写 `st = []`
