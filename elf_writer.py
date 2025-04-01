import struct

class ELFWriter:
    """Generates PS2-compatible ELF executables"""
    
    ELF_HEADER_FORMAT = '<4sBBBB7xHHIIIIIHHHHHH'
    PROGRAM_HEADER_FORMAT = '<8I'
    
    def __init__(self, dol_parser):
        self.dol = dol_parser
        self.segments = []
        
    def _create_elf_header(self):
        """Creates ELF32 header for MIPS architecture"""
        e_ident = b'\x7fELF\x01\x01\x01\x00'  # ELF32, little-endian
        e_type = 2  # ET_EXEC
        e_machine = 8  # EM_MIPS
        e_version = 1  # EV_CURRENT
        e_entry = self._convert_address(self.dol.entry_point)
        e_phoff = 52  # Program header offset
        e_shoff = 0  # No section headers
        e_flags = 0x1000  # MIPS N32 ABI
        e_ehsize = 52  # ELF header size
        e_phentsize = 32  # Program header size
        e_phnum = len(self.dol.segments)  # Number of program headers
        e_shentsize = 40  # Section header size
        e_shnum = 0  # No section headers
        e_shstrndx = 0  # No section name string table
        
        # Create and pack ELF header
        header = bytearray(52)  # Standard ELF header size
        
        # e_ident
        header[0:4] = e_ident
        header[4] = e_type
        header[5] = e_machine
        header[6] = e_version
        
        # e_entry (offset 24)
        header[24:28] = struct.pack('<I', e_entry)
        # e_phoff (offset 28)
        header[28:32] = struct.pack('<I', e_phoff)
        # e_shoff (offset 32)
        header[32:36] = struct.pack('<I', e_shoff)
        # e_flags (offset 36)
        header[36:40] = struct.pack('<I', e_flags)
        # e_ehsize (offset 40)
        header[40:42] = struct.pack('<H', e_ehsize)
        # e_phentsize (offset 42)
        header[42:44] = struct.pack('<H', e_phentsize)
        # e_phnum (offset 44)
        header[44:46] = struct.pack('<H', e_phnum)
        # e_shentsize (offset 46)
        header[46:48] = struct.pack('<H', e_shentsize)
        # e_shnum (offset 48)
        header[48:50] = struct.pack('<H', e_shnum)
        # e_shstrndx (offset 50)
        header[50:52] = struct.pack('<H', e_shstrndx)
        
        return bytes(header)
    
    def _convert_address(self, wii_addr):
        """Converts Wii address (0x8XXXXXXX) to PS2 address (0xAXXXXXXX)"""
        return wii_addr + 0x20000000  # Simple offset mapping
        
    def _create_program_headers(self):
        """Generates program headers for each segment"""
        headers = []
        offset = 52 + (32 * len(self.dol.segments))  # After ELF + program headers
        
        for i, seg in enumerate(self.dol.segments):
            p_type = 1  # PT_LOAD
            p_offset = offset
            p_vaddr = self._convert_address(seg['address'])
            p_paddr = p_vaddr
            p_filesz = seg['size']
            p_memsz = seg['size']
            p_flags = 5 if seg['is_text'] else 6  # RX or RW
            p_align = 0x80  # PS2 typical alignment
            
            headers.append(struct.pack(self.PROGRAM_HEADER_FORMAT,
                                     p_type, p_offset, p_vaddr, p_paddr,
                                     p_filesz, p_memsz, p_flags, p_align))
            offset += seg['size']
            
        return b''.join(headers)
    
    def save(self, output_path):
        """Writes the complete ELF file"""
        with open(output_path, 'wb') as f:
            # Write ELF header
            f.write(self._create_elf_header())
            
            # Write program headers
            f.write(self._create_program_headers())
            
            # Write segment data
            for i, seg in enumerate(self.dol.segments):
                f.seek(52 + (32 * len(self.dol.segments)) + sum(s['size'] for s in self.dol.segments[:i]))
                f.write(self.dol.get_segment_data(i))