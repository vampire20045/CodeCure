"""
Debugging assistant that provides intelligent suggestions
"""
from typing import List, Dict, Any
from .analyzer import Issue, CodeAnalyzer


class DebugAssistant:
    """Provides debugging suggestions and fixes for code issues"""
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
    
    def debug_file(self, file_path: str) -> Dict[str, Any]:
        """Debug a file and provide comprehensive analysis"""
        issues = self.analyzer.analyze_file(file_path)
        
        return {
            'file_path': file_path,
            'issues': [self._format_issue(issue) for issue in issues],
            'summary': self.analyzer.get_summary(),
            'suggestions': self._generate_suggestions(issues)
        }
    
    def _format_issue(self, issue: Issue) -> Dict[str, Any]:
        """Format an issue for output"""
        return {
            'location': f"{issue.file_path}:{issue.line_number}:{issue.column}",
            'severity': issue.severity,
            'message': issue.message,
            'type': issue.issue_type,
            'suggestion': issue.suggestion
        }
    
    def _generate_suggestions(self, issues: List[Issue]) -> List[str]:
        """Generate general debugging suggestions based on found issues"""
        suggestions = []
        
        error_count = sum(1 for issue in issues if issue.severity == 'error')
        warning_count = sum(1 for issue in issues if issue.severity == 'warning')
        
        if error_count > 0:
            suggestions.append("⚠️  Fix syntax errors first - they prevent code execution")
        
        if warning_count > 0:
            suggestions.append("🔍 Review warnings to improve code quality and prevent bugs")
        
        # Specific suggestions based on issue types
        issue_types = set(issue.issue_type for issue in issues)
        
        if 'print_statement' in issue_types:
            suggestions.append("📝 Consider implementing proper logging for better debugging")
        
        if 'bare_except' in issue_types:
            suggestions.append("🎯 Use specific exception handling for better error debugging")
        
        if 'console_log' in issue_types:
            suggestions.append("🚀 Remove console.log statements before production deployment")
        
        if 'todo_comment' in issue_types:
            suggestions.append("📋 Track TODO items in your issue tracker for better project management")
        
        if not suggestions:
            suggestions.append("✅ Great! No major issues found. Your code looks good!")
        
        return suggestions
    
    def suggest_fixes(self, issue: Issue) -> List[str]:
        """Provide specific fix suggestions for an issue"""
        fixes = []
        
        if issue.issue_type == 'syntax_error':
            fixes = [
                "Check for missing or extra parentheses",
                "Verify proper indentation (Python uses 4 spaces)",
                "Ensure quotes are properly closed",
                "Check for missing colons after if/for/while statements"
            ]
        
        elif issue.issue_type == 'print_statement':
            fixes = [
                "Replace print() with logging.info() or logging.debug()",
                "Import logging module: import logging",
                "Set up logging configuration in your main function"
            ]
        
        elif issue.issue_type == 'bare_except':
            fixes = [
                "Replace 'except:' with 'except Exception as e:'",
                "Catch specific exceptions like 'except ValueError:'",
                "Log the exception details for debugging"
            ]
        
        elif issue.issue_type == 'console_log':
            fixes = [
                "Remove console.log() statements",
                "Use a proper logging library",
                "Consider using debugger statements for development"
            ]
        
        elif issue.issue_type == 'trailing_whitespace':
            fixes = [
                "Configure your editor to remove trailing whitespace",
                "Use a linter to automatically fix whitespace issues",
                "Run a formatter like Black (Python) or Prettier (JS)"
            ]
        
        elif issue.issue_type == 'long_line':
            fixes = [
                "Break long lines at logical points",
                "Use parentheses for line continuation",
                "Extract complex expressions into variables"
            ]
        
        else:
            fixes = ["Review the code manually", "Consult language-specific best practices"]
        
        return fixes
    
    def generate_report(self, file_paths: List[str]) -> Dict[str, Any]:
        """Generate a comprehensive debugging report for multiple files"""
        all_results = []
        total_issues = 0
        
        for file_path in file_paths:
            result = self.debug_file(file_path)
            all_results.append(result)
            total_issues += len(result['issues'])
        
        # Overall statistics
        severity_totals = {'error': 0, 'warning': 0, 'info': 0}
        for result in all_results:
            for issue in result['issues']:
                severity_totals[issue['severity']] = severity_totals.get(issue['severity'], 0) + 1
        
        return {
            'files_analyzed': len(file_paths),
            'total_issues': total_issues,
            'severity_breakdown': severity_totals,
            'file_results': all_results,
            'overall_suggestions': self._generate_overall_suggestions(all_results)
        }
    
    def _generate_overall_suggestions(self, results: List[Dict[str, Any]]) -> List[str]:
        """Generate overall suggestions for the entire codebase"""
        suggestions = []
        
        total_errors = sum(result['summary']['severity_breakdown'].get('error', 0) for result in results)
        total_warnings = sum(result['summary']['severity_breakdown'].get('warning', 0) for result in results)
        
        if total_errors == 0 and total_warnings == 0:
            suggestions.append("🎉 Excellent! No major issues found across your codebase")
        
        if total_errors > 0:
            suggestions.append(f"🚨 Priority: Fix {total_errors} error(s) to ensure code runs properly")
        
        if total_warnings > 5:
            suggestions.append(f"⚠️  Consider addressing {total_warnings} warning(s) to improve code quality")
        
        # Check for patterns across files
        all_issue_types = set()
        for result in results:
            for issue in result['issues']:
                all_issue_types.add(issue['type'])
        
        if 'print_statement' in all_issue_types or 'console_log' in all_issue_types:
            suggestions.append("🔧 Set up a consistent logging strategy across your project")
        
        if 'trailing_whitespace' in all_issue_types or 'long_line' in all_issue_types:
            suggestions.append("📐 Consider setting up code formatting tools (Black, Prettier, etc.)")
        
        if 'todo_comment' in all_issue_types:
            suggestions.append("📝 Create a proper backlog for your TODO items")
        
        return suggestions