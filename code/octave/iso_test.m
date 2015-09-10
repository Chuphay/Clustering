m = 10;                   % n data points in each cluster
kNN = 15;                  % when using kNN
neighborhood = kNN;         % normalizing factor for distance -> adjacency
radius = 14;                % distance between clusters
alpha = 0.80; %alpha = 0.9 problem
p = 0.5;

randn('state',125)
[Distance,labels,xy] = Two_Spots(m, radius); Distance = Distance.^2;
W = Distance_To_Adjacency(Distance, neighborhood);

clusters = funIsoClustering(W, alpha, 1);
%clusters = FastCommDetectMod(W, false, alpha, p);
sum(clusters == 2)
clusters
possible_classes = [2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71];

classes = zeros(length(W));
%getting rid of everlapping regions
for prime = [2 3]
  prime
  this_level = !mod(clusters, prime);
classes = this_level*prime 
endfor


Visualize_Data(xy,clusters); 
