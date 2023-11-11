import unittest
from collections.abc import Iterable


# ExceptionType = TypeVar("ExceptionType", bound=Exception)
# ExpectedErrors = Dict[str, Tuple[Exception,]]
# Change this to a func
def test_attrs_raise_errors(
    class_obj: type,
    expected_errors: dict[str, tuple[Exception,]],
) -> None:
    """
    Test that the given attributes of the given class object raise the expected exceptions.

    Args:
        class_obj: The class object to test.
        expected_errors: A dictionary mapping attribute names to expected exceptions.

    Raises:
        Exception: If the raised Exception is not the expected error
        or
        AssertionError: If any of the attributes do not raise the expected exception.
    """

    for attribute, expected_error in expected_errors.items():
        # print(attribute)

        with unittest.TestCase.assertRaises(
            class_obj, expected_exception=expected_error
        ):
            if callable(getattr(class_obj, attribute)):
                assert getattr(
                    class_obj, attribute
                )(), f"{attribute} did not raise expected error {expected_error}"
            else:
                assert getattr(
                    class_obj, attribute
                ), f"{attribute} did not raise expected error {expected_error}"

    return None


def test_hasattrs(
    class_obj: type,
    attributes: Iterable[str],
) -> None:
    """
    Test that the given attributes of the given class object raise the expected exceptions.

    Args:
        class_obj: The class object to test.
        expected_errors: A dictionary mapping attribute names to expected exceptions.

    Raises:
        Exception: If the raised Exception is not the expected error
        or
        AssertionError: If any of the attributes do not raise the expected exception.
    """

    for attribute in attributes:
        # this will raise exceptions
        assert hasattr(class_obj, attribute)

    return None


def test_getattrs(
    class_obj: type,
    attributes: Iterable[str],
) -> None:
    """
    Test that the given attributes of the given class object raise the expected exceptions.

    Args:
        class_obj: The class object to test.
        expected_errors: A dictionary mapping attribute names to expected exceptions.

    Raises:
        Exception: If the raised Exception is not the expected error
        or
        AssertionError: If any of the attributes do not raise the expected exception.
    """

    for attribute in attributes:
        # will this raise exceptions so the assertion is kinda pointless?
        assert getattr(class_obj, attribute)

    return None
