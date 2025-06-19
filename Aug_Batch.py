class A():
    def __init__(self,a,b,c):
        self.a=a
        self.b=b
        self.c=c
    def display(self):
        print("value of a ",self.a)
        print("value of b ",self.b)
        print("value of c ",self.c)
obj1=A(10,20,30)
print(obj1.a)
print(obj1.b)
