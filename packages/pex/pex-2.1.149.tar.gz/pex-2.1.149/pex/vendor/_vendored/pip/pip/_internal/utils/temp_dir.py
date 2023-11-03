from __future__ import absolute_import

import errno
import itertools
import logging
import os.path
import tempfile
from contextlib import contextmanager

from pip._vendor.contextlib2 import ExitStack
from pip._vendor.six import ensure_text

from pip._internal.utils.compat import WINDOWS
from pip._internal.utils.misc import enum, rmtree
from pip._internal.utils.typing import MYPY_CHECK_RUNNING

if MYPY_CHECK_RUNNING:
    from typing import Any, Dict, Iterator, Optional, TypeVar, Union

    _T = TypeVar('_T', bound='TempDirectory')


logger = logging.getLogger(__name__)


# Kinds of temporary directories. Only needed for ones that are
# globally-managed.
tempdir_kinds = enum(
    BUILD_ENV="build-env",
    EPHEM_WHEEL_CACHE="ephem-wheel-cache",
    REQ_BUILD="req-build",
)


_tempdir_manager = None  # type: Optional[ExitStack]


@contextmanager
def global_tempdir_manager():
    # type: () -> Iterator[None]
    global _tempdir_manager
    with ExitStack() as stack:
        old_tempdir_manager, _tempdir_manager = _tempdir_manager, stack
        try:
            yield
        finally:
            _tempdir_manager = old_tempdir_manager


class TempDirectoryTypeRegistry(object):
    """Manages temp directory behavior
    """

    def __init__(self):
        # type: () -> None
        self._should_delete = {}  # type: Dict[str, bool]

    def set_delete(self, kind, value):
        # type: (str, bool) -> None
        """Indicate whether a TempDirectory of the given kind should be
        auto-deleted.
        """
        self._should_delete[kind] = value

    def get_delete(self, kind):
        # type: (str) -> bool
        """Get configured auto-delete flag for a given TempDirectory type,
        default True.
        """
        return self._should_delete.get(kind, True)


_tempdir_registry = None  # type: Optional[TempDirectoryTypeRegistry]


@contextmanager
def tempdir_registry():
    # type: () -> Iterator[TempDirectoryTypeRegistry]
    """Provides a scoped global tempdir registry that can be used to dictate
    whether directories should be deleted.
    """
    global _tempdir_registry
    old_tempdir_registry = _tempdir_registry
    _tempdir_registry = TempDirectoryTypeRegistry()
    try:
        yield _tempdir_registry
    finally:
        _tempdir_registry = old_tempdir_registry


class _Default(object):
    pass


_default = _Default()


