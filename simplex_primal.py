import numpy as np

A = np.array([[2, 3], [-1, 1]])
b = np.array([6, 1])
c = np.array([-1, -3])

# std form
n_constrictions, n_vars = A.shape
A = np.hstack([A, np.eye(n_constrictions)])
c = np.concatenate([c, np.zeros(n_constrictions)])
B = list(range(n_vars, n_vars + n_constrictions))
N = list(range(n_vars))

def reduced_costs(c,N,B,A): # c_N - c_B * B^-1 * A_N
    B_inv = np.linalg.inv(A[:, B])
    lambda_ = c[B].dot(B_inv)       # dual prices (shadow prices)
    r = c[N] - lambda_.dot(A[:, N]) # non basic reduced costs
    return r

def choose_entering_variable(r): # most negative reduced cost
    return np.argmin(r) if np.min(r) < 0 else -1  # if all >= 0, optimal

def choose_leaving_variable(x_B, d): # minimun ratio test
    ratios = x_B / d
    positive_ratios = np.where(d > 0, ratios, np.inf)
    return np.argmin(positive_ratios)

def simplex(A, b, c, B, N):
    while True:
        B_inv = np.linalg.inv(A[:, B])
        x_B = B_inv.dot(b)   

        r = reduced_costs(c, N, B, A)

        entering_idx = choose_entering_variable(r)
        if entering_idx == -1:
            solution = np.zeros(len(c))
            solution[B] = x_B
            return solution[:n_vars], c[B].dot(x_B)  
        
        entering_var = N[entering_idx]

        d = B_inv.dot(A[:, entering_var])

        
        if np.all(d <= 0):
            raise ValueError("The problem is unbounded.")
        
        leaving_idx = choose_leaving_variable(x_B, d)
        leaving_var = B[leaving_idx]
        
        B[leaving_idx] = entering_var
        N[entering_idx] = leaving_var
        
solution, objective = simplex(A, b, c, B, N)
print(f"Optimal solution: {solution}")
print(f"Optimal value: {objective}")


