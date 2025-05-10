% Matriz de custos (exemplo simples de 3 tarefas e 3 recursos)
costMatrix = [
    9, 2, 7;
    6, 4, 3;
    3, 8, 5
];

% Chama a função matchpairs para encontrar o emparelhamento ótimo
[assignments, totalCost] = matchpairs(costMatrix);

% Exibir os resultados
disp('Emparelhamentos:')
disp(assignments)  % Mostra quais elementos de uma coluna são emparelhados com as linhas
disp('Custo total:')
disp(totalCost)
