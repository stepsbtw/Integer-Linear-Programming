from scipy.optimize import linprog

# Coeficientes da função objetivo (minimizar z)
c = [2, 3, 5, 2, 3]

# Matriz de restrições
A = [
    [-1, -2, -1, 2, -2],
    [-3, -1, -1, -3, -1]
]

# Limites das restrições
b = [-4, -3]

# Limites de não negatividade para x1, x2, x3, x4, x5
x_bounds = [(0, None)] * 5

# Resolvendo o problema
result = linprog(c, A_ub=A, b_ub=b, bounds=x_bounds, method='highs')

# Exibindo os resultados
if result.success:
    print("Solução ótima encontrada:")
    print("Valores das variáveis:", result.x)
    print("Valor mínimo de z:", result.fun)
else:
    print("Não foi possível encontrar uma solução ótima.")
    
# Coeficientes da função objetivo do dual (maximizar w)
c_dual = [-4, -3]

# Matriz de restrições do dual
A_dual = [
    [1, 3],
    [2, 1],
    [1, 1],
    [-2, 3],
    [2, 1]
]

# Limites das restrições do dual
b_dual = [-2, -3, -5, -2, -3]

# Resolvendo o problema dual
result_dual = linprog(c_dual, A_ub=A_dual, b_ub=b_dual, bounds=[(None, 0), (None, 0)], method='highs')

# Exibindo os resultados
if result_dual.success:
    print("Solução ótima do dual encontrada:")
    print("Valores das variáveis dual:", result_dual.x)
    print("Valor máximo de w:", result_dual.fun)
else:
    print("Não foi possível encontrar uma solução ótima para o dual.")