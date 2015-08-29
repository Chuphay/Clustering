
function y = pdist (x, distfun, varargin)

if (nargin < 1)
print_usage ();
elseif (nargin > 1) && ...
! (ischar (distfun) || ...
strcmp (class(distfun), "function_handle"))
error ("pdist: the distance function must be either a string or a function handle.");
endif

if (nargin < 2)
distfun = "euclidean";
endif

if (isempty (x))
error ("pdist: x cannot be empty");
elseif (length (size (x)) > 2)
error ("pdist: x must be 1 or 2 dimensional");
endif

sx1 = size (x, 1);
y = [];
## compute the distance
for i = 1:sx1
tmpd = feval (distfun, x(i,:), x(i+1:sx1,:), varargin{:});
y = [y;tmpd(:)];
endfor

endfunction