class TempDirectory(object):
    """Helper class that owns and cleans up a temporary directory.

    This class can be used as a context manager or as an OO representation of a
    temporary directory.

    Attributes:
        path
            Location to the created temporary directory
        delete
            Whether the directory should be deleted when exiting
            (when used as a contextmanager)

    Methods:
        cleanup()
            Deletes the temporary directory

    When used as a context manager, if the delete attribute is True, on
    exiting the context the temporary directory is deleted.
    """

    def __init__(
        self,
        path=None,    # type: Optional[str]
        delete=_default,  # type: Union[bool, None, _Default]
        kind="temp",  # type: str
        globally_managed=False,  # type: bool
    ):
        super(TempDirectory, self).__init__()

        if delete is _default:
            if path is not None:
                # If we were given an explicit directory, resolve delete option
                # now.
                delete = False
            else:
                # Otherwise, we wait until cleanup and see what
                # tempdir_registry says.
                delete = None

        # The only time we specify path is in for editables where it
        # is the value of the --src option.
        if path is None:
            path = self._create(kind)

        self._path = path
        self._deleted = False
        self.delete = delete
        self.kind = kind

        if globally_managed:
            assert _tempdir_manager is not None
            _tempdir_manager.enter_context(self)

    @property
    def path(self):
        # type: () -> str
        assert not self._deleted, (
            "Attempted to access deleted path: {}".format(self._path)
        )
        return self._path

    def __repr__(self):
        # type: () -> str
        return "<{} {!r}>".format(self.__class__.__name__, self.path)

    def __enter__(self):
        # type: (_T) -> _T
        return self

    def __exit__(self, exc, value, tb):
        # type: (Any, Any, Any) -> None
        if self.delete is not None:
            delete = self.delete
        elif _tempdir_registry:
            delete = _tempdir_registry.get_delete(self.kind)
        else:
            delete = True

        if delete:
            self.cleanup()

    def _create(self, kind):
        # type: (str) -> str
        """Create a temporary directory and store its path in self.path
        """
        # We realpath here because some systems have their default tmpdir
        # symlinked to another directory.  This tends to confuse build
        # scripts, so we canonicalize the path by traversing potential
        # symlinks here.
        path = os.path.realpath(
            tempfile.mkdtemp(prefix="pip-{}-".format(kind))
        )
        logger.debug("Created temporary directory: %s", path)
        return path

    def cleanup(self):
        # type: () -> None
        """Remove the temporary directory created and reset state
        """
        self._deleted = True
        if not os.path.exists(self._path):
            return
        # Make sure to pass unicode on Python 2 to make the contents also
        # use unicode, ensuring non-ASCII names and can be represented.
        # This is only done on Windows because POSIX platforms use bytes
        # natively for paths, and the bytes-text conversion omission avoids
        # errors caused by the environment configuring encodings incorrectly.
        if WINDOWS:
            rmtree(ensure_text(self._path))
        else:
            rmtree(self._path)


class AdjacentTempDirectory(TempDirectory):
    """Helper class that creates a temporary directory adjacent to a real one.

    Attributes:
        original
            The original directory to create a temp directory for.
        path
            After calling create() or entering, contains the full
            path to the temporary directory.
        delete
            Whether the directory should be deleted when exiting
            (when used as a contextmanager)

    """
    # The characters that may be used to name the temp directory
    # We always prepend a ~ and then rotate through these until
    # a usable name is found.
    # pkg_resources raises a different error for .dist-info folder
    # with leading '-' and invalid metadata
    LEADING_CHARS = "-~.=%0123456789"

    def __init__(self, original, delete=None):
        # type: (str, Optional[bool]) -> None
        self.original = original.rstrip('/\\')
        super(AdjacentTempDirectory, self).__init__(delete=delete)

    @classmethod
    def _generate_names(cls, name):
        # type: (str) -> Iterator[str]
        """Generates a series of temporary names.

        The algorithm replaces the leading characters in the name
        with ones that are valid filesystem characters, but are not
        valid package names (for both Python and pip definitions of
        package).
        """
        for i in range(1, len(name)):
            for candidate in itertools.combinations_with_replacement(
                    cls.LEADING_CHARS, i - 1):
                new_name = '~' + ''.join(candidate) + name[i:]
                if new_name != name:
                    yield new_name

        # If we make it this far, we will have to make a longer name
        for i in range(len(cls.LEADING_CHARS)):
            for candidate in itertools.combinations_with_replacement(
                    cls.LEADING_CHARS, i):
                new_name = '~' + ''.join(candidate) + name
                if new_name != name:
                    yield new_name

    def _create(self, kind):
        # type: (str) -> str
        root, name = os.path.split(self.original)
        for candidate in self._generate_names(name):
            path = os.path.join(root, candidate)
            try:
                os.mkdir(path)
            except OSError as ex:
                # Continue if the name exists already
                if ex.errno != errno.EEXIST:
                    raise
            else:
                path = os.path.realpath(path)
                break
        else:
            # Final fallback on the default behavior.
            path = os.path.realpath(
                tempfile.mkdtemp(prefix="pip-{}-".format(kind))
            )

        logger.debug("Created temporary directory: %s", path)
        return path
