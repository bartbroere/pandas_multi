# pandas_multi
Simple loop for reading multiple csv files (matching a certain pattern) as a 
``pandas.DataFrame``.

I'm aware this need can be solved in even one line of Python, but loading 
multiple similar csv's is just something that should be as easy as loading 
one csv. If you don't want to add a new dependency to your project, google 
what ``os.listdir`` and ``glob`` can do for you.

Installation can be done by typing:
``
pip install pandas_multi
``

Usage of ``pandas_multi.read_csvs`` has been kept as similar as possible to 
``pandas.read_csv``:

```python
import pandas_multi

# <sarcasm>
#   Note that dataframes only work if you give them the non-descriptive name df
# </sarcasm>
df = pandas_multi.readcsvs('./20180728*.csv')
# if you provide it with a path to a folder and nothing else, it will assume 
# everything in the folder is a comma-separated file
df = pandas_multi.readcsvs('./data/')
# if this is not the case, do this:
df = pandas_multi.readcsvs('./data/*.csv')
```
