import os.path
import pytest


def test(args=[]):
    """Test mubody library"""

    pytest.main([os.path.dirname(os.path.abspath(__file__))] + args)


if __name__ == "__main__":
    test()
