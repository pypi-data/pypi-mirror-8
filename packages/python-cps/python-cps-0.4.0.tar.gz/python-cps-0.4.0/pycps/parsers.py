# -*- coding: utf-8 -*-
"""
Read all the things.
"""
import os
import re
import json
import zipfile
import logging
import importlib
from pathlib import Path
from functools import partial, wraps
from itertools import dropwhile
from collections import OrderedDict, defaultdict
from contextlib import contextmanager

import arrow
import pandas as pd

from pycps.compat import StringIO, str_types

#-----------------------------------------------------------------------------
# Globals
logger = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Settings


@contextmanager
def _open_file_or_stringio(maybe_file):
    """
    Align API
    """
    if isinstance(maybe_file, StringIO):
        yield maybe_file
    else:
        yield open(maybe_file)


def _skip_module_docstring(f):
    next(f)  # first """
    f = dropwhile(lambda x: not x.startswith('"""'), f)
    next(f)  # second """
    return f


def read_settings(filepath):
    """
    Read a mostly valid JSON file with comments. Do path substitution
    and fixup func replacement.

    Parameters
    ----------
    filepath: str or StringIO
        should be JSON like file

    Returns
    -------
    settings: dict

    """
    logger.info("Reading settings from {}".format(filepath))

    with _open_file_or_stringio(filepath) as f:
        f = _skip_module_docstring(f)
        f = ''.join(list(f))  # TODO: could be lazier
        # TODO: skiplines starting with comment char
        f = json.loads(f)

    # need to sort so that we can substitue down the line
    paths = sorted(filter(lambda x: isinstance(x[1], str_types), f.items()),
                   key=lambda x: x.count('/'))
    paths = OrderedDict(paths)

    def count_brackets(x):
        return sum([y.count('{') for y in x.values()
                    if hasattr(y, 'count')])

    # nested loop needed so that a sub in foo/{b}
    # will show up in foo/{b}/{c}
    while count_brackets(paths) > 0:
        current = count_brackets(paths)
        for k, v in paths.items():
            paths[k] = _sub_path(v, paths)
        new = count_brackets(paths)
        if current == new:
            raise ValueError

    f.update(paths)

    # Parse fixup functions in data_dictionary_fixups
    # Go from [paths] -> [{dd_name: funcs}]
    matcher = re.compile(r'(cpsm\d{4}_\d{2})_(.*)')
    dd_fu_paths = f.get('data_dictionary_fixups', [])
    f['data_dictionary_fixups'] = defaultdict(list)

    keyfunc = lambda s: matcher.match(s.__name__).groups()[0]
    from itertools import groupby

    for fu in dd_fu_paths:
        # get rid of `.py` extension and replace '/' with '.'
        to_import = _sub_path_import(fu)

        # import stuff from that path. keep ones that match matcher
        m = importlib.import_module(to_import)
        funcs = [getattr(m, x) for x in dir(m) if matcher.match(x)]
        dds = [keyfunc(x) for x in funcs]

        # groupby dd_name (mYYYY_mm) append to a list for that dd
        for k, group in groupby(zip(dds, funcs), lambda x: x[0]):
            for func in group:
                f['data_dictionary_fixups'][k].append(func[1])
    return f


def _sub_path(v, f):
    pat = r'\{(.*)\}'
    m = re.match(pat, v)
    if m:
        to_sub = m.groups()[0]
        v = re.sub(pat, f[to_sub].rstrip('/\\'), v)
    return v


def _sub_path_import(s):
    return ''.join(s.split('.')[:-1]).replace(os.path.sep, '.')


#-----------------------------------------------------------------------------
# Data Dictionaries


