import numpy as np
from scipy.optimize import linprog
# ALWAYS Min Ax <= b

def main():
  A = np.array([[20,15,5,3,7]])
  b = np.array([50])
  c = np.array([-10,-5,-3,-2,-1])
  x_bounds = [(0,None)] * len(c)
  #x_bounds = [(0,1)] * len(c) # for binary problems.
  result = linprog(c=c,A_ub=A,b_ub=b,bounds=x_bounds,method="highs")
  objective, solution = result.fun, result.x
  print(result.success)
  objective_int, solution_int = branch_and_bound(A,b,c,x_bounds)
  print("Optimal LINEAR value:", objective)
  print("Optimal LINEAR solution:", solution)
  print("Optimal INTEGER value:", objective_int)
  print("Optimal INTEGER solution:", solution_int)
  result = linprog(c=c,A_ub=A,b_ub=b,bounds=x_bounds,integrality=1,method="highs")
  objective_int_native, solution_int_native = result.fun, result.x
  print("Optimal INTEGER LINPROG value:", objective_int_native)
  print("Optimal INTEGER LINPROG solution:", solution_int_native)

def branch_and_bound(A,b,c,bounds):
  # Dual Simplex to solve the relaxed linear problem
  dual_simplex = linprog(c=c,A_ub=A,b_ub=b,bounds=bounds,method="highs")

  if not dual_simplex.success: # if not feasible
    return float('inf'), None

  relax_objective, relax_x = dual_simplex.fun, dual_simplex.x
  if np.all(relax_x == np.floor(relax_x)): # if are already integers
    return relax_objective, relax_x # OK! No branch needed

  best_obj = float('inf')
  best_x = None

  for i, x in enumerate(relax_x):
    if int(x) != x:
      # CREATE 2 NEW AUXILIARY PROBLEMS.
      upper_bound = bounds.copy()
      lower_bound = bounds.copy()

      upper_bound[i] = (bounds[i][0], np.floor(x))
      lower_bound[i] = (np.ceil(x), bounds[i][1])

      lb_obj, lb_x = branch_and_bound(A, b, c, lower_bound)
      ub_obj, ub_x = branch_and_bound(A, b, c, upper_bound)

      if lb_obj < best_obj:
        best_obj = lb_obj
        best_x = lb_x

      if ub_obj < best_obj:
        best_obj = ub_obj
        best_x = ub_x

  return best_obj, best_x

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
