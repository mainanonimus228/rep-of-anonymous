n = int(input())

nums = list(map(int , input().split()))

max = nums[0]
max_index = 0

for i in range (1, n):
    if nums[i] > max:
        max = nums[i]
        max_index = i
print(max_index + 1)