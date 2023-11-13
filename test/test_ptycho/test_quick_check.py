import pytest


class TestClass:
    @pytest.fixture
    def setup_data(self, request):
        # Get the parameters using the request fixture
        param_a = request.param[0]
        param_b = request.param[1]

        # Fixture setup code goes here
        data = {"param_a": param_a, "param_b": param_b}
        return data

    @pytest.mark.parametrize("setup_data", [(1, 2), (3, 0)], indirect=True)
    def test_example(self, setup_data):
        # Use the fixture in the test
        assert setup_data["param_a"] + setup_data["param_b"] == 3
