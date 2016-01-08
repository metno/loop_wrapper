
import unittest

import sys
import os
from subprocess import check_output, Popen, PIPE, STDOUT
from datetime import date

exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')

class Test_Basic(unittest.TestCase):
    """ Test the most basic functionalities """

    def test_error_when_no_datestr(self):
        """ Test an error is triggered if no {d:} construct is found """
        cmd = exe + '--quiet 20040225 20040303 echo missing'
        p = Popen(cmd,stdout=PIPE,stderr=STDOUT,shell=True)
        out, err = p.communicate()
        self.assertNotEqual(p.returncode,0,msg='This run should have failed!')

    def test_echo_doer(self):
        """ Test basic date looping with 1-day step (with and without ENV) """
        cmd = [exe,'--quiet','20040225','20040303','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),8,msg='Basic date looping failed!')
        #cmd2 = ['env','-i',]
        #cmd2.extend(cmd,)
        #out = check_output(cmd2)
        #lines = out.splitlines()
        #self.assertEqual(len(lines),8,msg='Basic date looping failed (when ENV is empty)!')

    def test_quiet(self):
        """ Test the --quiet flag """
        cmd = [exe,'--quiet','{:%Y%m%d}'.format(date.today(),),'{:%Y%m%d}'.format(date.today(),),'echo','{d:%Y}']
        out = check_output(cmd,stderr=STDOUT)
        lines = out.splitlines()
        self.assertEqual(len(lines),1,msg='The --quiet flag does not work (got {} lines of output)'.format(len(lines)))
        self.assertEqual(str(date.today().year),lines[0],
                         msg='The --quiet flag does not work as expected')

    #def test_call_noENV(self):
    #    """ Test we can call the script in a 'crontab-like' environment (missing ENV) """
    #    cmd = ['env','-i',exe,'-v']
    #    out = check_output(cmd,stderr=STDOUT)
    #    self.assertEqual('loop_wrapper',out.split(' ')[0],
    #                     msg='Did not manage to system call to loop_wrapper')

    def test_call(self):
        """ Test we can call the binary and retrieve some stdout/sterr text """
        cmd = [exe,'-v']
        out = check_output(cmd,stderr=STDOUT)
        self.assertEqual('loop_wrapper',out.split(' ')[0],
                         msg='Did not manage to system call to loop_wrapper')

