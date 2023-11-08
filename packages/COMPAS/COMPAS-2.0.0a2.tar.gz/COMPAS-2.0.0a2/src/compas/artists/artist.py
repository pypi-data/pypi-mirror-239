from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import inspect
from abc import abstractmethod
from collections import defaultdict

import compas
from compas.artists.exceptions import DataArtistNotRegistered
from compas.artists.exceptions import NoArtistContextError
from compas.plugins import PluginValidator
from compas.plugins import pluggable

from .descriptors.protocol import DescriptorProtocol


@pluggable(category="drawing-utils")
def clear():
    raise NotImplementedError


@pluggable(category="drawing-utils")
def redraw():
    raise NotImplementedError


@pluggable(category="factories", selector="collect_all")
def register_artists():
    """Registers artists available in the current context."""
    raise NotImplementedError


def is_viewer_open():
    """Returns True if an instance of the compas_view2 App is available.

    Returns
    -------
    bool

    """
    # TODO: implement [without introducing compas_view2 as a dependency..?]
    # make the viewer app a singleton
    # check for the exitence of an instance of the singleton
    # if the instance exists, return True
    # in this case, the viewer is the current context
    # to do this without introducing compas_view2 as a dependency,
    # creating the singleton instance should modify a class attribute of the Artist
    # (or potentially a module level attribute of compas itself)
    return False


def _detect_current_context():
    """Chooses an appropriate context depending on available contexts and open instances. with the following priority:
    1. Viewer
    2. Plotter
    3. Rhino / GH - checked explicitly since Artists for both get registered when code is run from either.
    4. Other

    Returns
    -------
    str
        Name of an available context, used as key in :attr:`Artist.ITEM_ARTIST`

    """
    if is_viewer_open():
        return "Viewer"
    if compas.is_grasshopper():
        return "Grasshopper"
    if compas.is_rhino():
        return "Rhino"
    if compas.is_blender():
        return "Blender"
    other_contexts = [v for v in Artist.ITEM_ARTIST.keys()]
    if other_contexts:
        return other_contexts[0]
    raise NoArtistContextError()


def _get_artist_cls(data, **kwargs):
    # in any case user gets to override the choice
    context_name = kwargs.get("context") or _detect_current_context()

    dtype = type(data)
    cls = None

    if "artist_type" in kwargs:
        cls = kwargs["artist_type"]
    else:
        context = Artist.ITEM_ARTIST[context_name]

        for type_ in inspect.getmro(dtype):
            cls = context.get(type_, None)
            if cls is not None:
                break

    if cls is None:
        raise DataArtistNotRegistered(
            "No artist is registered for this data type: {} in this context: {}".format(dtype, context_name)
        )

    return cls


class Artist(object):
    """Base class for all artists.

    Parameters
    ----------
    item : Any
        The item which should be visualized using the created Artist.
    context : str, optional
        Explicit context to pick the Artist from.
        If not specified, an attempt will be made to automatically detect the appropriate context.

    Attributes
    ----------
    ITEM_ARTIST : dict[str, dict[Type[:class:`~compas.data.Data`], Type[:class:`~compas.artists.Artist`]]]
        Dictionary mapping data types to the corresponding artists types per visualization context.

    """

    # add this to support the descriptor protocol vor Python versions below 3.6
    __metaclass__ = DescriptorProtocol

    __ARTISTS_REGISTERED = False

    ITEM_ARTIST = defaultdict(dict)

    def __new__(cls, item, **kwargs):
        if not Artist.__ARTISTS_REGISTERED:
            cls.register_artists()
            Artist.__ARTISTS_REGISTERED = True

        if item is None:
            raise ValueError(
                "Cannot create an artist for None. Please ensure you pass a instance of a supported class."
            )

        cls = _get_artist_cls(item, **kwargs)
        PluginValidator.ensure_implementations(cls)
        return super(Artist, cls).__new__(cls)

    def __init__(self, item, **kwargs):
        self._item = item
        self._transformation = None

    @property
    def transformation(self):
        """The transformation matrix of the artist.

        Returns
        -------
        :class:`Transformation` or None
            The transformation matrix.

        """
        return self._transformation

    @transformation.setter
    def transformation(self, transformation):
        self._transformation = transformation

    @staticmethod
    def build(item, **kwargs):
        """Build an artist corresponding to the item type.

        Parameters
        ----------
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`~compas.artists.Artist`
            An artist of the type matching the provided item according to the item-artist map :attr:`~Artist.ITEM_ARTIST`.
            The map is created by registering item-artist type pairs using :meth:`~Artist.register`.

        """
        artist_type = _get_artist_cls(item, **kwargs)
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def build_as(item, artist_type, **kwargs):
        """Build an artist with the given type.

        Parameters
        ----------
        artist_type : :class:`~compas.artists.Artist`
        **kwargs : dict[str, Any], optional
            The keyword arguments (kwargs) collected in a dict.
            For relevant options, see the parameter lists of the matching artist type.

        Returns
        -------
        :class:`~compas.artists.Artist`
            An artist of the given type.

        """
        artist = artist_type(item, **kwargs)
        return artist

    @staticmethod
    def clear():
        """Clear all objects from the view.

        Returns
        -------
        None

        """
        return clear()

    @staticmethod
    def redraw():
        """Redraw the view.

        Returns
        -------
        None

        """
        return redraw()

    @staticmethod
    def register_artists():
        """Register Artists using available plugins.

        Returns
        -------
        List[str]
            List containing names of discovered Artist plugins.

        """
        return register_artists()

    @staticmethod
    def register(item_type, artist_type, context=None):
        """Register an artist type to a data type.

        Parameters
        ----------
        item_type : :class:`~compas.data.Data`
            The type of data item.
        artist_type : :class:`~compas.artists.Artist`
            The type of the corresponding/compatible artist.
        context : Literal['Viewer', 'Rhino', 'Grasshopper', 'Blender'], optional
            The visualization context in which the pair should be registered.

        Returns
        -------
        None

        """
        Artist.ITEM_ARTIST[context][item_type] = artist_type

    @abstractmethod
    def draw(self):
        """The main drawing method."""
        raise NotImplementedError

    @staticmethod
    def draw_collection(collection):
        """Drawing method for drawing an entire collection of objects."""
        raise NotImplementedError
