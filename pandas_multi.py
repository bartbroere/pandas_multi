import inspect
import os
import warnings
from glob import glob

import pandas
from pandas.errors import EmptyDataError


def read_multiple_files(reader, filename, filenames_as_keys=False, **k):
    """
    Read multiple csv's into a single pandas.DataFrame

    :param reader: the original pandas reader function
    :param filename: file path that allows wildcards, or folder path
    :param filenames_as_keys: add index with original filename to the DataFrame
                              cannot be used together with the option ``keys``
    :param k: keyword arguments that will be passed to read_csv or concat
    :return: the output of the call to pandas.concat for all files matching
    the filename
    """
    read_csv_args = inspect.signature(reader).parameters.keys()
    concat_args = inspect.signature(pandas.concat).parameters.keys()
    read_csv_kwargs = {}
    concat_kwargs = {}
    for kwarg, value in k.items():
        if kwarg in read_csv_args:
            read_csv_kwargs[kwarg] = value
        elif kwarg in concat_args:
            concat_kwargs[kwarg] = value
        else:
            raise NotImplementedError("Neither {readername} nor "
                                      "pandas.concat knows about the "
                                      "argument {kwarg}".format(
                readername=reader.__name__,
                kwarg=kwarg))
    if os.path.isdir(filename):
        dircontents = os.listdir(filename)
        if filenames_as_keys:
            concat_kwargs['keys'] = dircontents
        return pandas.concat([pandas.read_csv(os.path.join(filename, file),
                                              **read_csv_kwargs)
                              for file in dircontents],
                             **concat_kwargs)
    else:
        if filenames_as_keys:
            concat_kwargs['keys'] = [os.path.basename(path) for path in
                                     glob(filename)]
        dfs = []
        for file in glob(filename):
            try:
                dfs.append(pandas.read_csv(file, **read_csv_kwargs))
            except EmptyDataError:
                warnings.warn('Reading ' + file + ' raised an EmptyDataError.' +
                              'Continuing without its contents.')
                continue
        try:
            return pandas.concat(dfs, **concat_kwargs)
        except ValueError as e:
            if str(e) == 'No objects to concatenate':
                warnings.warn('No files matched the specified path, or '
                              'matching files have been skipped for other '
                              'reasons (e.g. EmptyDataError).')
                return pandas.DataFrame()
            else:
                raise


def read_csvs(filename, filenames_as_keys=False, **k):
    return read_multiple_files(pandas.read_csv,
                               filename,
                               filenames_as_keys=filenames_as_keys,
                               **k)
