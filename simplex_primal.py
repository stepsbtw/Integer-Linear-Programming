import numpy as np

def main(): 
    A = np.array([[2, 3], [-1, 1]])
    b = np.array([6, 1])
    c = np.array([1, 3])
    inequalities = [-1,-1]  # 1 = '≥' , -1 = '≤'
    objective_type = "max"
    
    n_constrictions, n_vars = A.shape
    B = list(range(n_vars, n_vars + n_constrictions))
    N = list(range(n_vars + n_constrictions))
    
    A, c = to_standard_form(A,c,n_constrictions,objective_type,inequalities)  # get rid of inequalities

    # solution, objective = simplex(A, b, c, B, N)
    solution, obhective = two_phase(A,b,c,B,N)
    print(f"Optimal solution: {solution}")
    print(f"Optimal value: {objective}")

def two_phase(A,b,c,B,N): # determine initial viable 
    m, n = A.shape
    A_aux = np.hstack([A, np.eye(m)])  # add artificial vars
    c_aux = np.hstack([np.zeros(n), np.ones(m)])  # minimize sum of artificials vars
    B_aux = list(range(n, n + m))
    N_aux = list(range(n))
    return simplex(A, b, c, B, N)

def to_standard_form(A,c,n_constrictions,objective_type="max",inequalities=[-1,-1]):
    if objective_type == "max":
        c = -c  # convert to min
        
    # adding slack/surplus vars
    slack_surplus_vars = []
    for i in range(n_constrictions):
        slack = np.zeros(n_constrictions)
        if inequalities[i] == -1:  # '≤' -> adicionar variável de folga
            slack[i] = 1
        elif inequalities[i] == 1:  # '≥' -> adicionar variável de excesso
            slack[i] = -1
        slack_surplus_vars.append(slack)
        
    slack_surplus_matrix = np.column_stack(slack_surplus_vars)
    A_std = np.hstack([A, slack_surplus_matrix])
    
    c_std = np.hstack([c, np.zeros(len(slack_surplus_vars))])
    return A_std, c_std
    
def reduced_costs(c,B,N,A):         # c_N - c_B * B^-1 * A_N
    B_inv = np.linalg.inv(A[:, B])  # this selects all basic columns
    lambda_ = c[B].dot(B_inv)       # dual prices (shadow prices)
    r = c[N] - lambda_.dot(A[:, N]) # non basic reduced costs
    return r

def choose_entering_variable(r):                  # most negative reduced cost
    return np.argmin(r) if np.min(r) < 0 else -1  # if all >= 0, optimal

def choose_leaving_variable(x_B, d): # minimun ratio test
    ratios = x_B / d
    positive_ratios = np.where(d > 0, ratios, np.inf)
    return np.argmin(positive_ratios)

def simplex(A, b, c, B, N):
    
    while True:
        B_inv = np.linalg.inv(A[:, B])
        x_B = B_inv.dot(b)   

        r = reduced_costs(c, B, N, A)

        entering_idx = choose_entering_variable(r)
        if entering_idx == -1:
            solution = np.zeros(len(c))
            solution[B] = x_B
            return solution[:len(N)], c[B].dot(x_B)
        
        entering_var = N[entering_idx]

        d = B_inv.dot(A[:, entering_var])

        
        if np.all(d <= 0):
            raise ValueError("The problem is unbounded.")
        
        leaving_idx = choose_leaving_variable(x_B, d)
        leaving_var = B[leaving_idx]
        
        B[leaving_idx] = entering_var
        N[entering_idx] = leaving_var

if __name__ == '__main__':
    main()
