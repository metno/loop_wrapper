
import unittest

import sys
import os
from subprocess import check_output, Popen, PIPE, STDOUT
from datetime import date

if os.getenv('LW_TEST_SYSTEM'):
    exe_dir = '/usr/bin'
else:
    exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')

class Test_Basic(unittest.TestCase):
    """ Test the most basic functionalities """

    def test_error_when_no_datestr(self):
        """ Test an error is triggered if no {d:} construct is found """
        cmd = exe + '--quiet 20040225 20040303 echo missing'
        p = Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=True, universal_newlines=True)
        out, err = p.communicate()
        self.assertNotEqual(p.returncode,0,msg='This run should have failed!')

    def test_format_with_empty_datestr(self):
        """ Test use of {d:} (empty datestr format) is valid, and defaults to %Y%m%d """
        cmd = [exe,'--quiet','20040225','20040303','echo','{d:}']
        out = check_output(cmd, universal_newlines=True)
        lines = out.splitlines()
        lengths = [len(d) for d in lines]
        self.assertEqual(set(lengths),set([8,]),
                         msg='Date looping with {{d:}} shortcut failed (got {} instead of YYYYMMDD)!'.format(lines[0]))

    def test_echo_doer(self):
        """ Test basic date looping with 1-day step """
        cmd = [exe,'--quiet','20040225','20040303','echo','{d:%Y%m%d}']
        out = check_output(cmd, universal_newlines=True)
        lines = out.splitlines()
        self.assertEqual(len(lines),8,msg='Basic date looping failed!')

    def test_quiet(self):
        """ Test the --quiet flag """
        cmd = [exe,'--quiet','{:%Y%m%d}'.format(date.today(),),'{:%Y%m%d}'.format(date.today(),),'echo','{d:%Y}']
        out = check_output(cmd,stderr=STDOUT, universal_newlines=True)
        lines = out.splitlines()
        self.assertEqual(len(lines),1,msg='The --quiet flag does not work (got {} lines of output)'.format(len(lines)))
        self.assertEqual(str(date.today().year),lines[0],
                         msg='The --quiet flag does not work as expected')

    def test_call(self):
        """ Test we can call the binary and retrieve some stdout/sterr text """
        cmd = [exe,'-v']
        out = check_output(cmd,stderr=STDOUT, universal_newlines=True)
        self.assertEqual('loop_wrapper',out.split(' ')[0],
                         msg='Did not manage to system call to loop_wrapper')

