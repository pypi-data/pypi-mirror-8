##########################################################################
#
#   MRC FGU Computational Genomics Group
#
#   $Id$
#
#   Copyright (C) 2009 Andreas Heger
#
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
##########################################################################
'''
IOTools - tools for I/O operations
==================================

:Author: Andreas Heger
:Release: $Id$
:Date: |today|
:Tags: Python

Code
----

'''

import string
import re
import sys
import os
import collections
import types
import glob
import stat
import gzip
import subprocess
import itertools

import numpy
import numpy.ma

########################################################################


def readMap(infile,
            columns=(0, 1),
            map_functions = (str, str),
            both_directions=False,
            has_header = False):
    """read a map (pairs of values) from infile.
    returns a hash.

    Use map functions to convert elements.
    If both_directions is set to true, both mapping directions are returned.
    """
    m = {}
    r = {}
    n = 0

    if columns == "all":
        key_column = 0
        value_column = None
    else:
        key_column, value_column = columns

    key_function, value_function = map_functions
    # default is to return a tuple for multiple values
    datatype = None

    for l in infile:
        if l[0] == "#":
            continue
        n += 1

        if has_header and n == 1:
            if columns == "all":
                header = l[:-1].split("\t")
                # remove the first column
                datatype = collections.namedtuple("DATA", header[1:])
            continue

        d = l[:-1].split("\t")
        if len(d) < 2:
            continue
        key = key_function(d[key_column])
        if value_column:
            val = value_function(d[value_column])
        elif datatype:
            val = datatype._make([d[x] for x in range(1, len(d))])
        else:
            val = tuple(map(value_function, [d[x] for x in range(1, len(d))]))

        m[key] = val
        if val not in r:
            r[val] = []
        r[val].append(key)

    if both_directions:
        return m, r
    else:
        return m

########################################################################


def readList(infile,
             column=0,
             map_function=str,
             map_category={},
             with_title=False):
    """read a list of values from infile.

    Use map_function to convert values.
    Use map_category, to map read values directory 
    If with_title, first line is assumed to be a title
    """

    m = []
    errors = []
    title = None
    for l in infile:
        if l[0] == "#":
            continue
        if with_title and not title:
            title = l[:-1].split("\t")[column]
            continue

        try:
            d = map_function(l[:-1].split("\t")[column])
        except ValueError:
            continue

        if map_category:
            d = map_category[d]
        m.append(d)

    if with_title:
        return title, m
    else:
        return m

########################################################################


def ReadList(infile, column=0, map_function=str, map_category={}):
    """read a list of values from infile.

    Use map_function to convert values.
    Use map_category, to map read values directory 
    """

    m = []
    errors = []
    for l in infile:
        if l[0] == "#":
            continue
        try:
            d = map_function(l[:-1].split("\t")[column])
        except ValueError:
            continue
        try:
            if map_category:
                d = map_category[d]

        except KeyError:
            errors.append(d)
            continue
        m.append(d)

    return m, errors

########################################################################


def readMultiMap(infile,
                 columns=(0, 1),
                 map_functions = (str, str),
                 both_directions=False,
                 has_header = False,
                 dtype = dict):
    """read a map (pairs of values) from infile.
    returns a hash. 

    Use map functions to convert elements.
    If both_directions is set to true, both mapping directions are returned.
    This function can have n:n matches
    """
    m = dtype()
    r = dtype()
    n = 0
    for l in infile:
        if l[0] == "#":
            continue
        n += 1

        if has_header and n == 1:
            continue

        d = l[:-1].split("\t")
        try:
            key = map_functions[0](d[columns[0]])
            val = map_functions[1](d[columns[1]])
        except (ValueError, IndexError), msg:
            raise ValueError("parsing error in line %s: %s" % (l[:-1], msg))

        if key not in m:
            m[key] = []
        m[key].append(val)
        if val not in r:
            r[val] = []
        r[val].append(key)

    if both_directions:
        return m, r
    else:
        return m

########################################################################
# Read a table


