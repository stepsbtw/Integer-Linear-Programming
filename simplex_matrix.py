import numpy as np

def main():
    # inputs
    # -> Min Ax <= b ou Min Ax = b, x >= 0
    A = np.array([[2, 3], [-1, 1]])
    b = np.array([6, 1])
    c = np.array([-1, -3])
    solucao, objetivo = simplex(A, b, c)
    print(f"Solucao otima: {solucao}")
    print(f"Valor otimo: {objetivo}")

def simplex(A, b, c):
    # forma padrao
    m = len(A)    # numero de restricoes
    n = len(A[0]) # numero de variaveis
    # variaveis de folga com matriz identidade
    A = np.hstack([A,np.eye(m)])
    
    #c += [0] * m  
    c = np.concat([c,np.zeros(m)]) # folga tem custo 0

    # indices basicos e nao basicos
    B = list(range(n, n + m))
    N = list(range(n))

    # solucao inicial basica viavel, (folgas)
    xB = b[:]  # copia de b

    while True:
        # matriz basica
        A_B = [[A[i][B[j]] for j in range(m)] for i in range(m)]
        
        '''
        for i in range(m):
            for j in range(m):
                A_B = A[i][B[j]]
        '''
        
        # inverter a matriz basica
        B_inv = np.linalg.inv(A_B)
        xB = B_inv.dot(b)  # xB = B^-1 * b

        # custos reduzidos p cada nao basica
        r = [0] * len(N)
        for i, j in enumerate(N):
            #a_j = [A[k][j] for k in range(m)]  
            a_j = A[:,j] # coluna especifica da variavel j
            r[i] = c[j] - B_inv.dot(a_j).dot(c[B])

        # ja posso ter a solucao otima
        if min(r) >= 0:
            solucao = [0] * len(c)
            for i in range(m):
                solucao[B[i]] = xB[i]
            return solucao[:n], c[B].dot(xB)  # SOLUCAO OTIMA e OBJETIVO

        # quem entra
        entra_idx = r.index(min(r)) # o indice da variavel que ao entrar minimiza r.
        entra = N[entra_idx]

        # calcular direcao (quanto as variaveis basicas reagem a ela.)
        # teste da razao
        #d = B_inv.dot(A[k][entra] for k in range(m))
        d = B_inv.dot(A[:,entra]) # dot com a coluna da que entra
        razoes = []
        for i in range(m):
            if d[i] > 0: 
                razoes.append(xB[i] / d[i])
            else: 
                float('inf') # por infinito nas negativas.
                
        # quem sai
        sai_idx = razoes.index(min(razoes)) # indice da variavel que tem a razao minima POSITIVA.
        sai = B[sai_idx]

        # atualizar os indices basicos e nao basicos
        B[sai_idx] = entra
        N[entra_idx] = sai

if __name__ == "__main__":
    main()
