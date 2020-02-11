#  ----- ---- --- -- -
#  Copyright 2020 The Axiom Foundation. All Rights Reserved.
# 
#  Licensed under the Apache License 2.0 (the "License").  You may not use
#  this file except in compliance with the License.  You can obtain a copy
#  in the file LICENSE in the source distribution or at
#  https://www.apache.org/licenses/LICENSE-2.0.txt
#  - -- --- ---- -----

import unittest
import os
from w2rn import processInputDir


class TestWebflow2ReactNative(unittest.TestCase):
    def test_full_run(self):
        processInputDir("test/data/input1", "test/data/output1")
        self.assertEqual(
            os.path.exists("test/data/output1/src/ui/views/IndexView.js"), True
        )


if __name__ == "__main__":
    unittest.main()
