n = int(input())

if n == 0:
    print()
else:
    a, b = 0, 1
    
    for i in range(n):
        if i == n - 1:
            print(a)
        else:
            print(a, end=",")
        a, b = b, a + b