A Wii DOL to PS2 ELF Converter

A tool to convert Nintendo Wii executables (main.dol) to PlayStation 2 compatible ELF files.

## Features
- Converts Wii PowerPC executables to PS2 MIPS format
- Preserves segment structure and entry points
- Handles address space conversion (0x8XXXXXXX → 0xAXXXXXXX)
- Basic segment validation
- Command-line interface with progress feedback

## Installation
```bash
git clone https://github.com/yourusername/wii-dol-to-ps2-elf.git
cd wii-dol-to-ps2-elf
```

## Usage
```bash
python converter.py input.dol output.elf
```

Options:
- `-v` Verbose mode (shows conversion details)
- `-f` Force overwrite of existing files

## Requirements
- Python 3.8+
- No external dependencies

## Implementation Details
- `dol_parser.py`: Parses Wii DOL format headers and segments
- `elf_writer.py`: Generates PS2-compatible ELF files
- `architecture_utils.py`: Handles platform-specific conversions
- `converter.py`: Main conversion script with CLI interface

## Testing
Run unit tests:
```bash
python -m unittest tests/test_dol_to_elf.py
```

## Limitations
- Does not perform actual code translation (PowerPC→MIPS)
- Only handles basic segment mapping
- Requires valid Wii DOL files as input
- Limited address space validation

## License
MIT License
