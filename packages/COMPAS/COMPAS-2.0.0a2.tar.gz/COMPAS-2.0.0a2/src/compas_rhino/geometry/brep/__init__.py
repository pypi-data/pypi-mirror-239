from compas.plugins import plugin
from .brep import RhinoBrep
import Rhino


@plugin(category="factories", requires=["Rhino"])
def new_brep(*args, **kwargs):
    # Note: this is called inside Brep.__new__, thus Brep.__init__ will be ran by the interpreter
    # upon returning from __new__. This means any fully initialized instance returned here will be overwritten!
    return object.__new__(RhinoBrep, Rhino.Geometry.Brep())


@plugin(category="factories", requires=["Rhino"])
def from_native(*args, **kwargs):
    return RhinoBrep.from_native(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_box(*args, **kwargs):
    return RhinoBrep.from_box(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_cylinder(*args, **kwargs):
    return RhinoBrep.from_cylinder(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_sphere(*args, **kwargs):
    return RhinoBrep.from_sphere(*args, **kwargs)


@plugin(category="factories", requires=["Rhino"])
def from_mesh(*args, **kwargs):
    return RhinoBrep.from_mesh(*args, **kwargs)
