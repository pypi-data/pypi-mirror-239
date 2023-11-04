import itertools
import numba


# @numba.jit(nopython=True)  # Just-in-time compilation (即时编译)
def ess(n):
    """
    求2到n范围内所有素数
    https://zhuanlan.zhihu.com/p/400818808
    """
    es = [2]
    Td = [True] * (n + 1)
    for i in range(3, n + 1, 2):
        if Td[i]:
            es.append(i)
            for j in range(i ** 2, n + 1, 2 * i):
                Td[j] = False
    return es


def chunk(ary, size: int, is_iter: bool = False):
    """
    同 PHP 的 array_chunk
    例如: chunk(range(1, 15), 3)
    https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    """
    _arr = iter(ary)
    _itr = iter(lambda: tuple(itertools.islice(_arr, size)), ())
    return _itr if is_iter else list(_itr)


def array_split(ary, count: int) -> list:
    """
    将 ary 里的数据尽量均分成 count 份
    例如: array_split(list(range(1, 15)), 3)
    效果类似于 numpy.array_split(range(1,15), 3)
    """
    nums = [int(len(ary) / count) for _ in range(count)]
    for i in range(len(ary) - int(len(ary) / count) * count):  # 还剩这些数据尚未分配
        nums[i] += 1
    pairs = [(sum(nums[0:i]), nums[i]) for i in range(count)]
    parts = [ary[begin: begin + num] for begin, num in pairs]
    return parts


if __name__ == "__main__":
    print(array_split(list(range(1, 15)), 18))