def readTable(file,
              separator="\t",
              numeric_type=numpy.float,
              take="all",
              headers=True,
              truncate=None,
              cumulate_out_of_range=True,
              ):
    """read a table of values. There probably is a routine for this in
    Numpy, which I haven't found yet.

    If cumulate_out_of_range is set to true, the terminal bins will
    contain the cumulative values of bins out of range.

    """

    lines = filter(lambda x: x[0] != "#", file.readlines())

    if len(lines) == 0:
        return None, []

    if take == "all":
        num_cols = len(string.split(lines[0][:-1], "\t"))
        take = range(0, num_cols)
    else:
        num_cols = len(take)

    if headers:
        headers = lines[0][:-1].split("\t")
        headers = map(lambda x: headers[x], take)
        del lines[0]

    num_rows = len(lines)
    matrix = numpy.ma.masked_array(
        numpy.zeros((num_rows, num_cols), numeric_type))

    if truncate:
        min_row, max_row = truncate

    nrow = 0
    min_data = [0] * num_cols
    max_data = None
    for l in lines:
        data = l[:-1].split("\t")
        data = map(lambda x: data[x], take)

        # try conversion. Unparseable fields set to missing_value
        for x in range(len(data)):
            try:
                data[x] = float(data[x])
            except ValueError:
                data[x] = numpy.ma.masked

        if truncate is not None:
            if data[0] < min_row:
                if cumulate_out_of_range:
                    for x in range(1, num_cols):
                        min_data[x] += data[x]
                continue
            elif data[0] >= max_row:
                if max_data is None:
                    max_data = [0] * num_cols
                    max_data[0] = max_row
                for x in range(1, num_cols):
                    try:
                        max_data[x] += data[x]
                    except TypeError:
                        # missing values cause type errors
                        continue
                continue
            elif min_row is not None:
                if cumulate_out_of_range:
                    for x in range(0, num_cols):
                        try:
                            min_data[x] += data[x]
                        except TypeError:
                            # missing values cause type errors
                            continue
                    else:
                        min_data = data
                data = min_data
                min_row = None

        # copy values into matrix
        # this is a bit clumsy, but missing values
        # cause an error otherwise
        for x in range(len(data)):
            matrix[nrow, x] = data[x]

        nrow += 1

    if truncate is not None:
        if cumulate_out_of_range:
            if max_data is not None:
                matrix[nrow] = max_data

        # truncate matrix
        matrix = matrix[0:nrow + 1, 0:num_cols]

    return matrix, headers

########################################################################


def writeTable(outfile, table, columns=None, fillvalue=""):
    '''write a table to outfile.

    If table is a dictionary, output columnwise. If *columns* is a list,
    only output columns in columns in the specified order.
    '''

    if type(table) == dict:
        if columns is None:
            columns = table.keys()
        outfile.write("\t".join(columns) + "\n")
        # get data
        data = [table[x] for x in columns]
        # transpose
        data = list(itertools.izip_longest(*data, fillvalue=fillvalue))

        for d in data:
            outfile.write("\t".join(map(str, d)) + "\n")

    else:
        raise NotImplementedError

########################################################################


def readMatrix(infile, dtype=numpy.float):
    '''read a numpy matrix from infile.

    return tuple of matrix, row_headers, col_headers
    '''

    lines = [l for l in infile.readlines() if not l.startswith("#")]
    nrows = len(lines) - 1
    col_headers = lines[0][:-1].split("\t")[1:]
    ncols = len(col_headers)
    matrix = numpy.zeros((nrows, ncols), dtype=dtype)
    row_headers = []

    for row, l in enumerate(lines[1:]):
        data = l[:-1].split("\t")
        row_headers.append(data[0])
        matrix[row] = numpy.array(data[1:], dtype=dtype)

    return matrix, row_headers, col_headers

########################################################################


def writeMatrix(outfile, matrix, row_headers, col_headers, row_header=""):
    '''write a numpy matrix to outfile.

    *row_header* gives the title of the rows
    '''

    outfile.write("%s\t%s\n" % (row_header, "\t".join(col_headers)))
    for x, row in enumerate(matrix):
        outfile.write("%s\t%s\n" % (row_headers[x], "\t".join(map(str, row))))

