import numpy as np
from scipy import linalg
import sympy as sp

# invert base_coeficients matrix
# calculate xB , xR and z
# who enters in the base? max(reduced cost)
# who leave from base? min(ratio_test)
# new base! calculate obj function start again.


def main():
    n_restrictions = int(input("How many restrictions in the LP? "))
    
    cost_vector = input("Enter the costs (objective function), separating by spaces: ").split()
    cost_vector = np.array([float(x) for x in cost_vector])
    
    coeficients_matrix, bias_vector = input_restrictions(n_restrictions)
    
    initial_base = input("Enter a starting viable base (only indexes), separating by spaces: ").split()
    initial_base = np.array([float(x) for x in initial_base])
    
    # A*x = b
    # A = [a1:an]
    x_values = np.array(0*cost_vector.size)
    
    #z = c*x
    z_value = cost_vector.dot(x_values)
    
    # c = cB + cN
    # x = xB + xN
    base_idx = []
    non_base_idx = []
    
    # xB = (B^-1)*b
    # z[j] - c[j] = cB*(B^-1)*a1 - c1
    # z = cB*xB + cN*xN
    basic_solution = []
    reduced_costs = []
    
    # who_enter = max(reduced_costs)
    # ratio_test = xB / B^-1*a[who_enter]
    # who_leaves = min(ratio_test)
    who_enter = []
    ratio_test = []
    who_leave = []
    
def input_restrictions(m):
    coef = []
    biases = []
    for i in range(m):
        restriction = input("Insert the coeficients from restriction "+(i+1)+", separating it by spaces: \n").split()
        restriction = [float(x) for x in restriction]
        coef.append(restriction)
        bias = float(input("Insert bias from restriction "+(i+1)+": "))
        biases.append(bias)
    return np.array(coef), np.array(biases)
    
if __name__ == "__main__":
    main()