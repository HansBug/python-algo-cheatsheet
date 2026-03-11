"""
Python 哈希表计数与去重模板 - 基于 dict / set
支持 Python 3.7-3.14

核心原理：
- `dict` 适合做计数、位置记录、分组
- `set` 适合做去重、判重、快速查存在
- 平均时间复杂度通常是 O(1)，所以很多 O(n^2) 枚举题都能降到 O(n)
"""


def count_freq(nums):
    """统计频次 - O(n)"""
    cnt = {}
    for x in nums:
        cnt[x] = cnt.get(x, 0) + 1
    return cnt


def dedup_keep_order(nums):
    """去重且保留首次出现顺序 - O(n)"""
    seen = set()
    ans = []
    for x in nums:
        if x not in seen:
            seen.add(x)
            ans.append(x)
    return ans


def two_sum(nums, target):
    """两数之和 - O(n)"""
    pos = {}
    for i, x in enumerate(nums):
        need = target - x
        if need in pos:
            return [pos[need], i]
        pos[x] = i
    return []


def group_anagrams(words):
    """字母异位词分组 - O(n * k log k)"""
    groups = {}
    for word in words:
        key = ''.join(sorted(word))
        groups.setdefault(key, []).append(word)
    return list(groups.values())


if __name__ == '__main__':
    print("=" * 60)
    print("Python 哈希表计数与去重模板完整示例")
    print("=" * 60)

    nums = [3, 1, 3, 2, 2, 5, 1]
    print("\n【1. 频次统计】")
    print(count_freq(nums))

    print("\n【2. 去重保序】")
    print(dedup_keep_order(nums))

    print("\n【3. 两数之和】")
    print(two_sum([2, 7, 11, 15], 9))

    print("\n【4. 字母异位词分组】")
    print(group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]))

    print("\n【5. 实战提醒】")
    print("✓ 计数优先写 cnt[x] = cnt.get(x, 0) + 1")
    print("✓ 判重优先想到 set")
    print("✓ 需要保序时，seen 和 ans 分开维护")
    print("✗ 不要一上来就排序，很多题本来能 O(n)")

    print("\n" + "=" * 60)
    print("示例运行完成！")
    print("=" * 60)