class DDParser:
    """
    Data Dictionary Parser

    Parameters
    ----------

    infile: pathlib.Path
    settings: dict
    info: dict

    Attributes
    ----------

    infile: Path
        ddf from CPS
    outpath: str
        path to HDFStore for output
    store_name:
        key to use inside HDFStore

    Notes
    -----

    There are two regularization passes:

    1. self.regularize_ids
        Occurs immediately after parsing the file. Simple replacement
        of names.
    2. self.make_consistent
        Occurs after self.regularize_ids. Any functions depending on a
        column id should refer to the *regularized* names.

    """

    def __init__(self, infile, settings, info):
        if not isinstance(infile, Path):
            infile = Path(infile)
        self.infile = infile
        self.outpath = settings['dd_path']

        # TODO: whither 94-01, 94-04?, 95-06, 13-01?
        styles = {"cpsm1989-01": 0, "cpsm1992-01": 0, "cpsm1994-01": 2,
                  "cpsm1994-04": 2, "cpsm1995-06": 2, "cpsm1995-09": 2,
                  "cpsm1998-01": 1, "cpsm2003-01": 2, "cpsm2004-05": 2,
                  "cpsm2005-08": 2, "cpsm2007-01": 2, "cpsm2009-01": 2,
                  "cpsm2010-01": 2, "cpsm2012-05": 2, "cpsm2013-01": 2
                  }

        self.store_path = settings['dd_store']
        self.store_name = infile.stem

        # default to most recent
        self.style = styles.get(self.store_name, max(styles.values()))
        self.regex = self.make_regex(style=self.style)
        self.settings = settings

        self.fixups = settings['data_dictionary_fixups'].get(
            self.store_name.replace('-', '_'), {})

        if self.store_name in ('cpsm2009-01', 'cpsm2010-01', 'cpsm2012-05'):
            self.encoding = 'latin_1'
        elif self.store_name == 'cpsm2013-01':
            self.encoding = "cp1252"
        else:
            self.encoding = None
        self.info = info
        self.col_rename = info['col_rename_by_dd'].get(self.store_name, {})

    def run(self):
        """
        Run the parser.

        Returns
        -------
        formatted : DataFrame

        Raises
        ------
        AssertionError : If the DataFrame is not consistent
        in both widths per line and steps between line

        Notes
        -----
        A few steps

        1. Match lines against a regex
        2. Transform matched lines to DataFrame
        3. Renaming via `col_rename` defined in `info`
        4. Fixups via `self.make_consistent`
        """
        logger.info("Starting DDParser on {}".format(self.infile))

        with self.infile.open(encoding=self.encoding) as f:
            # get all header lines
            lines = (self.regex.match(line) for line in f)
            lines = filter(None, lines)

            # regularize format; intentional thunk
            formatted = pd.DataFrame([self.formatter(x) for x in lines],
                                     columns=['id', 'length', 'start', 'end'])

        # ensure consistency across lines
        if self.col_rename:
            formatted = self.regularize_ids(formatted,
                                            replacer=self.col_rename)
        df = self.make_consistent(formatted)
        try:
            assert self.is_consistent(df)
            logger.info("Passed consistency check for {}".format(self.infile))
        except AssertionError:
            logger.error("Failed consistency check for {}".format(self.infile))
            if not check_width(df).all():
                logger.error("Bad widths: {}".format(df[~check_width(df)]))
            else:
                bad = pd.concat([df.shift()[~check_steps(df)],
                                 df[~check_steps(df)]], axis=1,
                                keys=['low', 'high'])
                logger.error("Bad steps: {}".format(bad))
            raise ValueError("Data Dictionary is not consistent")
        return df

    @staticmethod
    def is_consistent(formatted):
        """
        Given a list of tuples, make sure the column numbering is
        internally consistent.

        Checks that

        1. width == (end - start) + 1
        2. start_1 == end_0 + 1
        """
        return check_width(formatted).all() and check_steps(formatted).all()

    @staticmethod
    def regularize_ids(df, replacer):
        """
        Regularize the ids as early as possible.

        Parameters
        ----------
        df: DataFrame returned from DDParser.run
        replace: dict
            {cps_id -> regularized_id}
            probably defined in info.json
        """
        return df.replace({'id': replacer})

    @staticmethod
    def make_regex(style=None):
        """
        Regex factory to match. Each dd has a style (just an id for that regex)
        Some dds share styles.
        The default style is the most recent.
        """
        # As new styles are added the current default should be moved into the
        # dict.
        # TODO: this smells terrible
        default = re.compile(u'[\x0c]{0,1}(\w+)\*?[\s\t]*(\d{1,2})[\s\t]*(.*?)'
                             u'[\s\t]*\(*(\d+)\s*[\-–]\s*(\d+)\)*\s*$')
        d = {0: re.compile(r'(\w{1,2}[\$\-%]\w*|PADDING)\s*CHARACTER\*(\d{3})'
                           '\s*\.{0,1}\s*\((\d*):(\d*)\).*'),
             1: re.compile(r'D (\w+) \s* (\d{1,2}) \s* (\d*)'),
             2: default}
        return d.get(style, default)

    def formatter(self, match):
        """
        Conditional on a match, format them into a nice tuple of
            id, length, start, end

        match is a regex object.
        """
        # TODO: namedtuple return values
        if self.style == 1:
            id_, length, start = match.groups()
            length = int(length)
            start = int(start)
            end = start + length - 1
        else:
            try:
                id_, length, start, end = match.groups()
                id_ = self.handle_replacers(id_)
            except ValueError:
                id_, length, description, start, end = match.groups()
            length = int(length)
            start = int(start)
            end = int(end)
        return (id_, length, start, end)

    def write(self, df):
        """
        Once you have all the dataframes, write them to that outfile,
        an HDFStore.

        Parameters
        ----------
        storepath: str

        Returns
        -------
        None: IO

        """
        logger.info("Writing {} to {}".format(self.store_name,
                                              self.store_path))
        df.to_hdf(self.store_path, key=self.store_name, format='f')

    @staticmethod
    def handle_replacers(id_):
        """
        Prefer ids to be valid python names.
        """
        replacers = {'$': 'd', '%': 'p', '-': 'h'}
        for bad_char, good_char in replacers.items():
            id_ = id_.replace(bad_char, good_char)
        return id_

    def make_consistent(self, formatted):
        """
        redo
        """
        def generate_cpsm200511(formatted):
            """
            The CPS added new questions in November 2005 (Katrina related).
            They should have defined a new data dictionary. They didn't...

            This function:

                0. ignores the end at col 886 and makes formatted throug the
                   end of the file
                1. writes out that *new* formatted as cpsm2005-11 to HDF?
                2. Truncates the current `formatted` at col 886 (correct fo
                   2005-08 thru 2005-10)
                3. return to the original control flow.

            Good luck trying to test this.
            """
            # generate and write cpsm2005-11
            new = formatted.drop(376).reset_index()
            key = 'cpsm2005-11'
            # The debt is real
            new = self.regularize_ids(
                new, replacer=self.info['col_rename_by_dd'][key])

            assert self.is_consistent(new)

            # write this out.
            new.to_hdf(self.store_path, key=key, format='f')

            # fix original (for aug. thru oct. 2005)
            return formatted.loc[:376]

        dispatch = self.fixups

        if self.store_name == 'cpsm2005-08':
            dispatch.append(generate_cpsm200511)

        for func in dispatch:
            logger.info("Applying {} to {}".format(func, self.store_name))
            formatted = func(formatted)

        return formatted