########################################################################


def getInvertedDictionary(dict, make_unique=False):
    """returns an inverted dictionary with keys and values swapped.
    """
    inv = {}
    if make_unique:
        for k, v in dict.iteritems():
            inv[v] = k
    else:
        for k, v in dict.iteritems():
            inv.setdefault(v, []).append(k)
    return inv

########################################################################
# Read a sequence from a fasta file


def readSequence(file):
    """read sequence from a fasta file.

    returns a tuple with description and sequence
    """

    s = []
    for line in file:
        if line[0] == ">":
            description = line[1:-1]
            continue
        elif line[0] == "#":
            continue
        else:
            s.append(re.sub("\s", "", line[:-1]))

    return description, "".join(s)


def getFirstLine(filename):
    # U is to open it with Universal newline support
    f = open(filename, 'rU')
    line = f.readline()
    f.close()
    return line


def getLastLine(filename, nlines=1, read_size=1024):
    """return last line of a file.
    """

    # U is to open it with Universal newline support
    f = open(filename, 'rU')
    offset = read_size
    f.seek(0, 2)
    file_size = f.tell()
    if file_size == 0:
        return ""
    while 1:
        if file_size < offset:
            offset = file_size
        f.seek(-1 * offset, 2)
        read_str = f.read(offset)
        # Remove newline at the end
        if read_str[offset - 1] == '\n':
            read_str = read_str[:-1]
        lines = read_str.split('\n')
        if len(lines) >= nlines + 1:
            return "\n".join(lines[-nlines:])
        if offset == file_size:   # reached the beginning
            return read_str
        offset += read_size
    f.close()


def getNumLines(filename, ignore_comments=True):
    '''get number of lines in filename.'''

    if ignore_comments:
        filter_cmd = '| grep -v "#" '
    else:
        filter_cmd = ""

    # the implementation below seems to fastest
    # see https://gist.github.com/0ac760859e614cd03652
    # and
    # http://stackoverflow.com/questions/845058/how-to-get-line-count-cheaply-in-python
    if filename.endswith(".gz"):
        cmd = "zcat %(filename)s %(filter_cmd)s | wc -l" % locals()
    else:
        cmd = "cat %(filename)s %(filter_cmd)s | wc -l" % locals()

    out = subprocess.Popen(cmd,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT
                           ).communicate()[0]
    return int(out.partition(b' ')[0])


def ReadMap(*args, **kwargs):
    """compatibility - see readMap."""
    return readMap(*args, **kwargs)


def isEmpty(filename):
    '''return True if file exists and is empty.

    raises OSError if file does not exist
    '''
    # don't now about stdin
    if filename == "-":
        return False
    return os.stat(filename)[stat.ST_SIZE] == 0


def isComplete(filename):
    '''return True if file exists and is complete.

    A file in complete if its last line starts
    with '# job finished'
    '''
    if filename.endswith(".gz"):
        raise NotImplementedError(
            'isComplete not implemented for compressed files')
    if isEmpty(filename):
        return False
    lastline = getLastLine(filename)
    return lastline.startswith("# job finished")


