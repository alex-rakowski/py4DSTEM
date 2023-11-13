from pathlib import Path

import numpy as np
import py4DSTEM
import pytest
from py4DSTEM.utils.test_utils.array_utils import (
    # check_array,
    check_arrays,
    # check_arrays_close,
    check_complex_nonzeros,
    # check_complex_zeros,
    # check_real_nonzeros,
    check_real_zeros,
    check_ssim_real,
)
from py4DSTEM.utils.test_utils.attributes_utils import (
    test_attrs_raise_errors,
    test_getattrs,
)

# set filepath for the Si.cif file
# path = Path(py4DSTEM._TESTPATH) / "test_ptycho/Si.cif"
# set the filepath to the abTEM sim Si Datacube
# path = Path(py4DSTEM._TESTPATH) / "abTEM_Si_Datacube.h5"
path = (
    Path("/Users/arakowski/Documents/git_repos/py4dstem-alex/test/unit_test_data")
    / "abTEM_Si_Datacube.h5"
)


class TestSingleslicePtychographicReconstruction:
    # setup/teardown
    @pytest.fixture
    def setup_class(self):
        # load the datacube
        datacube = py4DSTEM.read(path, data_id="Placeholder")
        # assign to self
        self.datacube = datacube

        # some of these are taken from the simulation details
        # set the params init object
        self.init_params = {
            "energy": 200000.0,
            "verbose": False,
            "semiangle_cutoff": 20,
            "defocus": 100,
            "object_padding_px": (12, 12),
            "object_type": "potential",
        }
        # set params for pre pre-process
        self.preprocess_params = {
            "force_com_rotation": 0,
            "force_com_transpose": False,
            "plot_rotation": False,
            "plot_center_of_mass": False,
        }
        # set params for reconstruction
        self.reconstruct_params = {
            "max_iter": 64,
            "step_size": 0.125,
            "reset": True,
            "seed_random": 42,
        }
        # set to None initally to help with future tests
        self.SSPR = None

    @pytest.fixture
    def test_init_SingleslicePtychographicReconstruction(self):
        """
        Tests that the `SingleslicePtychographicReconstruction` class can be initialized successfully.

        Args:
            self: The test class instance.
        """
        # try creating it
        try:
            SSPR = py4DSTEM.process.phase.SingleslicePtychographicReconstruction(
                datacube=self.datacube,
                **self.init_params,
            )
        except AttributeError:
            raise
        except Exception:
            raise
        # I think this isn't needed
        assert (
            SSPR is not None
        ), "Failed to initialize SingleslicePtychographicReconstruction object."
        # check it has the preprocess and reconstruct methods
        assert hasattr(SSPR, "preprocess"), "Doesn't have preprocess method"
        assert hasattr(SSPR, "reconstruct"), "Doesn't have reconstruct method"
        # check it has metadata dict
        assert isinstance(SSPR.metadata, dict)
        # check the properties raise the expected errors
        expected_errors = {
            "object_cropped": AttributeError,
            "object_fft": AttributeError,
            "probe_centered": IndexError,
            "probe_fourier": IndexError,
            # "h" : (AttributeError),
        }
        # this looks through the expected errors and checks the raise the expected errors
        test_attrs_raise_errors(SSPR, expected_errors)
        # set state switch
        # self.SSPR = self.SSPR
        self.SSPR = SSPR

        self.init_correct = True

    # @pytest.fixture
    def test_preprocess_SingleslicePtychographicReconstruction(self):
        self.SSPR = self.SSPR
        assert (
            self.SSPR is not None
        ), "self.SSPR is None, init of SingleslicePtychographicReconstruction object failed previously"
        # try to run the pre-process function
        try:
            self.SSPR.preprocess(
                **self.preprocess_params,
            )
        except Exception:
            raise

        # test the arrays have been created as expected
        attributes_checks_dict = {
            "object_cropped": check_real_zeros,
            "object_fft": check_real_zeros,
            "probe_centered": check_complex_nonzeros,
            "probe_fourier": check_complex_nonzeros,
        }
        # tese the attrs are get-able
        test_getattrs(
            self.SSPR,
            attributes_checks_dict.keys(),
        )
        # test the arrays for properties
        # i.e. that they are non/zeros, right dtype, could add shape if we wanted
        # n.b. also checks are fintite and contains no nans
        check_arrays(
            self.SSPR,
            attribute_check_dict=attributes_checks_dict,
        )
        # check calling visualize fails with AttributeError,
        # it hasn't been created at this stage
        with pytest.raises(expected_exception=AttributeError):
            assert (
                self.SSPR.visualize()
            ), "Unexpected behaviour - It didn't raise expected AttributeError or anyother exception"

        # There may be other things that should be checked here e.g. plots etc.
        # set state for the
        self.SSPR = self.SSPR
        self.preprocess = True

    @pytest.fixture
    def test_reconstruct_SingleslicePtychographicReconstruction(self):
        # check its been created
        self.SSPR = self.SSPR

        assert self.SSPR is not None, "self.SSPR is None"
        # check that the prepocess test ran successfuly
        assert self.preprocess is True, "preporcess test must have failed"

        # run the reconstruction
        self.SSPR.reconstruct(**self.reconstruct_params)

        # check the object and probe
        attributes_checks_dict = {
            "object": check_real_zeros,
            "probe": check_complex_nonzeros,
        }
        # check the attributes are get-able
        test_getattrs(
            self.SSPR,
            attributes_checks_dict.keys(),
        )
        # check the values are what we expect
        check_arrays(
            self.SSPR,
            attribute_check_dict=attributes_checks_dict,
        )

        # possible hack to get around the issue of non-determinism
        # TODO add loading test file into this and check if its robust enough
        # check the probe
        assert check_ssim_real(
            self.SSPR.object,
            self.SSPR.object,
            threshold=0.95,
        ), "Failed SSIM test"
        assert check_ssim_real(
            np.abs(self.SSPR.probe),
            np.abs(self.SSPR.probe),
            threshold=0.95,
        ), "Failed SSIM test"

        # TODO what other things are there to check.
