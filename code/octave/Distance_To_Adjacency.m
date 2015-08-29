%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
%   Distance to Adjacency                           
%   
%
%   Converts the Square of a Distance Graph into a normalized
%    Similarity matrix in Decision Space
%
%   Adapted from group code entitled construct_kNN_graph
%
%
%   Written by: David Haley
%   Last Edit: 11/4/2014
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


function W = Distance_To_Adjacency(D, threshold)

    N=size(D,2);

    [D_sorted,index]=sort(D,2);

    %Choose sigma to be the average distance of the i^th nearest neighbor
    sigma = mean(sqrt(D_sorted(:,threshold)));

    
    weights=exp(-D./(2*sigma^2));

    W = triu(weights,1);
    W = max(W, W');
    
end