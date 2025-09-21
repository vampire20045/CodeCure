# CodeCure Documentation

## Installation

### From Source
```bash
git clone https://github.com/vampire20045/CodeCure.git
cd CodeCure
pip install -e .
```

### Using pip (once published)
```bash
pip install codecure
```

## Usage

### Command Line Interface

#### Analyze a Single File
```bash
python -m codecure.main --analyze myfile.py
```

#### Analyze Multiple Files
```bash
python -m codecure.main --analyze file1.py file2.js file3.ts
```

#### Analyze All Files in a Directory
```bash
python -m codecure.main --directory src --extensions py js ts
```

#### Get JSON Output
```bash
python -m codecure.main --analyze myfile.py --json
```

#### Quiet Mode (Summary Only)
```bash
python -m codecure.main --analyze myfile.py --quiet
```

### Python API

```python
from codecure.debugger import DebugAssistant

# Create assistant
assistant = DebugAssistant()

# Debug a single file
result = assistant.debug_file("myfile.py")
print(f"Found {len(result['issues'])} issues")

# Generate report for multiple files
files = ["file1.py", "file2.js", "file3.ts"]
report = assistant.generate_report(files)
print(f"Analyzed {report['files_analyzed']} files")
```

## Features

### Supported Languages

#### Python
- **Syntax Errors**: Detects Python syntax issues
- **Print Statements**: Suggests using logging instead
- **Bare Except Clauses**: Recommends specific exception handling
- **TODO Comments**: Tracks outstanding tasks

#### JavaScript/TypeScript
- **Console.log Statements**: Suggests proper logging
- **Loose Equality**: Recommends === over ==
- **General Code Quality**: Basic best practices

#### Generic Files
- **Trailing Whitespace**: Detects unnecessary spaces/tabs
- **Long Lines**: Identifies lines over 120 characters
- **File Encoding**: Handles encoding issues

### Issue Severity Levels

- **Error** ❌: Syntax errors and critical issues that prevent execution
- **Warning** ⚠️: Code smells and best practice violations
- **Info** ℹ️: Style issues and minor improvements

### Output Formats

- **Console**: Rich, colorful output with icons and suggestions
- **JSON**: Machine-readable format for integration with other tools

## Examples

### Example Output

```bash
$ python -m codecure.main --analyze examples/test_file.py

🔍 Analyzing: examples/test_file.py

📋 Issues found in examples/test_file.py:
  ⚠️  examples/test_file.py:8:4: Consider using logging instead of print for better debugging
   💡 Replace with logging.info() or logging.debug()
  ⚠️  examples/test_file.py:12:4: Bare except clause - consider catching specific exceptions
   💡 Use 'except SpecificException:' instead

==================================================
📊 ANALYSIS SUMMARY
==================================================
Total issues found: 2
⚠️  Warnings: 2

==================================================
💡 SUGGESTIONS
==================================================
  🔍 Review warnings to improve code quality and prevent bugs
  📝 Consider implementing proper logging for better debugging
  🎯 Use specific exception handling for better error debugging
```

### JSON Output Example

```json
{
  "file_path": "examples/test_file.py",
  "issues": [
    {
      "location": "examples/test_file.py:8:4",
      "severity": "warning",
      "message": "Consider using logging instead of print for better debugging",
      "type": "print_statement",
      "suggestion": "Replace with logging.info() or logging.debug()"
    }
  ],
  "summary": {
    "total_issues": 1,
    "severity_breakdown": {"warning": 1},
    "issue_type_breakdown": {"print_statement": 1}
  },
  "suggestions": [
    "🔍 Review warnings to improve code quality and prevent bugs",
    "📝 Consider implementing proper logging for better debugging"
  ]
}
```

## Development

### Running Tests
```bash
python -m unittest discover tests/ -v
```

### Project Structure
```
CodeCure/
├── codecure/           # Main package
│   ├── __init__.py     # Package initialization
│   ├── analyzer.py     # Core analysis engine
│   ├── debugger.py     # Debugging assistant
│   └── main.py         # CLI interface
├── tests/              # Test suite
│   ├── test_analyzer.py
│   └── test_debugger.py
├── examples/           # Example files for testing
├── docs/               # Documentation
└── README.md           # Project overview
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## Roadmap

- [ ] Support for more programming languages (Java, C++, Go, Rust)
- [ ] Integration with popular IDEs and editors
- [ ] Advanced static analysis features
- [ ] Custom rule configuration
- [ ] CI/CD integration plugins
- [ ] Web interface for team collaboration
- [ ] Machine learning-based suggestion improvements