import inspect
import os
from glob import glob

import pandas


def read_csvs(filename, **k):
    """
    Read multiple csv's into a single pandas.DataFrame

    :param filename: file path that allows wildcards, or folder path
    :param k: keyword arguments that will be passed to read_csv or concat
    :return: the output of the call to pandas.concat for all files matching
    the filename
    """
    read_csv_args = inspect.signature(pandas.read_csv).parameters.keys()
    concat_args = inspect.signature(pandas.concat).parameters.keys()
    read_csv_kwargs = {}
    concat_kwargs = {}
    for kwarg, value in k.items():
        if kwarg in read_csv_args:
            read_csv_kwargs[kwarg] = value
        elif kwarg in concat_args:
            concat_kwargs[kwarg] = value
        else:
            raise NotImplementedError("Neither pandas.read_csv nor "
                                      "pandas.concat knows about the "
                                      "argument {kwarg}".format(kwarg=kwarg))
    if os.path.isdir(filename):
        return pandas.concat(pandas.read_csv(os.path.join(filename, file), **k)
                             for file in os.listdir(filename))
    else:
        return pandas.concat(pandas.read_csv(file, **k) for file in
                             glob(filename))
