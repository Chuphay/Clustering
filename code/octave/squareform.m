
function y = squareform (x, method)

  if ((nargin < 1) ||  (~isnumeric(x)))
    usage (['squareform: must input distance matrix or vector; see help']);
  endif

  if (nargin < 2)
    if (isscalar (x) || isvector (x))
      method = 'tomatrix';
elseif (issquare (x))
method = 'tovector';
 else
   usage ('squareform: must input distance matrix or vector; see help');
    endif
    else
      method = lower (method);
if (~any (strcmp ({'tovector' 'tomatrix'}, method)))
  usage ('squareform: method must be either "tovector" or "tomatrix"');
    endif
  endif

    if (strcmp ('tovector', method))
      if (~issquare (x))
	usage ('squareform: x is not a square matrix');
elseif (any (diag (x) ~= 0))
usage ('squareform: x is not a hollow matrix');
elseif (~issymmetric(x))
warning ('squareform:symmetric', ...
	 'squareform: x is not a symmetric matrix');
    endif

    sx = size (x, 1);
y = zeros (1, (sx - 1) * sx / 2);
idx = 1;
for i = 2 : sx
	  newidx = idx + sx - i;
y(1, idx:newidx) = x(i:sx, i-1);
idx = newidx + 1;
    endfor
 else
    ## we're converting to a matrix

    ## make sure that x is a column
    x = x(:);

    ## the dimensions of y are the solution to the quadratic formula for:
    ## length (x) = (sy - 1) * (sy / 2)
    sy = (1 + sqrt (1 + 8 * length (x))) / 2;
    if (floor (sy) ~= sy)
      usage ('squareform: incorrect vector size; see help');
    else
      y = zeros (sy);
      for i = 1 : sy-1
        step = sy - i;
        y((sy-step+1):sy, i) = x(1:step);
        x(1:step) = [];
      endfor
      y = y + y';
    endif
  endif

endfunction
