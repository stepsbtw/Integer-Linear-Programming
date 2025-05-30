function plot_tour(coords, tour, nome)
    figure;
    plot(coords(:,1), coords(:,2), 'bo', 'MarkerSize', 8);
    hold on;
    plot(coords(tour,1), coords(tour,2), '-r', 'LineWidth', 2);
    title(['Solução - ', nome]);
    xlabel('X'); ylabel('Y');
    axis equal;
    grid on;
end
