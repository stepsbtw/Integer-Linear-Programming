from scipy.optimize import linprog

A = [[20,15,5,3,7]]
b = [50]
c = [-10,-5,-3,-2,-1]

x_bounds = [(0,None)] * len(c)

# ALWAYS Min Ax <= b

result = linprog(c=c,A_ub=A,b_ub=b,bounds=x_bounds,integrality=0)
print("Optimal value:", -result.fun)
print("Optimal solution:", result.x)
