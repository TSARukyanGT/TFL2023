# Примеры ввода
# Q
# Q1, Q3
# (Q, a) -> Q1
# (Q1, a) -> QQ
# (Q1, c) -> Q3
# (Q3, b) -> Q
# (QQ, b) -> Q1

# Q0
# Q3
# (Q0, a) -> Q1
# (Q0, b) -> Q2
# (Q1, a) -> Q1
# (Q1, a) -> Q3
# (Q1, b) -> Q3
# (Q1, a) -> Q2
# (Q2, b) -> Q1


# README
# Предполагается, что в файле на вход нет состояний с именами S, F
#                                         а также переходов $
# также предполагается что в каждой строке только 3 имени, не содержащих символы [',', ' ', '\n', '\t', '(', ')', '-', '>']
# расположенных в порядке: Исходное состояние, Переход, Состояние по переходу

def getname(s):
    res = ""
    for i in range(0, len(s)):
        if s[i] in [',', ' ', '\n', '\t', '(', ')', '-', '>']:
            if res != "":
                return res, s[i:]
        else:
            res += s[i]
    return res, ""
text = open("input.txt", 'r')

automat = []
startcond, _ = getname(text.readline())
finishcond = []
secondline = text.readline()

while secondline != "":
    cond, secondline = getname(secondline)
    if cond != "":
        finishcond.append(cond)
conditions = []
conditions.append(startcond)
conditions.extend(finishcond)
for line in text:
    expr = line + " "
    first, expr = getname(expr)
    path, expr = getname(expr)
    second, expr = getname(expr)
    automat.append([first, path, second])
    if not second in conditions:
        conditions.append(second)
conditions.extend(['S', 'F'])
automat.append(['S', '$', startcond])
for cond in finishcond:
    automat.append([cond, '$', 'F'])

condition_reg = {}
condition_path_num = {}
maxpath = 0
for cond in conditions:
    condition_reg.update({cond: ""})
    pathnum = 0
    for line in automat:
        if line[0] == cond or line[2] == cond:
            pathnum += 1
    condition_path_num.update({cond: pathnum})
    if pathnum > maxpath:
        maxpath = pathnum

ordered_conditions = []
for i in range(0, maxpath+1):
    for cond in condition_path_num:
        if i == condition_path_num[cond] and cond != 'S' and cond != 'F':
            ordered_conditions.append(cond)

# print(ordered_conditions)         #Состояния для исключения (в нужном порядке)

# print(automat)                    #Автомат до изменения

for deleting_cond in ordered_conditions:
    additional_rules = []
    for i in automat:
        for o in automat:
            if i[2] == deleting_cond and o[0] == deleting_cond:
                additional_rules.append([i[0], i[1]+condition_reg[deleting_cond]+o[1], o[2]])
    automat.extend(additional_rules)
    temp_automat = list(automat)
    for i in automat:
        if (i[0] == deleting_cond) or (i[2] == deleting_cond):
            temp_automat.remove(i)
        elif i[0] == i[2]:
            condition_reg[i[0]] += "("+i[1]+")*"
            temp_automat.remove(i)


##### Начало "схлопывания" правил вида (1, a) -> 2
####                                   (1, b) -> 2
#                                       В (1, (a | b)) -> 2
    automat = list(temp_automat)
    temp_automat = list(automat)
    for i in range(0 , len(automat)-1):
        for j in range(i+1, len(automat)):
            if (automat[i][0] == automat[j][0]) and (automat[i][2] == automat[j][2]) and (automat[i][1] != automat[j][1]):
                temp_automat.remove(automat[i])
                temp_automat.remove(automat[j])
                temp_automat.append([automat[i][0], "("+automat[i][1]+" | "+automat[j][1]+")", automat[i][2]])

##### Конец "схлопывания". Если закомментировать код посередине - будет правильный набор, но эти правила разделит на 2 части
    automat = list(temp_automat)

# print(automat)            # Итоговый автомат, где из состояний остались только S и F
result_regex = ""
for rule in automat:
    if result_regex != "":
        result_regex += " | "
    result_regex += rule[1]
result_regex = result_regex.replace('$', "")
print("Result REGEX:")
print(result_regex)
