import numpy as np
from scipy.optimize import linprog
# ALWAYS Min Ax <= b

def main():
  A = np.array([[20,15,5,3,7]])
  b = np.array([50])
  c = np.array([-10,-5,-3,-2,-1])
  x_bounds = [(0,None)] * len(c)
  #x_bounds = [(0,1)] * len(c) # for binary problems.

  objective, solution = branch_and_bound(A,b,c,x_bounds)
  print("Optimal LINEAR value:", objective)
  print("Optimal LINEAR solution:", solution)

def branch_and_bound(A,b,c,bounds):
  # Dual Simplex to solve the relaxed linear problem
  dual_simplex = linprog(c=c,A_ub=A,b_ub=b,bounds=bounds,integrality=0,method="highs-ds")
  
  if not dual_simplex.success: # if not feasible
    return float('inf'), None
    
  relax_objective, relax_x = dual_simplex.fun, dual_simplex.x
  if np.all(relax_x == np.floor(relax_x)): # if are already integers 
    return relax_objective, relax_x # OK! No branch needed
    
  for i, x in enumerate(relax_x):
    if int(x) != x:
      # CREATE 2 NEW AUXILIARY PROBLEMS.
      upper_bound = bounds.copy()
      lower_bound = bounds.copy()
      
      upper_bound[i] = (bounds[i][0], floor(x))
      lower_bound[i] = (ceil(x), bounds[i][1])
      
      lb_obj, lb_x = branch_and_bound(A, b, c, lower_bound)
      ub_obj, ub_x = branch_and_bound(A, b, c, upper_bound)

      if ub_obj >= lb_obj: # return which bounded solution is better
          return ub_obj, ub_x
      else:
          return lb_obj, lb_x
  
if __name__ == "__main__":
  main()

'''
# other way to create the bounds
ub = np.zeros(len(A)) # new restriction
ub[i] = 1
A_ub = np.append(A, ub) 
b_ub = floor(x) # <= floor(x)
branch_and_bound(A_ub,b_ub,c,bounds)
lb = np.zeros(len(A)) # new restriction
lb[i] = 1
A_lb = np.append(A, lb) # x
b_lb = -ceil(relax_x[i]) # >= ceil(x)
branch_and_bound(A_lb,b_lb,c,bounds)
'''
