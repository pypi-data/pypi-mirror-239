
[![DOI](https://zenodo.org/badge/46057982.svg)](https://zenodo.org/badge/latestdoi/46057982)

## marcumQ

This is a scipy wrapper to evaluate the generalized Marcum-Q function. This is defined as:

<img src="https://github.com/dgerosa/marcumq/assets/7237041/701bacaf-f1b8-4bc6-8946-c968bb8bf8f3" width="500">

For properties and applications

- [wikipedia.org/wiki/Marcum_Q-function](https://en.wikipedia.org/wiki/Marcum_Q-function)
- [mathworld.wolfram.com/MarcumQ-Function.html](https://mathworld.wolfram.com/MarcumQ-Function.html)

Ours is a straightforward implementation that simply converts the relevant conventions from [`scipy.stats.ncx2`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ncx2.html). Install this package with `pip install marcumq` and then use it with:

```
import marcumq
marcumq.marcumq(nu=1,a=1.5,b=2.5)
```

If you use this code, it would be great if you could cite the following paper (this implementation is introduced in the appendix):

