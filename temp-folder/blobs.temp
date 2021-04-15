alist = [[0, 1788], [1, 1966], [2, 1744]]
# blist = [[1, 0], [3, 3]]
blist = []

FRAME = 5

for x in range(FRAME):
    for aitem in alist:
        found = False
        for bitem in blist:
            if aitem[0] == bitem[0]:
                found = True
                if bitem[1] < 3:
                    bitem[1] += 1
        if not found:
            blist.append([aitem[0], 0])
    temp_blist = []
    for bitem in blist:
        found = False
        to_be_copied = True
        for aitem in alist:
            if aitem[0] == bitem[0]:
                found = True
        if not found:
            bitem[1] -= 1
            if bitem[1] == -1:
                to_be_copied = False
        if to_be_copied:
            temp_blist.append(bitem)
    blist.clear()
    blist = temp_blist.copy()
    temp_blist.clear()


print(blist)

