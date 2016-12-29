import numpy as np

a= np.array([[1,3,4],[2,7,6]])
b= np.array([[5,2,9],[3,6,4]])

print a
print b
print a+b
print a>b
print np.where(a>b,10,5)

c = np.random.randint(0,20,12)
#Estraggo nono,primo e quarto valore
print c
print c[[8,0,3]]

d = np.reshape(c,(3,4))
print d
print d[[2, 0, 0], [0, 0, 3]]

bool_matx = a > b
print bool_matx

e=a[bool_matx]
print e