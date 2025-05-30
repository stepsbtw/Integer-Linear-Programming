function [tour, cost] = tsp_2opt(coords)
    n = size(coords,1);
    tour = [1:n 1]; % tour inicial sequencial
    improved = true;

    while improved
        improved = false;
        for i = 2:n-2
            for j = i+1:n
                if j - i == 1, continue; end
                newTour = tour;
                newTour(i:j) = tour(j:-1:i); % swap 2-opt
                if tour_cost(coords, newTour) < tour_cost(coords, tour)
                    tour = newTour;
                    improved = true;
                end
            end
        end
    end
    cost = tour_cost(coords, tour);
    tour = tour(1:end-1); % remove retorno duplicado
end

function cost = tour_cost(coords, tour)
    cost = sum(vecnorm(coords(tour(1:end-1),:) - coords(tour(2:end),:), 2, 2));
end
