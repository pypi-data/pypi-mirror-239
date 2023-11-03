#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import time
from distutils.version import StrictVersion as Version
from operator import mul
from functools import reduce
from itertools import product, islice
from PyFiberModes.fiber import Fiber
from PyFiberModes.slrc import SLRC
from PyFiberModes import material as materialmod
from PyFiberModes.fiber import geometry as geometrymod
from PyFiberModes.solver.solver import FiberSolver
from PyFiberModes.material.compmaterial import CompMaterial


__version__ = "0.0.1"


class LayerProxy(object):
    def __init__(self, layer):
        self._layer = layer

    def __getattr__(self, name):
        if name in self._layer:
            return self._layer[name]
        else:
            raise AttributeError

    def __setattr__(self, name, value):
        if name == "_layer":
            super().__setattr__(name, value)
        elif name == "material":
            self._material(value)
        elif name == "type":
            self._type(value)
        elif name in self._layer:
            self._layer[name] = value
        else:
            super().__setattr__(name, value)

    def __getitem__(self, name):
        return self._layer[name]

    def __setitem__(self, name, value):
        if name in self._layer:
            self._layer[name] = value
        else:
            raise KeyError

    def _material(self, value):
        if value != self.material:
            self._layer["material"] = value
            self._layer["mparams"] = [0] * materialmod.__dict__[value].nparams

    def _type(self, value):
        self._layer["type"] = value
        dp = geometrymod.__dict__[value].DEFAULT_PARAMS
        tp = self._layer["tparams"]
        for i in range(len(tp) - 1, len(dp)):
            tp.append(dp[i])
        # print("_type", value, self._layer["tparams"])

    @property
    def radius(self):
        return self._layer["tparams"][0]

    @radius.setter
    def radius(self, value):
        self._layer["tparams"][0] = value


class LayersProxy(object):

    def __init__(self, factory):
        self.factory = factory

    def __len__(self):
        return len(self.factory._fibers["layers"])

    def __getitem__(self, index):
        return LayerProxy(self.factory._fibers["layers"][index])


