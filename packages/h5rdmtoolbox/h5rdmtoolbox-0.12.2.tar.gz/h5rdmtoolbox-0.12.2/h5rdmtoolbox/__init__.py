"""h5rdtoolbox repository"""
import atexit
import pathlib
# noinspection PyUnresolvedReferences
import pint_xarray
import shutil
import xarray as xr
from typing import Union, Callable

from h5rdmtoolbox._cfg import set_config, get_config, get_ureg

pint_xarray.unit_registry = get_ureg()

from . import conventions
from .conventions.core import Convention
from . import plotting
from . import wrapper
from ._user import UserDir
from ._version import __version__
from . import database
from . import utils
from .wrapper.core import lower, Lower, File, Group, Dataset
from . import errors

from .wrapper.accessory import register_special_dataset

name = 'h5rdmtoolbox'
__this_dir__ = pathlib.Path(__file__).parent
__author__ = 'Matthias Probst'
__author_orcid__ = 'https://orcid.org/0000-0001-8729-0482'

logger = utils.create_tbx_logger('h5rdmtoolbox')

logger.setLevel(get_config()['init_logger_level'])

cv_h5py = conventions.Convention('h5py',
                                 contact=__author_orcid__)
cv_h5py.register()

# cv_h5tbx = conventions.Convention.from_yaml(__this_dir__ / 'data/h5tbx_convention.yaml')

use = conventions.core.use
use(None)


class FileDB:
    """User-friendly interface to database.Folder, database.File or database.Files"""

    def __new__(cls, path, rec=False, **kwargs):
        if isinstance(path, (list, tuple)):
            filenames = []
            for p in [pathlib.Path(_p) for _p in path]:
                if p.is_file():
                    filenames.append(p)
                elif p.is_dir():
                    if rec:
                        for f in p.rglob('*.hdf'):
                            filenames.append(f)
                    else:
                        for f in p.glob('*.hdf'):
                            filenames.append(f)
            return database.Files(filenames, **kwargs)

        path = pathlib.Path(path)
        if path.is_dir():
            return database.Folder(path, rec=rec, **kwargs)
        return database.File(path, **kwargs)


def guess_filename(func):
    """wrapper to guess the filename from the first argument"""

    def wrapper(hdf_filename, *args, **kwargs):
        if not isinstance(hdf_filename, (str, pathlib.Path)):
            if hasattr(hdf_filename, 'hdf_filename'):
                hdf_filename = hdf_filename.hdf_filename
            else:
                raise TypeError(f'Expected str or pathlib.Path, got {type(hdf_filename)}')
        return func(hdf_filename, *args, **kwargs)

    return wrapper


@guess_filename
def find(hdf_filename, *args, **kwargs):
    """Opens file with `FileDB` and calls `find()` on the root group"""
    return FileDB(hdf_filename).find(*args, **kwargs)


@guess_filename
def find_one(hdf_filename, *args, **kwargs):
    """Opens file with `FileDB` and calls `find_one()` on the root group"""
    return FileDB(hdf_filename).find_one(*args, **kwargs)


@guess_filename
def distinct(hdf_filename, key, objfilter=None):
    """Opens file and calls `distinct()` on the root group"""
    with File(hdf_filename) as h5:
        return h5.distinct(key, objfilter)


def dump(src: Union[str, File, pathlib.Path]) -> None:
    """Call h5.dump() on the provided HDF5 file

    Parameters
    ----------
    src : str, File, pathlib.Path
        the HDF5 file or filename to dump. An object which has a hdf_filename attribute can also be provided.
    """
    if isinstance(src, File):
        with File(src.hdf_filename) as h5:
            return h5.dump()

    if isinstance(src, (str, pathlib.Path)):
        pass
    else:
        if hasattr(src, 'hdf_filename'):
            src = src.hdf_filename

    with File(src) as h5:
        return h5.dump()


def dumps(src: Union[str, File, pathlib.Path]):
    """Call h5.dumps() on the provided HDF5 file

    Parameters
    ----------
    src : str, File, pathlib.Path
        the HDF5 file or filename to dump. An object which has a hdf_filename attribute can also be provided.
    """
    if isinstance(src, File):
        with File(src.hdf_filename) as h5:
            return h5.dumps()

    if isinstance(src, (str, pathlib.Path)):
        pass
    else:
        if hasattr(src, 'hdf_filename'):
            src = src.hdf_filename

    with File(src) as h5:
        return h5.dumps()


def register_dataset_decoder(decoder: Callable, decoder_name: str = None, overwrite: bool = False):
    """A decoder function takes a xarray.DataArray and a dataset as input and returns a xarray.DataArray
    It is called after the dataset is loaded into memory and before being returned to the user. Be careful:
    Multiple decoders can be registered and they are called in the order of registration. Hence, your decoder
    may behave unexpectedly!
    """
    from .wrapper import ds_decoder
    if decoder_name is None:
        decoder_name = decoder.__name__
    registered_decorators = ds_decoder.registered_dataset_decoders
    if decoder_name in registered_decorators or decoder in registered_decorators.values():
        if not overwrite:
            raise ValueError(f'decoder "{decoder_name}" already registered. Name and function must be unique.')
    ds_decoder.registered_dataset_decoders[decoder_name] = decoder


atexit_verbose = False


@atexit.register
def clean_temp_data(full: bool = False):
    """cleaning up the tmp directory"""
    from ._user import _user_root_dir

    failed_dirs = []
    failed_dirs_file = UserDir['tmp'] / 'failed.txt'
    if full:
        root_tmp = _user_root_dir / 'tmp'
        if root_tmp.exists():
            try:
                shutil.rmtree(root_tmp)
                root_tmp.mkdir(exist_ok=True, parents=True)
            except PermissionError as e:
                print(f'removing tmp folder "{root_tmp}" failed due to "{e}".')
        return

    for _tmp_session_dir in [UserDir['tmp'], ]:
        if atexit_verbose:
            print(f'cleaning up tmp directory "{_tmp_session_dir}"')
        if _tmp_session_dir.exists():
            try:
                if atexit_verbose:
                    print(f'try deleting tmp in session dir: {_tmp_session_dir}')
                shutil.rmtree(_tmp_session_dir)
            except PermissionError as e:
                if atexit_verbose:
                    print(f'[!] failed deleting tmp session dir: {_tmp_session_dir}')
                failed_dirs.append(UserDir['tmp'])
                if atexit_verbose:
                    print(f'removing tmp folder "{_tmp_session_dir}" failed due to "{e}". Best is you '
                          f'manually delete the directory.')
            finally:
                lines = []
                if failed_dirs_file.exists():
                    with open(failed_dirs_file, 'r') as f:
                        lines = f.readlines()
                        for line in lines:
                            try:
                                shutil.rmtree(line.strip())
                            except Exception:
                                if pathlib.Path(line).exists():
                                    failed_dirs.append(line)

                if lines or failed_dirs:
                    with open(failed_dirs_file, 'w') as f:
                        for fd in failed_dirs:
                            f.writelines(f'{fd}\n')
                else:
                    failed_dirs_file.unlink(missing_ok=True)
        else:
            logger.debug(f'No user tmp dir not found: {_tmp_session_dir}')


xr.set_options(display_expand_data=False)

__all__ = ('__version__', '__author__', '__author_orcid__', 'UserDir', 'use',
           'File', 'Group', 'Dataset',
           'dump', 'dumps', 'cv_h5py', 'lower', 'Lower',
           'set_config', 'get_config', 'get_ureg',
           'Convention')
