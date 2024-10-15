import numpy as np

def main():
    # inputs
    # -> Min Ax <= b ou Min Ax = b, x >= 0
    A = np.array([[2,3],[-1,1]])
    b = np.array([6,1])
    c = np.array([-1,-3])
    solucao, objetivo = simplex(A,b,c)
    print(f"Solucao otima {solucao}")
    print(f"Valor maximo: {objetivo}")

def simplex(A,b,c):
    # forma padrao
    # A(mxn) m -> n restricoes, n -> n variaveis
    '''
    m = len(A)
    n = len(A[0])
    '''
    m,n = A.shape
    A = np.hstack([A,np.eye(m)])
    #c = np.concat([c,np.zeros(m)])
    c += [0] * m

    # indices basicos e nao basicos
    # variaveis de folga sao inicialmente basicas
    B = list(range(n,n+m))
    N = list(range(n))

    # SOLUCAO BASICA INICIAL:
    xB = b[:] # ORIGEM CONSIDERADA VIÁVEL.
    # (copia)
    
    while True:
        # INVERTER MATRIZ BASICA AB^-1
        B_inv = np.linalg.inv(A[:,B]) # colunas das variaveis de folga
        xB = B_inv.dot(b) # B^-1b

        # quem entra : custos reduzidos
        
        # calcular os custos reduzidos das nao basicas xj
        #r = np.zeros(len(N))
        r = [0] * len(N)
        for i, j in enumerate(N):
            a_j = A[:,j] # coluna coef. da variavel j
            r[i] = c[j] - B_inv.dot(a_j).dot(c[B])
            
        # se forem positivos, ACABOU!
        if np.min(r) < 0:
            entra_idx = np.argmin(r)
        else:
            solucao = np.zeros(len(c))
            solucao[B] = xB
            return solucao[:n], c[B].dot(xB)
            # solucao otima e valor objetivo
        
        entra = N[entra_idx]
        
        # quem sai : TESTE DA RAZAO MINIMA
        # matriz distancia
        # mostra o quanto cada variavel basica reage a variavel que entra
        d = B_inv.dot(A[:,entra])
        razoes = xB/d
        # sai o que tiver razao positiva menos impactante
        razoes_positivas = np.where(d>0,razoes,np.inf)
        # todos valores positivos recebe o valor da razao
        # todos os valores negativos ou 0 recebem infinito
        sai_idx = np.argmin(razoes_positivas)
        
        sai = B[sai_idx]
        
        # ATUALIZAR TUDO!
        B[sai_idx] = entra
        N[entra_idx] = sai

if __name__ == "__main__":
    main()

    
    



