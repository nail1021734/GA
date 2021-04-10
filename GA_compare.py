import GA_binary
import GA_float
import matplotlib.pyplot as plt

test_time = 1
# test_list1 = []
# for pop in range(10, 110, 10):
#     best_list = []
#     for i in range(test_time):
#         best_iter, bit_li, best_li, _ = GA_binary.GA(n_pop=pop, min_bound=0, max_bound=1, max_iter=1000000,
#                         crossover_rate=0.25, mutation_rate=0.01, objective="min")
#         best_list.append(best_iter)
#     test_list1.append(sum(best_list) / test_time)
# print(test_list1)

# test_list2 = []
# for cr in [c_Rate / 100 for c_Rate in range(50, 101, 25)]:
#     best_list = []
#     for i in range(test_time):
#         best_iter, bit_li, best_li, _ = GA_float.GA(n_pop=10, min_bound=0, max_bound=1, max_iter=1000000,
#                         crossover_rate=cr, mutation_rate=0.01, objective="min")
#         best_list.append(best_iter)
#     test_list2.append(sum(best_list) / test_time)
# print(test_list2)

# plt.plot()