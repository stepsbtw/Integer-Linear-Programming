import numpy as np

def main():
    # Min Ax <= b, x >= 0
    A = np.array([[2, 3], [-1, 1]])
    b = np.array([6, 1])
    c = np.array([-1, -3])
    solution, objective = simplex_primal(A,b,c)
    print(f"Optimal Solution: {solution}")
    print(f"Optimal Objective Funcion Value: {objective}")
    
def simplex_primal(A,b,c):
    # standard form
    m , n = A.shape
    A = np.hstack([A,np.eye(m)])
    c = np.concat([c,np.zeros(m)])
    B = list(range(n, n + m))
    N = list(range(n)) 
    xB = b[:]
    
    # simplex primal
    while True:
        A_B = A[:,B]
        B_inv = np.linalg.inv(A_B)
        xB = B_inv.dot(b)
        
    # who enters the base
        r = np.zeros(len(N))
        for i, j in enumerate(N):
            a_j = A[:,j]
            r[i] = c[j] - B_inv.dot(a_j).dot(c[B])
        
        # maybe solution is found.
        if np.min(r) >= 0:
            solution = np.zeros(len(c))
            solution[B] = xB
            return solution[:n], c[B].dot(xB)
        
        enter_idx = np.argmin(r)
        enter = N[enter_idx]
            
    # who leaves the base
        d = B_inv.dot(A[:,enter])
        ratios = []
        for i in range(m):
            if d[i] > 0: 
                ratios.append(xB[i] / d[i])
            else: 
                ratios.append(float('inf'))
        leave_idx = np.argmin(ratios)
        leave = B[leave_idx]
        
    # update base
        B[leave_idx] = enter
        N[enter_idx] = leave


if __name__ == "__main__":
    main()
