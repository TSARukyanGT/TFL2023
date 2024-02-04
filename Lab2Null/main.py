
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

original_automat = []
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
    original_automat.append([first, path, second])
    if not second in conditions:
        conditions.append(second)
conditions.extend(['S', 'F'])
original_automat.append(['S', '', startcond])
for cond in finishcond:
    original_automat.append([cond, '', 'F'])

original_cond_reg = {}
condition_path_num = {}

for cond in conditions:
    original_cond_reg.update({cond: ""})

temp_automat = list(original_automat)
for i in original_automat:
    if i[0] == i[2]:
        if len(i[1]) == 1:
            if original_cond_reg[i[0]] == "":
                original_cond_reg[i[0]] += i[1] + "*"
            elif original_cond_reg[i[0]][-2:] == ")*":
                original_cond_reg[i[0]] = original_cond_reg[i[0]][:-2] + "|" + i[1] + ")*"
            else:
                original_cond_reg[i[0]] = "(" + original_cond_reg[i[0]][:-1] + "|" + i[1] + ")*"
        else:
            if original_cond_reg[i[0]] == "":
                original_cond_reg[i[0]] += "("+i[1]+")*"
            elif original_cond_reg[i[0]][-2:] == ")*":
                original_cond_reg[i[0]] = original_cond_reg[i[0]][:-2] + "|" + i[1] + ")*"
            else:
                original_cond_reg[i[0]] = "(" + original_cond_reg[i[0]][:-1] + "|" + i[1] + ")*"
        temp_automat.remove(i)
original_automat = list(temp_automat)

maxpath = 0
for cond in conditions:
    pathnum = 0
    for line in original_automat:
        if line[0] == cond or line[2] == cond:
            pathnum += 1
    condition_path_num.update({cond: pathnum})
    if pathnum > maxpath:
        maxpath = pathnum

orders = []
ordered_conditions = []
for i in range(0, maxpath+1):
    for cond in condition_path_num:
        if i == condition_path_num[cond] and cond != 'S' and cond != 'F':
            ordered_conditions.append(cond)
orders.append(ordered_conditions)
ord = list(ordered_conditions)
ord.remove(startcond)
ord.append(startcond)
orders.append(ord)
ord2 = list(ord)
for f in finishcond:
    ord2.remove(f)
    ord2.append(f)
orders.append(ord2)
ord3 = list(ordered_conditions)
for f in finishcond:
    ord3.remove(f)
    ord3.append(f)
orders.append(ord3)

def accumulation(aut):
    res_reg = ""
    for rule in aut:
        if res_reg != "":
            res_reg += "|"
        res_reg += rule[1]
    return res_reg

result_regex = ""
for ord_cons in orders:
    condition_reg = dict(original_cond_reg)
    automat = list(original_automat)
    for deleting_cond in ord_cons:
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

        automat = list(temp_automat)
        temp_automat = list(automat)
        for i in range(0 , len(automat)-1):
            for j in range(i+1, len(automat)):
                if (automat[i][0] == automat[j][0]) and (automat[i][2] == automat[j][2]) and (automat[i][1] != automat[j][1]):
                    temp_automat.remove(automat[i])
                    temp_automat.remove(automat[j])
                    word = ""
                    if automat[i][1] == "":
                        word = automat[j][1]
                    elif automat[j][1] == "":
                        word = automat[i][1]
                    else:
                        word = "("+automat[i][1]+"|"+automat[j][1]+")"
                    temp_automat.append([automat[i][0], word, automat[i][2]])

        automat = list(temp_automat)
    reg = accumulation(automat)
    if result_regex == "":
        temp_reg = "Empty"
    else:
        temp_reg = result_regex
    print("Сравнение {0} и {1}: Длина {2} против {3}".format(temp_reg, reg, len(result_regex), len(reg)))
    if result_regex == "" or len(reg) < len(result_regex):
        print("Замена {0} на {1}".format(temp_reg, reg))
        result_regex = reg

print("Result REGEX:")
print(result_regex)