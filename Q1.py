from random import randint, random
from math import sin
from tqdm import tqdm
import copy
import matplotlib.pyplot as plt

def eval(x1, x2):
    # return x1
    return ((x1**2 + x2**2)**0.25) * (sin(50 * (x1**2 + x2**2)**0.1)**2 + 1)


def b2n(binary_list, min_bound, interval):
    num = 0
    for i in range(len(binary_list)):
        num += 2**i * binary_list[i]

    return min_bound + num * interval


def select(pop, scores, objective, k):
    select_index = randint(0, len(pop) - 1)

    for _ in range(k):
        index = randint(0, len(pop) - 1)
        if objective == "max":
            if scores[select_index] < scores[index]:
                select_index = index
        if objective == "min":
            if scores[select_index] > scores[index]:
                select_index = index
    return pop[select_index]


def crossover(p1, p2, crossover_rate):
    c1, c2 = copy.deepcopy(p1), copy.deepcopy(p2)
    if random() < crossover_rate:
        p_list = list(zip(p1, p2))
        for i in range(len(p_list)):
            x1, x2 = p_list[i]
            cross_point = randint(1, len(x1)-2)
            c1[i] = x1[:cross_point] + x2[cross_point:]
            c2[i] = x2[:cross_point] + x1[cross_point:]
    return [c1, c2]


def mutation(child, mutation_rate):
    temp = copy.deepcopy(child)
    for x_i, x in enumerate(child):
        for bit_i, bit in enumerate(x):
            if random() < mutation_rate:
                temp[x_i][bit_i] = 1 - bit
    return temp


def GA(
    n_pop,
    min_bound,
    max_bound,
    max_iter,
    crossover_rate,
    mutation_rate,
    objective,
    precision=1e-4,
):
    n_bit = 1
    while precision < (max_bound - min_bound) / (2**n_bit - 1):
        n_bit += 1
    interval = (max_bound - min_bound) / (2**n_bit)
    pop = [[[randint(0, 1) for _ in range(n_bit)], [randint(0, 1)
                                                    for _ in range(n_bit)]] for _ in range(n_pop)]
    best_score_list = []
    bit_list = []
    iter_tqdm = tqdm(range(max_iter))

    for iteration in iter_tqdm:
        scores = [
            eval(
                b2n(i[0], min_bound=min_bound, interval=interval),
                b2n(i[1], min_bound=min_bound, interval=interval)
            ) for i in pop]

        selected_parent = [select(pop=pop, scores=scores, objective=objective, k=5)
                           for i in range(n_pop)]
        child_list = []
        if n_pop % 2 == 1:
            child = mutation(
                child=selected_parent[-1],
                mutation_rate=mutation_rate
            )
            child_list.append(child)

        for i in range(
            0,
            len(selected_parent) if len(
                selected_parent) % 2 == 0 else len(selected_parent) - 1,
            2
        ):
            p1, p2 = selected_parent[i], selected_parent[i+1]

            for child in crossover(p1=p1, p2=p2, crossover_rate=crossover_rate):
                child = mutation(child=child, mutation_rate=mutation_rate)
                child_list.append(child)

        if objective == "max":
            best_score, best_index = max(scores), scores.index(max(scores))
            best_x1 = b2n(binary_list=pop[best_index][0],
                          min_bound=min_bound, interval=interval)
            best_x2 = b2n(binary_list=pop[best_index][1],
                          min_bound=min_bound, interval=interval)
        if objective == "min":
            best_score, best_index = min(scores), scores.index(min(scores))
            best_x1 = b2n(binary_list=pop[best_index][0],
                          min_bound=min_bound, interval=interval)
            best_x2 = b2n(binary_list=pop[best_index][1],
                          min_bound=min_bound, interval=interval)

        best_score_list.append(best_score)
        bit_list.append(pop[best_index])
        iter_tqdm.set_description(
            desc=f'iter:{iteration}, best_point:({best_x1:.5f}, {best_x2:.5f}), score:{best_score:.5f}')

        pop = child_list

    return bit_list, best_score_list, [best_x1, best_x2]


if __name__ == "__main__":
    bit_li, best_li, _ = GA(n_pop=10, min_bound=0, max_bound=1, max_iter=1000,
                    crossover_rate=0.25, mutation_rate=0.01, objective="min")
    plt.plot(best_li)
    plt.show()
    # interval = 100
    # for i in range(0, len(best_li), interval):
    #     print(
    #         f'iteration{i}-{i+interval-1} avg:{sum(best_li[i:i+interval])/len(best_li[i:i+interval])}')
    # print(*bit_li, sep='\n')