"""
Tests for CodeCure analyzer
"""
import unittest
import tempfile
import os
from codecure.analyzer import CodeAnalyzer, Issue


class TestCodeAnalyzer(unittest.TestCase):
    
    def setUp(self):
        self.analyzer = CodeAnalyzer()
    
    def test_analyze_nonexistent_file(self):
        """Test analyzing a file that doesn't exist"""
        issues = self.analyzer.analyze_file("nonexistent.py")
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0].issue_type, 'file_not_found')
        self.assertEqual(issues[0].severity, 'error')
    
    def test_analyze_python_syntax_error(self):
        """Test Python file with syntax errors"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write("def broken_function(\n    print('missing closing parenthesis')")
            f.flush()
            
            issues = self.analyzer.analyze_file(f.name)
            
            # Should detect syntax error
            syntax_errors = [i for i in issues if i.issue_type == 'syntax_error']
            self.assertGreater(len(syntax_errors), 0)
            self.assertEqual(syntax_errors[0].severity, 'error')
            
            os.unlink(f.name)
    
    def test_analyze_python_print_statements(self):
        """Test detection of print statements"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('print("Hello, world!")\n')
            f.flush()
            
            issues = self.analyzer.analyze_file(f.name)
            
            print_issues = [i for i in issues if i.issue_type == 'print_statement']
            self.assertEqual(len(print_issues), 1)
            self.assertEqual(print_issues[0].severity, 'warning')
            
            os.unlink(f.name)
    
    def test_analyze_python_bare_except(self):
        """Test detection of bare except clauses"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('try:\n    pass\nexcept:\n    pass\n')
            f.flush()
            
            issues = self.analyzer.analyze_file(f.name)
            
            except_issues = [i for i in issues if i.issue_type == 'bare_except']
            self.assertEqual(len(except_issues), 1)
            self.assertEqual(except_issues[0].severity, 'warning')
            
            os.unlink(f.name)
    
    def test_analyze_javascript_console_log(self):
        """Test detection of console.log statements"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
            f.write('console.log("Debug message");\n')
            f.flush()
            
            issues = self.analyzer.analyze_file(f.name)
            
            console_issues = [i for i in issues if i.issue_type == 'console_log']
            self.assertEqual(len(console_issues), 1)
            self.assertEqual(console_issues[0].severity, 'warning')
            
            os.unlink(f.name)
    
    def test_analyze_trailing_whitespace(self):
        """Test detection of trailing whitespace"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write('line with spaces   \n')
            f.flush()
            
            issues = self.analyzer.analyze_file(f.name)
            
            whitespace_issues = [i for i in issues if i.issue_type == 'trailing_whitespace']
            self.assertEqual(len(whitespace_issues), 1)
            self.assertEqual(whitespace_issues[0].severity, 'info')
            
            os.unlink(f.name)
    
    def test_analyze_long_lines(self):
        """Test detection of long lines"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            long_line = 'x' * 150  # Create a line longer than 120 characters
            f.write(f'{long_line}\n')
            f.flush()
            
            issues = self.analyzer.analyze_file(f.name)
            
            long_line_issues = [i for i in issues if i.issue_type == 'long_line']
            self.assertEqual(len(long_line_issues), 1)
            self.assertEqual(long_line_issues[0].severity, 'info')
            
            os.unlink(f.name)
    
    def test_get_summary(self):
        """Test summary generation"""
        # Create some mock issues
        self.analyzer.issues = [
            Issue("test.py", 1, 0, "error", "Test error", "test_error"),
            Issue("test.py", 2, 0, "warning", "Test warning", "test_warning"),
            Issue("test.py", 3, 0, "info", "Test info", "test_info"),
        ]
        
        summary = self.analyzer.get_summary()
        
        self.assertEqual(summary['total_issues'], 3)
        self.assertEqual(summary['severity_breakdown']['error'], 1)
        self.assertEqual(summary['severity_breakdown']['warning'], 1)
        self.assertEqual(summary['severity_breakdown']['info'], 1)


if __name__ == '__main__':
    unittest.main()