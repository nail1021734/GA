import random
from tqdm import tqdm
from math import sin


def eval(x1, x2):
    return ((x1**2 + x2**2)**0.25) * (sin(50 * (x1**2 + x2**2)**0.1)**2 + 1)


def move(p, precision):
    result_list = [
        [p[0] + precision, p[1] + precision],
        [p[0] + precision, p[1] - precision],
        [p[0] - precision, p[1] - precision],
        [p[0] - precision, p[1] + precision]
    ]

    return result_list


def hill_climbing(
    min_bound,
    max_bound,
    precision,
    objective,
    max_iter
):
    now_point = [random.uniform(min_bound, max_bound) for i in range(2)]

    best_score = []
    gen_iter = tqdm(range(max_iter))
    for iteration in gen_iter:
        all_possible_move = move(p=now_point, precision=precision)
        move_score = [eval(x1, x2) for x1, x2 in all_possible_move]

        if objective == "max":
            best_score.append(max(move_score))
            best_index = move_score.index(best_score[-1])
        elif objective == "min":
            best_score.append(min(move_score))
            best_index = move_score.index(best_score[-1])

        new_point = all_possible_move[best_index]
        best_x1 = new_point[0]
        best_x2 = new_point[1]

        now_point = new_point

        if len(best_score) >= 2:
            if objective == "min" and best_score[-1] > best_score[-2]:
                break
            elif objective == "max" and best_score[-1] < best_score[-2]:
                break

        gen_iter.set_description(
            desc=f'iter:{iteration},best_point:({best_x1:.4f}, {best_x2:.4f}), best_score:{best_score[-1]:.4f}'
        )


if __name__ == '__main__':
    for _ in range(100):
        hill_climbing(min_bound=0, max_bound=1, precision=1e-4,
                      objective="min", max_iter=10000)
