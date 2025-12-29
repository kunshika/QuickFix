import argparse
import sys
import os
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.prompt import Confirm
from .utils import read_file_segment, get_file_extension, write_file_segment
from .processor import CodeProcessor

load_dotenv()

console = Console()

print("Gemini API Key: ", os.getenv("GEMINI_API_KEY"))

def main():
    parser = argparse.ArgumentParser(description="Code Formatter & Explainer CLI")
    parser.add_argument("file", help="Path to the source file")
    parser.add_argument("--start", type=int, required=True, help="Start line number (1-based)")
    parser.add_argument("--end", type=int, required=True, help="End line number (1-based)")
    parser.add_argument("--api-key", help="Gemini API Key (optional, can use env var GEMINI_API_KEY)")
    parser.add_argument("--apply", action="store_true", help="Apply changes to the file")

    args = parser.parse_args()

    # Validate file
    if not os.path.exists(args.file):
        console.print(f"[red]Error: File '{args.file}' not found.[/red]")
        sys.exit(1)

    # Read Code
    try:
        code_segment = read_file_segment(args.file, args.start, args.end)
    except Exception as e:
        console.print(f"[red]Error reading file: {e}[/red]")
        sys.exit(1)

    if not code_segment.strip():
        console.print("[yellow]Warning: Selected range is empty.[/yellow]")
        sys.exit(0)

    ext = get_file_extension(args.file)
    
    # Display Original
    console.print(Panel(Syntax(code_segment, ext, theme="monokai", line_numbers=True, start_line=args.start), title="[bold blue]Original Code[/bold blue]", expand=False))

    # Process
    with console.status("[bold green]Processing with AI...[/bold green]"):
        processor = CodeProcessor(api_key=args.api_key)
        result = processor.process_code(code_segment, language=ext or "text")

    # Display Result
    console.print("\n")
    console.print(Panel(Syntax(result["code"], ext, theme="monokai", line_numbers=True), title="[bold green]Improved Implementation[/bold green]", expand=False))
    
    console.print("\n")
    console.print(Panel(Markdown(result["explanation"]), title="[bold magenta]Detailed Explanation[/bold magenta]", expand=False))

    # Apply Changes
    if args.apply or Confirm.ask("\n[bold yellow]Do you want to apply these changes to the file?[/bold yellow]"):
        try:
            write_file_segment(args.file, args.start, args.end, result["code"])
            console.print(f"[bold green]Successfully updated {args.file}[/bold green]")
        except Exception as e:
            console.print(f"[red]Error writing to file: {e}[/red]")

if __name__ == "__main__":
    main()
