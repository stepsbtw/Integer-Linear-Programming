function [bestPath, bestCost] = improve_3opt(path, distMatrix)
    n = length(path);
    bestPath = path;
    bestCost = pathCost(path, distMatrix);
    improved = true;

    while improved
        improved = false;
        for i = 1:n-5
            for j = i+2:n-3
                for k = j+2:n-1
                    segments = {[i j k], [i k j], [j i k], [j k i], [k i j], [k j i]};
                    for s = 1:length(segments)
                        p = bestPath;
                        [a,b,c] = deal(segments{s}(1), segments{s}(2), segments{s}(3));
                        newPath = [p(1:a), fliplr(p(a+1:b)), fliplr(p(b+1:c)), p(c+1:end)];
                        newCost = pathCost(newPath, distMatrix);
                        if newCost < bestCost
                            bestPath = newPath;
                            bestCost = newCost;
                            improved = true;
                            break;
                        end
                    end
                    if improved, break; end
                end
                if improved, break; end
            end
            if improved, break; end
        end
    end
end
