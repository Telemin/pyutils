# pyutils
a python module of my useful snippets

The major useful snippet here right now is the pyutils.ipython.ProgressBar class which provides a simple, progress bar for loops in an ipython notebook.

Use as follows, (in an ipython notebook cell!)

```
from pyutils.ipython import ProgressBar
from time import sleep
for i in ProgressBar(range(100)):
    sleep(0.1)
```
