
import unittest

import sys
import os
from subprocess import check_output, STDOUT

if os.getenv('LW_TEST_SYSTEM'):
    exe_dir = '/usr/bin'
else:
    exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')

class Test_Backwards(unittest.TestCase):
    """ Test the looping over a date range with --backwards """

    def test_backwards(self):
        """ Test date looping with --every step with specified yearly resolution"""
        cmd = [exe,'--quiet','--every','6Y','19800501','20130601','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),6,'Date looping with "--every 6Y" failed!')

class Test_Every(unittest.TestCase):
    """ Test the looping over a date range with --every """

    def test_every_Y(self):
        """ Test date looping with --every step with specified yearly resolution"""
        cmd = [exe,'--quiet','--every','6Y','19800501','20130601','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),6,'Date looping with "--every 6Y" failed!')

    def test_every_m(self):
        """ Test date looping with --every step with specified monthly resolution"""
        cmd = [exe,'--quiet','--every','1m','20120501','20130601','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),14,'Date looping with "--every 1m" failed!')

    def test_every_w(self):
        """ Test date looping with --every step with specified weekly resolution"""
        cmd = [exe,'--quiet','--every','2w','20150505','20150602','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),3,msg='Date looping with "--every 2w" failed!')

    def test_every_S(self):
        """ Test date looping with --every step with specified secondly resolution"""
        cmd = [exe,'--quiet','--every','3600S','20040225','20040226','echo','{d:%Y%m%d %H%M%S}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),25,msg='Date looping with "--every 3600S" failed!')

    def test_every_M(self):
        """ Test date looping with --every step with specified minutely resolution"""
        cmd = [exe,'--quiet','--every','45M','20040225','20040226','echo','{d:%Y%m%d %H%M}']
        out = check_output(cmd)
        lines = out.splitlines()
        print lines
        print len(lines)
        self.assertEqual(len(lines),33,msg='Date looping with "--every 45M" failed!')

    def test_every_H(self):
        """ Test date looping with --every step with specified hourly resolution"""
        cmd = [exe,'--quiet','--every','6H','20040225','20040301','echo','{d:%Y%m%d %H}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),21,msg='Date looping with "--every 6H" failed!')

    def test_every_d(self):
        """ Test date looping with --every step with specified daily resolution"""
        cmd = [exe,'--quiet','--every','2d','20040225','20040303','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),4,msg='Date looping with "--every 2d" failed!')

    def test_every_default(self):
        """ Test date looping with --every step with default (daily) resolution"""
        cmd = [exe,'--quiet','--every','2','20040225','20040303','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),4,msg='Date looping with "--every 2" failed!')

