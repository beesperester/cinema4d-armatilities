import c4d

import unittest

from beutils import dictutils, exceptions
from armaturebits import doodle


class TestDoodleModule(unittest.TestCase):
    def test_create_shape(self):
        result = doodle.create_shape("Foobar", c4d.Onull)
        result_expected = {"name": "Foobar", "type": c4d.Onull}

        try:
            dictutils.assert_is_subset(result_expected, result)
        except exceptions.ComparisonBaseError as e:
            raise AssertionError(e) from e


if __name__ == "__main__":
    unittest.main()
