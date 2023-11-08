from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from compas_rhino import conversions

from compas.artists import GeometryArtist
from .artist import GHArtist


class PolylineArtist(GHArtist, GeometryArtist):
    """Artist for drawing polylines.

    Parameters
    ----------
    polyline : :class:`~compas.geometry.Polyline`
        A COMPAS polyline.
    **kwargs : dict, optional
        Additional keyword arguments.

    """

    def __init__(self, polyline, **kwargs):
        super(PolylineArtist, self).__init__(geometry=polyline, **kwargs)

    def draw(self):
        """Draw the polyline.

        Returns
        -------
        :rhino:`Rhino.Geometry.PolylineCurve`.

        """
        geometry = conversions.polyline_to_rhino_curve(self.geometry)

        if self.transformation:
            geometry.Transform(conversions.transformation_to_rhino(self.transformation))

        return geometry