class FilePool:

    """manage a pool of output files

    This class will keep a large number of files open. To
    see if you can handle this, check the limit within the shell::

       ulimit -n

    The number of currently open and maximum open files in the system:

      cat /proc/sys/fs/file-nr

    Changing these limits might not be easy for a user.

    This class is inefficient if the number of files is larger than
    :attr:`maxopen` and calls to `write` do not group keys together.
    """

    maxopen = 5000

    def __init__(self,
                 output_pattern=None,
                 header=None,
                 force=True):

        self.mFiles = {}
        self.mOutputPattern = output_pattern

        self.open = open

        if output_pattern:
            _, ext = os.path.splitext(output_pattern)
            if ext.lower() in (".gz", ".z"):
                self.open = gzip.open

        self.mCounts = collections.defaultdict(int)
        self.mHeader = header
        if force and output_pattern:
            for f in glob.glob(re.sub("%s", "*", output_pattern)):
                os.remove(f)

    def __del__(self):
        """close all open files."""
        for file in self.mFiles.values():
            file.close()

    def __len__(self):
        return len(self.mCounts)

    def close(self):
        """close all open files."""
        for file in self.mFiles.values():
            file.close()

    def values(self):
        return self.mCounts.values()

    def keys(self):
        return self.mCounts.keys()

    def iteritems(self):
        return self.mCounts.iteritems()

    def items(self):
        return self.mCounts.items()

    def __iter__(self):
        return self.mCounts.__iter__()

    def getFile(self, identifier):
        return identifier

    def getFilename(self, identifier):
        """get filename for an identifier."""

        if self.mOutputPattern:
            return re.sub("%s", str(identifier), self.mOutputPattern)
        else:
            return identifier

    def setHeader(self, header):
        self.mHeader = header

    def openFile(self, filename, mode="w"):
        """open file.

        If file is in a new directory, create directories.
        """
        if mode in ("w", "a"):
            dirname = os.path.dirname(filename)
            if dirname and not os.path.exists(dirname):
                os.makedirs(dirname)

        return self.open(filename, mode)

    def write(self, identifier, line):

        filename = self.getFilename(identifier)

        if filename not in self.mFiles:

            if self.maxopen and len(self.mFiles) > self.maxopen:
                for f in self.mFiles.values():
                    f.close()
                self.mFiles = {}

            self.mFiles[filename] = self.openFile(filename, "a")
            if self.mHeader:
                self.mFiles[filename].write(self.mHeader)

        try:
            self.mFiles[filename].write(line)
        except ValueError, msg:
            raise ValueError(
                "error while writing to %s: msg=%s" % (filename, msg))
        self.mCounts[filename] += 1

    def deleteFiles(self, min_size=0):
        """delete all files below a minimum size."""

        ndeleted = 0
        for filename, counts in self.mCounts.items():
            if counts < min_size:
                os.remove(filename)
                ndeleted += 1

        return ndeleted


class FilePoolMemory(FilePool):

    """manage a pool of output files

    The data is cached in memory before writing to disk.
    """

    maxopen = 5000

    def __init__(self, *args, **kwargs):
        FilePool.__init__(self, *args, **kwargs)

        self.data = collections.defaultdict(list)
        self.isClosed = False

    def __del__(self):
        """close all open files.
        """
        if not self.isClosed:
            self.close()

    def close(self):
        """close all open files.
        writes the data to disk.
        """
        if self.isClosed:
            raise IOError("write on closed FilePool in close()")

        for filename, data in self.data.iteritems():
            f = self.openFile(filename, "a")
            if self.mHeader:
                f.write(self.mHeader)
            f.write("".join(data))
            f.close()

        self.isClosed = True

    def write(self, identifier, line):

        filename = self.getFilename(identifier)
        self.data[filename].append(line)
        self.mCounts[filename] += 1


def val2str(val, format="%5.2f", na="na"):
    '''return formatted value.

    If value does not fit format string, return "na"
    '''
    if type(val) == int:
        return format % val
    elif type(val) == float:
        return format % val

    try:
        x = format % val
    except (ValueError, TypeError):
        x = na
    return x


def str2val(val, format="%5.2f", na="na"):
    '''guess type of value.'''
    try:
        x = int(val)
    except ValueError:
        try:
            x = float(val)
        except ValueError:
            return val
    return x


def prettyFloat(val, format="%5.2f"):
    """deprecated, use val2str"""
    return val2str(val, format)


def prettyPercent(numerator, denominator, format="%5.2f", na="na"):
    """output a percent value or "na" if not defined"""
    try:
        x = format % (100.0 * numerator / denominator)
    except (ValueError, ZeroDivisionError):
        x = "na"
    return x


def prettyString(val):
    '''output val or na if val is None'''
    if val is not None:
        return val
    else:
        return "na"


