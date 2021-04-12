import random
from tqdm import tqdm
from math import sin, exp
import copy


def eval(x1, x2):
    return ((x1**2 + x2**2)**0.25) * (sin(50 * (x1**2 + x2**2)**0.1)**2 + 1)


def move(p, precision, min_bound, max_bound):
    mv_list = [
        [p[0] + random.uniform(precision/10, precision * 1000),
         p[1] + random.uniform(precision/10, precision * 1000)],
        [p[0] + random.uniform(precision/10, precision * 1000),
         p[1] - random.uniform(precision/10, precision * 1000)],
        [p[0] - random.uniform(precision/10, precision * 1000),
         p[1] - random.uniform(precision/10, precision * 1000)],
        [p[0] - random.uniform(precision/10, precision * 1000),
         p[1] + random.uniform(precision/10, precision * 1000)]
    ]
    for m_index, pos in enumerate(mv_list):
        for p_index, num in enumerate(pos):
            if num < min_bound:
                mv_list[m_index][p_index] = min_bound
            if num > max_bound:
                mv_list[m_index][p_index] = max_bound
    return mv_list


def anneling_alg(
    min_bound,
    max_bound,
    precision,
    objective,
    T,
    max_iter
):
    now_point = [random.uniform(min_bound, max_bound) for i in range(2)]
    T_list = []

    while T > 1:
        T_list.append(T)
        T = T * 0.99

    best_score = []
    points = []
    for tm in T_list:
        gen_iter = tqdm(range(max_iter))
        for iteration in gen_iter:
            all_possible_move = move(
                p=now_point,
                precision=precision,
                min_bound=min_bound,
                max_bound=max_bound
            )
            move_score = [eval(x1, x2) for x1, x2 in all_possible_move]

            if objective == "max":
                best_score.append(max(move_score))
                best_index = move_score.index(best_score[-1])
                points.append(all_possible_move[best_index])
            elif objective == "min":
                best_score.append(min(move_score))
                best_index = move_score.index(best_score[-1])
                points.append(all_possible_move[best_index])

            new_point = all_possible_move[best_index]
            best_x1 = new_point[0]
            best_x2 = new_point[1]

            gen_iter.set_description(
                desc=f'iter:{iteration}, T:{tm}, best_point:({best_x1:.4f}, {best_x2:.4f}), best_score:{best_score[-1]:.4f}'
            )

            if objective == "min" and len(best_score) >= 2 and best_score[-2] < best_score[-1]:
                if random.random() < exp((best_score[-2] - best_score[-1]) / T):
                    now_point = new_point
                else:
                    break
            else:
                now_point = new_point
            if objective == "max" and len(best_score) >= 2 and best_score[-2] > best_score[-1]:
                if random.random() < exp((best_score[-1] - best_score[-2]) / T):
                    now_point = new_point
                else:
                    break
            else:
                now_point = new_point
    if objective == "min":
        return min(best_score), points[best_score.index(min(best_score))]
    if objective == "max":
        return max(best_score), points[best_score.index(max(best_score))]

if __name__ == "__main__":
    exp_times = 100
    all_exp_score = []
    for _ in range(exp_times):
        best_score = []
        points = []
        rp_times = 10
        obj = "min"
        for rp in range(rp_times):
            min_score, point = anneling_alg(
                min_bound=0,
                max_bound=1,
                precision=1e-4,
                objective=obj,
                T=10,
                max_iter=10
            )
            best_score.append(min_score)
            points.append(point)
        if obj == "min":
            all_exp_score.append(min(best_score))
            print(min(best_score), points[best_score.index(min(best_score))])
        if obj == "max":
            all_exp_score.append(max(best_score))
            print(max(best_score), points[best_score.index(max(best_score))])
    print(sum(all_exp_score) / exp_times)