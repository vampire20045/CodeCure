#!/usr/bin/env python3
"""
CodeCure - Main CLI interface for debugging code
"""
import argparse
import json
import sys
from pathlib import Path
from typing import List

from .debugger import DebugAssistant
from . import __version__


def format_issue_output(issue: dict, show_suggestions: bool = True) -> str:
    """Format a single issue for console output"""
    severity_icons = {
        'error': '❌',
        'warning': '⚠️ ',
        'info': 'ℹ️ '
    }
    
    icon = severity_icons.get(issue['severity'], '•')
    output = f"{icon} {issue['location']}: {issue['message']}"
    
    if show_suggestions and issue.get('suggestion'):
        output += f"\n   💡 {issue['suggestion']}"
    
    return output


def print_summary(summary: dict):
    """Print analysis summary"""
    print("\n" + "="*50)
    print("📊 ANALYSIS SUMMARY")
    print("="*50)
    
    total = summary['total_issues']
    if total == 0:
        print("✅ No issues found! Your code looks great.")
        return
    
    print(f"Total issues found: {total}")
    
    if 'severity_breakdown' in summary:
        breakdown = summary['severity_breakdown']
        if breakdown.get('error', 0) > 0:
            print(f"❌ Errors: {breakdown['error']}")
        if breakdown.get('warning', 0) > 0:
            print(f"⚠️  Warnings: {breakdown['warning']}")
        if breakdown.get('info', 0) > 0:
            print(f"ℹ️  Info: {breakdown['info']}")


def print_suggestions(suggestions: List[str]):
    """Print debugging suggestions"""
    if not suggestions:
        return
    
    print("\n" + "="*50)
    print("💡 SUGGESTIONS")
    print("="*50)
    
    for suggestion in suggestions:
        print(f"  {suggestion}")


def analyze_single_file(file_path: str, args):
    """Analyze a single file"""
    assistant = DebugAssistant()
    
    print(f"🔍 Analyzing: {file_path}")
    result = assistant.debug_file(file_path)
    
    if args.json:
        print(json.dumps(result, indent=2))
        return
    
    # Console output
    if result['issues']:
        print(f"\n📋 Issues found in {file_path}:")
        for issue in result['issues']:
            print(f"  {format_issue_output(issue, args.show_suggestions)}")
    else:
        print(f"✅ No issues found in {file_path}")
    
    if not args.quiet:
        print_summary(result['summary'])
        print_suggestions(result['suggestions'])


def analyze_multiple_files(file_paths: List[str], args):
    """Analyze multiple files"""
    assistant = DebugAssistant()
    
    print(f"🔍 Analyzing {len(file_paths)} files...")
    report = assistant.generate_report(file_paths)
    
    if args.json:
        print(json.dumps(report, indent=2))
        return
    
    # Console output
    for result in report['file_results']:
        file_path = result['file_path']
        issues = result['issues']
        
        print(f"\n📁 {file_path}")
        if issues:
            for issue in issues:
                print(f"  {format_issue_output(issue, args.show_suggestions)}")
        else:
            print("  ✅ No issues found")
    
    if not args.quiet:
        print_summary({
            'total_issues': report['total_issues'],
            'severity_breakdown': report['severity_breakdown']
        })
        print_suggestions(report['overall_suggestions'])


def find_source_files(directory: str, extensions: List[str]) -> List[str]:
    """Find source files in a directory"""
    path = Path(directory)
    files = []
    
    for ext in extensions:
        files.extend(path.rglob(f"*.{ext}"))
    
    return [str(f) for f in files]


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="CodeCure - An intelligent debugging assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  codecure --analyze myfile.py                    # Analyze single file
  codecure --analyze *.py                         # Analyze Python files
  codecure --directory src --extensions py js     # Analyze directory
  codecure --analyze myfile.py --json             # Output as JSON
        """
    )
    
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'CodeCure {__version__}'
    )
    
    parser.add_argument(
        '--analyze', '-a',
        nargs='+',
        help='Files to analyze'
    )
    
    parser.add_argument(
        '--directory', '-d',
        help='Directory to analyze recursively'
    )
    
    parser.add_argument(
        '--extensions', '-e',
        nargs='+',
        default=['py', 'js', 'ts'],
        help='File extensions to analyze (default: py js ts)'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Suppress summary and suggestions'
    )
    
    parser.add_argument(
        '--no-suggestions',
        action='store_true',
        help='Hide fix suggestions'
    )
    
    args = parser.parse_args()
    args.show_suggestions = not args.no_suggestions
    
    # Determine files to analyze
    files_to_analyze = []
    
    if args.analyze:
        # Handle glob patterns and individual files
        for pattern in args.analyze:
            path = Path(pattern)
            if path.is_file():
                files_to_analyze.append(str(path))
            elif '*' in pattern:
                # Simple glob handling
                from glob import glob
                files_to_analyze.extend(glob(pattern))
            else:
                print(f"Warning: {pattern} is not a valid file", file=sys.stderr)
    
    elif args.directory:
        files_to_analyze = find_source_files(args.directory, args.extensions)
        if not files_to_analyze:
            print(f"No source files found in {args.directory}")
            return 1
    
    else:
        parser.print_help()
        return 1
    
    if not files_to_analyze:
        print("No files to analyze")
        return 1
    
    # Analyze files
    try:
        if len(files_to_analyze) == 1:
            analyze_single_file(files_to_analyze[0], args)
        else:
            analyze_multiple_files(files_to_analyze, args)
        
        return 0
    
    except KeyboardInterrupt:
        print("\nAnalysis interrupted by user")
        return 1
    except Exception as e:
        print(f"Error during analysis: {e}", file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())