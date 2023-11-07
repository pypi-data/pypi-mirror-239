"""lazy objects. user can work with datasets and groups without having to open the file him/her-self"""
import h5py
import pathlib
from typing import Union, List, Dict


class LGroup:
    """Lazy Group"""

    def __init__(self, obj: h5py.Group):
        self.filename = pathlib.Path(obj.file.filename)
        if isinstance(obj.attrs, h5py._hl.attrs.AttributeManager):
            self._attrs = dict(obj.attrs)
        else:
            self._attrs = dict(obj.attrs.raw)

        for k, v in _get_dataset_properties(obj, ('file', 'name',)).items():
            setattr(self, k, v)

    def __repr__(self):
        return f'<LGroup "{self.name}" in "{self.filename}">'

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name and self.filename == other.filename and self.attrs == other.attrs

    def __enter__(self):
        from .. import File
        self._file = File(self.filename)
        return self._file[self.name]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    @property
    def basename(self) -> str:
        """Return the basename of the object"""
        return self.name.rsplit('/', 1)[1]

    @property
    def parentname(self) -> str:
        """Return the parent name of the object path"""
        return self.name.rsplit('/', 1)[0]

    @property
    def parentnames(self) -> List[str]:
        """Return the parent names of the object path"""
        return self.parentname.split('/')[1:]  # first is '', so skip

    @property
    def attrs(self) -> Dict:
        """Return the attributes of the group as a LAttributeManager object"""
        return self._attrs

    def find(self, flt: Union[Dict, str],
             objfilter: Union[str, h5py.Dataset, h5py.Group, None] = None,
             rec: bool = True,
             ignore_attribute_error: bool = False):
        """Find"""
        from .file import find as _find
        with self as obj:
            if isinstance(obj, h5py.Dataset):
                return [lazy(i) for i in _find(obj, flt, objfilter, find_one=False, recursive=False,
                                               ignore_attribute_error=ignore_attribute_error)]
            return [lazy(i) for i in _find(obj, flt, objfilter, find_one=False, recursive=rec,
                      ignore_attribute_error=ignore_attribute_error)]

    def find_one(self,
                 flt: Union[Dict, str],
                 objfilter=None,
                 rec: bool = True,
                 ignore_attribute_error: bool = False):
        """Find one occurrence"""
        from .file import find as _find
        with self as obj:
            return lazy(_find(obj, flt, objfilter, find_one=True, recursive=rec,
                              ignore_attribute_error=ignore_attribute_error))


class LDataset(LGroup):
    """Lazy Dataset"""

    def __init__(self, obj: h5py.Dataset):
        super().__init__(obj)

        keys = ("name", "ndim", "shape", "dtype", "size", "chunks",
                "compression", "compression_opts",
                "shuffle", "fletcher32", "maxshape",
                "fillvalue", "scaleoffset", "external",
                "file")
        for k, v in _get_dataset_properties(obj, keys).items():
            setattr(self, k, v)
        self._file = None

    def __repr__(self):
        attrs_str = ', '.join({f'{k}={v}' for k, v in self.attrs.items() if not k.isupper()})
        return f'<LDataset "{self.name}" in "{self.filename}" attrs=({attrs_str})>'

    def __getitem__(self, item):
        from .. import File
        with File(self.filename, mode='r') as h5:
            return h5[self.name][item]

    def coords(self):
        from .. import File
        with File(self.filename) as h5:
            return h5[self.name].coords()

    def isel(self, **indexers):
        from .. import File
        with File(self.filename) as h5:
            return h5[self.name].isel(**indexers)

    def sel(self, **coords):
        from .. import File
        with File(self.filename) as h5:
            return h5[self.name].sel(**coords)

    def find(self, flt: Union[Dict, str],
             objfilter: Union[str, h5py.Dataset, h5py.Group, None] = None,
             ignore_attribute_error: bool = False):
        """Find"""
        return super().find(flt, objfilter, rec=False, ignore_attribute_error=ignore_attribute_error)

    def find_one(self,
                 flt: Union[Dict, str],
                 objfilter=None,
                 ignore_attribute_error: bool = False):
        """Find one occurrence"""
        return super().find_one(flt, objfilter, rec=False, ignore_attribute_error=ignore_attribute_error)


def _get_dataset_properties(h5obj, keys):
    return {k: getattr(h5obj, k) for k in keys}


def lazy(h5obj) -> Union[None, LDataset, LGroup]:
    """Make a lazy object from a h5py object"""
    if h5obj is None:
        return None
    if isinstance(h5obj, h5py.Group):
        return LGroup(h5obj)
    elif isinstance(h5obj, h5py.Dataset):
        return LDataset(h5obj)
    elif isinstance(h5obj, (tuple, list)):
        # expecting h5obj=(filename, obj_name)
        with h5py.File(h5obj[0]) as h5:
            return lazy(h5[h5obj[1]])
    raise TypeError(f'Cannot make {type(h5obj)} lazy')
