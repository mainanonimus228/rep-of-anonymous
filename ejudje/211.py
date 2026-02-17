numbers = list(map(int, input().split()))

n = numbers[0]
fiind = numbers[1]
seind = numbers[2]

nums = list(map(int, input().split()))

nums[fiind-1:seind] = reversed(nums[fiind-1:seind])

for i in range(n):
    print(nums[i], end =" ")
