% Heurísticas construtivas para o TSP
clc; clear;

%% Parâmetros
numCities = 8;
numRuns = 30;  % Número de execuções para métodos estocásticos
cityCoords = rand(numCities, 2) * 100; % Coordenadas aleatórias

distMatrix = squareform(pdist(cityCoords)); % Matriz de distâncias
%% Algoritmo 1: Força Bruta
fprintf("Executando força bruta...\n");
tic;
permsList = perms(1:numCities);
numPerms = size(permsList, 1);
bestCostBrute = inf;
for i = 1:numPerms
    path = permsList(i,:);
    cost = pathCost(path, distMatrix);
    if cost < bestCostBrute
        bestCostBrute = cost;
        bestPathBrute = path;
    end
end
timeBrute = toc;

%% Algoritmo 2: Busca Aleatória
fprintf("Executando busca aleatória...\n");
bestCostRand = inf;
tic;
for i = 1:numRuns
    path = randperm(numCities);
    cost = pathCost(path, distMatrix);
    if cost < bestCostRand
        bestCostRand = cost;
        bestPathRand = path;
    end
end
timeRand = toc;

%% Resultados
fprintf("\nResultados:\n");
fprintf("Força Bruta: Custo = %.2f | Tempo = %.2f s\n", bestCostBrute, timeBrute);
fprintf("Busca Aleatória: Custo = %.2f | Tempo = %.2f s\n", bestCostRand, timeRand);
fprintf("Algoritmo Genético: Custo = %.2f | Tempo = %.2f s\n", bestCostGA, timeGA);

%% Funções auxiliares

function cost = pathCost(path, distMatrix)
    path = [path path(1)]; % volta à cidade inicial
    cost = sum(arrayfun(@(i) distMatrix(path(i), path(i+1)), 1:length(path)-1));
end
