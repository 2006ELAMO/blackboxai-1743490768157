#!/usr/bin/env python3
import sys
from dol_parser import DOLParser
from elf_writer import ELFWriter
from architecture_utils import ArchitectureUtils

class ConversionError(Exception):
    """Custom exception for conversion failures"""
    pass

def main():
    if len(sys.argv) != 3:
        print("Usage: python converter.py input.dol output.elf")
        return 1

    try:
        print(f"Converting {sys.argv[1]} to {sys.argv[2]}...")
        
        # Parse input DOL
        print("- Parsing DOL file...")
        dol = DOLParser(sys.argv[1])
        print(f"  Found {len(dol.segments)} segments")
        print(f"  Entry point: 0x{dol.entry_point:08X}")

        # Validate segments
        print("- Validating segments for PS2 compatibility...")
        for i, seg in enumerate(dol.segments):
            ArchitectureUtils.validate_segment(seg)
            print(f"  Segment {i}: {'TEXT' if seg['is_text'] else 'DATA'} "
                  f"0x{seg['address']:08X} → 0x{ArchitectureUtils.convert_address(seg['address']):08X}")

        # Generate ELF
        print("- Generating ELF file...")
        elf = ELFWriter(dol)
        elf.save(sys.argv[2])
        
        print("\nConversion successful!")
        print(f"Output saved to {sys.argv[2]}")
        return 0
        
    except Exception as e:
        raise ConversionError(f"Conversion failed: {str(e)}")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except ConversionError as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)