import random
from tqdm import tqdm
from math import sin


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
        elif objective == "min":
            best_score.append(min(move_score))
            best_index = move_score.index(best_score[-1])

        new_point = all_possible_move[best_index]
        best_x1 = new_point[0]
        best_x2 = new_point[1]
        last_x1 = now_point[0]
        last_x2 = now_point[1]

        now_point = new_point

        if len(best_score) >= 2:
            if objective == "min" and best_score[-1] > best_score[-2]:
                return best_score[-2], (last_x1, last_x2)
            elif objective == "max" and best_score[-1] < best_score[-2]:
                return best_score[-2], (last_x1, last_x2)

        gen_iter.set_description(
            desc=f'iter:{iteration},best_point:({best_x1:.4f}, {best_x2:.4f}), best_score:{best_score[-1]:.4f}'
        )
    return best_score[-1], (best_x1, best_x2)

if __name__ == '__main__':
    exp_times = 100
    exp_result = []
    for _ in range(exp_times):
        rp_times = 1000
        score_list = []
        points = []
        for _ in range(rp_times):
            score, point = hill_climbing(min_bound=0, max_bound=1, precision=1e-4,
                        objective="min", max_iter=10)
            score_list.append(score)
            points.append(point)
        print(f'min_score: {min(score_list)}, point:{points[score_list.index(min(score_list))]}')
        exp_result.append(min(score_list))
    print(sum(exp_result) / exp_times)