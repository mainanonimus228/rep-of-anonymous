def CircleArea(num):
    Area = 3.14159 * num * num
    return Area

num = int(input())

print(f"{CircleArea(num):.2f}")