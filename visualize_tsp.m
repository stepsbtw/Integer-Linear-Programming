function visualize_tsp(coords, path, titleStr)
    path = [path path(1)];
    figure('Name', titleStr);
    plot(coords(path,1), coords(path,2), '-o', 'LineWidth', 2);
    title(['TSP - ' titleStr]);
    axis equal; grid on;
end
