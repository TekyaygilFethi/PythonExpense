def vkn_verification(t):
    if len(t) != 10:
        return False

    total = 0
    for x in range(0, 9):
        tmp1 = (int(t[x]) + (9 - x)) % 10
        tmp2 = (tmp1 * (2 ** (9 - x))) % 9
        if tmp1 != 0 and tmp2 == 0:
            tmp2 = 9

        total += tmp2

    if total % 10 == 0:
        check_num = 0
    else:
        check_num = 10 - (total % 10)

    return int(t[9]) == check_num