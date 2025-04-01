import os
import sys
import struct
import unittest
from converter import main
from elf_writer import ELFWriter
from dol_parser import DOLParser

class TestDOLToELF(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Create a simple test DOL file"""
        cls.test_dol = "tests/test.dol"
        cls.test_elf = "tests/test.elf"
        
        # Create a minimal valid DOL file
        with open(cls.test_dol, 'wb') as f:
            # Create one valid text segment
            # Segment offset = 0x100, address = 0x80000000, size = 4
            f.write(b'\x00' * 0x100)  # Pad to segment start
            f.write(b'\x00\x01\x02\x03')  # Sample code
            
            # Set up segment headers
            f.seek(0)  # Text segment 0
            f.write(struct.pack('>I', 0x100))  # File offset
            f.write(struct.pack('>I', 0x80000000))  # RAM address
            f.write(struct.pack('>I', 4))  # Size
            
            # Zero out remaining segment headers (17 more)
            f.write(b'\x00' * (17 * 12))
            
            # Entry point at 0x80000000
            f.seek(0xE0)
            f.write(struct.pack('>I', 0x80000000))

    def test_conversion(self):
        """Test the full conversion workflow"""
        # Backup original sys.argv
        old_argv = sys.argv
        try:
            # Simulate command line arguments
            sys.argv = [__file__, self.test_dol, self.test_elf]
            retcode = main()
            self.assertEqual(retcode, 0)
        finally:
            # Restore original sys.argv
            sys.argv = old_argv
        self.assertTrue(os.path.exists(self.test_elf))
        
        # Verify ELF header
        with open(self.test_elf, 'rb') as f:
            magic = f.read(4)
            self.assertEqual(magic, b'\x7fELF')

    @classmethod
    def tearDownClass(cls):
        """Clean up test files"""
        if os.path.exists(cls.test_dol):
            os.remove(cls.test_dol)
        if os.path.exists(cls.test_elf):
            os.remove(cls.test_elf)

if __name__ == "__main__":
    unittest.main()