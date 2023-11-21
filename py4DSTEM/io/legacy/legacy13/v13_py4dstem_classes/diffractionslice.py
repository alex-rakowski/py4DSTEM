# Defines the DiffractionSlice class, which stores 2(+1)D,
# diffraction-shaped data
from __future__ import annotations

from py4DSTEM.io.legacy.legacy13.v13_emd_classes.array import Array

import numpy as np
import h5py


class DiffractionSlice(Array):
    """
    Stores a diffraction-space shaped 2D data array.
    """

    def __init__(
        self,
        data: np.ndarray,
        name: str | None = "diffractionslice",
        slicelabels: bool | list | None = None,
    ):
        """
        Accepts:
            data (np.ndarray): the data
            name (str): the name of the diffslice
            slicelabels(None or list): names for slices if this is a 3D stack
        Returns:
            (DiffractionSlice instance)
        """

        # initialize as an Array
        Array.__init__(
            self, data=data, name=name, units="intensity", slicelabels=slicelabels
        )

    # HDF5 read/write

    # write inherited from Array

    # read
    def from_h5(group):
        from py4DSTEM.io.legacy.legacy13.v13_py4dstem_classes.io import (
            DiffractionSlice_from_h5,
        )

        return DiffractionSlice_from_h5(group)


############ END OF CLASS ###########
