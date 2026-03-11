"""
Python 栈（Stack）模板 - 基于 list

Python 里写栈，直接用 list 就够了：
- 入栈：append(x)
- 出栈：pop()
- 看栈顶：st[-1]

支持 Python 3.7-3.14，无第三方依赖

核心原理：
- 栈是后进先出（LIFO）
- list 尾部 append / pop 是摊还 O(1)
- 不要用 insert(0) / pop(0)，那是 O(n)
"""


def is_valid_parentheses(s):
    """括号匹配 - O(n)"""
    pairs = {')': '(', ']': '[', '}': '{'}
    st = []

    for ch in s:
        if ch in '([{':
            st.append(ch)
        elif not st or st.pop() != pairs[ch]:
            return False

    return not st


def eval_rpn(tokens):
    """逆波兰表达式求值 - O(n)"""
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


def remove_adjacent_duplicates(s):
    """消除相邻重复字符 - O(n)"""
    st = []

    for ch in s:
        if st and st[-1] == ch:
            st.pop()
        else:
            st.append(ch)

    return ''.join(st)


def next_greater(nums):
    """下一个更大元素 - O(n)"""
    ans = [-1] * len(nums)
    st = []  # 单调递减栈，存索引

    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            ans[st.pop()] = x
        st.append(i)

    return ans


def dfs_iter(graph, start):
    """迭代 DFS - O(V + E)"""
    order = []
    st = [start]
    seen = {start}

    while st:
        u = st.pop()
        order.append(u)

        # 逆序入栈，结果更接近递归 DFS
        for v in reversed(graph.get(u, [])):
            if v not in seen:
                seen.add(v)
                st.append(v)

    return order


if __name__ == '__main__':
    print("=" * 60)
    print("Python 栈操作完整示例")
    print("=" * 60)

    print("\n【1. 基本操作】")
    print("-" * 60)
    st = []
    st.append(3)
    st.append(5)
    st.append(7)
    print(f"入栈 3, 5, 7 后: {st}")  # [3, 5, 7]
    print(f"当前栈顶: {st[-1]}")  # 7
    print(f"弹出栈顶: {st.pop()}")  # 7
    print(f"弹出后的栈: {st}")  # [3, 5]

    print("\n【2. 括号匹配】")
    print("-" * 60)
    s1 = "()[]{}"
    s2 = "([)]"
    print(f"{s1} -> {is_valid_parentheses(s1)}")  # True
    print(f"{s2} -> {is_valid_parentheses(s2)}")  # False

    print("\n【3. 逆波兰表达式】")
    print("-" * 60)
    tokens = ["2", "1", "+", "3", "*"]
    print(f"{tokens} = {eval_rpn(tokens)}")  # 9

    print("\n【4. 相邻重复字符消除】")
    print("-" * 60)
    s = "abbaca"
    print(f"{s} -> {remove_adjacent_duplicates(s)}")  # ca

    print("\n【5. 下一个更大元素】")
    print("-" * 60)
    nums = [2, 1, 2, 4, 3]
    print(f"{nums} -> {next_greater(nums)}")  # [4, 2, 4, -1, -1]

    print("\n【6. 迭代 DFS】")
    print("-" * 60)
    graph = {
        0: [1, 2],
        1: [3],
        2: [4],
        3: [],
        4: []
    }
    print(f"DFS 顺序: {dfs_iter(graph, 0)}")  # [0, 1, 3, 2, 4]

    print("\n【7. 时间复杂度】")
    print("-" * 60)
    print("append(x)  - O(1) 摊还")
    print("pop()      - O(1) 摊还")
    print("st[-1]     - O(1)")
    print("not st     - O(1)")
    print("len(st)    - O(1)")

    print("\n【8. 实战提醒】")
    print("-" * 60)
    print("✓ 栈就用 list")
    print("✓ 只在尾部操作")
    print("✓ 先判空，再访问 st[-1]")
    print("✗ 不要用 pop(0) / insert(0)")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
