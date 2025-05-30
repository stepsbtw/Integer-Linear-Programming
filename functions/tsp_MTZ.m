function [f, intcon, Aineq, bineq, Aeq, beq, lb, ub] = tsp_MTZ(distMatrix)
    nCities = size(distMatrix,1);
    nVars = nCities^2;

    edgeIndex = @(i,j) (i-1)*nCities + j;
    uIndex = @(i) nVars + i - 1;

    % funcao objetivo
    f = distMatrix(:);

    % x(i,j) em {0,1}
    lb = zeros(nVars,1);
    ub = ones(nVars,1);

    % u(i) em {1,n-1}
    f = [f; zeros(nCities-1,1)];
    lb = [lb; ones(nCities-1,1)];
    ub = [ub; (nCities-1)*ones(nCities-1,1)];

    intcon = 1:(nVars + nCities -1);

    % sem loops em si mesmo
    for i = 1:nCities
        lb(edgeIndex(i,i)) = 0;
        ub(edgeIndex(i,i)) = 0;
    end

    % retricao de grau dos nos
    Aeq = zeros(2*nCities, nVars + nCities -1);
    beq = ones(2*nCities,1);

    % no so sai uma vez
    for i = 1:nCities
        Aeq(i, edgeIndex(i,1:nCities)) = 1;
    end

    % no so entra uma vez
    for j = 1:nCities
        Aeq(nCities + j, j:nCities:nVars) = 1;
    end

    % restricao MTZ
    nMTZ = (nCities-1)*(nCities-2);
    Aineq = zeros(nMTZ, nVars + nCities -1);
    bineq = (nCities - 2)*ones(nMTZ,1);

    row = 1;
    for i = 2:nCities
        for j = 2:nCities
            if i ~= j
                Aineq(row, edgeIndex(i,j)) = nCities - 1;
                Aineq(row, uIndex(i)) = 1;
                Aineq(row, uIndex(j)) = -1;
                row = row + 1;
            end
        end
    end
end
