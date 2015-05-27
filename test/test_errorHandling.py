
import unittest

import sys
import os
from subprocess import PIPE, Popen, STDOUT

exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')
doer = os.path.join(os.path.realpath(os.path.dirname(__file__)),'doer1')

class Test_DieOnError(unittest.TestCase):
    """
       Test the --die-on-error action
       We use script ./doer1 that barks on one date
    """

    def test_DoE_PLL_withFlag(self):
        """ Test pll run with --die-on-error """
        cmd = exe + ' --die-on-error --cpu 2 --quiet 20100225 20100310 '+ doer + ' {d:%Y%m%d}'
        p = Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=True)
        out, err = p.communicate()
        ok_run = 0
        fail_run = 0
        for l in out.splitlines():
            if l.startswith('process '):
                ok_run += 1
            elif l.startswith('ERROR:'):
                fail_run += 1

        print out
        print err
        print ok_run, fail_run
        self.assertEqual((ok_run+fail_run),9,msg='Did not spawn expected number of "doer1" runs')
        self.assertEqual(ok_run,8,msg='Did not receive expected number of SUCCESS "doer1" runs')
        self.assertEqual(fail_run,1,msg='Did not receive expected number of ERROR "doer1" runs')
        self.assertNotEqual(p.returncode,0,msg='This run should have returned non-zero return code (got {})'.format(p.returncode,))

    def test_DoE_PLL_woutFlag(self):
        """ Test pll run without --die-on-error """
        cmd = exe + ' --cpu all --quiet 20100225 20100310 '+ doer + ' {d:%Y%m%d}'
        p = Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=True)
        out, err = p.communicate()
        ok_run = 0
        fail_run = 0
        for l in out.splitlines():
            if l.startswith('process '):
                ok_run += 1
            elif l.startswith('ERROR:'):
                fail_run += 1

        self.assertEqual((ok_run+fail_run),14,msg='Did not spawn expected number of "doer1" runs')
        self.assertEqual(ok_run,13,msg='Did not receive expected number of SUCCESS "doer1" runs')
        self.assertEqual(fail_run,1,msg='Did not receive expected number of ERROR "doer1" runs')
        self.assertNotEqual(p.returncode,0,msg='This run should have returned non-zero return code (got {})'.format(p.returncode,))

    def test_DoE_serial_withFlag(self):
        """ Test serial run with --die-on-error """
        cmd = [exe,'--die-on-error','--quiet','20100225','20100310',doer,'{d:%Y%m%d}']
        p = Popen(cmd,stdout=PIPE,stderr=STDOUT)
        out, err = p.communicate()
        ok_run = 0
        fail_run = 0
        for l in out.splitlines():
            if l.startswith('process '):
                ok_run += 1
            elif l.startswith('ERROR:'):
                fail_run += 1

        self.assertEqual((ok_run+fail_run),7,msg='Did not spawn expected number of "doer1" runs')
        self.assertEqual(ok_run,6,msg='Did not receive expected number of SUCCESS "doer1" runs')
        self.assertEqual(fail_run,1,msg='Did not receive expected number of ERROR "doer1" runs')
        self.assertNotEqual(p.returncode,0,msg='This run should have returned non-zero return code (got {})'.format(p.returncode,))

    def test_DoE_serial_woutFlag(self):
        """ Test serial run without --die-on-error """
        cmd = [exe,'--quiet','20100225','20100310',doer,'{d:%Y%m%d}']
        p = Popen(cmd,stdout=PIPE,stderr=STDOUT)
        out, err = p.communicate()
        ok_run = 0
        fail_run = 0
        for l in out.splitlines():
            if l.startswith('process '):
                ok_run += 1
            elif l.startswith('ERROR:'):
                fail_run += 1

        self.assertEqual((ok_run+fail_run),14,msg='Did not spawn expected number of "doer1" runs')
        self.assertEqual(ok_run,13,msg='Did not receive expected number of SUCCESS "doer1" runs')
        self.assertEqual(fail_run,1,msg='Did not receive expected number of ERROR "doer1" runs')
        self.assertNotEqual(p.returncode,0,msg='This run should have returned non-zero return code (got {})'.format(p.returncode,))


