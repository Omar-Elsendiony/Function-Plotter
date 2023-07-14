import utility
import numpy as np



x = np.linspace(0,10,50)
equation = "6*x/3"
equation = "5*x^3+2*x"
equation = "5*x3*x"
i , a , t = utility.computeY(equation,x)

print(i,a)

