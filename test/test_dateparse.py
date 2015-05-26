
import unittest

import sys
import os
from subprocess import check_output, STDOUT, CalledProcessError

exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')

class Test_DateParse(unittest.TestCase):
    """ Test the parsing of start and end dates """

    # this stop_date will be used for all tests
    stop_date = "20100315"

    def test_parse_wrongFmt(self):
        """ Test date parsing of dates with unsupported format """
        cmd = [exe,'--quiet','2010-03-14',self.stop_date,'echo','{d:%Y%m%d}']
        try:
            out = check_output(cmd,stderr=STDOUT)
            caught = False
        except CalledProcessError:
            caught= True
        self.assertTrue(caught,msg="Failed to bark at un-supported date format!")

    def test_parse_wrongDate(self):
        """ Test date parsing of unexisting dates """
        cmd = [exe,'--quiet','20090229',self.stop_date,'echo','{d:%Y%m%d}']
        try:
            out = check_output(cmd,stderr=STDOUT)
            caught = False
        except CalledProcessError:
            caught= True
        self.assertTrue(caught,msg="Failed to bark at impossible date!")

    def test_parse_YYYYMMDDHHMMSS(self):
        """ Test date parsing of dates with YYYYMMDDHHMMSS format """
        cmd = [exe,'--quiet','--every','10M','20100314214005',self.stop_date,'echo','{d:%Y%m%d %H:%M:%S}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),14,'Parsing YYYYMMDDHHMMSS date failed!')

    def test_parse_YYYYMMDDHHMM(self):
        """ Test date parsing of dates with YYYYMMDDHHMM format """
        cmd = [exe,'--quiet','--every','20M','201003141240',self.stop_date,'echo','{d:%Y%m%d %H:%M}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),35,'Parsing YYYYMMDDHHMM date failed!')

    def test_parse_YYYYMMDDHH(self):
        """ Test date parsing of dates with YYYYMMDDHH format """
        cmd = [exe,'--quiet','--every','12H','2010031106',self.stop_date,'echo','{d:%Y%m%d %H}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),8,'Parsing YYYYMMDDHH date failed!')

    def test_parse_YYYYMMDD(self):
        """ Test date parsing of dates with YYYYMMDD format """
        cmd = [exe,'--quiet','20100215',self.stop_date,'echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),29,'Parsing YYYYMMDD date failed!')

    def test_parse_YYYYMM(self):
        """ Test date parsing of dates with YYYYMM format """
        cmd = [exe,'--quiet','201003',self.stop_date,'echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        print len(lines), lines
        self.assertEqual(len(lines),15,'Parsing YYYYMM date failed!')

    def test_parse_YYYY(self):
        """ Test date parsing of dates with YYYY format """
        cmd = [exe,'--quiet','2010',self.stop_date,'echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        print len(lines), lines
        self.assertEqual(len(lines),74,'Parsing YYYY date failed!')

