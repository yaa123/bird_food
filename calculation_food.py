from scipy.optimize import linprog
import pandas as pd


inaccuracy = (0.95, 1.1)

print('Введите количество корма в килограммах')
count_food = int(input())

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
print('Содержание необходимых веществ в корме, не менее {} % и не более {:.0f} %'.format(inaccuracy[0] * 100, inaccuracy[1] * 100))


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

    A_eq = [[1 for i in range(food.index.stop)]]
    b_eq = [[10]]
    #print(A_ub, '\n', b_ub)
    return c, A_ub, b_ub, A_eq, b_eq


def work(c, A_ub, b_ub, A_eq, b_eq):
    x = linprog(c, A_ub, b_ub, A_eq, b_eq, options={"presolve": False}, method='revised simplex')
    return x, x.x


c, A_ub, b_ub, A_eq, b_eq = make_params(num_bird, bird, row, food)
result_all, result_x = work(c, A_ub, b_ub, A_eq, b_eq)
result_x = pd.Series(result_x)
#print(result_all)
result_food = []
for i in row:
    result_food.append((result_x * food[i]).sum())
print('Стоимость {} кг. корма - {}'.format(count_food, result_all.fun))
result_to_exel = food.copy()
result_to_exel['Count GR in KG'] = [i * count_food * 100 for i in result_x.tolist()]
result_to_exel['Price for count'] = result_to_exel['Price'] * result_to_exel['Count GR in KG']
result_to_exel['Price Food'] = result_all.fun * 100 * count_food
result_to_exel = result_to_exel.drop(result_to_exel[result_to_exel['Count GR in KG'] == 0].index)
result_to_exel = result_to_exel.reset_index(drop=True)
result_to_exel.to_excel('Корм {}.xlsx'.format(name_bird), sheet_name='Корм')





