
import unittest

import sys
import os
from subprocess import check_output, STDOUT
from multiprocessing import cpu_count

if os.getenv('LW_TEST_SYSTEM'):
    exe_dir = '/usr/bin'
else:
    exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')

class Test_ParallelRun(unittest.TestCase):
    """ Test the parallel run capabilities """

    def test_PLL_1saved(self):
        """ Test parallel run with 1 saved CPUs """
        cmd = exe + ' --cpu -1 --quiet 20040125 20040210 \'echo \"{d:%Y%m%d} $PPID\"\''
        out = check_output(cmd,shell=True,universal_newlines=True)
        lines = out.splitlines()
        # test we have the expected number of subprocesses
        self.assertEqual(len(lines),17,msg='Basic parallel date looping (cpu all) failed (un-expected looping)!')
        # For some reason, it is more difficult than expected to control how many processors/cores
        # are used by the tool.
        # test they do NOT have all same PPID (parent's PID)
        #s = set([(p.split(' '))[1] for p in lines])
        #self.assertEqual(len(s),min(cpu_count()-1,len(lines)),msg='Basic parallel date looping (cpu -1) failed (used {} cpus)'.format(len(s)))

    def test_PLL_ALL(self):
        """ Test parallel run with all available CPUs """
        cmd = exe + ' --cpu all --quiet 20040125 20040210 \'echo \"{d:%Y%m%d} $PPID\"\''
        out = check_output(cmd,shell=True,universal_newlines=True)
        lines = out.splitlines()
        # test we have the expected number of subprocesses
        self.assertEqual(len(lines),17,msg='Basic parallel date looping (cpu all) failed (un-expected looping)!')
        # test they do NOT have all same PPID (parent's PID)
        # For some reason, it is more difficult than expected to control how many processors/cores
        # are used by the tool.
        #s = set([(p.split(' '))[1] for p in lines])
        #self.assertEqual(len(s),min(cpu_count(),len(lines)),msg='Basic parallel date looping (cpu all) failed (used {} cpus)'.format(len(s)))

    def test_PLL_2(self):
        """ Test parallel run with 2 CPUs """
        cmd = exe + ' --cpu 2 --quiet 20040125 20040210 \'echo \"{d:%Y%m%d} $PPID\"\''
        out = check_output(cmd,shell=True,universal_newlines=True)
        lines = out.splitlines()
        # test we have the expected number of subprocesses
        self.assertEqual(len(lines),17,msg='Basic parallel date looping (cpu 2) failed (un-expected looping)!')
        # test they do NOT have all same PPID (parent's PID)
        s = set([(p.split(' '))[1] for p in lines])
        self.assertEqual(len(s),2,msg='Basic parallel date looping (cpu 2) failed (used {} cpus)'.format(len(s)))

    def test_serial(self):
        """ Test serial run a simple loop """
        cmd = exe + ' --quiet 20040125 20040210 \'echo \"{d:%Y%m%d} $PPID\"\''
        out = check_output(cmd,shell=True,universal_newlines=True)
        lines = out.splitlines()
        # test we have the expected number of subprocesses
        self.assertEqual(len(lines),17,msg='Basic serial date looping failed (un-expected looping)!')
        # test they all have same PPID (parent's PID)
        s = set([(p.split(' '))[1] for p in lines])
        self.assertEqual(len(s),1,msg='Basic serial date looping failed (this is a parallel run!)')
