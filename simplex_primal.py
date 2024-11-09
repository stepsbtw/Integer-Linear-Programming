import numpy as np

def main(): 
    A = np.array([[-1, -2], [-1, 2], [-2,-3], [-1,-1], [-3,-1]]).T
    c = np.array([2, 3, 5, 2, 3])
    b = np.array([-4, -3])
    inequalities = [-1,-1]  # 1 = '≥' , -1 = '≤'
    objective_type = "min"
    
    m, n = A.shape
    B = list(range(n, n + m))
    N = list(range(n+ m))
    
    A, c = to_standard_form(A, c, m, objective_type, inequalities)  # get rid of inequalities

    # solution, objective = simplex(A, b, c, B, N)
    solution, objective = two_phase(A,b,c,B,N)
    print(f"Optimal solution: {solution}")
    print(f"Optimal value: {objective}")

def two_phase(A,b,c,B,N): # determine initial viable solution
    m, n = A.shape
    
    # PHASE 1 - add artificial vars and solve aux
    A_aux = np.hstack([A, np.eye(m)])
    c_aux = np.hstack([np.zeros(n), np.ones(m)])  # second objective -> minimize sum of artificials vars
    B_aux = list(range(n, n + m))
    N_aux = list(range(n))
    
    solution_aux, objective_aux = simplex(A_aux, b, c_aux, B_aux, N_aux)
    
    # feasibility: sum of artificials = 0
    if objective_aux > 0:
        raise ValueError("The problem is unbounded.")
    
    # PHASE 2 - remove artificial vars and solve original
    A_orig = A_aux[:,:n]
    return simplex(A_orig, b, c, B, N)

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
