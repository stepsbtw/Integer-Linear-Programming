import numpy as np

# Define the LP
A = np.array([[1, 2], [1, -2], [2, 3], [1, 1], [3, 1]]).T
c = np.array([2, 3, 5, 2, 3])
b = np.array([4, 3])
inequalities = [1, 1]  # 1 = '≥' , -1 = '≤'
objective_type = "min"

A = np.array([[-1, -2], [-1, 2], [-2, -3], [-1, -1], [-3, -1]]).T
c = np.array([2, 3, 5, 2, 3])
b = np.array([-4, -3])
inequalities = [-1, -1]  # 1 = '≥' , -1 = '≤'
objective_type = "min"
    
if objective_type == "max":
    c = -c # convert to min

# 1 = '≥' , -1 = '≤'
inequalities = [-1,-1]
m, n = A.shape

# adding slack/surplus vars
for i in range(m):
    if inequalities[i] == -1:  # '≤'
        slack_column = np.zeros(m)
        slack_column[i] = 1
        A = np.hstack([A, slack_column.reshape(-1, 1)])
    elif inequalities[i] == 1:  # '≥'
        surplus_column = np.zeros(m)
        surplus_column[i] = -1
        A = np.hstack([A, surplus_column.reshape(-1, 1)])

# 0 cost to slack
c = np.hstack([c, np.zeros(m)])

def dual_simplex(A, b, c):
    B = list(range(n - m, n))
    N = list(range(n - m))
    # dual simplex
    B_inv = np.linalg.inv(A[:, B]) # inverse of the basis
    while True:
        # dual variables (shadow prices)
        lambda_ = c[B].dot(B_inv)

        # reduced costs for non-basic variables
        reduced_costs = c[N] - lambda_.dot(A[:, N])

        # dual feasibility, optimal solution
        if np.all(reduced_costs >= 0):
            x = np.zeros(len(c))
            x[B] = B_inv.dot(b)
            optimal_value = c.dot(x)
            return x, -optimal_value if objective_type == "max" else optimal_value

        # who leaves : most negative basic var
        xB = B_inv.dot(b)
        leaving_idx = np.argmin(xB)
        if xB[leaving_idx] >= 0:
            raise ValueError("The problem is unbounded.")

        direction = B_inv.dot(A[:, N])
        # handle division by 0
        valid_directions = direction[:, leaving_idx] > 0
        if not np.any(valid_directions):
            raise ValueError("The problem is unbounded.")
        
        # who enters : minimum ratio
        ratios = np.full(len(N), np.inf)
        ratios[valid_directions] = reduced_costs[valid_directions] / direction[valid_directions, leaving_idx]
        entering_idx = np.argmin(ratios)
        
        # pivot
        B[leaving_idx], N[entering_idx] = N[entering_idx], B[leaving_idx]
        
        # update inverse
        B_inv = np.linalg.inv(A[:, B])

solution, objective = dual_simplex(A, b, c)
print("Optimal solution:", solution)
print("Optimal value:", objective)
