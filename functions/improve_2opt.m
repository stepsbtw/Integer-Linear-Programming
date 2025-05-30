function [improvedPath, improvedCost] = improve_2opt(path, distMatrix)
    n = length(path);
    improved = true;
    while improved
        improved = false;
        for i = 2:n-2
            for j = i+1:n-1
                if j - i == 1, continue; end
                newPath = [path(1:i-1), fliplr(path(i:j)), path(j+1:end)];
                if pathCost(newPath, distMatrix) < pathCost(path, distMatrix)
                    path = newPath;
                    improved = true;
                end
            end
        end
    end
    improvedPath = path;
    improvedCost = pathCost(path, distMatrix);
end
