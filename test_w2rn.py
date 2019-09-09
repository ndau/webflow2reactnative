import unittest
import os
from w2rn import processInputDir


class TestWebflow2ReactNative(unittest.TestCase):

    def test_full_run(self):
        processInputDir("test/data/input1", "test/data/output1")
        self.assertEqual(os.path.exists(
            "test/data/output1/src/ui/views/IndexView.js"), True)


if __name__ == '__main__':
    unittest.main()
