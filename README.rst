pandas_multi
============

Simple loop for reading multiple csv files (matching a certain pattern) as a 
``pandas.DataFrame``.

I'm aware this need can be solved in even one line of Python, but loading 
multiple similar csv's is just something that should be as easy as loading 
one csv. If you don't want to add a new dependency to your project, google 
what ``os.listdir`` and ``glob`` can do for you.

Installation can be done by typing::

    pip install pandas_multi
Usage of ``pandas_multi.read_csvs`` has been kept as similar as possible to
``pandas.read_csv``::

    import pandas_multi

    # <sarcasm>
    #   Note that dataframes only work if you give them the non-descriptive name df
    # </sarcasm>
    df = pandas_multi.read_csvs('./20180728*.csv')
    # if you provide it with a path to a folder and nothing else, it will assume
    # everything in the folder is a comma-separated file
    df = pandas_multi.read_csvs('./data/')
    # if this is not the case, do this:
    df = pandas_multi.read_csvs('./data/*.csv')
All options that are available to ``pandas.read_csv`` or ``pandas.concat`` 
can be passed into ``pandas_multi.read_csvs`` and will be redirected to the 
appropriate underlying functions.

If you wish to maintain a trace back to the original data, you can run the 
function with the keyword argument ``filenames_as_keys=True``. Note that you
should no longer use the keyword argument ``keys``. This will be ignored.

Please note that the API for concatenation of Excel sheets is not yet stable.
