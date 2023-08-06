import os
import sys
import re
import subprocess
from contextlib import contextmanager
import logging
logger = logging.getLogger(__name__)


MAJOR_VERSION_RE = re.compile(r'(\d+)[.](saas~|)(\d*)(\w*)')


class WorkingDirectoryKeeper(object):
    """A context manager to get back the working directory as it was before.

    If you want to stack working directory keepers, you need a new instance
    for each stage.
    """

    active = False

    def __enter__(self):
        if self.active:
            raise RuntimeError("Already in a working directory keeper !")
        self.wd = os.getcwd()
        self.active = True

    def __exit__(self, *exc_args):
        os.chdir(self.wd)
        self.active = False

working_directory_keeper = WorkingDirectoryKeeper()


@contextmanager
def use_or_open(provided, path, *open_args):
    """A context manager to use an open file if not None or open one.

    Useful for code that should be unit-testable, but work on a default file if
    None is passed.
    """
    if provided is not None:
        yield provided
    else:
        with open(path, *open_args) as f:
            yield f


def major_version(version_string):
    """The least common denominator of OpenERP versions : two numbers.

    OpenERP version numbers are a bit hard to compare if we consider nightly
    releases, bzr versions etc. It's almost impossible to compare them without
    an a priori knowledge of release dates and revisions.

    Here are some examples::

       >>> major_version('1.2.3-foo.bar')
       (1, 2)
       >>> major_version('6.1-20121003-233130')
       (6, 1)
       >>> major_version('7.0alpha')
       (7, 0)

    Beware, the packaging script does funny things, such as labeling current
    nightlies as 6.2-date-time whereas version_info is (7, 0, 0, ALPHA)
    We can in recipe code check for >= (6, 2), that's not a big issue.

    Regarding OpenERP saas releases (e.g. 7.saas~1) that are short-lived stable
    versions between two "X.0" LTS releases, the 'saas~' argument before the
    minor version number is stripped. For instance::

       >>> major_version('7.saas~3')
       (7, 3)

    """

    m = MAJOR_VERSION_RE.match(version_string)

    if m is None:
        raise ValueError("Unparseable version string: %r" % version_string)

    major = int(m.group(1))
    minor = m.group(3)

    try:
        return major, int(minor)
    except TypeError:
        raise ValueError(
            "Unrecognized second version segment in %r" % version_string)


def mkdirp(path):
    """Same as mkdir -p."""
    if not os.path.exists(path):
        parent, name = os.path.split(path)
        mkdirp(parent)
        os.mkdir(path)


def is_object_file(filename):
    """True if given filename is a python object file."""
    return filename.endswith('.pyc') or filename.endswith('.pyo')


def clean_object_files(directory):
    """Recursively remove object files in given directory.

    Also remove resulting empty directories.
    """
    dirs_to_remove = []
    for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
        to_delete = [os.path.join(dirpath, f)
                     for f in filenames if is_object_file(f)]
        if not dirnames and len(to_delete) == len(filenames):
            dirs_to_remove.append(dirpath)
        for p in to_delete:
            try:
                os.unlink(p)
            except:
                logger.exception("Error attempting to unlink %r. "
                                 "Proceeding anyway.", p)
    for d in dirs_to_remove:
        try:
            os.rmdir(d)
        except:
            logger.exception("Error attempting to rmdir %r",
                             "Proceeding anyway.", p)


def check_output(*popenargs, **kwargs):
    r"""Backport of subprocess.check_output from python 2.7.

    Example (this doctest would be more readable with ELLIPSIS, but
    that's good enough for today):

    >>> out = check_output(["ls", "-l", "/dev/null"])
    >>> out.startswith('crw-rw-rw')
    True

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> os.environ['LANG'] = 'C'  # for uniformity of error msg
    >>> err = check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=subprocess.STDOUT)
    >>> err.strip().endswith("No such file or directory")
    True
    """

    if sys.version >= (2, 7):
        return subprocess.check_output(*popenargs, **kwargs)
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')

    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        # in python 2.6, CalledProcessError.__init__ does not have output kwarg
        exc = subprocess.CalledProcessError(retcode, cmd)
        exc.output = output
        raise exc
    return output


def total_seconds(td):
    """Uniformity backport of :meth:`datetime.timedelta.total_seconds``

    :param td: a :class:`datetime.timedelta` instance
    :returns: the number of seconds in ``tdelta``

    The implementation for Python < 2.7 is taken from the
    `standard library documentation
    <https://docs.python.org/2.7/library/datetime.html>`_
    """
    if sys.version_info >= (2, 7):
        return td.total_seconds()

    return ((td.microseconds +
             (td.seconds + td.days * 24 * 3600) * 1e6) / 10**6)
