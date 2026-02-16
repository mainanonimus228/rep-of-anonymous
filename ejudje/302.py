def isusual(num):
    while num % 5 == 0:
        num = num / 5
    while num % 3 == 0:
        num = num / 3
    while num % 2 == 0:
        num = num / 2

    return num == 1


num = int(input())
var = isusual(num)

if var:
    print("Yes")
else:
    print("No")