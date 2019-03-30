"""
basic tests
"""
import unittest
from example.color_util import ColorCM

class Callme(object):
    """callme records calls"""
    def __init__(self):
        self.myargs = []
        self.mykwargs = []

    def __call__(self, *args, **kwargs):
        self.myargs = self.myargs.extend(args)
        self.mykwargs = self.mykwargs.extend(dict(kwargs))

class TestColors(unittest.TestCase):
    """test colors"""

    def test_should_work_as_context_mgr(self):
        """tests whether teh contxt manager works"""
        callme = Callme()
        with ColorCM(callme, "blue") as colorm:
            colorm("this is a test")
        self.assertEqual(callme.myargs, ["\033[94mthis is a test", "\033[0m"])
