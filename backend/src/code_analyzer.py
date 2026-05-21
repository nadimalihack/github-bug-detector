"""Code Quality Analyzer - Detects errors, code smells, and potential bugs"""
import re
from typing import Dict, List, Tuple

class CodeAnalyzer:
    """Analyzes code for common errors and code smells"""
    
    def __init__(self):
        # Common error patterns
        self.error_patterns = {
            'null_check': {
                'pattern': r'(==\s*null|!=\s*null)',
                'severity': 'medium',
                'message': 'Use strict equality (=== null) instead of loose equality',
                'fix': 'Replace == with === or != with !== for null checks',
                'impact': 'Loose equality can cause unexpected type coercion bugs'
            },
            'console_log': {
                'pattern': r'console\.(log|debug|info)',
                'severity': 'low',
                'message': 'Console statements left in code',
                'fix': 'Remove console statements or use proper logging',
                'impact': 'Can expose sensitive data and clutter production logs'
            },
            'todo_fixme': {
                'pattern': r'(TODO|FIXME|HACK|XXX)',
                'severity': 'low',
                'message': 'Unresolved TODO/FIXME comments',
                'fix': 'Complete the TODO or create a proper issue tracker ticket',
                'impact': 'Indicates incomplete or temporary code'
            },
            'try_without_catch': {
                'pattern': r'try\s*\{[^}]*\}\s*(?!catch)',
                'severity': 'high',
                'message': 'Try block without catch - potential unhandled errors',
                'fix': 'Add a catch block to handle potential errors',
                'impact': 'Errors may crash the application or go unnoticed'
            },
            'eval_usage': {
                'pattern': r'\beval\s*\(',
                'severity': 'critical',
                'message': 'eval() usage - security risk',
                'fix': 'Use JSON.parse() or safer alternatives instead of eval()',
                'impact': 'Can execute arbitrary code, major security vulnerability'
            },
            'sql_injection': {
                'pattern': r'(SELECT|INSERT|UPDATE|DELETE).*\+.*["\']',
                'severity': 'critical',
                'message': 'Potential SQL injection vulnerability',
                'fix': 'Use parameterized queries or prepared statements',
                'impact': 'Attackers can execute arbitrary SQL, steal or delete data'
            },
            'hardcoded_password': {
                'pattern': r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']',
                'severity': 'critical',
                'message': 'Hardcoded password detected',
                'fix': 'Use environment variables or secure credential storage',
                'impact': 'Credentials exposed in source code, major security risk'
            },
            'deprecated_api': {
                'pattern': r'(var\s+|\.innerHTML\s*=|document\.write)',
                'severity': 'medium',
                'message': 'Deprecated API usage',
                'fix': 'Use modern alternatives (let/const, textContent, createElement)',
                'impact': 'May not work in future versions, potential XSS vulnerabilities'
            },
            'empty_catch': {
                'pattern': r'catch\s*\([^)]*\)\s*\{\s*\}',
                'severity': 'high',
                'message': 'Empty catch block - errors silently ignored',
                'fix': 'Add error logging or proper error handling',
                'impact': 'Errors are swallowed, making debugging impossible'
            },
            'magic_numbers': {
                'pattern': r'(?<![a-zA-Z0-9_])[0-9]{4,}(?![a-zA-Z0-9_])',
                'severity': 'low',
                'message': 'Magic numbers - consider using constants',
                'fix': 'Define named constants for better code readability',
                'impact': 'Reduces code maintainability and clarity'
            }
        }
        
        # Language-specific patterns
        self.language_patterns = {
            'python': {
                'bare_except': {
                    'pattern': r'except\s*:',
                    'severity': 'high',
                    'message': 'Bare except clause - catches all exceptions',
                    'fix': 'Specify exception types: except ValueError, TypeError:',
                    'impact': 'Can hide bugs by catching system exits and keyboard interrupts'
                },
                'mutable_default': {
                    'pattern': r'def\s+\w+\([^)]*=\s*(\[\]|\{\})',
                    'severity': 'high',
                    'message': 'Mutable default argument',
                    'fix': 'Use None as default and create list/dict inside function',
                    'impact': 'Default value is shared across all calls, causing unexpected behavior'
                }
            },
            'javascript': {
                'var_usage': {
                    'pattern': r'\bvar\s+',
                    'severity': 'medium',
                    'message': 'Use let/const instead of var',
                    'fix': 'Replace var with let (for variables) or const (for constants)',
                    'impact': 'var has function scope and hoisting issues'
                },
                'double_equals': {
                    'pattern': r'[^=!]==[^=]',
                    'severity': 'medium',
                    'message': 'Use === instead of ==',
                    'fix': 'Replace == with === for strict equality comparison',
                    'impact': 'Loose equality can cause unexpected type coercion'
                }
            }
        }
    
    def analyze_code(self, code: str, filename: str = '') -> Dict:
        """Analyze code for errors and code smells"""
        if not code or not code.strip():
            return {
                'issues': [],
                'severity_counts': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
                'total_issues': 0
            }
        
        issues = []
        
        # Detect language from filename
        language = self._detect_language(filename)
        
        # Check common patterns
        for name, pattern_info in self.error_patterns.items():
            matches = re.finditer(pattern_info['pattern'], code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                issues.append({
                    'type': name,
                    'severity': pattern_info['severity'],
                    'message': pattern_info['message'],
                    'line': line_num,
                    'code_snippet': self._get_line(code, line_num),
                    'fix': pattern_info.get('fix', 'Review and fix this issue'),
                    'impact': pattern_info.get('impact', 'May cause bugs or security issues')
                })
        
        # Check language-specific patterns
        if language in self.language_patterns:
            for name, pattern_info in self.language_patterns[language].items():
                matches = re.finditer(pattern_info['pattern'], code, re.IGNORECASE)
                for match in matches:
                    line_num = code[:match.start()].count('\n') + 1
                    issues.append({
                        'type': name,
                        'severity': pattern_info['severity'],
                        'message': pattern_info['message'],
                        'line': line_num,
                        'code_snippet': self._get_line(code, line_num),
                        'fix': pattern_info.get('fix', 'Review and fix this issue'),
                        'impact': pattern_info.get('impact', 'May cause bugs or security issues')
                    })
        
        # Count by severity
        severity_counts = {
            'critical': sum(1 for i in issues if i['severity'] == 'critical'),
            'high': sum(1 for i in issues if i['severity'] == 'high'),
            'medium': sum(1 for i in issues if i['severity'] == 'medium'),
            'low': sum(1 for i in issues if i['severity'] == 'low')
        }
        
        # Sort issues by severity (critical first)
        severity_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        issues.sort(key=lambda x: severity_order.get(x['severity'], 4))
        
        return {
            'issues': issues,
            'severity_counts': severity_counts,
            'total_issues': len(issues),
            'language': language
        }
    
    def analyze_diff(self, diff: str, filename: str = '') -> Dict:
        """Analyze code changes in a diff"""
        if not diff:
            return {'issues': [], 'severity_counts': {}, 'total_issues': 0}
        
        # Extract added lines (lines starting with +)
        added_lines = []
        for line in diff.split('\n'):
            if line.startswith('+') and not line.startswith('+++'):
                added_lines.append(line[1:])  # Remove the + prefix
        
        added_code = '\n'.join(added_lines)
        return self.analyze_code(added_code, filename)
    
    def calculate_code_quality_score(self, analysis: Dict) -> float:
        """Calculate a code quality score (0-1, higher is better)"""
        if analysis['total_issues'] == 0:
            return 1.0
        
        # Weight by severity
        severity_weights = {
            'critical': 1.0,
            'high': 0.7,
            'medium': 0.4,
            'low': 0.2
        }
        
        weighted_issues = sum(
            analysis['severity_counts'].get(severity, 0) * weight
            for severity, weight in severity_weights.items()
        )
        
        # Normalize to 0-1 scale (assuming 10 weighted issues = 0 quality)
        quality_score = max(0, 1 - (weighted_issues / 10))
        return round(quality_score, 2)
    
    def _detect_language(self, filename: str) -> str:
        """Detect programming language from filename"""
        ext_map = {
            '.py': 'python',
            '.js': 'javascript',
            '.jsx': 'javascript',
            '.ts': 'javascript',
            '.tsx': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rb': 'ruby',
            '.php': 'php'
        }
        
        for ext, lang in ext_map.items():
            if filename.endswith(ext):
                return lang
        
        return 'unknown'
    
    def _get_line(self, code: str, line_num: int) -> str:
        """Get a specific line from code"""
        lines = code.split('\n')
        if 0 < line_num <= len(lines):
            return lines[line_num - 1].strip()
        return ''
