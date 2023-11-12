from collections.abc import Iterable
from typing import Callable, Optional

import numpy as np
from skimage.metrics import structural_similarity as ssim


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

    assert (arr != 0).any(), "expected array to be non zeros, but got zeros"
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

    assert (arr != 0).any(), "expected array to be non zeros, but got zeros"
    assert arr.dtype in tuple(
        np.sctypes["int"] + np.sctypes["uint"] + np.sctypes["float"]
    ), f"expected complex data but got {arr.dtype}"
    assert np.isnan(arr).any() is not True, "array contains nans"
    assert np.isfinite(arr).all(), "array is not finite"


def check_arrays(
    class_obj: type,
    check_func: Optional[Callable | list[Callable] | tuple[Callable, ...]] = None,
    attributes: Optional[Iterable[str]] = None,
    attribute_check_dict: Optional[dict[str, Callable]] = None,
    shape: Optional[tuple[int, ...]] = None,
) -> None:
    """
    Checks the given attributes of the given class object for various properties using the given check function(s).

    Args:
        class_obj: The class object to check.
        check_func: The check function(s) to use. Can be a single check function, a list of check functions, or a tuple of check functions.
        attributres: The attributes to check.
        attribute_check_dict: A dictionary mapping attribute names to check functions.
        shape: The expected shape of the arrays to check. If `None`, no check will be performed.

    Raises:
        AssertionError: If any of the arrays do not meet the expected properties.
    """
    # check the valid function are passed
    assert attribute_check_dict is not None or (
        (check_func is not None) and attributes is not None
    ), "attribute_check_dict or (check_func and attributes) must be passed"

    # if the dict is passed
    if attribute_check_dict is not None:
        # loop over atributes and check_func pairs
        for attribute, check in attribute_check_dict.items():
            # get the attribute array
            arr = getattr(class_obj, attribute)
            # perform check
            check(arr=arr, shape=shape)
        return None
    # if there is a list of check_funcs
    if hasattr(check_func, "__len__"):
        # check the number of check funcs and attributes is equal
        assert len(check_func) == len(attributes)
        # loop over the attribute and check_func pairs
        for attribute, check in zip(attributes, check_func):
            # get the attribute array
            arr = getattr(class_obj, attribute)
            # perform check
            check(arr=arr, shape=shape)
    # if there is a single check_func
    else:
        # loop over the attributes
        for attributre in attributes:
            # get the arr
            arr = getattr(class_obj, attributre)
            # run the check func on it
            check_func(arr=arr, shape=shape)

    return None


### two array comparisons


def check_ssim_real(
    arr1: np.ndarray,
    arr2: np.ndarray,
    threshold: float = 0.95,
    data_range: Optional[float] = None,
) -> None:
    """
    Checks that the Structural Similarity Index Measure (SSIM) between two real arrays is greater than or equal to a given threshold.

    Args:
        arr1: The first array to compare.
        arr2: The second array to compare.
        threshold: The minimum SSIM score required. Must be between 0 and 1.
        data_range: The dynamic range of the pixel values in the arrays. If `None`, the maximum range of the two arrays will be used.

    Raises:
        AssertionError: If the SSIM score between the two arrays is less than the threshold.
    """

    # check the threshold was passed correctly
    assert (
        0 <= threshold < 1
    ), f"Threshold must be between [0,1), instead was passed {threshold}"
    # if a data range wasn't passed the calculate
    if data_range is None:
        data_range = np.max(
            arr1.max() - arr1.min(),
            arr2.max() - arr2.min(),
        )
    # check the SSIM score between the two arrarys and assert they are  >= threshold
    assert (
        ssim(arr1, arr2, data_range=data_range) >= threshold
    ), f"SSIM of arr1, arr2 {ssim(arr1, arr2, data_range=data_range) = } greater than the set threshold {threshold}"


def check_arrays_close(
    arr1: np.ndarray, arr2: np.ndarray, atol: float = 1e-08, rtol: float = 1e-05
) -> None:
    """
    Checks that two arrays are approximately equal using the NumPy `np.allclose()` function.

    Args:
        arr1: The first array to compare.
        arr2: The second array to compare.
        atol: The absolute tolerance.
        rtol: The relative tolerance.

    Raises:
        AssertionError: If the two arrays are not approximately equal.
    """

    assert np.allclose(
        arr1, arr2, atol=atol, rtol=rtol
    ), f"Arrays did no pass all close with provided tolerances {atol = }, {rtol = }."
