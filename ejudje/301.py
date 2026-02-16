
def isvalid(num):

    check = len(num)
    brum = 0

    for x in range(len(num)):
        if int(num[x]) % 2 == 0:
            brum += 1
        else:
            return False
    if brum == check:
        return True

num = input()
if isvalid(num) == False:
    print("Not valid")
else:
    print("Valid")