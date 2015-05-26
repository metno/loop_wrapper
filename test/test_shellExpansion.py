
import unittest

import sys
import os
from subprocess import check_output, STDOUT
from datetime import date

exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')
tst_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'test_data'))
doer2 = os.path.join(os.path.realpath(os.path.dirname(__file__)),'doer2')
doer3 = os.path.join(os.path.realpath(os.path.dirname(__file__)),'doer3')

class Test_ShellExpansion_wF(unittest.TestCase):
    """ Test the Shell Parameter Expansion, with {f:} reference """

    def test_shell_expansion_wF(self):
        """ Test combining date looping, shell parameter expansion  (with '?') and {f:} referencing """
        cmd = [exe,'--quiet','20051228','20060102',doer3,os.path.join(tst_dir,'{d:%Y}','tst_?_{d:%Y%m%d}.tar'),'{f:}.gz']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),18,msg='Basic shell expansion with "?" failed')
        # Test the {f:} substitution worked as expected
        ok_lines = 0
        for l in lines:
            if l.startswith('process '):
                if '.tar' in l and '.tar.gz' in l:
                    ok_lines += 1

        self.assertEqual(ok_lines,18,msg='Filename substitution with {f:} failed')

class Test_ShellExpansion_noF(unittest.TestCase):
    """ Test the Shell Parameter Expansion, without {f:} reference """

#    This does not work, because {,,,} interferes with python's {} in string formatting
#    def test_shell_expansion_select_noF(self):
#        """ Test combining date looping and shell parameter expansion  (with character select)"""
#        cmd = [exe,'--quiet','20051228','20060102',doer2,os.path.join(tst_dir,'{d:%Y}','tst_{{A,C}}_{d:%Y%m%d}.tar')]
#        out = check_output(cmd)
#        lines = out.splitlines()
#        self.assertEqual(len(lines),12,msg='Basic shell expansion with "{A,C}" failed')

    def test_shell_expansion_range_noF(self):
        """ Test combining date looping and shell parameter expansion  (with character ranges)"""
        cmd = [exe,'--quiet','20051228','20060102',doer2,os.path.join(tst_dir,'{d:%Y}','tst_[A:B]_{d:%Y%m%d}.tar')]
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),12,msg='Basic shell expansion with "[A-B]" failed')

    def test_shell_expansion_Qmark_noF(self):
        """ Test combining date looping and shell parameter expansion  (with '?') """
        cmd = [exe,'--quiet','20051228','20060102',doer2,os.path.join(tst_dir,'{d:%Y}','tst_?_{d:%Y%m%d}.tar')]
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),18,msg='Basic shell expansion with "?" failed')

    def test_shell_expansion_star_noF(self):
        """ Test combining date looping and shell parameter expansion  (with '*') """
        cmd = [exe,'--quiet','20051228','20060102',doer2,os.path.join(tst_dir,'{d:%Y}','tst_*_{d:%Y%m%d}.tar')]
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),20,msg='Basic shell expansion with "*" failed')