class FiberFactory(object):

    """FiberFactory is used to instantiate a
    :py:class:`~PyFiberModes.fiber.fiber.Fiber` or a series of
    Fiber objects.

    It can read fiber definition from json file, and write it back.
    Convenient functions are available to set fiber parameters, and to
    iterate through fiber objects.

    All fibers build from a given factory share the same number
    of layers, the same kind of geometries, and the same
    materials. However, parameters can vary.

    Args:
        filename: Name of fiber file to load, or None to construct
                  empty Fiberfactory object.

    """

    def __init__(self, filename=None):
        self._fibers = {
            "version": __version__,
            "name": "",
            "description": "",
            "author": "",
            "creation_date": time.time(),
            "time_stamp": time.time(),
            "layers": []
        }
        if filename:
            with open(filename, 'r') as f:
                self.load(f)

        self._Neff = None
        self._Cutoff = None

    @property
    def name(self):
        """Name of the fiber.

        The name simply is a string identifier.

        """
        return self._fibers["name"]

    @name.setter
    def name(self, value):
        self._fibers["name"] = value

    @property
    def author(self):
        """Author of the fiber definition.

        Used as a reference.

        """
        return self._fibers["author"]

    @author.setter
    def author(self, value):
        self._fibers["author"] = value

    @property
    def description(self):
        """Description of the fiber build form this factory.

        """
        return self._fibers["description"]

    @description.setter
    def description(self, value):
        self._fibers["description"] = value

    @property
    def creation_date(self):
        """Creation date of this factory.

        """
        return self._fibers["creation_date"]

    @property
    def time_stamp(self):
        """Timestamp (modification date).

        This is automatically updated when the fiber factory is saved.

        """
        return self._fibers["time_stamp"]

    @property
    def layers(self):
        """
        List of layers.

        """
        return LayersProxy(self)

    def add_layer(self,
            pos: int = None,
            name: str = "",
            radius: float = 0,
            material: str = "Fixed",
            geometry: str = "StepIndex",
            **kwargs):
        """Insert a new layer in the factory.

        Args:
            pos(int or None): Position the the inserted layer.
                              By default, new layer is inserted at the end.
            name(string): Layer name.
            radius(float): Radius of the layer (in meters).
            material(string): Name of the Material (default: Fixed)
            geometry(string): Name of the Geometry (default: StepIndex)
            tparams(list): Parameters for the Geometry
            mparams(list): Parameters for the Material
            index(float): Index of the layer (for Fixed Material, otherwise
                          parameters are calculated to give this index)
            x(float): Molar concentration for the Material
            wl(float): Wavelength (in m) used for calculating parameters
                       (when index is given)

        Please note that some parameters are specific to some
        :py:mod:`~PyFiberModes.fiber.material` or
        :py:mod:`~PyFiberModes.fiber.geometry`:

        :py:class:`~PyFiberModes.fiber.material.fixed.Fixed` material
            **index** is required. **mparams** is ignored.

        :py:class:`~PyFiberModes.fiber.material.compmaterial.CompMaterial` \
(:py:class:`~PyFiberModes.fiber.material.sio2geo2.SiO2GeO2`)
            You can specify either **x** or **index** and **wl**.
            **mparams** is ignored.

        """
        if pos is None:
            pos = len(self._fibers["layers"])
        layer = {
            "name": name,
            "type": geometry,
            "tparams": [radius] + kwargs.pop("tparams", []),
            "material": material,
            "mparams": kwargs.pop("mparams", []),
        }
        if material == "Fixed":
            index = kwargs.pop("index", 1.444)
            layer["mparams"] = [index]
        else:
            Mat = materialmod.__dict__[material]
            if issubclass(Mat, CompMaterial):
                if "x" in kwargs:
                    x = kwargs.pop("x")
                elif "index" in kwargs and "wl" in kwargs:
                    x = Mat.xFromN(kwargs.pop("wl"), kwargs.pop("index"))
                else:
                    x = 0
                layer["mparams"] = [x]

        assert len(kwargs) == 0, f"Unknown arguments {kwargs}"

        self._fibers["layers"].insert(pos, layer)

    def remove_layer(self, layer_idx=-1):
        """
        Remove layer at given position (default: last layer)

        Args:
            pos(int): Index of the layer to remove.

        """
        self._fibers["layers"].pop(layer_idx)

    def dump(self, file_pointer, **kwargs):
        """Dumps fiber factory to a file.

        Args:
            fp: File pointer.
            **kwargs: See json.dumps

        """
        file_pointer.write(self.dumps(**kwargs))

    def dumps(self, **kwargs):
        """Dumps fiber factory to a string.

        Args:
            **kwargs: See json.dumps.

        Returns:
            JSON string.

        """
        self._fibers["time_stamp"] = time.time()
        return json.dumps(self._fibers, **kwargs)

    def load(self, fp, **kwargs):
        """Loads fiber factory from file.

        File contents is validated when loaded, and version is
        upgraded is needed.

        Args:
            fp: File pointer.
            **kwargs: See json.loads

        """
        self.loads(fp.read(), **kwargs)

    def loads(self, s, **kwargs):
        """Loads fiber factory from JSON string.

        String contents is validated when loaded, and version is
        upgraded is needed.

        Args:
            s(string): JSON string
            **kwargs: See json.loads

        """
        fibers = json.loads(s, **kwargs)
        self.validate(fibers)
        self._fibers = fibers

    def validate(self, obj):
        """Validates that obj is a valid fiber factory.

        Args:
            obj(dict): Dict of fiber factory parameters.

        Raises:
            ValueError: Object does not validate.

        """
        for key in ("version", "name", "description",
                    "author", "creation_date", "time_stamp", "layers"):
            if key not in obj.keys():
                raise ValueError(
                    f"Missing '{key}' parameter"
                )

        if Version(obj["version"]) > Version(__version__):
            raise ValueError(
                "Version of loaded object is higher that version of current library"
            )
        elif Version(obj["version"]) < Version(__version__):
            self._upgrade(obj)

        for layernum, layer in enumerate(obj["layers"], 1):
            self._validateLayer(layer, layernum)

    def _validateLayer(self, layer, layernum):
        for key in ("name", "type", "tparams", "material", "mparams"):
            if key not in layer.keys():
                raise ValueError(f"Missing '{key}' parameter for layer {layernum}")

    def _upgrade(self, obj):
        obj["version"] = __version__

    def __iter__(self):
        self._buildFiberList()
        g = product(*(range(i) for i in self._nitems))
        return (self._buildFiber(i) for i in g)

    def __len__(self):
        if not self.layers:
            return 0
        self._buildFiberList()
        return reduce(mul, self._nitems)

    def __getitem__(self, key):
        self._buildFiberList()
        return self._buildFiber(self._getIndexes(key))

    def _buildFiberList(self):
        self._nitems = []
        for layer in self._fibers["layers"]:
            for key in ("tparams", "mparams"):
                for tp in layer[key]:
                    self._nitems.append(len(SLRC(tp)))

    def _getIndexes(self, index):
        """
        Get list of indexes from a single index.
        """
        g = product(*(range(i) for i in self._nitems))

        return next(islice(g, index, None))

    def setSolvers(self, Cutoff=None, Neff=None):
        assert Cutoff is None or issubclass(Cutoff, FiberSolver)
        assert Neff is None or issubclass(Neff, FiberSolver)
        self._Cutoff = Cutoff
        self._Neff = Neff

    def _buildFiber(self, indexes):
        """
        Build Fiber object from list of indexes
        """

        r, f, fp, m, mp, names = [], [], [], [], [], []

        # Get parameters for selected fiber
        ii = 0
        for i, layer in enumerate(self._fibers["layers"], 1):
            name = layer["name"] if layer["name"] else f"layer {i + 1}"
            names.append(name)

            if i < len(self._fibers["layers"]):
                rr = SLRC(layer["tparams"][0])
                rr.codeParams = ["r", "fp", "mp"]
                r.append(rr[indexes[ii]])
            ii += 1  # we count radius of cladding, even if we don't use it

            f.append(layer["type"])
            fp_ = []
            for p in layer["tparams"][1:]:
                ff = SLRC(p)
                ff.codeParams = ["r", "fp", "mp"]
                fp_.append(ff[indexes[ii]])
                ii += 1
            fp.append(fp_)

            m.append(layer["material"])
            mp_ = []
            for p in layer["mparams"]:
                mm = SLRC(p)
                mm.codeParams = ["r", "fp", "mp"]
                mp_.append(mm[indexes[ii]])
                ii += 1
            mp.append(mp_)

        # Execute code parts
        for i, p in enumerate(r):
            if callable(p):
                r[i] = float(p(r, fp, mp))
        for i, pp in enumerate(fp):
            for j, p in enumerate(pp):
                if callable(p):
                    fp[i][j] = float(p(r, fp, mp))
            fp[i] = tuple(fp[i])
        for i, pp in enumerate(mp):
            for j, p in enumerate(pp):
                if callable(p):
                    mp[i][j] = float(p(r, fp, mp))
            mp[i] = tuple(mp[i])

        # Remove unneeded layers
        i = len(m) - 2
        while i >= 0 and len(m) > 1:
            if (r[i] == 0 or
                    (i > 0 and r[i] <= r[i - 1]) or
                    (f[i] == f[i + 1] == 'StepIndex' and
                     m[i] == m[i + 1] and
                     mp[i] == mp[i + 1])):
                del r[i]
                del f[i]
                del fp[i]
                del m[i]
                del mp[i]
                del names[i]
            i -= 1

        fiber = Fiber(
            layer_radius=r,
            layer_types=f,
            fp=fp,
            material_parameters=m,
            layer_indexes=mp,
            layer_names=names,
            cutoff_solver=self._Cutoff,
            neff_solver=self._Neff
        )

        return fiber
