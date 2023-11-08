import unittest
from tikit.cli import Cli

class MyTestCase(unittest.TestCase):
    def test_something(self):
        args = ["configure", "-f", "/hoe/json"]
        Cli(args)()


if __name__ == '__main__':
    unittest.main()
