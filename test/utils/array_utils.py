from collections.abc import Iterable
from typing import Callable, Optional

import numpy as np


### Array Funcs
def check_array(
    arr: np.ndarray,
    dtype: Optional[str | np.dtype] = None,
    shape: Optional[tuple[int, ...]] = None,
    zeros: Optional[bool] = None,
    nans: bool = True,
    finite: Optional[bool] = None,
) -> None:
    """
    Checks the given array for various properties, such as shape, dtype, and whether it contains zeros, NaNs, or finite values.

    Args:
        arr: The array to check.
        dtype: The expected dtype of the array. If `None`, no check will be performed.
        shape: The expected shape of the array. If `None`, no check will be performed.
        zeroes: Whether the array is expected to contain only zeros. If `None`, no check will be performed.
        nans: Whether the array is expected to contain no NaNs. If `False`, NaNs will be allowed.
        finite: Whether the array is expected to contain only finite values. If `None`, no check will be performed.
    """

    # check the shape of the array
    assert arr.shape == shape

    # check the dtype of the data

    if dtype is not None:
        # santitize string
        dtype = dtype.lower()
        # define the expected dtypes
        dtypes = {
            "real": tuple(np.sctypes["int"] + np.sctypes["uint"] + np.sctypes["float"]),
            "complex": tuple(np.sctypes["complex"]),
        }
        # if passed string real or complex
        if dtype in ["real", "complex"]:
            assert (
                arr.dtype in dtypes[dtype]
            ), f"expected {dtype}, but array contains {arr.dtype}"
        # if passed specific dtype
        else:
            assert (
                arr.dtype == dtype
            ), f"expected {dtype}, but array contains {arr.dtype}"

    # check the zero'ness of the array
    if zeros is not None:
        assert (
            arr == 0 if zeros else arr != 0
        ).all(), f"expected {'==' if zeros else '!='} 0, but found {'==' if ~zeros else '!='}"
    # check if arrays, contain nans
    if nans:
        assert np.isnan(arr).any() is not True, "array contains nans"

    # check if array is finite:
    if finite:
        assert np.isfinite(arr).all(), "array is not finite"


def check_complex_zeros(
    arr: np.ndarray,
    shape: Optional[tuple[int, ...]] = None,
) -> None:
    """
    Checks the given complex array for the following properties:
        * Shape matches the expected shape (if provided).
        * All elements are zeros.
        * Array contains no NaNs.
        * Array contains only finite values.

    Args:
        arr: The complex array to check.
        shape: The expected shape of the array. If `None`, no check will be performed.
    """

    if shape is not None:
        assert (
            arr.shape == shape
        ), f"{arr.shape = } doesn't match expected shape {shape}"

    assert (arr == 0).all(), "expected array to be zeros, but got non zeros"
    assert arr.dtype in tuple(
        np.sctypes["complex"]
    ), f"expected complex data but got {arr.dtype}"
    assert np.isnan(arr).any() is not True, "array contains nans"
    assert np.isfinite(arr).all(), "array is not finite"


def check_complex_nonzeros(
    arr: np.ndarray,
    shape: Optional[tuple[int, ...]] = None,
) -> None:
    """
    Checks the given complex array for the following properties:
        * Shape matches the expected shape (if provided).
        * All elements are non-zeros.
        * Array contains no NaNs.
        * Array contains only finite values.

    Args:
        arr: The complex array to check.
        shape: The expected shape of the array. If `None`, no check will be performed.
    """

    if shape is not None:
        assert (
            arr.shape == shape
        ), f"{arr.shape = } doesn't match expected shape {shape}"

    assert (arr != 0).all(), "expected array to be non zeros, but got zeros"
    assert arr.dtype in tuple(
        np.sctypes["complex"]
    ), f"expected complex data but got {arr.dtype}"
    assert np.isnan(arr).any() is not True, "array contains nans"
    assert np.isfinite(arr).all(), "array is not finite"


def check_real_zeros(
    arr: np.ndarray,
    shape: Optional[tuple[int, ...]] = None,
) -> None:
    """
    Checks the given real array for the following properties:
        * Shape matches the expected shape (if provided).
        * All elements are zeros.
        * Array contains no NaNs.
        * Array contains only finite values.

    Args:
        arr: The real array to check.
        shape: The expected shape of the array. If `None`, no check will be performed.
    """

    if shape is not None:
        assert (
            arr.shape == shape
        ), f"{arr.shape = } doesn't match expected shape {shape}"

    assert (arr == 0).all(), "expected array to be zeros, but got non zeros"
    assert arr.dtype in tuple(
        np.sctypes["int"] + np.sctypes["uint"] + np.sctypes["float"]
    ), f"expected complex data but got {arr.dtype}"
    assert np.isnan(arr).any() is not True, "array contains nans"
    assert np.isfinite(arr).all(), "array is not finite"


def check_real_nonzeros(
    arr: np.ndarray,
    shape: Optional[tuple[int, ...]] = None,
) -> None:
    """
    Checks the given real array for the following properties:
        * Shape matches the expected shape (if provided).
        * All elements are non-zeros.
        * Array contains no NaNs.
        * Array contains only finite values.

    Args:
        arr: The real array to check.
        shape: The expected shape of the array. If `None`, no check will be performed.
    """
    if shape is not None:
        assert (
            arr.shape == shape
        ), f"{arr.shape = } doesn't match expected shape {shape}"

    assert (arr != 0).all(), "expected array to be non zeros, but got zeros"
    assert arr.dtype in tuple(
        np.sctypes["int"] + np.sctypes["uint"] + np.sctypes["float"]
    ), f"expected complex data but got {arr.dtype}"
    assert np.isnan(arr).any() is not True, "array contains nans"
    assert np.isfinite(arr).all(), "array is not finite"


def check_arrays(
    class_obj: type,
    check_func: Callable | list[Callable] | tuple[Callable, ...],
    attributes: Iterable[str],
    shape: Optional[tuple[int, ...]] = None,
) -> None:
    """
    Checks the given attributes of the given class object for various properties using the given check function(s).

    Args:
        class_obj: The class object to check.
        check_func: The check function(s) to use. Can be a single check function, a list of check functions, or a tuple of check functions.
        attributres: The attributes to check.
        shape: The expected shape of the arrays to check. If `None`, no check will be performed.

    Raises:
        AssertionError: If any of the arrays do not meet the expected properties.
    """
    # TODO change to dict?

    if hasattr(check_func, "len"):
        # check the number of check funcs and attributes is equal
        assert len(check_func) == len(attributes)
        for attribute, check in zip(attributes, check_func):
            arr = getattr(class_obj, attribute)
            check(arr=arr, shape=shape)
    # if single func
    else:
        # loop over the attributes
        for attributre in attributes:
            # get the arr
            arr = getattr(class_obj, attributre)
            # run the check func on it
            check_func(arr=arr, shape=shape)
