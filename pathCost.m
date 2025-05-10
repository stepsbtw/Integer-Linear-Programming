function cost = pathCost(path, distMatrix)
    path = [path path(1)];
    cost = sum(arrayfun(@(i) distMatrix(path(i), path(i+1)), 1:length(path)-1));
end
