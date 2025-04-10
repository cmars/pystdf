import unittest
from pystdf.BinSummarizer import BinSummarizer
from pystdf.V4 import prr, hbr, sbr

class MockDataSource:
    def __init__(self):
        self.name = "MockDataSource"

class TestBinSummarizer(unittest.TestCase):
    def setUp(self):
        self.summarizer = BinSummarizer()
        self.dataSource = MockDataSource()
        self.summarizer.before_begin(self.dataSource)

    def test_flags(self):
        # Test hard bin flags
        hbr_row = [0] * len(hbr.fieldNames)
        hbr_row[hbr.HBIN_PF] = 'F'
        self.assertEqual(self.summarizer.getHPfFlags(hbr_row), BinSummarizer.FLAG_FAIL)
        
        hbr_row[hbr.HBIN_PF] = 'P'
        self.assertEqual(self.summarizer.getHPfFlags(hbr_row), 0)
        
        hbr_row[hbr.HBIN_PF] = 'X'
        self.assertEqual(self.summarizer.getHPfFlags(hbr_row), BinSummarizer.FLAG_UNKNOWN)

        # Test soft bin flags
        sbr_row = [0] * len(sbr.fieldNames)
        sbr_row[sbr.SBIN_PF] = 'F'
        self.assertEqual(self.summarizer.getSPfFlags(sbr_row), BinSummarizer.FLAG_FAIL)
        
        sbr_row[sbr.SBIN_PF] = 'P'
        self.assertEqual(self.summarizer.getSPfFlags(sbr_row), 0)
        
        sbr_row[sbr.SBIN_PF] = 'X'
        self.assertEqual(self.summarizer.getSPfFlags(sbr_row), BinSummarizer.FLAG_UNKNOWN)

    def test_bin_storage(self):
        # Test HBR storage
        hbr_row = [0] * len(hbr.fieldNames)
        hbr_row[hbr.HEAD_NUM] = 255  # Overall bin
        hbr_row[hbr.HBIN_NUM] = 1
        self.summarizer.onHbr(hbr_row)
        self.assertEqual(len(self.summarizer.getOverallHbins()), 1)
        
        hbr_row[hbr.HEAD_NUM] = 1  # Site-specific bin
        hbr_row[hbr.SITE_NUM] = 1
        self.summarizer.onHbr(hbr_row)
        self.assertEqual(len(self.summarizer.getSiteHbins()), 1)

        # Test SBR storage
        sbr_row = [0] * len(sbr.fieldNames)
        sbr_row[sbr.HEAD_NUM] = 255  # Overall bin
        sbr_row[sbr.SBIN_NUM] = 1
        self.summarizer.onSbr(sbr_row)
        self.assertEqual(len(self.summarizer.getOverallSbins()), 1)
        
        sbr_row[sbr.HEAD_NUM] = 1  # Site-specific bin
        sbr_row[sbr.SITE_NUM] = 1
        self.summarizer.onSbr(sbr_row)
        self.assertEqual(len(self.summarizer.getSiteSbins()), 1)

    def test_part_tracking(self):
        prr_row = [0] * len(prr.fieldNames)
        prr_row[prr.SITE_NUM] = 1
        prr_row[prr.HARD_BIN] = 1
        prr_row[prr.SOFT_BIN] = 1
        prr_row[prr.PART_FLG] = 0  # Pass

        # Test part counting and pass/fail tracking
        self.summarizer.onPrr(prr_row)
        
        # Check hard bin tracking
        count, status = self.summarizer.hbinParts[(1, 1)]
        self.assertEqual(count[0], 1)
        self.assertEqual(status[0], 'P')

        # Check soft bin tracking
        count, status = self.summarizer.sbinParts[(1, 1)]
        self.assertEqual(count[0], 1)
        # Soft bins initialize with False, so they'll get ' ' status
        self.assertEqual(status[0], ' ')

        # Test fail case
        prr_row[prr.PART_FLG] = 0x08  # Fail
        self.summarizer.onPrr(prr_row)
        
        # Check status becomes mixed (' ') when both pass and fail seen
        count, status = self.summarizer.hbinParts[(1, 1)]
        self.assertEqual(count[0], 2)
        self.assertEqual(status[0], ' ')

if __name__ == '__main__':
    unittest.main()
