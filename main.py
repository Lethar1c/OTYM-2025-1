import math
from collections import defaultdict
from functools import lru_cache


def generate_expressions_optimized(max_pis):
    expressions = defaultdict(dict)

    expressions[1][math.pi] = "π"
    expressions[1][3.0] = "⌊π⌋"  # math.floor(math.pi)
    expressions[1][math.pi - 3] = "{π}"

    for k in range(2, max_pis + 1):
        current = {}

        splits = [(a, k - a) for a in range(1, k // 2 + 1)]

        for a, b in splits:
            for x, x_expr in expressions[a].items():
                for y, y_expr in expressions[b].items():
                    val = x + y
                    if val not in current:
                        current[val] = f"({x_expr}+{y_expr})"

                    val = x - y
                    if val > 1e-10 and val not in current:
                        current[val] = f"({x_expr}-{y_expr})"

                    val = y - x
                    if val > 1e-10 and val not in current:
                        current[val] = f"({y_expr}-{x_expr})"

                    val = x * y
                    if val not in current:
                        current[val] = f"({x_expr}*{y_expr})"

                    if abs(y) > 1e-10:
                        val = x / y
                        if val not in current:
                            current[val] = f"({x_expr}/{y_expr})"

                    if abs(x) > 1e-10:
                        val = y / x
                        if val not in current:
                            current[val] = f"({y_expr}/{x_expr})"

                    y_floor = math.floor(y)
                    if abs(y_floor) > 1e-10:
                        val = x / y_floor
                        if val not in current:
                            current[val] = f"({x_expr}/⌊{y_expr}⌋)"

        for val, expr in expressions[k - 1].items():
            floor_val = math.floor(val)
            if floor_val not in current:
                current[floor_val] = f"⌊{expr}⌋"

            frac_part = val - floor_val
            if frac_part not in current:
                current[frac_part] = f"{{{expr}}}"

        expressions[k] = current

    return expressions


@lru_cache(maxsize=None)
def find_min_pi_cached(n, max_pis=6):
    expressions = generate_expressions_optimized(max_pis)
    for k in sorted(expressions.keys()):
        for num in expressions[k]:
            if abs(num - n) < 1e-9:
                return k, expressions[k][num]
    return None, None


if __name__ == "__main__":
    test_numbers = [i for i in range(1, 1001)] # список чисел, для которых нужно найти представление
    max_pis = 5  # максимальное количество экземпляров числа pi.

    for n in test_numbers:
        k, expr = find_min_pi_cached(n, max_pis=max_pis)
        if expr:
            print(f"n = {n:5d}: {expr:60s} (за {k} π)")
        else:
            print(f"n = {n:5d}: не найдено за {max_pis} π")
