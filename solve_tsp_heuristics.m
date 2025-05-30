
% --- Carregar coords (supondo arquivo 'berlin52.tsp' no formato TSPLIB) ---
[coords, ~] = read_tsplib('berlin52.tsp'); % Use seu leitor TSPLIB

% --- Matriz de distâncias ---
distMatrix = squareform(pdist(coords));

% --- Montar modelo MTZ ---
[f, intcon, Aineq, bineq, Aeq, beq, lb, ub] = tsp_MTZ(distMatrix);

% --- Heurística 2-opt para solução rápida ---
[tour2opt, cost2opt] = tsp_2opt(coords);
fprintf('2-opt heuristic cost: %.2f\n', cost2opt);
plot_tour(coords, tour2opt, '2-opt heuristic');
