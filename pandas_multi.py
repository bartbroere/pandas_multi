import inspect
import os
import warnings
from collections import defaultdict
from glob import glob

import pandas
from pandas.errors import EmptyDataError


def read_multiple_files(reader, io, filenames_as_keys=False,
                        concat_axis='sheet', sheets_as_keys=False, **k):
    """
    Read multiple files, or all files in a folder into a single
    pandas.DataFrame

    :param reader: the original pandas reader function
    :param io: file path that allows wildcards, or folder path
    :param filenames_as_keys: add index with original filename to the DataFrame
                              cannot be used together with the option ``keys``
    :param concat_axis:
    :param sheets_as_keys:
    :param k: keyword arguments that will be passed to the reader or concat
    :return: the output of the call to pandas.concat for all files matching
             the filename
    """
    reader_args = inspect.signature(reader).parameters.keys()
    concat_args = inspect.signature(pandas.concat).parameters.keys()
    reader_kwargs = {}
    concat_kwargs = {}
    dfs = []

    for kwarg, value in k.items():
        if kwarg in reader_args:
            reader_kwargs[kwarg] = value
        elif kwarg in concat_args:
            concat_kwargs[kwarg] = value
        else:
            raise NotImplementedError("Neither {readername} nor "
                                      "pandas.concat knows about the "
                                      "argument {kwarg}".format(
                readername=reader.__name__,
                kwarg=kwarg))

    if os.path.isdir(io):
        filenames = os.listdir(io)
        if filenames_as_keys:
            concat_kwargs['keys'] = filenames
        filenames = [os.path.join(io, file) for file in filenames]
    else:
        if filenames_as_keys:
            concat_kwargs['keys'] = [os.path.basename(path) for path in
                                     glob(io)]
        filenames = glob(io)

    for file in filenames:
        try:
            dfs.append(reader(file, **reader_kwargs))
        except EmptyDataError:
            warnings.warn('Reading {file} raised an EmptyDataError. '
                          'Continuing without its contents.'.format(
                file=file,
            ))
            continue
    if concat_axis == 'sheet':
        sheets_dfs = defaultdict(pandas.DataFrame)
        for df in dfs:
            for sheet, data in df.items():
                if sheets_as_keys:
                    data['sheet'] = sheet
                    data = data.set_index('sheet', drop=False)
                sheets_dfs[sheet].append(data)
        return sheets_dfs
    elif concat_axis == 'within_file':
        sheets = []
        for df in dfs:
            for sheet, data in df.items():
                if sheets_as_keys:
                    data['sheet'] = sheet
                    data = data.set_index('sheet', drop=False)
                sheets.append(data)
        result = sheets[0]
        for sheet in sheets[1:]:
            result = result.append(sheet, sort=False)
        return result
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


def read_csvs(io, filenames_as_keys=False, **k):
    """
    Read multiple csv files, or all files in a folder into a single
    pandas.DataFrame.

    :param io: file path that allows wildcards, or folder path
    :param filenames_as_keys: add index with original filename to the DataFrame
                              cannot be used together with the option ``keys``
    :param k: keyword arguments that will be passed to the reader or concat
    :return: the output of the call to pandas.concat for all files matching
             the filename
    """
    return read_multiple_files(pandas.read_csv,
                               io,
                               filenames_as_keys=filenames_as_keys,
                               **k)


def read_excels(io, filenames_as_keys=False, **k):
    """
    Read multiple excel files, or all files in a folder into a single
    pandas.DataFrame.

    :param io: file path that allows wildcards, or folder path
    :param filenames_as_keys: add index with original filename to the DataFrame
                              cannot be used together with the option ``keys``
    :param k: keyword arguments that will be passed to the reader or concat
    :return: the output of the call to pandas.concat for all files matching
             the filename
    """
    return read_multiple_files(pandas.read_excel,
                               io,
                               filenames_as_keys=filenames_as_keys,
                               **k)
