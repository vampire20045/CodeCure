"""
Core code analyzer for detecting bugs and issues
"""
import ast
import re
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Issue:
    """Represents a code issue found during analysis"""
    file_path: str
    line_number: int
    column: int
    severity: str  # 'error', 'warning', 'info'
    message: str
    issue_type: str
    suggestion: Optional[str] = None


class CodeAnalyzer:
    """Main code analyzer that detects various types of issues"""
    
    def __init__(self):
        self.issues: List[Issue] = []
    
    def analyze_file(self, file_path: str) -> List[Issue]:
        """Analyze a single file for issues"""
        self.issues = []
        path = Path(file_path)
        
        if not path.exists():
            self.issues.append(Issue(
                file_path=file_path,
                line_number=0,
                column=0,
                severity='error',
                message=f"File not found: {file_path}",
                issue_type='file_not_found'
            ))
            return self.issues
        
        try:
            content = path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            self.issues.append(Issue(
                file_path=file_path,
                line_number=0,
                column=0,
                severity='error',
                message="File encoding error - cannot read file",
                issue_type='encoding_error'
            ))
            return self.issues
        
        # Determine file type and analyze accordingly
        if file_path.endswith('.py'):
            self._analyze_python(content, file_path)
        elif file_path.endswith(('.js', '.ts')):
            self._analyze_javascript(content, file_path)
        else:
            self._analyze_generic(content, file_path)
        
        return self.issues
    
    def _analyze_python(self, content: str, file_path: str):
        """Analyze Python code for issues"""
        lines = content.split('\n')
        
        # Check for syntax errors
        try:
            ast.parse(content)
        except SyntaxError as e:
            self.issues.append(Issue(
                file_path=file_path,
                line_number=e.lineno or 0,
                column=e.offset or 0,
                severity='error',
                message=f"Syntax error: {e.msg}",
                issue_type='syntax_error',
                suggestion="Check for missing parentheses, quotes, or indentation issues"
            ))
            return
        
        # Check for common Python issues
        for line_num, line in enumerate(lines, 1):
            self._check_python_line(line, line_num, file_path)
    
    def _check_python_line(self, line: str, line_num: int, file_path: str):
        """Check a single Python line for issues"""
        stripped = line.strip()
        
        # Check for print statements (should use logging)
        if 'print(' in line and not line.strip().startswith('#'):
            self.issues.append(Issue(
                file_path=file_path,
                line_number=line_num,
                column=line.find('print('),
                severity='warning',
                message="Consider using logging instead of print for better debugging",
                issue_type='print_statement',
                suggestion="Replace with logging.info() or logging.debug()"
            ))
        
        # Check for bare except clauses
        if re.match(r'\s*except\s*:', line):
            self.issues.append(Issue(
                file_path=file_path,
                line_number=line_num,
                column=line.find('except'),
                severity='warning',
                message="Bare except clause - consider catching specific exceptions",
                issue_type='bare_except',
                suggestion="Use 'except SpecificException:' instead"
            ))
        
        # Check for unused variables (basic pattern)
        if '=' in line and not line.strip().startswith('#'):
            var_match = re.match(r'\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*=', line)
            if var_match and var_match.group(1).startswith('_'):
                pass  # Intentionally unused variable
            elif var_match:
                var_name = var_match.group(1)
                if var_name not in ['self', 'cls'] and len(var_name) > 1:
                    # This is a simplified check - real implementation would need AST analysis
                    pass
        
        # Check for TODO/FIXME comments
        if 'TODO' in line.upper() or 'FIXME' in line.upper():
            self.issues.append(Issue(
                file_path=file_path,
                line_number=line_num,
                column=0,
                severity='info',
                message="TODO/FIXME comment found",
                issue_type='todo_comment',
                suggestion="Consider creating a proper issue tracker item"
            ))
    
    def _analyze_javascript(self, content: str, file_path: str):
        """Analyze JavaScript/TypeScript code for issues"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            stripped = line.strip()
            
            # Check for console.log statements
            if 'console.log(' in line and not line.strip().startswith('//'):
                self.issues.append(Issue(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('console.log('),
                    severity='warning',
                    message="console.log found - consider using proper logging",
                    issue_type='console_log',
                    suggestion="Use a proper logging library for production code"
                ))
            
            # Check for == instead of ===
            if '==' in line and '===' not in line and '!=' in line:
                self.issues.append(Issue(
                    file_path=file_path,
                    line_number=line_num,
                    column=line.find('=='),
                    severity='warning',
                    message="Use === for strict equality comparison",
                    issue_type='loose_equality',
                    suggestion="Replace == with === and != with !=="
                ))
    
    def _analyze_generic(self, content: str, file_path: str):
        """Analyze generic text files for basic issues"""
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check for trailing whitespace
            if line.endswith(' ') or line.endswith('\t'):
                self.issues.append(Issue(
                    file_path=file_path,
                    line_number=line_num,
                    column=len(line.rstrip()),
                    severity='info',
                    message="Trailing whitespace found",
                    issue_type='trailing_whitespace',
                    suggestion="Remove trailing spaces/tabs"
                ))
            
            # Check for very long lines
            if len(line) > 120:
                self.issues.append(Issue(
                    file_path=file_path,
                    line_number=line_num,
                    column=120,
                    severity='info',
                    message="Line too long (>120 characters)",
                    issue_type='long_line',
                    suggestion="Consider breaking the line into multiple lines"
                ))
    
    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of all issues found"""
        severity_counts = {}
        type_counts = {}
        
        for issue in self.issues:
            severity_counts[issue.severity] = severity_counts.get(issue.severity, 0) + 1
            type_counts[issue.issue_type] = type_counts.get(issue.issue_type, 0) + 1
        
        return {
            'total_issues': len(self.issues),
            'severity_breakdown': severity_counts,
            'issue_type_breakdown': type_counts,
            'files_analyzed': len(set(issue.file_path for issue in self.issues))
        }