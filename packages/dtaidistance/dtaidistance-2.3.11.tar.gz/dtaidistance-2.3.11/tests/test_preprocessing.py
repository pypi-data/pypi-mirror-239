import logging
import sys, os
import random
from pathlib import Path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

import pytest

from dtaidistance.preprocessing import differencing
from dtaidistance import util_numpy

logger = logging.getLogger("be.kuleuven.dtai.distance")
numpyonly = pytest.mark.skipif("util_numpy.test_without_numpy()")
scipyonly = pytest.mark.skipif("util_numpy.test_without_scipy()")


@numpyonly
@scipyonly
def test_differencing():
    with util_numpy.test_uses_numpy() as np:
        series = np.array([0.1, 0.3, 0.2, 0.1] * 3)
        series = differencing(series, smooth=0.1)
        np.testing.assert_array_almost_equal(
            series, np.array([0.19982795,  0.10894791,  0.0429936 ,  0.00856575, -0.00471123, -0.00838414,
                              -0.00740218, -0.00785088, -0.02099783, -0.05340167, -0.09960599]))

        series = np.array([[0.1, 0.3, 0.2, 0.1] * 3])
        series = differencing(series, smooth=0.1)
        np.testing.assert_array_almost_equal(
            series, np.array([[0.19982795, 0.10894791, 0.0429936, 0.00856575, -0.00471123, -0.00838414,
                               -0.00740218, -0.00785088, -0.02099783, -0.05340167, -0.09960599]]))


if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    directory = Path(os.environ.get('TESTDIR', Path(__file__).parent))
    print(f"Saving files to {directory}")
    test_differencing()
