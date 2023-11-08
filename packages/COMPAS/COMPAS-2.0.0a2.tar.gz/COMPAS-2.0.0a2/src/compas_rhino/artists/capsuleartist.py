from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import scriptcontext as sc  # type: ignore

from compas.artists import GeometryArtist
from compas.colors import Color
from compas_rhino.conversions import capsule_to_rhino_brep
from compas_rhino.conversions import transformation_to_rhino
from .artist import RhinoArtist
from ._helpers import attributes


class CapsuleArtist(RhinoArtist, GeometryArtist):
    """Artist for drawing capsule shapes.

    Parameters
    ----------
    capsule : :class:`~compas.geometry.Capsule`
        A COMPAS capsule.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, capsule, **kwargs):
        super(CapsuleArtist, self).__init__(geometry=capsule, **kwargs)

    def draw(self, color=None):
        """Draw the capsule associated with the artist.

        Parameters
        ----------
        color : rgb1 | rgb255 | :class:`~compas.colors.Color`, optional
            The RGB color of the capsule.

        Returns
        -------
        list[System.Guid]
            The GUIDs of the objects created in Rhino.

        """
        color = Color.coerce(color) or self.color
        attr = attributes(name=self.geometry.name, color=color, layer=self.layer)

        breps = capsule_to_rhino_brep(self.geometry)

        if self.transformation:
            transformation = transformation_to_rhino(self.transformation)
            for geometry in breps:
                geometry.Transform(transformation)

        guids = [sc.doc.Objects.AddBrep(brep, attr) for brep in breps]
        return guids
