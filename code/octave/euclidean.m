function d = euclidean(u, v)
d = sqrt (sum ((repmat (u, size (v,1), 1) - v).^2, 2));
endfunction
