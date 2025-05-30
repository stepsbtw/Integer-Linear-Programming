function [f, intcon, Aineq, bineq, Aeq, beq, lb, ub] = tsp_MTZ_new(distMatrix)
    n = size(distMatrix, 1);
    nX = n * n;           % x(i,j)
    nU = n - 1;           % u(2) até u(n)
    totalVars = nX + nU;

    edgeIdx = @(i,j) (i-1)*n + j;        % indexador para x(i,j)
    uIdx = @(i) nX + i - 1;              % indexador para u(i), i = 2..n

    %% Objetivo
    f = zeros(totalVars, 1);
    f(1:nX) = distMatrix(:);  % custos nas arestas

    %% Variáveis inteiras
    intcon = 1:totalVars;

    %% Bounds
    lb = zeros(totalVars, 1);
    ub = ones(totalVars, 1);

    for i = 2:n
        lb(uIdx(i)) = 1;
        ub(uIdx(i)) = n - 1;
    end

    for i = 1:n
        idx = edgeIdx(i,i);
        lb(idx) = 0;
        ub(idx) = 0;
    end

    %% Aeq – restrições de grau (2n)
    nnzAeq = 2 * n * (n - 1);
    rowsAeq = zeros(nnzAeq, 1);
    colsAeq = zeros(nnzAeq, 1);
    valsAeq = ones(nnzAeq, 1);
    beq = ones(2*n, 1);

    idx = 1;
    for i = 1:n
        for j = 1:n
            if i ~= j
                rowsAeq(idx) = i;
                colsAeq(idx) = edgeIdx(i,j);
                idx = idx + 1;
            end
        end
    end

    for j = 1:n
        for i = 1:n
            if i ~= j
                rowsAeq(idx) = n + j;
                colsAeq(idx) = edgeIdx(i,j);
                idx = idx + 1;
            end
        end
    end

    Aeq = sparse(rowsAeq, colsAeq, valsAeq, 2*n, totalVars);

    %% Aineq – restrições MTZ
    nMTZ = (n - 1) * (n - 2);
    rowsIneq = zeros(3 * nMTZ, 1);
    colsIneq = zeros(3 * nMTZ, 1);
    valsIneq = zeros(3 * nMTZ, 1);
    bineq = (n - 1) * ones(nMTZ, 1);

    row = 1;
    idx = 1;
    for i = 2:n
        for j = 2:n
            if i ~= j
                % u(i)
                rowsIneq(idx) = row;
                colsIneq(idx) = uIdx(i);
                valsIneq(idx) = 1;
                idx = idx + 1;

                % -u(j)
                rowsIneq(idx) = row;
                colsIneq(idx) = uIdx(j);
                valsIneq(idx) = -1;
                idx = idx + 1;

                % +n * x(i,j)
                rowsIneq(idx) = row;
                colsIneq(idx) = edgeIdx(i,j);
                valsIneq(idx) = n;
                idx = idx + 1;

                row = row + 1;
            end
        end
    end

    Aineq = sparse(rowsIneq, colsIneq, valsIneq, nMTZ, totalVars);
end
