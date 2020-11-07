from cvxopt.modeling import variable, op
import time
start = time.time()

row0 = ['name_food', 'price', 'energy', 'protein', 'calcium', 'phosphorus', 'sodium', 'vit_a', 'vit_d3', 'vit_b2']
row1 = ['name_food', 'price', 'energy', 'protein', 'calcium', 'phosphorus', 'sodium', 'vit_a', 'vit_d3', 'vit_b2']
row2 = ['name_food', 'price', 'energy', 'protein', 'calcium', 'phosphorus', 'sodium', 'vit_a', 'vit_d3', 'vit_b2']
table = [row0, row1,  row2]


def work():
    x = variable(range(len(table)), 'x')
    z = (30 * x[0] + 1 * x[1])
    # Функция цели
    mass1 = (90 * x[0] + 5 * x[1] <= 10000)  # "1"
    mass2 = (3 * x[0] - x[1] == 0)  # "2"
    x_non_negative = (x >= 0)  # "3"
    problem = op(z, [mass1, mass2, x_non_negative])
    problem.solve(solver='glpk')
    problem.status
    print("Прибыль:")
    print(abs(problem.objective.value()[0]))
    print("Результат:")
    print(x.value)
    stop = time.time()
    print("Время :")
    print(stop - start)
