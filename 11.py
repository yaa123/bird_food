from cvxopt.modeling import variable, op
import time
start = time.time()


count_food = 3
price = [0.04, 0.15, 0.4]
energy = []
protein = []
calcium = []
phosphorus = []
sodium = []
vit_a = []
vit_d3 = []
vit_b2 =[]
limit_food_proc = ['' for c in range(count_food)]
limit = ['' for c in range(count_food)]

func_purpose = ''
limit_energy = ''
limit_protein = ''
limit_calcium = ''
limit_phosphorus = ''
limit_sodium = ''
limit_vit_a = ''
limit_vit_d3 = ''
limit_vit_b2 = ''

for i in range(count_food):
    func_purpose = func_purpose + ('{}*x[{}] + '.format(price[i], i))
func_purpose = func_purpose[:-3]
#x = (1, 1)
#aaa = (eval(func_purpose) + 0.1 * x[1])

print(func_purpose)


x_sum = ''
for i in range(count_food):
    x_sum = x_sum + ('x[{}] + '.format(i))
for i in range(count_food):
    limit_food_proc[i] = limit_food_proc[i] + ('x[{}] * {} <= {}'.format(i, price[i], x_sum[:-3]))
print(limit_food_proc)
for i in range(count_food):
    limit[i] = limit[i][:-3]

print(limit)


def work(x, func_purpose, limit):
    x = variable(count_food, 'x')
    func_purpose1 = eval(func_purpose)
    for i in range(len(limit)):
        limit[i] = eval(limit[i])
# Функция цели
    #mass1 = (0.38*x[0] + 0.001*x[1] + 0.002*x[2] >= 0.08)
   # mass2 = (0.09*x[1] + 0.50*x[2] >= 0.22)
   # mass3 = (0.02*x[1] + 0.08*x[2] <= 0.05)
   # mass4 = (x[0] <= (x[0] + x[1] + x[2])*0.05)
   # x_non_negative = (x >= 0)

    problem = op(func_purpose1, limit)
    problem.solve(solver='glpk')
    problem.status
    print("Цена:")
    print(abs(problem.objective.value()[0]))
    print("Результат:")
    print(x.value)
    stop = time.time()
    print("Время :")
    print(stop - start)


work(count_food, func_purpose, limit_food_proc)