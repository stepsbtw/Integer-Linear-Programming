function [coords, nome] = read_tsplib(filename)
    f = fopen(filename, 'r');
    nome = '';
    % HEADERS
    while ~feof(f)
        line = strtrim(fgetl(f));
        if startsWith(line, 'NAME')
            nome = extractAfter(line, ':');
            nome = strtrim(nome);
        elseif startsWith(line, 'NODE_COORD_SECTION')
            data = textscan(f, '%f %f %f');
            coords = [data{2}, data{3}];
            break;
        end
    end
    fclose(f);
end
    