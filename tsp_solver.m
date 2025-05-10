clc; clear;

% === PARTE 1: Ler instância TSPLIB ===
[tspCoords, tspName] = readTSPLIB('Instances/ALL_tsp/berlin52/berlin52.tsp');
numCities = size(tspCoords, 1);
distMatrix = squareform(pdist(tspCoords));

% === Algoritmos ===
fprintf("Executando algoritmos no TSP %s...\n", tspName);

% ILP com formulação MTZ
[solILP, costILP, tILP] = tsp_ilp_mtz(distMatrix);

% === Resultados ===
fprintf("\n%-25s %-10s %-10s\n", "Algoritmo", "Custo", "Tempo(s)");
fprintf("%-25s %-10.2f %-10.2f\n", "Busca Aleatória", costRand, tRand);
fprintf("%-25s %-10.2f %-10.2f\n", "Alg. Genético", costGA, tGA);
fprintf("%-25s %-10.2f %-10.2f\n", "Simulated Annealing", costSA, tSA);
fprintf("%-25s %-10.2f %-10.2f\n", "ACO", costACO, tACO);
fprintf("%-25s %-10.2f %-10.2f\n", "ILP (MTZ)", costILP, tILP);

% === Visualizações ===
visualize_tsp(tspCoords, solRand, 'Busca Aleatória');
visualize_tsp(tspCoords, solGA, 'Algoritmo Genético');
visualize_tsp(tspCoords, solSA, 'Simulated Annealing');
visualize_tsp(tspCoords, solACO, 'ACO');
visualize_tsp(tspCoords, solILP, 'ILP (MTZ)');
