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
        [p[0] - precision, p[1] + precision],
        [p[0], p[1]]
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

    gen_iter = tqdm(range(max_iter))
    for iteration in gen_iter:
        all_possible_move = move(p=now_point, precision=precision)
        move_score = [eval(x1, x2) for x1, x2 in  all_possible_move]
        if objective == "max":
            best_index = move_score.index(max(move_score))
            if best_index == len(move_score) - 1:
                gen_iter.set_description(
                    desc=f'iter:{iteration},best_point:({now_point[0]:.4f}, {now_point[1]:.4f}), best_score:{min(move_score)}'
                )
                break
            now_point = all_possible_move[best_index]
            best_score = max(move_score)
        if objective == "min":
            best_index = move_score.index(min(move_score))
            if best_index == len(move_score) - 1:
                gen_iter.set_description(
                    desc=f'iter:{iteration}, best_point:({now_point[0]:.4f}, {now_point[1]:.4f}), best_score:{min(move_score):.4f}'
                )
                break
            now_point = all_possible_move[best_index]
            best_score = min(move_score)

        gen_iter.set_description(
            desc=f'iter:{iteration},best_point:({now_point[0]:.4f}, {now_point[1]:.4f}), best_score:{min(move_score):.4f}'
        )

if __name__ == '__main__':
    for _ in range(100):
        hill_climbing(min_bound=0, max_bound=1, precision=1e-4, objective="min", max_iter=10000)