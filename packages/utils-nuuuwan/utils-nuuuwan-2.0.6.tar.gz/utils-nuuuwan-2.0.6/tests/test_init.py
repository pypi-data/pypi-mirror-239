import unittest

from utils import WWW, Git, Image, LatLng, Tweet, _, _log, hashx, mr, xmlx


class TestCase(unittest.TestCase):
    def test_init(self):
        for x in [WWW, Git, Tweet, _, _log, hashx, mr, xmlx, Image, LatLng]:
            self.assertIsNotNone(x)
