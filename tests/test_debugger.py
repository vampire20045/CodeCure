"""
Tests for CodeCure debugger
"""
import unittest
import tempfile
import os
from codecure.debugger import DebugAssistant


class TestDebugAssistant(unittest.TestCase):
    
    def setUp(self):
        self.assistant = DebugAssistant()
    
    def test_debug_file_with_issues(self):
        """Test debugging a file with issues"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('print("Debug message")\n')
            f.flush()
            
            result = self.assistant.debug_file(f.name)
            
            self.assertIn('file_path', result)
            self.assertIn('issues', result)
            self.assertIn('summary', result)
            self.assertIn('suggestions', result)
            
            # Should find the print statement issue
            self.assertGreater(len(result['issues']), 0)
            
            os.unlink(f.name)
    
    def test_debug_file_clean(self):
        """Test debugging a clean file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write('import logging\n\ndef clean_function():\n    logging.info("Clean message")\n')
            f.flush()
            
            result = self.assistant.debug_file(f.name)
            
            # Should have no major issues
            error_issues = [i for i in result['issues'] if i['severity'] == 'error']
            self.assertEqual(len(error_issues), 0)
            
            os.unlink(f.name)
    
    def test_generate_report_multiple_files(self):
        """Test generating report for multiple files"""
        files = []
        
        # Create temporary files
        for i, content in enumerate([
            'print("File 1")\n',
            'console.log("File 2");\n',
            'def clean_function():\n    pass\n'
        ]):
            suffix = '.py' if i == 0 or i == 2 else '.js'
            with tempfile.NamedTemporaryFile(mode='w', suffix=suffix, delete=False) as f:
                f.write(content)
                f.flush()
                files.append(f.name)
        
        try:
            report = self.assistant.generate_report(files)
            
            self.assertEqual(report['files_analyzed'], 3)
            self.assertIn('total_issues', report)
            self.assertIn('severity_breakdown', report)
            self.assertIn('file_results', report)
            self.assertIn('overall_suggestions', report)
            
            # Should have some issues from the first two files
            self.assertGreater(report['total_issues'], 0)
            
        finally:
            # Clean up
            for file_path in files:
                os.unlink(file_path)
    
    def test_suggest_fixes(self):
        """Test fix suggestions for different issue types"""
        from codecure.analyzer import Issue
        
        # Test syntax error suggestions
        syntax_issue = Issue("test.py", 1, 0, "error", "Syntax error", "syntax_error")
        fixes = self.assistant.suggest_fixes(syntax_issue)
        self.assertGreater(len(fixes), 0)
        self.assertTrue(any("parentheses" in fix for fix in fixes))
        
        # Test print statement suggestions
        print_issue = Issue("test.py", 1, 0, "warning", "Print statement", "print_statement")
        fixes = self.assistant.suggest_fixes(print_issue)
        self.assertGreater(len(fixes), 0)
        self.assertTrue(any("logging" in fix for fix in fixes))


if __name__ == '__main__':
    unittest.main()