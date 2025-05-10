function exportToAMPL(distMatrix, filename)
    n = size(distMatrix, 1);
    fid = fopen([filename '.dat'], 'w');
    fprintf(fid, 'set CITIES := ');
    fprintf(fid, '%d ', 1:n);
    fprintf(fid, ';\n\nparam d : ');
    fprintf(fid, '%d ', 1:n);
    fprintf(fid, ':=\n');
    for i = 1:n
        fprintf(fid, '%d ', i);
        fprintf(fid, '%g ', distMatrix(i,:));
        fprintf(fid, '\n');
    end
    fprintf(fid, ';\n');
    fclose(fid);
end
