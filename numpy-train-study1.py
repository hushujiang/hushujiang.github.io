#numpy库简单应用
import numpy as np
import random
 
#定义矩阵大小
m = 15
 
mBtemp = [] 
for x in range(2*m-1):
    mBtemp.append(random.randint(1, 10))
mB = np.matrix(np.array(mBtemp[0:m]))
for x in range(1, m):
    mB = np.insert(mB, x, values=np.array(mBtemp[-1*x:] + mBtemp[0:m-x]), axis = 0)
    
vb = []
for x in range(m):
    vb.append(random.randint(1, 10))
     
print("B = \n", mB)
print("vb = ", vb)
 
#invB = np.linalg.inv(mB)
 
print("Bx = b, x = ", np.linalg.solve(mB, vb))