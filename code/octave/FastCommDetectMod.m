function [ classes ] = FastCommDetectMod( varargin )
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% FastCommDetect (Community Detection)
%
% Detects small communities within a fixed set
%
% This code is optimized vs. previous version to run
%  in O(n^2) time
%
%
% Ins:
%      W = n x n weighted adjacency matrix
%
%      (optional)
%           neg_starts = (boolean) true to label starting nodes as
%                         negative and false for normal operation
%
%           alpha = parameter expressing strictness of inequality
%
%           p = which L-p norm to use
%
% Outs:
%      classes = n x 1 column vector of classifications
%            (as natural numbers 1 up to # of clusters)
%
% Coded by: David Haley
% Last Edit: 07/28/2015
%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %After how many nodes will a progress display be shown
    ALERT_AFTER = 1000;

    if(nargin == 1)
        W = varargin{1};
        neg_starts = false;
        alpha = 1.0;
        p = 1.0;
    elseif(nargin == 2)
        W = varargin{1};
        neg_starts = varargin{2};
        alpha = 1.0;
        p = 1.0;
    elseif(nargin == 3)
        W = varargin{1};
        neg_starts = varargin{2};
        alpha = varargin{3};
        p = 1.0;
    elseif(nargin == 4)
        W = varargin{1};
        neg_starts = varargin{2};
        alpha = varargin{3};
        p = varargin{4};
    else
        error('Wrong number of arguments to FastCommDetect');
    end
        
    W = W .^ p;
    
    %n = number of nodes
    n = size(W,2);
    
    %D = col vector of densities at nodes.
    D = sum(W,2);
    %D = cold vector of densities using only unclassified edges
    D_unc = D;
    
    %initialize class labels
    classes = zeros(n,1);
    
    unclassified = ones(n,1);
    
    %iterator to keep track of number of newest community
    new_comm = 0;
    
    disp('Beginning detection...');
    
    
    %while unclassified nodes exist
    while (sum(unclassified) > 0)
    
       
        
        %start at node with highest degree that has not been classified
        %have to be careful here for things that might have zero local
        %unclassified density so we add one to the density
        %that way if it is unclassified it has lower bound of 1
        %but classified is always zero (thus not the max)
        [~, starting_node] = max(unclassified .* (D_unc+1));
        
        %[~, starting_node] = max(unclassified .* rand(n,1));   %rand
        
        
        

            
        %give the new community a distinct identifying number
        new_comm = new_comm + 1;

    
        old_perimeter = 0;   %initialize
    
        %initialize
        Winside = zeros(n,1);
        new_perimeter = sum(W(:,starting_node));
        
        old_area = 0;        %initialize
        new_area = 0;        %initialize
        
        inside = zeros(n,1);



        %this line included so that the starting node will be classified in
        % the first iteration of the while loop
        present_node = starting_node;

        i = 1;

        %present stopping condition based on capacitance
        % continue while (1-alpha) * dA/A >= (alpha) * dP/P
        
        %stopping condition
        while(  (1.0-alpha) * old_perimeter * (new_area-old_area) ...
                 >= alpha * old_area * (new_perimeter-old_perimeter))
            
            %the community is still satisfied, so accept the current neighbor
            %into the growing community
            %(this should label the starting_node in the first iteration)
            classes(present_node) = new_comm;

            %logicals
            unclassified(present_node) = 0;
            inside(present_node) = 1;
        
            %trap for the case where everything is labelled
            if (sum(unclassified) <= 0)
                break;
            end
    
            %update variables
            old_perimeter = new_perimeter;
            old_area = new_area;
            
            %update the weights leading into the developing community
            Winside = Winside + W(:,present_node);
            
        
            %decide best neighbor
            ratios = Winside ./ abs(D - Winside);
            %put abs here so that ratio is very high if D ~ Winside
            ratios(D - Winside < eps) = inf;
            
            [~, present_node] = max((ratios+1) .* unclassified);
            %find present node by best ratio and not yet in a community
            %have to add 1 to ratio so that the lower bound of unclassified
            %nodes is 1, that way it is > 0 which is the value of classified
            %nodes
        
            %For purposes of next calculation, must include present_node
            inside(present_node) = true;

            %calculate new perimeter, area
            new_perimeter = old_perimeter ...
                            - 2*Winside(present_node) + D(present_node);
            new_area = old_area + Winside(present_node);
            
            if( mod(i, ALERT_AFTER) == 0)
                disp(['  detection continuing, ', ...
                    num2str(i), ' found so far']);
            end
            
            i = i + 1;

        end
    
        %label starting node as negative number
        if(neg_starts)
            classes(starting_node) = -classes(starting_node);
        end
        
        
        
        %update the list of densities based on edges to unclassified nodes
        D_unc = D_unc - Winside;
        
        disp(['Cluster ', num2str(new_comm), ' found, ', ...
            num2str(floor(100*(1-(sum(unclassified)/n)))), '% complete']);
        
    end

end
