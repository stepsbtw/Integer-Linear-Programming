function [bestPath, bestCost, elapsedTime] = tsp_ilp_mtz(distMatrix)
    n = size(distMatrix, 1);
    f = distMatrix(:);
    intcon = 1:n^2;
    lb = zeros(n^2,1);
    ub = ones(n^2,1);

    % Restrições de entrada e saída
    Aeq = zeros(2*n, n^2);
    beq = ones(2*n,1);
    for i = 1:n
        Aeq(i, i:n:end) = 1;
        Aeq(n+i, (i-1)*n+1:i*n) = 1;
    end

    % Impedir loops i->i
    A = eye(n^2);
    b = zeros(n^2,1);
    for i = 1:n
        A((i-1)*n + i,:) = [];
        b((i-1)*n + i,:) = [];
    end

    % Variáveis auxiliares MTZ
    u = n^2+1:n^2+n-1;
    A_mtz = zeros((n-1)^2, n^2 + n-1);
    b_mtz = (n - 1) * ones((n-1)^2, 1);
    row = 1;
    for i = 2:n
        for j = 2:n
            if i == j, continue; end
            A_mtz(row, n^2+i-1) = 1;
            A_mtz(row, n^2+j-1) = -1;
            A_mtz(row, (i-1)*n + j) = n;
            row = row + 1;
        end
    end

    A = [A, zeros(size(A,1), n-1); A_mtz];
    b = [b; b_mtz];
    Aeq = [Aeq, zeros(size(Aeq,1), n-1)];
    lb = [lb; ones(n-1,1)];
    ub = [ub; (n-1)*ones(n-1,1)];
    f = [f; zeros(n-1,1)];

    tic;
    [x,~,~,~,~] = intlinprog(f, [intcon u], A, b, Aeq, beq, lb, ub);
    elapsedTime = toc;

    x = round(x(1:n^2));
    solMatrix = reshape(x, [n n]);
    bestPath = zeros(1,n);
    bestPath(1) = 1;
    for i = 2:n
        bestPath(i) = find(solMatrix(bestPath(i-1),:));
    end
    bestCost = pathCost(bestPath, distMatrix);
end
