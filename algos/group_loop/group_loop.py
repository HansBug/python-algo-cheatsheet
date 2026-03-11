"""
Python 分组循环模板 - 按连续相同元素分段处理
支持 Python 3.7-3.14

核心原理：
- 用 `i` 指向一组的开头，再用 `j` 扫到这一组的结尾
- 每轮处理一整组 `[i, j)`，然后令 `i = j`
- 很多字符串压缩、连续段统计、按值分块的题都能直接套
"""


def split_groups(nums):
    """把连续相同元素切成若干组 - O(n)"""
    ans = []
    i = 0
    n = len(nums)

    while i < n:
        j = i + 1
        while j < n and nums[j] == nums[i]:
            j += 1
        ans.append((nums[i], i, j - 1, j - i))
        i = j

    return ans


def compress_string(s):
    """字符串压缩 - O(n)"""
    if not s:
        return ''

    parts = []
    i = 0

    while i < len(s):
        j = i + 1
        while j < len(s) and s[j] == s[i]:
            j += 1
        parts.append(s[i] + str(j - i))
        i = j

    return ''.join(parts)


def longest_run(s):
    """最长连续重复段长度 - O(n)"""
    ans = 0
    i = 0

    while i < len(s):
        j = i + 1
        while j < len(s) and s[j] == s[i]:
            j += 1
        ans = max(ans, j - i)
        i = j

    return ans


if __name__ == '__main__':
    print("=" * 60)
    print("Python 分组循环模板完整示例")
    print("=" * 60)

    print("\n【1. 连续段拆分】")
    print(split_groups([1, 1, 1, 2, 2, 3, 5, 5]))

    print("\n【2. 字符串压缩】")
    print(compress_string("aaabbccccd"))

    print("\n【3. 最长连续重复段】")
    print(longest_run("abbcccddddcc"))

    print("\n【4. 实战提醒】")
    print("✓ 分组循环的核心是 while i < n")
    print("✓ 每轮先找 j，再统一处理 [i, j)")
    print("✓ 连续相同元素题别一位一位硬分类讨论")
    print("✗ 别忘了最后令 i = j")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
