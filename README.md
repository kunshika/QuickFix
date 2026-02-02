# QuickFix (qfix)

A powerful command-line tool that uses AI (Google Gemini) to format and explain specific blocks of code within your files. It allows you to target specific lines, receive intelligent improvements without logic changes, and optionally write the changes back to your file in proper format. 

## Features

-   **Targeted Formatting**: Select specific line ranges to process, leaving the rest of the file untouched.
-   **AI-Powered**: Uses Google's Gemini models (e.g., `gemini-2.0-flash`) to understand and format code.
-   **Strict Formatting**: Enforces best practices (indentation, spacing) without altering the underlying logic.
-   **Detailed Explanations**: Provides a Markdown-formatted explanation of *why* changes were made.
-   **Write-Back Support**: Apply the improved code directly to your file with the `--apply` flag or interactive prompt.
-   **Mock Mode**: Works offline or without an API key (returns a mock response for testing).

## Prerequisites

-   Python 3.8+
-   A Google Gemini API Key (Get one from [Google AI Studio](https://aistudio.google.com/))

## Installation

1.  **Clone the repository** (or navigate to the project directory):
    ```bash
    cd /path/to/qfix
    ```

2.  **Create a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install .
    ```

## Configuration

1.  Create a `.env` file in the root directory:
    ```bash
    touch .env
    ```

2.  Add your Gemini API Key to `.env`:
    ```env
    GEMINI_API_KEY=kfnkmfkjn...
    ```

    *Alternatively, you can pass the key via the CLI argument `--api-key`.*

## Usage

Run the tool using `qfix` with the target file and line range.

### Basic Usage (View Only)
This will print the original code, the improved version, and the explanation to the console without modifying the file.

```bash
qfix path/to/file.py --start 10 --end 20
```

### Apply Changes
To write the formatted code back to the file, use the `--apply` flag or answer "Yes" to the interactive prompt.

```bash
qfix path/to/file.py --start 10 --end 20 --apply
```

### Command Line Arguments

| Argument | Description | Required |
| :--- | :--- | :--- |
| `file` | Path to the source file to process. | Yes |
| `--start` | Start line number (1-based). | Yes |
| `--end` | End line number (1-based). | Yes |
| `--apply` | Automatically apply changes to the file. | No |
| `--api-key`| Provide API key directly (overrides `.env`).| No |

## Example

**Input File (`example.py`):**
```python
7  def complex_logic(a, b):
8      # This is a bad implementation
9      if a > b: return a - b
10     else: return
11     b - a
```

**Command:**
```bash
qfix example.py --start 7 --end 11
```

**Output:**
The tool will display:
1.  **Original Code**: Syntax-highlighted view of lines 7-11.
2.  **Improved Implementation**: Properly formatted code (e.g., fixing the `else: return` line break).
3.  **Detailed Explanation**: "Fixed indentation and line breaks for readability..."

## Troubleshooting

-   **429 Quota Exceeded**: The free tier of Gemini API has rate limits. If you see this error, wait a minute and try again.
-   **Mock Explanation**: If you see this, it means the tool couldn't access the API (missing key or network issue). Check your `.env` file.
