from emdfile import save as _save
import warnings
from typing import Union, Optional
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename


def save(
    filepath: Optional[Union[str, Path]] = None,
    data=None,
    mode: str = "w",
    emdpath=None,
    tree: bool = True,
):
    """
    Saves data to an EMD 1.0 formatted HDF5 file at filepath.

    For the full docstring, see py4DSTEM.emdfile.save.
    """
    # This function wraps emdfile's save and adds a small piece
    # of metadata to the calibration to allow linking to calibrated
    # data items on read
    if data is None:
        raise ValueError("No Data passed to be saved")

    if filepath is None:
        try:
            root = Tk()
            root.withdraw()
            filepath = asksaveasfilename()
        except Exception as e:
            raise Exception(
                "unable to launch GUI file selector, pass filepath manually"
            ) from e

    cal = None
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        if hasattr(data, "calibration") and data.calibration is not None:
            cal = data.calibration
            rp = "/".join(data._treepath.split("/")[:-1])
            cal["_root_treepath"] = rp

    _save(filepath, data=data, mode=mode, emdpath=emdpath, tree=tree)

    if cal is not None:
        del cal._params["_root_treepath"]
