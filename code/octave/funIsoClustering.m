function classes  = funIsoClustering( varargin )

   if(nargin == 1)
        W = varargin{1};
        alpha = 1.0;
        p = 1.0;
    elseif(nargin == 2)
        W = varargin{1};
        alpha = varargin{2};
        p = 1.0;
    elseif(nargin == 3)
        W = varargin{1};
        alpha = varargin{2};
        p = varargin{3};
    else
        error('Wrong number of arguments to FastCommDetect');
    endif


    data.W = W; % .^ p;                  %adjacenecy matrix with optional L-p norm stuff...
    data.N = size(W,2);                  %total number of vertices
    data.D = sum(W,2);                   %degree of each vertex
    classes = ones(data.N,1);            %final classification of the vertices
    

    possible_classes = [2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71];
    num_clusters = 0; 

    for i = 1:(data.N)
	if(num_clusters >= length(possible_classes))
	    error("Error... max number of clusters exceeded");
	endif
        if (classes(i) == 1)
	    num_clusters = num_clusters + 1;
            clustered = funClustering(i, alpha, data);
	    classes = (clustered .* possible_classes(num_clusters) + !clustered) .* classes;
	endif
    endfor
endfunction
 

function classified = funClustering(seed, alpha, data)
    internalW = data.W(:,seed);       %keeps track of all edges in or coming out of the cluster
    perimeter = data.D(seed);         %the size of the current perimeter
    area = 0;                         %the size of the current area 
    unclassified = ones(data.N,1);    %indicator for unclassified vertices

    unclassified(seed) = 0; 

    for i = 1:(data.N - 1) %we minus 1, because the seed is already classified  

        temp_perimeter = perimeter - 2*internalW + data.D;
        temp_area = area + internalW;
    
        ratios = temp_area ./ temp_perimeter;  
        [a, new_node] = max((ratios+1) .* unclassified); %we add 1 to the ratio... 

        if((1.0-alpha) * perimeter * (temp_area(new_node) - area) ...
                >= alpha * area * (temp_perimeter(new_node) - perimeter))

	    unclassified(new_node) = 0;
            internalW = internalW + data.W(:, new_node);
            perimeter = temp_perimeter(new_node);
            area = temp_area(new_node);
	else
            break
        endif
    endfor

    classified = !unclassified;
endfunction
    
