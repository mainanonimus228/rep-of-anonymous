n =int(input())
count = 0

nums = list(map(int , input().split()))

for x in nums:
    if x > 0:
        count += 1

print(count)


