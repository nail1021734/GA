import random
from tqdm import tqdm
from math import sin, exp
import copy


def eval(x1, x2):
    return ((x1**2 + x2**2)**0.25) * (sin(50 * (x1**2 + x2**2)**0.1)**2 + 1)


def b2n(binary_list, min_bound, interval):
    num = 0
    for i in range(len(binary_list)):
        num += 2**i * binary_list[i]

    return min_bound + num * interval


def move(p):
    result_list = []
    for x_index in range(len(p)):
        for bit_index in range(len(p[x_index])):
            temp = copy.deepcopy(p)
            temp[x_index][bit_index] = 1 - temp[x_index][bit_index]
            result_list.append(temp)

    return result_list


def anneling_alg(
    min_bound,
    max_bound,
    precision,
    objective,
    T,
    repeat_threshold,
    max_iter
):
    n_bit = 1
    while precision < (max_bound - min_bound) / ((2**n_bit) - 1):
        n_bit += 1
    interval = (max_bound - min_bound) / (2**n_bit)

    now_point = [[random.randint(0, 1) for _ in range(n_bit)]
                 for _ in range(2)]

    best_score = []
    gen_iter = tqdm(range(max_iter))
    cnt = 0
    for iteration in gen_iter:
        all_possible_move = move(p=now_point)
        move_score = [
            eval(
                b2n(binary_list=x1, min_bound=min_bound, interval=interval),
                b2n(binary_list=x2, min_bound=min_bound, interval=interval)
            ) for x1, x2 in all_possible_move
        ]

        if objective == "max":
            best_score.append(max(move_score))
            best_index = move_score.index(best_score[-1])
        elif objective == "min":
            best_score.append(min(move_score))
            best_index = move_score.index(best_score[-1])

        new_point = all_possible_move[best_index]
        best_x1 = b2n(binary_list=new_point[0],
                      min_bound=min_bound, interval=interval)
        best_x2 = b2n(binary_list=new_point[1],
                      min_bound=min_bound, interval=interval)

        gen_iter.set_description(
            desc=f'iter:{iteration}, best_point:({best_x1:.4f}, {best_x2:.4f}), best_score:{best_score[-1]:.4f}'
        )

        if objective == "min" and len(best_score) >= 2 and best_score[-2] < best_score[-1]:
            if random.random() < exp((best_score[-2] - best_score[-1]) / T):
                now_point = new_point
                cnt = 0
            else:
                cnt += 1
        elif objective == "max" and len(best_score) >= 2 and best_score[-2] > best_score[-1]:
            if random.random() < exp((best_score[-1] - best_score[-2]) / T):
                now_point = new_point
                cnt = 0
            else:
                cnt += 1
        else:
            now_point = new_point

        if cnt >= repeat_threshold:
            return best_score[-1], (best_x1, best_x2)

    return best_score[-1], (best_x1, best_x2)


if __name__ == '__main__':
    best_score = []
    best_point = []
    obj = "max"
    for T in [x / 1e5 for x in range(10, 0, -1)]:
        for _ in range(1):
            score, point = anneling_alg(min_bound=0, max_bound=1, precision=1e-4,
                                        objective=obj, T=T, repeat_threshold=1, max_iter=10000)
            best_score.append(score)
            best_point.append(point)
    if obj == "min":
        print(
            f'min_value: {min(best_score)} at point {best_point[best_score.index(min(best_score))]}')
    if obj == "max":
        print(
            f'max_value: {max(best_score)} at point {best_point[best_score.index(max(best_score))]}')
