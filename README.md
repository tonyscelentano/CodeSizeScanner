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

## LLM Configuration

This tool is designed to be "agent-aware." You can configure it as a machine-wide tool for Gemini CLI or other AI agents to help them map unfamiliar codebases.

### 1. Global Installation
Move the compiled `codesize.exe` to a directory in your system PATH or a dedicated agent binary folder (e.g., `C:\Users\<User>\.gemini\bin\codesize.exe`).

### 2. Machine-Wide Policy
Add the tool to your global agent policy (e.g., in `GEMINI.md`) so agents know when to use it:

```markdown
# Research & Codebase Analysis
Before deep-reading files in an unfamiliar or large codebase, use codesize.exe 
to map the structure and identify monolithic files.
```

### 3. Custom Slash Commands
You can map the tool to a slash command like `/scan` in your agent configuration to trigger high-density codebase analysis with a single keyword.

## License
MIT License - See [LICENSE](LICENSE) for details.
