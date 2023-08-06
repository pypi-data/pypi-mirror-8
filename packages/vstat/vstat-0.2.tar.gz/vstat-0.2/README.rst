v-statistic
------------

Implements the v-statistic, a measure that compares the estimation
accuracy of the ordinary least squares estimator against a random benchmark.

See the paper here: http://www.ncbi.nlm.nih.gov/m/pubmed/23661222/ which features
and implementation in R.

I also wrote a Julia version, see https://github.com/dostodabsi/V.jl.

install and run
---------------

install with 

```
[sudo] pip install vstat
```

import with

```
from vstat import vstat
```

and run with

```
vstat(120, 4, .05)
```
