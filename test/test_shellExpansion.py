
import unittest

import sys
import os
from subprocess import check_output, STDOUT
from datetime import date

if os.getenv('LW_TEST_SYSTEM'):
    exe_dir = '/usr/bin'
else:
    exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')
tst_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'test_data'))
doer2 = os.path.join(os.path.realpath(os.path.dirname(__file__)),'doer2')
doer3 = os.path.join(os.path.realpath(os.path.dirname(__file__)),'doer3')

class Test_ShellExpansion_wF(unittest.TestCase):
    """ Test the Shell Parameter Expansion, with {f:} reference """

    def test_shell_expansion_wF_nowildcard(self):
        """ Test combining date looping, no wildcard and {F:} referencing """
        cmd = [exe,'--quiet','20051228','20060102',doer3,
               '['+os.path.join(tst_dir,'{d:%Y}','tst_A_{d:%Y%m%d}.tar')+']','/tmp/{F:}.gz']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),6,msg='Basic substitution with {F:} failed when no wildcards are used')
        # Test the {F:} substitution worked as expected
        ok_lines = 0
        for l in lines:
            if l.startswith('process '):
                from_file = (l.split())[1]
                to_file   = (l.split())[-1]
                if from_file.endswith('.tar') and os.path.exists(from_file) and \
                   to_file == os.path.join('/tmp',os.path.basename(from_file))+'.gz':
                    ok_lines += 1

        self.assertEqual(ok_lines,6,msg='Filename substitution with {F:} failed when no wildcards are used')

    def test_shell_expansion_wF(self):
        """ Test combining date looping, shell parameter expansion  (with '?') and {F:} referencing """
        cmd = [exe,'--quiet','20051228','20060102',doer3,
               '['+os.path.join(tst_dir,'{d:%Y}','tst_?_{d:%Y%m%d}.tar')+']','/tmp/{F:}.gz']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),18,msg='Basic shell expansion with "?" failed')
        # Test the {F:} substitution worked as expected
        ok_lines = 0
        for l in lines:
            if l.startswith('process '):
                from_file = (l.split())[1]
                to_file   = (l.split())[-1]
                if from_file.endswith('.tar') and os.path.exists(from_file) and \
                   to_file == os.path.join('/tmp',os.path.basename(from_file))+'.gz':
                    ok_lines += 1

        self.assertEqual(ok_lines,18,msg='Filename substitution with {F:} failed')

    def test_shell_expansion_wf(self):
        """ Test combining date looping, shell parameter expansion  (with '?') and {f:} referencing """
        cmd = [exe,'--quiet','20051228','20060102',doer3,
               '['+os.path.join(tst_dir,'{d:%Y}','tst_?_{d:%Y%m%d}.tar')+']','{f:}.gz']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),18,msg='Basic shell expansion with "?" failed')
        # Test the {f:} substitution worked as expected
        ok_lines = 0
        for l in lines:
            if l.startswith('process '):
                from_file = (l.split())[1]
                to_file   = (l.split())[-1]
                if from_file.endswith('.tar') and os.path.exists(from_file) and \
                   to_file == from_file+'.gz':
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
        cmd = [exe,'--quiet','20051228','20060102',doer2,
               '['+os.path.join(tst_dir,'{d:%Y}','tst_[A:B]_{d:%Y%m%d}.tar')+']']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),12,msg='Basic shell expansion with "[A-B]" failed')
        # Test that the files exists
        ok_lines = 0
        for l in lines:
            fn = (l.split(' '))[-1]
            if os.path.exists(fn):
                ok_lines += 1
            else:
                print("ERROR: file {} should exist!".format(fn,))
        self.assertEqual(ok_lines,12,msg='Basic shell expansion failed')

    def test_shell_expansion_Qmark_noF(self):
        """ Test combining date looping and shell parameter expansion  (with '?') """
        cmd = [exe,'--quiet','20051228','20060102',doer2,
               '['+os.path.join(tst_dir,'{d:%Y}','tst_?_{d:%Y%m%d}.tar')+']']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),18,msg='Basic shell expansion with "?" failed')

    def test_shell_expansion_star_noF(self):
        """ Test combining date looping and shell parameter expansion  (with '*') """
        cmd = [exe,'--quiet','20051228','20060102',doer2,
               '['+os.path.join(tst_dir,'{d:%Y}','tst_*_{d:%Y%m%d}.tar')+']']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),20,msg='Basic shell expansion with "*" failed')

