# Code Size Scanner

A portable TUI tool to visualize codebase monoliths by line count.

## Usage

### Standalone Executable (Recommended)
Just run the executable followed by the directory you want to scan:

```powershell
.\codesize.exe C:\path\to\your\code
```

### Batch Script
Alternatively, use the batch script:
```powershell
.\scan.bat C:\path\to\your\code
```

## Features
- Standalone `.exe` (No Python required)
- Color-coded line counts
- Automatically ignores noise (.git, node_modules, etc.)

## Development

### Requirements
- Python 3.12+
- Packages listed in `requirements.txt`

### Build from Source
To recreate the executable:
```powershell
pip install -r requirements.txt pyinstaller
pyinstaller --onefile --name codesize --clean scanner.py
```

## License
MIT License - See [LICENSE](LICENSE) for details.
