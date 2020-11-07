from scipy.optimize import linprog
import time
import pandas as pd


inaccuracy = (0.95, 1.2)

# print('Введите количество корма')
# count_food = int(input())

food = pd.read_excel('calculation_food.xlsx', sheet_name='Корма', header=3)
food = food.fillna(0)

row = food.columns.tolist()
row = row[2:-2]

bird = pd.read_excel('calculation_food.xlsx', sheet_name='Птица', header=3)
bird = bird.fillna(0)

print('Введите название птицы')
name_bird = input()

while name_bird not in bird['Name_bird'].tolist():
    print('Введите название еще раз')
    name_bird = input()
else:
    for i in range(len(bird['Name_bird'])):
        if bird['Name_bird'][i] == name_bird:
            num_bird = i
print('Содержание необходимых веществ в корме, не менее {} % и не более {} %'.format(inaccuracy[0] * 100, inaccuracy[1] * 100))


def make_params(num_bird, bird, row, food):
    c = []
    for i in range(food.index.stop):
        c.append(food['Price'][i] * 0.1)

    A_ub = []
    for i in row:
        temp = []
        for j in range(food.index.stop):
            temp.append(-food[i][j])
        A_ub.append(temp)
    for i in row:
        temp = []
        for j in range(food.index.stop):
            temp.append(food[i][j])
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
    for i in range(len(b_ub)):
        b_ub[i] = b_ub[i] * inaccuracy[0]

    temp = []
    for i in range(len(bird.loc[num_bird])):
        temp.append(bird.loc[num_bird][i])
    temp = temp[1:-1]
    for i in range(len(temp)):
        b_ub.append(temp[i] * inaccuracy[1])

    for i in range(food.index.stop):
        b_ub.append(0)

    A_eq = [[100 for i in range(food.index.stop)]]
    b_eq = [[1000]]
    #print(A_ub, '\n', b_ub)
    return c, A_ub, b_ub, A_eq, b_eq


def work(c, A_ub, b_ub, A_eq, b_eq):
    start = time.time()
    x = linprog(c, A_ub, b_ub, A_eq, b_eq, options={"presolve": False})
    stop = time.time()
    # print("Время : {}".format(stop - start))
    # print(x)
    return x, x.x


c, A_ub, b_ub, A_eq, b_eq = make_params(num_bird, bird, row, food)
result_all, result_x = work(c, A_ub, b_ub, A_eq, b_eq)
result_x = pd.Series(result_x)
print(result_all)
result_food = []
print(result_x)
for i in row:
    result_food.append((result_x * food[i]).sum())
print(result_food)
result_x.to_excel('result.xlsx', sheet_name='Корм')


#x_food = pd.Series(result_x)
#x_food = x_food[x_food > 0.001]
#print(len(x_food))
#food1 = food.copy()
#food1 = food1.loc[x_food.index]
#food1 = food1.reindex(range(len(food1)), method='bfill')
#food1.to_excel('result.xlsx', sheet_name='123')


#row1 = food.columns.tolist()
#row1 = row1[2:-2]
#c, A_ub, b_ub, A_eq, b_eq = make_params(num_bird, bird, row1, food1)

#result_all, result_x = work(c, A_ub, b_ub, A_eq, b_eq)
#result_x = pd.Series(result_x)
#print(result_all)
