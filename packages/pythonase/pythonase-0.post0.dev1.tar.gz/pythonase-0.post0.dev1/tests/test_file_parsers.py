import unittest
import os
from pythonase.file_parser_mem.gtf import parse_gtf, write_gtf, GTF_HEADER


class GtfCase(unittest.TestCase):
    def setUp(self) -> None:
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        self.gtf_file = os.path.join(self.current_dir, "datasets/test.gtf")
        self.gtf_obj = parse_gtf(self.gtf_file)

    def test_read(self):
        self.assertTrue(all(h in self.gtf_obj.columns for h in GTF_HEADER))
        self.assertTrue(self.gtf_obj.shape[0] == 2)  # two records in the sample gtf file

    def test_write(self):
        write_to = os.path.join(self.current_dir, "test_write.gtf")
        write_gtf(self.gtf_obj, write_to)
        gtf_reread = parse_gtf(write_to)
        self.assertTrue(self.gtf_obj.shape[0] == gtf_reread.shape[0])
        self.assertTrue(self.gtf_obj.shape[1] == gtf_reread.shape[1])


if __name__ == '__main__':
    unittest.main()
