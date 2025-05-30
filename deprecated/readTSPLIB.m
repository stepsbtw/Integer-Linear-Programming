function [coordMatrix, name] = readTSPLIB(filename)
    fid = fopen(filename);
    name = '';
    while true
        line = fgetl(fid);
        if contains(line, 'NODE_COORD_SECTION')
            break;
        elseif contains(line, 'NAME')
            name = strtrim(strrep(line, 'NAME:', ''));
        end
    end
    coordMatrix = [];
    while true
        line = fgetl(fid);
        if isempty(line) || contains(line, 'EOF')
            break;
        end
        nums = sscanf(line, '%f');
        coordMatrix(end+1,:) = nums(2:3); %#ok<AGROW>
    end
    fclose(fid);
end