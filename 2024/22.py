def load_nums() -> [int]:
    with open('22.txt') as f:
        return [int(line.strip()) for line in f]


def main_1() -> None:
    nums = load_nums()
    for i in range(len(nums)):
        n = nums[i]
        for _ in range(2000):
            n = (n ^ (n << 6)) & 0xffffff
            n = (n ^ (n >> 5))
            n = (n ^ (n << 11)) & 0xffffff
        nums[i] = n
    print(sum(nums))


def initial_secret_to_prices_and_diff(n: int) -> ([int], [int]):
    prices = [n % 10]
    for _ in range(2000):
        n = (n ^ (n << 6)) & 0xffffff
        n = (n ^ (n >> 5))
        n = (n ^ (n << 11)) & 0xffffff
        prices.append(n % 10)
    return prices, [prices[i] - prices[i - 1] for i in range(1, len(prices))]


def calc_from_initial(initial: int, diffs_to_sum: {(int, int, int, int): int}) -> None:
    seen_diffs: {(int, int, int, int)} = set()
    diff_d, diff_c, diff_b, diff_a = None, None, None, None
    n = initial
    last_price = n % 10
    for _ in range(2000):
        n = (n ^ (n << 6)) & 0xffffff
        n = (n ^ (n >> 5))
        n = (n ^ (n << 11)) & 0xffffff
        diff_d, diff_c, diff_b, diff_a = diff_c, diff_b, diff_a, n % 10 - last_price
        last_price = n % 10
        key = (diff_d, diff_c, diff_b, diff_a)
        if key not in seen_diffs:
            seen_diffs.add(key)
            diffs_to_sum[key] = diffs_to_sum.get(key, 0) + last_price


def main_2() -> None:
    initial_nums = load_nums()
    diffs_to_sum: {(int, int, int, int): int} = dict()
    for initial in initial_nums:
        calc_from_initial(initial, diffs_to_sum)

    results = set()
    for key, value in diffs_to_sum.items():
        if None not in key:
            results.add(value)
    print(max(results))


if __name__ == '__main__':
    main_1()
    main_2()
