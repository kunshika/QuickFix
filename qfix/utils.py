import os

def read_file_segment(file_path: str, start_line: int, end_line: int) -> str:
    """
    Reads a specific range of lines from a file.
    Lines are 1-indexed.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Adjust for 0-based indexing
    start_index = max(0, start_line - 1)
    end_index = min(len(lines), end_line)

    if start_index >= len(lines):
        return ""

    return "".join(lines[start_index:end_index])

def get_file_extension(file_path: str) -> str:
    """Returns the file extension without the dot."""
    return os.path.splitext(file_path)[1].lstrip('.')

def write_file_segment(file_path: str, start_line: int, end_line: int, new_content: str):
    """
    Replaces a specific range of lines in a file with new content.
    Lines are 1-indexed.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Adjust for 0-based indexing
    start_index = max(0, start_line - 1)
    end_index = min(len(lines), end_line)

    # Prepare new content lines
    new_lines = new_content.splitlines(keepends=True)
    if not new_content.endswith('\n'):
        new_lines[-1] += '\n'

    # Replace lines
    lines[start_index:end_index] = new_lines

    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
