"""
Python 单调栈（Monotonic Stack）模板 - 基于 list

推荐写法：
- 用 list 当栈
- 栈里优先存索引，方便算距离和边界
- 每个元素最多进栈一次、出栈一次，所以总复杂度通常是 O(n)

支持 Python 3.7-3.14，无第三方依赖

核心原理：
- 单调递减栈常用来找下一个更大元素
- 单调递增栈常用来找下一个更小元素
- 重复值题要先想清楚严格 / 非严格比较
"""


def next_greater(nums):
    """下一个更大元素 - O(n)"""
    ans = [-1] * len(nums)
    st = []  # 单调递减栈，存索引

    for i, x in enumerate(nums):
        while st and nums[st[-1]] < x:
            ans[st.pop()] = x
        st.append(i)

    return ans


def previous_less_index(nums):
    """左边第一个更小元素的索引 - O(n)"""
    ans = [-1] * len(nums)
    st = []  # 单调递增栈，存索引

    for i, x in enumerate(nums):
        while st and nums[st[-1]] >= x:
            st.pop()
        ans[i] = st[-1] if st else -1
        st.append(i)

    return ans


def daily_temperatures(temperatures):
    """每日温度 - O(n)"""
    ans = [0] * len(temperatures)
    st = []  # 单调递减栈，存还没找到更高温度的天数

    for i, t in enumerate(temperatures):
        while st and temperatures[st[-1]] < t:
            j = st.pop()
            ans[j] = i - j
        st.append(i)

    return ans


def largest_rectangle_area(heights):
    """柱状图最大矩形 - O(n)"""
    ans = 0
    st = []

    for i, h in enumerate(heights + [0]):  # 末尾补 0，统一触发结算
        while st and heights[st[-1]] >= h:
            height = heights[st.pop()]
            left = st[-1] if st else -1
            ans = max(ans, height * (i - left - 1))
        st.append(i)

    return ans


def sum_subarray_mins(nums):
    """子数组最小值之和 - O(n)"""
    n = len(nums)
    left = [-1] * n
    right = [n] * n
    st = []

    # 左边保留 <= 当前值的最近位置
    for i, x in enumerate(nums):
        while st and nums[st[-1]] > x:
            st.pop()
        left[i] = st[-1] if st else -1
        st.append(i)

    st = []
    # 右边保留 < 当前值的最近位置，重复值只算一边
    for i in range(n - 1, -1, -1):
        while st and nums[st[-1]] >= nums[i]:
            st.pop()
        right[i] = st[-1] if st else n
        st.append(i)

    total = 0
    for i, x in enumerate(nums):
        total += x * (i - left[i]) * (right[i] - i)

    return total


if __name__ == '__main__':
    print("=" * 60)
    print("Python 单调栈模板完整示例")
    print("=" * 60)

    print("\n【1. 下一个更大元素】")
    print("-" * 60)
    nums = [2, 1, 2, 4, 3]
    print(f"{nums} -> {next_greater(nums)}")  # [4, 2, 4, -1, -1]

    print("\n【2. 左边第一个更小元素】")
    print("-" * 60)
    nums = [3, 7, 4, 2, 5]
    print(f"{nums} -> {previous_less_index(nums)}")  # [-1, 0, 0, -1, 3]

    print("\n【3. 每日温度】")
    print("-" * 60)
    temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    print(f"{temperatures} -> {daily_temperatures(temperatures)}")

    print("\n【4. 柱状图最大矩形】")
    print("-" * 60)
    heights = [2, 1, 5, 6, 2, 3]
    print(f"{heights} -> {largest_rectangle_area(heights)}")  # 10

    print("\n【5. 子数组最小值之和】")
    print("-" * 60)
    nums = [3, 1, 2, 4]
    print(f"{nums} -> {sum_subarray_mins(nums)}")  # 17

    print("\n【6. 时间复杂度】")
    print("-" * 60)
    print("push / pop  - O(1) 摊还")
    print("peek        - O(1)")
    print("单次扫描      - O(n)")

    print("\n【7. 实战提醒】")
    print("-" * 60)
    print("✓ 单调栈优先存索引")
    print("✓ 找更大: 维护递减栈")
    print("✓ 找更小: 维护递增栈")
    print("✓ 重复值先想清楚严格 / 非严格")
    print("✗ 不要把边界和数值逻辑混在一起硬写")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
