
import unittest

import sys
import os
from subprocess import check_output, STDOUT, CalledProcessError

if os.getenv('LW_TEST_SYSTEM'):
    exe_dir = '/usr/bin'
else:
    exe_dir = os.path.realpath(os.path.join(os.path.dirname(__file__),'..'))
exe = os.path.join(exe_dir,'loop_wrapper')

class Test_DateParse(unittest.TestCase):
    """ Test the parsing of start and end dates """

    # this stop_date will be used for all tests
    stop_date = "20100315"

    def test_parse_wrongFmt2(self):
        """ Test date parsing of dates with unsupported format """
        sdate = '2010-03-14'
        cmd = [exe,'--quiet',sdate,self.stop_date,'echo','{d:%Y%m%d}']
        try:
            out = check_output(cmd,stderr=STDOUT)
            caught = False
        except CalledProcessError:
            caught= True
        self.assertTrue(caught,msg="Failed to bark at un-supported date format ({})!".format(sdate,))

    def test_parse_wrongFmt1(self):
        """ Test date parsing of dates with unsupported format """
        sdate = '200403010'
        cmd = [exe,'--quiet',sdate,self.stop_date,'echo','{d:%Y%m%d}']
        try:
            out = check_output(cmd,stderr=STDOUT)
            caught = False
        except CalledProcessError:
            caught= True
        self.assertTrue(caught,msg="Failed to bark at un-supported date format ({})!".format(sdate,))

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
        self.assertEqual(len(lines),15,'Parsing YYYYMM date failed!')

    def test_parse_YYYY(self):
        """ Test date parsing of dates with YYYY format """
        cmd = [exe,'--quiet','2010',self.stop_date,'echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),74,'Parsing YYYY date failed!')

    def test_parse_TODAY_and_YESTERDAY(self):
        """ Test date parsing of date entered as TODAY and YESTERDAY """
        cmd = [exe,'--quiet','YESTERDAY','TODAY','echo','{d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(len(lines),2,'Parsing TODAY and YESTERDAY date failed!')

    def test_reldate_format_year(self):
        """ Test relative date formats (Y/d/H/M/S) """
        cmd = [exe,'--quiet','20251231','20260101','echo','{d+1Y:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20261231','Error in reldate year')

    def test_reldate_format_month(self):
        cmd = [exe,'--quiet','20251001','20251002','echo','{d-11m:%Y%m%d} {d+3m:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20241101 20260101','Error in reldate day')

    def test_reldate_format_day(self):
        cmd = [exe,'--quiet','20251231','20260101','echo','{d-45d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20251116','Error in reldate day')

    def test_reldate_format_hour(self):
        cmd = [exe,'--quiet','20251231','20260101','echo','{d+11H:%Y%m%dT%H%M%SZ}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20251231T110000Z','Error in reldate hour')

    def test_reldate_format_minute(self):
        cmd = [exe,'--quiet','20251231','20260101','echo','{d+90M:%Y%m%dT%H%M%SZ}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20251231T013000Z','Error in reldate minute')

    def test_reldate_format_second(self):
        cmd = [exe,'--quiet','20251231','20260101','echo','{d+361S:%Y%m%dT%H%M%SZ}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20251231T000601Z','Error in reldate second')
        
    def test_reldate_year_rollover_multi(self):
        """ Test relative date year rollover with multiple dates (and order of cmds with cpu=1) """
        cmd = [exe,'--quiet','--cpu','1','20251231','20260101','echo','{d-1d:%Y%m%d}','{d+1d:%Y%m%d}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20251230 20260101','Error in reldate year rollover')
        self.assertEqual(lines[1],b'20251231 20260102','Error in reldate year rollover')

    def test_reldate_instring(self):
        """ Test relative hour with/without hour in datestring (also for day) """
        cmd = [exe,'--quiet','--cpu','1','20251231','20260101','echo','{d-1d:%Y%m%d}','{d+2H:%Y%m%d}','{d-1d:%Y%m}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'20251230 20251231 202512','Error in reldate should not effecting string')

        cmd = [exe,'--quiet','--cpu','1','20251231','20260101','echo','{d-1d:%Y%m%d%H%M}','{d+2H:%Y%m%d%H%M}','{d+1d:%Y%m}']
        out = check_output(cmd)
        lines = out.splitlines()
        self.assertEqual(lines[0],b'202512300000 202512310200 202601','Error in reldate hour/day should effect string ')

