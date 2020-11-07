from scipy.optimize import linprog
import time
import pandas as pd
print('Введите номер птицы')
num_bird = int(input())
#print('Введите количество корма')
#count_food = int(input())

row = ['Energy', 'Protein', 'Calcium', 'Phosphorus', 'Sodium', 'Vit_A', 'Vit_D3', 'Vit_B2']

food = pd.read_excel('calculation_food.xlsx', sheet_name='Корма', header=3)
food = food.fillna(0)

bird = pd.read_excel('calculation_food.xlsx', sheet_name='Птица', header=3)
bird = bird.fillna(0)

c = []
for i in range(food.index.stop):
    c.append(food['Price'][i])

A_ub = []
for i in row:
    temp = []
    for j in range(food.index.stop):
        temp.append(-food[i][j])
    A_ub.append(temp)
temp = []
for i in range(food.index.stop):
    temp.append(food['Limit'][i] * 0.01)

for i in temp:
    temp2 = []
    for j in range(food.index.stop):
        temp2.append(-i)
    temp2[0] = 1 - i
    A_ub.append(temp2)

b_ub = []
for i in range(len(bird.loc[num_bird])):
    b_ub.append(bird.loc[num_bird][i] * -1)
b_ub = b_ub[1:-1]
for i in range(food.index.stop):
    b_ub.append(0)

A_eq = [[100 for i in range(food.index.stop)]]
b_eq = [[1000]]


def work(c, A_ub, b_ub, A_eq, b_eq):
    start = time.time()
    x = linprog(c, A_ub, b_ub, A_eq, b_eq, options={"presolve": False})
    stop = time.time()
    #print("Время : {}".format(stop - start))
    return x.x


#work(c, A_ub, b_ub, A_eq, b_eq)
result = pd.Series(work(c, A_ub, b_ub, A_eq, b_eq))
#result.to_excel('result.xlsx', sheet_name='123')
#print(result)

x_food = pd.Series(result)
result_food = []
for i in row:
    result_food.append((x_food * food[i]).sum())
print(row)
print(result_food)
