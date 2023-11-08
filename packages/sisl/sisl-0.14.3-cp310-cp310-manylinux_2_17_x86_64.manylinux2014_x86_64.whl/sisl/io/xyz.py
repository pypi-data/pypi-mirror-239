# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
"""
Sile object for reading/writing XYZ files
"""
import numpy as np

import sisl._array as _a
from sisl import BoundaryCondition, Geometry, Lattice
from sisl._internal import set_module
from sisl.messages import deprecate_argument, warn

# Import sile objects
from ._help import header_to_dict
from ._multiple import SileBinder
from .sile import *

__all__ = ["xyzSile"]


@set_module("sisl.io")
class xyzSile(Sile):
    """XYZ file object"""

    def _parse_lattice(self, header, xyz, lattice):
        """Internal helper routine for extracting the lattice"""
        if lattice is not None:
            return lattice

        # Parse
        nsc = None
        if "nsc" in header:
            nsc = list(map(int, header.pop("nsc").split()))

        BC = BoundaryCondition
        bc = BC.UNKNOWN
        if "pbc" in header:
            bc = []
            for pbc in header.pop("pbc").split():
                if pbc == "T":
                    bc.append(BoundaryCondition.PERIODIC)
                else:
                    bc.append(BoundaryCondition.UNKNOWN)
        if "boundary_condition" in header:
            bc = []
            for b in header.pop("boundary_condition").split():
                bc.append(getattr(BC, b.upper()))
            bc = _a.arrayi(bc).reshape(3, 2)

        if "Lattice" in header:
            cell = _a.fromiterd(header.pop("Lattice").split()).reshape(3, 3)
        elif "cell" in header:
            cell = _a.fromiterd(header.pop("cell").split()).reshape(3, 3)
        else:
            cell = xyz.max(0) - xyz.min(0) + 10

        origin = None
        if "Origin" in header:
            origin = _a.fromiterd(header.pop("Origin").strip('"').split()).reshape(3)

        return Lattice(cell, nsc=nsc, origin=origin, boundary_condition=bc)

    @sile_fh_open()
    def write_geometry(self, geometry, fmt=".8f", comment=None):
        """Writes the geometry to the contained file

        Parameters
        ----------
        geometry : Geometry
           the geometry to be written
        fmt : str, optional
           used format for the precision of the data
        comment : str, optional
           if None, a sisl made comment that can be used for parsing the unit-cell is used
           else this comment will be written at the 2nd line.
        """
        # Check that we can write to the file
        sile_raise_write(self)
        lattice = geometry.lattice

        # Write the number of atoms in the geometry
        self._write("   {}\n".format(len(geometry)))

        # Write out the cell information in the comment field
        # This contains the cell vectors in a single vector (3 + 3 + 3)
        # quantities, plus the number of supercells (3 ints)
        fields = []
        fields.append(
            ('Lattice="' + f"{{:{fmt}}} " * 9 + '"').format(*geometry.cell.ravel())
        )
        nsc = geometry.nsc[:]
        fields.append('nsc="{} {} {}"'.format(*nsc))
        pbc = ["T" if n else "F" for n in lattice.pbc]
        fields.append('pbc="{} {} {}"'.format(*pbc))
        BC = BoundaryCondition.getitem
        bc = [f"{BC(n[0]).name} {BC(n[1]).name}" for n in lattice.boundary_condition]
        fields.append('boundary_condition="{}  {}  {}"'.format(*bc))
        if comment is not None:
            fields.append(f'Comment="{comment}"')

        self._write(" ".join(fields) + "\n")

        fmt_str = "{{0:2s}}  {{1:{0}}}  {{2:{0}}}  {{3:{0}}}\n".format(fmt)
        for ia, a, _ in geometry.iter_species():
            s = a.symbol
            s = {"fa": "Ds"}.get(s, s)
            self._write(fmt_str.format(s, *geometry.xyz[ia, :]))

    def _r_geometry_skip(self, *args, **kwargs):
        """Read the geometry for a generic xyz file (not sisl, nor ASE)"""
        line = self.readline()
        if line == "":
            return None

        na = int(line)
        line = self.readline
        for _ in range(na + 1):
            line()
        return na

    @SileBinder(skip_func=_r_geometry_skip)
    @sile_fh_open()
    @deprecate_argument(
        "sc", "lattice", "use lattice= instead of sc=", from_version="0.15"
    )
    def read_geometry(self, atoms=None, lattice=None):
        """Returns Geometry object from the XYZ file

        Parameters
        ----------
        atoms : Atoms, optional
            the atoms to be associated with the Geometry
        lattice : Lattice, optional
            the lattice to be associated with the geometry
        """
        line = self.readline()
        if line == "":
            return None

        # Read number of atoms
        na = int(line)

        # Read header, and try and convert to dictionary
        header = self.readline()
        header = {k: v.strip('"') for k, v in header_to_dict(header).items()}

        # Read atoms and coordinates
        sp = [None] * na
        xyz = np.empty([na, 3], np.float64)
        line = self.readline
        for ia in range(na):
            l = line().split(maxsplit=5)
            sp[ia] = l[0]
            xyz[ia, :] = l[1:4]

        if atoms is not None:
            sp = atoms

        lattice = self._parse_lattice(header, xyz, lattice)
        return Geometry(xyz, atoms=sp, lattice=lattice)

    def ArgumentParser(self, p=None, *args, **kwargs):
        """Returns the arguments that is available for this Sile"""
        newkw = Geometry._ArgumentParser_args_single()
        newkw.update(kwargs)
        return self.read_geometry().ArgumentParser(p, *args, **newkw)


add_sile("xyz", xyzSile, case=False, gzip=True)
