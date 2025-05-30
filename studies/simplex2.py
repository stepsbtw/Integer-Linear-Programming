import numpy as np

def main(): 
    A = np.array([[1, 2], [1, -2], [2, 3], [1, 1], [3, 1]]).T
    c = np.array([2, 3, 5, 2, 3])
    b = np.array([4, 3])
    inequalities = [1, 1]  # 1 = '≥' , -1 = '≤'
    objective_type = "min"
    
    solution, objective = simplex_method(A, b, c)
    print(f"Optimal solution: {solution}")
    print(f"Optimal value: {objective}")

def simplex_method(A, b, c):
    # Inicialização das variáveis
    num_vars = len(c)
    num_constraints = len(b)
    
    # Construindo a tabela inicial
    tableau = np.zeros((num_constraints + 1, num_vars + num_constraints + 1))
    tableau[:num_constraints, :num_vars] = A
    tableau[:num_constraints, num_vars:num_vars + num_constraints] = np.eye(num_constraints)
    tableau[:num_constraints, -1] = b
    tableau[-1, :num_vars] = -c

    while True:
        # Escolha da variável de entrada (menor valor na linha da função objetivo)
        if np.all(tableau[-1, :-1] >= 0):
            # Todas as entradas são >= 0, logo, encontramos uma solução ótima
            break

        entering_var = np.argmin(tableau[-1, :-1])
        
        # Teste para escolher a variável de saída (menor razão positiva)
        ratios = tableau[:-1, -1] / tableau[:-1, entering_var]
        ratios[ratios <= 0] = np.inf  # Evita divisões por zero e razões não positivas
        
        leaving_var = np.argmin(ratios)
        if ratios[leaving_var] == np.inf:
            raise ValueError("Problema ilimitado")

        # Operações de pivotamento
        pivot = tableau[leaving_var, entering_var]
        tableau[leaving_var, :] /= pivot
        for i in range(num_constraints + 1):
            if i != leaving_var:
                tableau[i, :] -= tableau[i, entering_var] * tableau[leaving_var, :]

    # Extrair solução
    solution = np.zeros(num_vars)
    for i in range(num_constraints):
        col = tableau[:, i]
        if np.count_nonzero(col[:-1]) == 1 and col[-1] == 0:
            row = np.where(col[:-1] == 1)[0][0]
            solution[i] = tableau[row, -1]

    return solution, tableau[-1, -1]

if __name__ == "__main__":
    main()