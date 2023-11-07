from __future__ import (
    absolute_import,
    unicode_literals,
)

import glob
import os
import sys
import warnings
import unittest

if sys.version_info[0] > 2:
    import isatools.isatab

class AbstractTestIsa(unittest.TestCase):

    def assertIsaWasExported(self, study_id):
        """checks if tempdir contains generated files"""
        for isa_glob in ("i_Investigation.txt", "a_*.txt", "s_*.txt"):
            isa_glob = os.path.join(self.out_dir, study_id, isa_glob)
            self.assertTrue(glob.glob(isa_glob))

    if sys.version_info[0] > 2:
        def assertIsaIsValid(self, study_id):
            """validates generated ISA using isa-api"""
            result = isatools.isatab.validate(
                open(os.path.join(self.out_dir, study_id, "i_Investigation.txt")),
                self.config_dir, log_level=50,
            )
            self.assertEqual(result['errors'], [])

    else:
        def assertIsaIsValid(self, study_id):
            return True
