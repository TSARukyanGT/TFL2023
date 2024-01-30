
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

for cond in conditions:
    condition_reg.update({cond: ""})

temp_automat = list(automat)
for i in automat:
    if i[0] == i[2]:
        if len(i[1]) == 1:
            if condition_reg[i[0]] == "":
                condition_reg[i[0]] += i[1] + "*"
            elif condition_reg[i[0]][-2:] == ")*":
                condition_reg[i[0]] = condition_reg[i[0]][:-2] + "|" + i[1] + ")*"
            else:
                condition_reg[i[0]] = "(" + condition_reg[i[0]][:-1] + "|" + i[1] + ")*"
        else:
            if condition_reg[i[0]] == "":
                condition_reg[i[0]] += "("+i[1]+")*"
            elif condition_reg[i[0]][-2:] == ")*":
                condition_reg[i[0]] = condition_reg[i[0]][:-2] + "|" + i[1] + ")*"
            else:
                condition_reg[i[0]] = "(" + condition_reg[i[0]][:-1] + "|" + i[1] + ")*"
        temp_automat.remove(i)
automat = list(temp_automat)

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
            
# ordered_conditions.remove(startcond)
# ordered_conditions.append(startcond)
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
            if len(i[1]) == 1:
                if condition_reg[i[0]] == "":
                    condition_reg[i[0]] += i[1] + "*"
                elif condition_reg[i[0]][-2:] == ")*":
                    condition_reg[i[0]] = condition_reg[i[0]][:-2] + "|" + i[1] + ")*"
                else:
                    condition_reg[i[0]] = "(" + condition_reg[i[0]][:-1] + "|" + i[1] + ")*"
            else:
                if condition_reg[i[0]] == "":
                    condition_reg[i[0]] += "(" + i[1] + ")*"
                elif condition_reg[i[0]][-2:] == ")*":
                    condition_reg[i[0]] = condition_reg[i[0]][:-2] + "|" + i[1] + ")*"
                else:
                    condition_reg[i[0]] = "(" + condition_reg[i[0]][:-1] + "|" + i[1] + ")*"
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
                temp_automat.append([automat[i][0], "("+automat[i][1]+"|"+automat[j][1]+")", automat[i][2]])

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
