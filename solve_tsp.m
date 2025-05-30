% Carregar dados
[coords, nome] = read_tsplib('berlin52.tsp');
nCities = size(coords,1);
distMatrix = squareform(pdist(coords)); % distancias

% Montar o modelo
[f, intcon, Aineq, bineq, Aeq, beq, lb, ub] = tsp_MTZ(distMatrix);
% Solve

options = optimoptions('intlinprog', 'Display', 'iter');
[x, fval, exitflag] = intlinprog(f, intcon, Aineq, bineq, Aeq, beq, lb, ub, options);

% Montar o Tour
X = reshape(x(1:nCities^2), nCities, nCities);
tour = build_tour(X);

% Plotar
plot_tour(coords, tour, 'test')

