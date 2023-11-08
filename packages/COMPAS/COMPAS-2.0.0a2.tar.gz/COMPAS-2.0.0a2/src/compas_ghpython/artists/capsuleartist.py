from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class CapsuleArtist(GHArtist, GeometryArtist):
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

    def draw(self):
        """Draw the capsule associated with the artist.

        Returns
        -------
        list[:rhino:`Rhino.Geometry.Brep`]

        """
        breps = conversions.capsule_to_rhino_brep(self.geometry)

        if self.transformation:
            transformation = conversions.transformation_to_rhino(self.transformation)
            for geometry in breps:
                geometry.Transform(transformation)

        return breps
