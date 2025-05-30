function tour = build_tour(X)
    n = size(X,1);
    tour = zeros(1,n+1);
    atual = 1;
    for i = 1:n
        tour(i) = atual;
        prox = find(X(atual,:) > 0.5);
        atual = prox(1);
    end
    
    tour(n+1) = tour(1); % fechar
end
        