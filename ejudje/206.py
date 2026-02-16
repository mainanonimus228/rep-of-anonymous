n = int(input())

nums = list(map(int , input().split()))

max =nums[0]

for i in nums:
    if i > max:
        max = i
print(max)