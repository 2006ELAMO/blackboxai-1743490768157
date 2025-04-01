class ArchitectureUtils:
    """Handles architecture-specific conversions between Wii (PowerPC) and PS2 (MIPS)"""
    
    @staticmethod
    def convert_address(wii_addr):
        """
        Converts Wii memory address to PS2 compatible address
        Wii range: 0x80000000-0x81800000 → PS2 range: 0xA0000000-0xA1800000
        """
        if not 0x80000000 <= wii_addr <= 0x81800000:
            raise ValueError(f"Invalid Wii address: 0x{wii_addr:08X}")
        return wii_addr + 0x20000000

    @staticmethod
    def validate_segment(segment):
        """
        Validates a DOL segment for PS2 compatibility
        Returns adjusted segment if needed
        """
        # PS2 requires 16-byte alignment for code segments
        if segment['is_text']:
            if segment['address'] % 16 != 0:
                raise ValueError(f"Text segment not 16-byte aligned: 0x{segment['address']:08X}")
        
        # PS2 has stricter memory region requirements
        converted_addr = ArchitectureUtils.convert_address(segment['address'])
        if not 0xA0000000 <= converted_addr <= 0xA2000000:
            raise ValueError(f"Converted address out of PS2 range: 0x{converted_addr:08X}")
            
        return segment