class nested_dict(collections.defaultdict):

    """Auto-vivifying nested dictionaries.

    For example::

      nd= nested_dict()
      nd["mouse"]["chr1"]["+"] = 311 

   """

    def __init__(self):
        collections.defaultdict.__init__(self, nested_dict)

    def iterflattened(self):
        """
        iterate through values with nested keys flattened into a tuple
        """

        for key, value in self.iteritems():
            if isinstance(value, nested_dict):
                for keykey, value in value.iterflattened():
                    yield (key,) + keykey, value
            else:
                yield (key,), value


def flatten(l, ltypes=(list, tuple)):
    '''flatten a nested list/tuple.'''
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)


def which(program):
    """check if program is in path.

    from post at http://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
    """

    def is_exe(fpath):
        return os.path.exists(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


def convertValue(value, list_detection=False):
    '''convert a value to int, float or str.'''
    rx_int = re.compile("^\s*[+-]*[0-9]+\s*$")
    rx_float = re.compile("^\s*[+-]*[0-9.]+[.+\-eE][+-]*[0-9.]*\s*$")

    if value is None:
        return value

    if list_detection and "," in value:
        values = []
        for value in value.split(","):
            if rx_int.match(value):
                values.append(int(value))
            elif rx_float.match(value):
                values.append(float(value))
            else:
                values.append(value)
        return values
    else:
        if rx_int.match(value):
            return int(value)
        elif rx_float.match(value):
            return float(value)
        return value


def iterate_tabular(infile, sep="\t"):
    '''iterate over infile skipping comments.'''
    for line in infile:
        if line.startswith("#"):
            continue
        yield line[:-1].split(sep)


def openFile(filename, mode="r", create_dir=False):
    '''open file in *filename* with mode *mode*.

    If *create* is set, the directory containing filename
    will be created if it does not exist.

    gzip - compressed files are recognized by the
    suffix ``.gz`` and opened transparently.

    Note that there are differences in the file
    like objects returned, for example in the
    ability to seek.

    returns a file or file-like object.
    '''

    _, ext = os.path.splitext(filename)

    if create_dir:
        dirname = os.path.dirname(filename)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)

    if ext.lower() in (".gz", ".z"):
        return gzip.open(filename, mode)
    else:
        return open(filename, mode)


def iterate(infile):
    '''iterate over infile and return a namedtuple according to
    first row.'''

    n = 0
    for line in infile:
        if line.startswith("#"):
            continue
        n += 1
        if n == 1:
            # replace non-alphanumeric characters with _
            header = re.sub("[^a-zA-Z0-9_\s]", "_", line[:-1]).split()
            DATA = collections.namedtuple("DATA", header)
            continue

        result = DATA(*line[:-1].split())

        yield result


def zapFile(filename):
    '''replace *filename* with empty file.

    File attributes such as accession times are preserved.

    If the file is a link, the link will be removed and
    replaced with an empty file having the same attributes
    as the file linked to.

    returns a stat object of the file cleaned and the link
    destination.

    '''
    # stat follows times to links
    original = os.stat(filename)

    # return if file already has size 0
    if original.st_size == 0:
        return None, None

    if os.path.islink(filename):
        linkdest = os.readlink(filename)
        os.unlink(filename)
        f = open(filename, "w")
        f.close()
    else:
        linkdest = None
        f = open(filename, "w")
        f.truncate()
        f.close()

    # Set original times
    os.utime(filename, (original.st_atime, original.st_mtime))
    os.chmod(filename, original.st_mode)

    return original, linkdest


def iterator_split(infile, regex):
    '''Return an iterator of file chunks based on a known logical start point
    `regex` that splits the file into intuitive chunks.  This assumes the file
    is structured in some fashion.  For arbitrary number of bytes use
    file.read(`bytes`).
    If a header is present it is returned as the first file chunk.

    infile must be either an open file handle or an iterable.'''
    
    chunk_list = []

    regex = re.compile(regex)

    for x in infile:
        if regex.search(x):
            if len(chunk_list):
                # return the current chunk and start a new one from this point
                yield chunk_list
            chunk_list = []
            chunk_list.append(x)
        else:
            chunk_list.append(x)
        
    yield chunk_list
