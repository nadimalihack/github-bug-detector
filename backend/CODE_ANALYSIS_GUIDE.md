# Code Analysis Guide

## What Gets Analyzed

The system performs static code analysis on every commit to detect:

### 🔴 Critical Issues (Security Risks)

#### SQL Injection
- **Pattern**: String concatenation in SQL queries
- **Example**: `"SELECT * FROM users WHERE id = '" + userId + "'"`
- **Fix**: Use parameterized queries or prepared statements
- **Impact**: Attackers can execute arbitrary SQL, steal or delete data

#### Hardcoded Passwords
- **Pattern**: Password variables with string values
- **Example**: `password = "admin123"`
- **Fix**: Use environment variables or secure credential storage
- **Impact**: Credentials exposed in source code, major security risk

#### eval() Usage
- **Pattern**: Using eval() function
- **Example**: `eval(userInput)`
- **Fix**: Use JSON.parse() or safer alternatives
- **Impact**: Can execute arbitrary code, major security vulnerability

### 🟠 High Severity Issues

#### Empty Catch Blocks
- **Pattern**: Catch blocks with no error handling
- **Example**: `catch (error) { }`
- **Fix**: Add error logging or proper error handling
- **Impact**: Errors are swallowed, making debugging impossible

#### Try Without Catch
- **Pattern**: Try blocks without catch
- **Example**: `try { riskyCode() }`
- **Fix**: Add a catch block to handle potential errors
- **Impact**: Errors may crash the application or go unnoticed

#### Bare Except (Python)
- **Pattern**: `except:` without exception type
- **Example**: `except:`
- **Fix**: Specify exception types: `except ValueError, TypeError:`
- **Impact**: Can hide bugs by catching system exits and keyboard interrupts

#### Mutable Default Arguments (Python)
- **Pattern**: Lists/dicts as default parameters
- **Example**: `def func(items=[])`
- **Fix**: Use None as default and create list/dict inside function
- **Impact**: Default value is shared across all calls, causing unexpected behavior

### 🟡 Medium Severity Issues

#### Loose Equality
- **Pattern**: Using == instead of ===
- **Example**: `if (value == null)`
- **Fix**: Replace == with === for strict equality
- **Impact**: Loose equality can cause unexpected type coercion bugs

#### var Usage (JavaScript)
- **Pattern**: Using var keyword
- **Example**: `var count = 0`
- **Fix**: Replace var with let (for variables) or const (for constants)
- **Impact**: var has function scope and hoisting issues

#### Deprecated API Usage
- **Pattern**: innerHTML, document.write, etc.
- **Example**: `element.innerHTML = userInput`
- **Fix**: Use modern alternatives (textContent, createElement)
- **Impact**: May not work in future versions, potential XSS vulnerabilities

### 🟢 Low Severity Issues

#### Console Statements
- **Pattern**: console.log, console.debug, etc.
- **Example**: `console.log("Debug info")`
- **Fix**: Remove console statements or use proper logging
- **Impact**: Can expose sensitive data and clutter production logs

#### TODO/FIXME Comments
- **Pattern**: TODO, FIXME, HACK, XXX comments
- **Example**: `// TODO: Fix this later`
- **Fix**: Complete the TODO or create a proper issue tracker ticket
- **Impact**: Indicates incomplete or temporary code

#### Magic Numbers
- **Pattern**: Large numeric literals in code
- **Example**: `if (count > 86400)`
- **Fix**: Define named constants for better code readability
- **Impact**: Reduces code maintainability and clarity

## How It Works

1. **Fetch Commits**: Pulls commit history from GitHub
2. **Extract Diffs**: Gets code changes from each commit
3. **Pattern Matching**: Uses regex to detect known issues
4. **Severity Assignment**: Categorizes issues by severity
5. **Risk Adjustment**: Increases file risk scores based on issues found
6. **Detailed Reporting**: Shows line numbers, code snippets, and fixes

## Supported Languages

- JavaScript/TypeScript
- Python
- Java
- C/C++
- Go
- Ruby
- PHP

## Example Output

```json
{
  "file": "auth.js",
  "risk_score": 0.85,
  "reason": "High bug frequency (5/10 commits) | 2 critical code issues detected",
  "critical_issues": 2,
  "high_issues": 3,
  "detailed_issues": [
    {
      "type": "sql_injection",
      "severity": "critical",
      "message": "Potential SQL injection vulnerability",
      "line": 42,
      "code_snippet": "query = 'SELECT * FROM users WHERE id = ' + userId",
      "fix": "Use parameterized queries or prepared statements",
      "impact": "Attackers can execute arbitrary SQL, steal or delete data"
    }
  ]
}
```

## Best Practices

1. **Fix Critical Issues First**: Address security vulnerabilities immediately
2. **Review High Severity**: These can cause serious bugs
3. **Plan Medium/Low Fixes**: Schedule time to improve code quality
4. **Use in CI/CD**: Integrate into your build pipeline
5. **Track Progress**: Monitor issue counts over time

## Limitations

- **Pattern-Based**: May have false positives/negatives
- **No Context**: Doesn't understand business logic
- **Static Only**: Doesn't execute code
- **Language Coverage**: Best for JavaScript/Python

## Future Enhancements

- [ ] More language-specific rules
- [ ] Custom rule configuration
- [ ] Integration with ESLint/Pylint
- [ ] AI-powered code review
- [ ] Performance analysis
- [ ] Code complexity metrics
