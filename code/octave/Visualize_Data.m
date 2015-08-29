%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Visualize Data                        
%   
%   Displays Data given to the function on an appropriate
%   graph (i.e. 1D, 2D, or 3D) based on a classification vector
%
%   NEW: If the classification is negative, it will display as the
%        positive result, but much larger
%
%   Ins:
%   X      -- the data
%   C      -- the classes of the data
%   
%   Outs:
%   none
%   
%
%
%   Written by: David Haley
%   Last Edit: 2/15/2015
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function [] = Visualize_Data(X,C)

%how much bigger the callout nodes should appear
bigness = 5;

dim = size(X,2);        % number of columns = number of observables

%make negative class numbers larger, then revert
bigger = (C(:,1) < 0)*bigness+1;
C = abs(C);

num_clusters = max(C(:,1));

if (dim <= 3)
    
    figure();
    clf;

    colormap(lines(num_clusters)); 

    
    if (dim == 1)                              
        scatter(X(:,1),zeros(size(X,1),1),10*bigger, C(:,1),'fill');
                              % graphs 1D projection
    elseif (dim == 2)
        scatter(X(:,1),X(:,2),10*bigger, C(:,1),'fill');
                              % graphs 2D projection
    
    elseif (dim == 3)
        scatter3(X(:,1),X(:,2), X(:,3),10*bigger, C(:,1),'fill');
                              % graphs 3D projection
    
    end
    
                           
    
end

                             


end
