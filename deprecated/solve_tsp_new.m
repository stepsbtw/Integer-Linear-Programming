coords = read_tsplib('instances/berlin52.tsp');
distMatrix = squareform(pdist(coords));
[f, intcon, Aineq, bineq, Aeq, beq, lb, ub] = tsp_MTZ_new(distMatrix);

options = optimoptions('intlinprog', 'Display', 'iter', ...
    'Heuristics', 'advanced', 'CutGeneration','advanced', ...
    'MaxTime', 600);  % limite de tempo

[x, fval, exitflag] = intlinprog(f, intcon, Aineq, bineq, Aeq, beq, lb, ub, options);