#-----------------------------------------------------------------------------
# Monthly Data Files

def _month_to_dd(month):
    """
    lookup dd for a given month.
    """
    dd_to_month = {"cpsm1989-01": ["1989-01", "1991-12"],
                   "cpsm1992-01": ["1992-01", "1993-12"],
                   "cpsm1994-01": ["1994-01", "1994-03"],
                   "cpsm1994-04": ["1994-04", "1995-05"],
                   "cpsm1995-06": ["1995-06", "1995-08"],
                   "cpsm1995-09": ["1995-09", "1997-12"],
                   "cpsm1998-01": ["1998-01", "2002-12"],
                   "cpsm2003-01": ["2003-01", "2004-04"],
                   "cpsm2004-05": ["2004-05", "2005-07"],
                   "cpsm2005-08": ["2005-08", "2005-10"],
                   "cpsm2005-11": ["2005-11", "2006-12"],
                   "cpsm2007-01": ["2007-01", "2008-12"],
                   "cpsm2009-01": ["2009-01", "2009-12"],
                   "cpsm2010-01": ["2010-01", "2012-04"],
                   "cpsm2012-05": ["2012-05", "2012-12"],
                   "cpsm2013-01": ["2013-01", "2014-05"]}

    def mk_range(v):
        return arrow.Arrow.range(start=arrow.get(v[0]),
                                 end=arrow.get(v[1]),
                                 frame='month')

    rngs = {k: mk_range(v) for k, v in dd_to_month.items()}

    def isin(value, key):
        return value in rngs[key]

    f = partial(isin, arrow.get(month))
    dd = filter(f, dd_to_month)
    return list(dd)[0]


