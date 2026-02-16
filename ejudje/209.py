n = int(input())

nums = list(map(int, input().split()))

biggest = nums[0]
smallest = nums[0]

for i in range (n):
    if nums[i] > biggest:
        biggest = nums[i]
    if nums[i] < smallest:
        smallest = nums[i]

for i in range (n):
    if nums[i] == biggest:
        nums[i] = smallest

for x in nums:
    print(x , end=" ")
print(" ")