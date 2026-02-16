#1
class MyClass:  #create class
  x = 5

#1

p1 = MyClass() #create object
print(p1.x)

#3

del p1  # delete the object

#4

p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)

#5

class Person: 
  pass #to avoid getting error