@contextmanager
def ensure_cleanup_zip(archive, filename, parent_dir):
    path = os.path.join(parent_dir, filename)
    archive.extract(filename, path=parent_dir)
    yield
    os.remove(path)


def read_monthly(infile, dd):
    """
    Parameters
    ----------

    infile: str
    dd: DataFrame

    Returns
    -------
    df: DataFrame

    """
    widths = dd.length.tolist()
    logger.info("Reading monthly {}".format(infile))

    if isinstance(infile, StringIO):
        df = pd.read_fwf(infile, widths=widths, names=dd.id.values)
    elif infile.endswith('.zip'):
        archive = zipfile.ZipFile(infile)
        filename = archive.namelist()[0]
        parent_dir = str(Path(infile).parent)
        colspec = pd.concat([dd.start - 1, dd.end], axis=1)
        colspec = colspec.values.tolist()

        with ensure_cleanup_zip(archive, filename, parent_dir):
            df = pd.read_fwf(os.path.join(parent_dir, filename),
                             colspecs=colspec, names=dd.id.values)
    # TODO: Fix stripping of 0s
    return df


def write_monthly(df, storepath, key):
    """
    Add a monthly datafile to the store.

    Parameters
    ----------
    storepath: str
    key: name in store

    Returns
    -------
    None: IO

    """
    logger.info("Writing {} to {}".format(key, storepath))
    df.to_hdf(storepath, key=key, format='f')


def fixup_by_dd(df, fixups):
    """
    Fixup *data* by Data Dictionary.

    Parameters
    ----------
    df : DataFrame
    fixups: [(function, {kwargs})], a list of tuples of functions
        and dictionaries mapping kwargs to values for that function.
        Fixups should come from pycps.monthly_data_fixups or
        a user supplied file.

    Returns
    -------
    fixed : DataFrame
    """
    for func, kwargs in fixups:
        df = func(df, **kwargs)

    return df


def log_transform(obj_name):
    """
    Log that the object `obj_name` is being transformed by the function being
    decorated.
    """
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            logger.info("Transforming {} via {}".format(obj_name,
                                                        func.__name__))
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorate

# ----------------------------------------------------------------------------
# Consistency checks
check_width = lambda df: df['length'] == df['end'] - df['start'] + 1
check_steps = lambda df: df.start - df.end.shift(1).fillna(0) - 1 == 0
# ----------------------------------------------------------------------------

# def align_lfsr(df, dd_name):
#     """Jan1989 and Jan1999. LFSR (labor focrce status recode)
#     had
#        1 = WORKING
#        2 = WITH JOB,NOT AT WORK
#        3 = UNEMPLOYED, LOOKING FOR WORK
#        4 = UNEMPLOYED, ON LAYOFF
#        5 = NILF - WORKING W/O PAY < 15 HRS;
#                   TEMP ABSENT FROM W/O PAY JOB
#        6 = NILF - UNAVAILABLE
#        7 = OTHER NILF
#     newer ones have
#        1   EMPLOYED-AT WORK
#        2   EMPLOYED-ABSENT
#        3   UNEMPLOYED-ON LAYOFF
#        4   UNEMPLOYED-LOOKING
#        5   NOT IN LABOR FORCE-RETIRED
#        6   NOT IN LABOR FORCE-DISABLED
#        7   NOT IN LABOR FORCE-OTHER
#     this func does several things:
#         1. Change 3 -> 4 and 4 -> 3 in the old ones.
#         2. Change 5 and 6 to 7.
#         2. Read retired from AhNLFREA == 4 and set to 5.
#         3. Read ill/disabled from AhNLFREA == 2 and set to 6.
#     Group 7 kind of loses meaning now.
#     """
#     # 1. realign 3 & 3
#     status = df["AhLFSR"]
#     # status = status.replace({3: 4, 4: 3})  # chcek on ordering

#     status_ = status.copy()
#     status_[status == 3] = 4
#     status_[status == 4] = 3
#     status = status_

#     # 2. Add 5 and 6 to 7
#     status = status.replace({5: 7, 6: 7})

#     # 3. ill/disabled -> 6
#     status[df['AhNLFREA'] == 2] = 6

#     df['PEMLR'] = status
#     df = df.drop(["AhLFSR", "AhNLFREA"], axis=1)
#     return df
