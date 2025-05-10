% Executa o Concorde na instância TSPLIB
system('concorde Instances/ALL_tsp/berlin52/berlin52.tsp');

% Lê a solução do arquivo .sol gerado
concordePath = readConcordeSolution('Instances/ALL_tsp/berlin52/berlin52.sol');
costConcorde = pathCost(concordePath, distMatrix);

% Visualização
visualize_tsp(tspCoords, concordePath, 'Concorde (Otimizado)');

exportToAMPL(distMatrix, 'Instances/ALL_tsp/berlin52/berlin52.tsp');

function sol = readConcordeSolution(filename)
    fid = fopen(filename);
    fgetl(fid); % número de cidades
    sol = fscanf(fid, '%d');
    sol = sol' + 1; % indexação MATLAB
    fclose(fid);
end
