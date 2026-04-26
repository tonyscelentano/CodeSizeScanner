import os
import sys
from pathlib import Path
from rich.console import Console
from rich.tree import Tree
from rich.text import Text

def count_lines(file_path):
    """Fast line counter with size limit."""
    try:
        # Don't even try to count lines for files > 10MB
        if file_path.stat().st_size > 10 * 1024 * 1024:
            return -1 
            
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\x00' in chunk: return None
        
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return sum(1 for _ in f)
    except Exception:
        return 0

def build_tree(path, tree, ignore_dirs=None, current_depth=0, max_depth=3):
    """Optimized tree builder."""
    if current_depth > max_depth:
        return

    if ignore_dirs is None:
        ignore_dirs = {'.git', '__pycache__', '.venv', 'node_modules', '.idea', '.vscode', 'dist', 'build', 'AppData', 'Local', 'Roaming', 'Microsoft', 'Windows'}
    
    try:
        entries = list(Path(path).iterdir())
        # Filter hidden and ignored
        entries = [e for e in entries if not e.name.startswith('.') and e.name not in ignore_dirs]
        # Sort: Dirs first
        entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
    except (PermissionError, OSError):
        return

    # Cap files per directory to prevent massive floods
    file_count = 0
    for p in entries:
        if p.is_dir():
            branch = tree.add(f"[bold blue]📁 {p.name}[/]")
            build_tree(p, branch, ignore_dirs, current_depth + 1, max_depth)
        else:
            file_count += 1
            if file_count > 50: # Only show first 50 files per dir
                if file_count == 51: tree.add("[dim]... (more files truncated)[/]")
                continue
                
            line_count = count_lines(p)
            if line_count is None: continue
            
            # Labeling
            suffix = f" ({line_count} lines)" if line_count >= 0 else " (Large File)"
            color = "bright_black"
            if line_count > 1000: color = "bold red"
            elif line_count > 500: color = "red"
            elif line_count > 200: color = "yellow"
            elif line_count > 50: color = "green"
            
            text = Text()
            text.append(f"📄 {p.name}", style="white")
            text.append(suffix, style=color)
            tree.add(text)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Code Size Scanner - Find monolithic files.")
    parser.add_argument("target", nargs="?", default=".", help="Directory to scan")
    parser.add_argument("--over", type=int, default=0, help="Only show files with more than X lines")
    parser.add_argument("--over300", action="store_true", help="Shortcut for --over 300")
    parser.add_argument("--over500", action="store_true", help="Shortcut for --over 500")
    parser.add_argument("--over1000", action="store_true", help="Shortcut for --over 1000")
    
    args = parser.parse_args()
    
    # Resolve threshold
    threshold = args.over
    if args.over1000: threshold = 1000
    elif args.over500: threshold = 500
    elif args.over300: threshold = 300

    target_path = Path(args.target).absolute()
    
    if not target_path.exists():
        print(f"Error: Path {target_path} does not exist.")
        sys.exit(1)
        
    console = Console()
    header = f"\n[bold underline]Code Size Scanner[/]"
    if threshold > 0:
        header += f" [yellow](Filtering files > {threshold} lines)[/]"
    console.print(header + "\n", style="magenta")
    
    root_tree = Tree(f"[bold cyan]ROOT: {target_path}[/]")
    
    def build_tree_filtered(path, tree, current_depth=0, max_depth=3):
        if current_depth > max_depth: return
        ignore_dirs = {'.git', '__pycache__', '.venv', 'node_modules', 'AppData', 'Local', 'Roaming', 'Microsoft', 'Windows'}
        
        try:
            entries = list(Path(path).iterdir())
            entries = [e for e in entries if not e.name.startswith('.') and e.name not in ignore_dirs]
            entries.sort(key=lambda p: (not p.is_dir(), p.name.lower()))
        except (PermissionError, OSError): return

        for p in entries:
            if p.is_dir():
                # For directories, we create the branch but only keep it if it contains matching files
                branch = Tree(f"[bold blue]📁 {p.name}[/]")
                build_tree_filtered(p, branch, current_depth + 1, max_depth)
                if branch.children:
                    tree.add(branch)
            else:
                line_count = count_lines(p)
                if line_count is None: continue
                if line_count < threshold: continue
                
                suffix = f" ({line_count} lines)" if line_count >= 0 else " (Large File)"
                color = "bright_black"
                if line_count > 1000: color = "bold red"
                elif line_count > 500: color = "red"
                elif line_count > 200: color = "yellow"
                elif line_count > 50: color = "green"
                
                text = Text()
                text.append(f"📄 {p.name}", style="white")
                text.append(suffix, style=color)
                tree.add(text)

    with console.status("[bold green]Calculating monolithic metrics..."):
        build_tree_filtered(target_path, root_tree)
        
    if not root_tree.children:
        console.print(f"[bright_black]No files found matching the criteria in {target_path}[/]")
    else:
        console.print(root_tree)
    
    console.print("\n[dim]Legend: [bold red]>1000[/] [red]>500[/] [yellow]>200[/] [green]>50[/] [bright_black]Small[/][/]\n")

if __name__ == "__main__":
    main()
