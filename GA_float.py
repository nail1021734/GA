from random import randint, random, uniform
from math import sin
from tqdm import tqdm
import copy


def eval(x1, x2):
    # return x1
    return ((x1**2 + x2**2)**0.25) * (sin(50 * (x1**2 + x2**2)**0.1)**2 + 1)

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
        c1[randint(0, len(c1) - 1)] = p2[randint(0, len(p2) - 1)]
        c2[randint(0, len(c2) - 1)] = p1[randint(0, len(p1) - 1)]
    return [c1, c2]


def mutation(child, min_bound, max_bound, mutation_rate):
    temp = copy.deepcopy(child)
    for x_i, x in enumerate(child):
        if random() < mutation_rate:
            temp[randint(0, len(temp) - 1)] = uniform(min_bound, max_bound)
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
    pop = [[uniform(min_bound, max_bound) for _ in range(2)] for _ in range(n_pop)]

    best_score_list = []
    bit_list = []
    iter_tqdm = tqdm(range(max_iter))

    for iteration in iter_tqdm:
        scores = [eval(i[0], i[1]) for i in pop]

        selected_parent = [select(pop=pop, scores=scores, objective=objective, k=3)
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
                child = mutation(
                    child=child,
                    max_bound=max_bound,
                    min_bound=min_bound,
                    mutation_rate=mutation_rate
                )
                child_list.append(child)

        if objective == "max":
            best_score, best_index = max(scores), scores.index(max(scores))
            best_x1, best_x2 = pop[best_index][0], pop[best_index][1]
        if objective == "min":
            best_score, best_index = min(scores), scores.index(min(scores))
            best_x1, best_x2 = pop[best_index][0], pop[best_index][1]

        best_score_list.append(best_score)
        iter_tqdm.set_description(
            desc=f'iter:{iteration}, best_point:({best_x1:.5f}, {best_x2:.5f}), score:{best_score:.5f}')

        pop = child_list

    return best_score_list, [best_x1, best_x2]


if __name__ == "__main__":
    best_li, _ = GA(n_pop=100, min_bound=0, max_bound=1, max_iter=10000,
                    crossover_rate=0.25, mutation_rate=0.01, objective="min")
    interval = 100
    for i in range(0, len(best_li), interval):
        print(
            f'iteration{i}-{i+interval-1} avg:{sum(best_li[i:i+interval])/len(best_li[i:i+interval])}')