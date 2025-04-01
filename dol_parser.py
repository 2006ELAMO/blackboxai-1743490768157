import struct

class DOLParser:
    """Parses Nintendo Wii main.dol executable files"""
    
    def __init__(self, filepath):
        self.filepath = filepath
        self.segments = []
        self.entry_point = 0
        self._parse_header()
        
    def _parse_header(self):
        with open(self.filepath, 'rb') as f:
            # Read segment offsets and addresses
            self.segments = []
            for i in range(18):  # 7 text + 11 data segments
                offset = struct.unpack('>I', f.read(4))[0]
                addr = struct.unpack('>I', f.read(4))[0]
                size = struct.unpack('>I', f.read(4))[0]
                if size > 0:
                    self.segments.append({
                        'offset': offset,
                        'address': addr,
                        'size': size,
                        'is_text': i < 7  # First 7 segments are text
                    })
            
            # Read entry point
            f.seek(0xE0)
            self.entry_point = struct.unpack('>I', f.read(4))[0]
            
    def get_segment_data(self, index):
        """Returns raw binary data for a segment"""
        seg = self.segments[index]
        with open(self.filepath, 'rb') as f:
            f.seek(seg['offset'])
            return f.read(seg['size'])