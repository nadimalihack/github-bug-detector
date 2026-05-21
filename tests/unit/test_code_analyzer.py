"""
Unit tests for code analyzer module
"""
import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


class TestCodeAnalyzer:
    """Test cases for CodeAnalyzer class"""
    
    def test_detect_sql_injection(self, sample_code_snippet):
        """Test SQL injection detection"""
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(sample_code_snippet)
        
        sql_issues = [i for i in issues if i["type"] == "SQL Injection"]
        assert len(sql_issues) > 0
        
    def test_detect_hardcoded_credentials(self, sample_code_snippet):
        """Test hardcoded credentials detection"""
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(sample_code_snippet)
        
        cred_issues = [i for i in issues if "credential" in i["type"].lower() or "secret" in i["type"].lower()]
        assert len(cred_issues) > 0
        
    def test_detect_xss_vulnerability(self):
        """Test XSS vulnerability detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
def render_page(user_input):
    html = f"<div>{user_input}</div>"
    return html
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        xss_issues = [i for i in issues if "xss" in i["type"].lower()]
        assert len(xss_issues) > 0
        
    def test_detect_command_injection(self):
        """Test command injection detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
import os
def execute_command(user_input):
    os.system(f"ls {user_input}")
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        cmd_issues = [i for i in issues if "command" in i["type"].lower()]
        assert len(cmd_issues) > 0
        
    def test_detect_path_traversal(self):
        """Test path traversal detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
def read_file(filename):
    with open(f"/var/data/{filename}", 'r') as f:
        return f.read()
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        path_issues = [i for i in issues if "path" in i["type"].lower()]
        assert len(path_issues) > 0
        
    def test_detect_weak_crypto(self):
        """Test weak cryptography detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
import hashlib
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        crypto_issues = [i for i in issues if "crypto" in i["type"].lower() or "hash" in i["type"].lower()]
        assert len(crypto_issues) > 0
        
    def test_detect_insecure_deserialization(self):
        """Test insecure deserialization detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
import pickle
def load_data(data):
    return pickle.loads(data)
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        deser_issues = [i for i in issues if "deserial" in i["type"].lower() or "pickle" in i["type"].lower()]
        assert len(deser_issues) > 0
        
    def test_detect_xxe_vulnerability(self):
        """Test XXE vulnerability detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
import xml.etree.ElementTree as ET
def parse_xml(xml_string):
    return ET.fromstring(xml_string)
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        xxe_issues = [i for i in issues if "xxe" in i["type"].lower() or "xml" in i["type"].lower()]
        assert len(xxe_issues) > 0
        
    def test_detect_ssrf_vulnerability(self):
        """Test SSRF vulnerability detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
import requests
def fetch_url(url):
    return requests.get(url)
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        ssrf_issues = [i for i in issues if "ssrf" in i["type"].lower()]
        assert len(ssrf_issues) > 0
        
    def test_detect_race_condition(self):
        """Test race condition detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
import threading
counter = 0
def increment():
    global counter
    counter += 1
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        race_issues = [i for i in issues if "race" in i["type"].lower() or "thread" in i["type"].lower()]
        assert len(race_issues) > 0
        
    def test_detect_memory_leak(self):
        """Test memory leak detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
cache = {}
def store_data(key, value):
    cache[key] = value  # Never cleaned up
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        memory_issues = [i for i in issues if "memory" in i["type"].lower() or "leak" in i["type"].lower()]
        assert len(memory_issues) > 0
        
    def test_detect_null_pointer(self):
        """Test null pointer detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
def process_data(data):
    result = data.get('value')
    return result.upper()  # Potential None reference
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        null_issues = [i for i in issues if "null" in i["type"].lower() or "none" in i["type"].lower()]
        assert len(null_issues) > 0
        
    def test_detect_buffer_overflow(self):
        """Test buffer overflow detection"""
        from code_analyzer import CodeAnalyzer
        
        code = """
def copy_data(source):
    buffer = [0] * 10
    for i in range(len(source)):
        buffer[i] = source[i]  # No bounds checking
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        buffer_issues = [i for i in issues if "buffer" in i["type"].lower() or "overflow" in i["type"].lower()]
        assert len(buffer_issues) > 0
        
    def test_detect_code_smell_long_function(self):
        """Test long function code smell detection"""
        from code_analyzer import CodeAnalyzer
        
        code = "def long_function():\n" + "    pass\n" * 100
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        smell_issues = [i for i in issues if "long" in i["type"].lower() or "complex" in i["type"].lower()]
        assert len(smell_issues) > 0
        
    def test_detect_code_smell_too_many_parameters(self):
        """Test too many parameters code smell"""
        from code_analyzer import CodeAnalyzer
        
        code = """
def complex_function(a, b, c, d, e, f, g, h, i, j):
    return a + b + c + d + e + f + g + h + i + j
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        param_issues = [i for i in issues if "parameter" in i["type"].lower()]
        assert len(param_issues) > 0
        
    def test_analyze_empty_code(self):
        """Test analysis of empty code"""
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code("")
        
        assert isinstance(issues, list)
        
    def test_analyze_safe_code(self):
        """Test analysis of safe code"""
        from code_analyzer import CodeAnalyzer
        
        code = """
def add_numbers(a, b):
    return a + b
"""
        
        analyzer = CodeAnalyzer()
        issues = analyzer.analyze_code(code)
        
        assert isinstance(issues, list)
        
    def test_get_severity_level(self):
        """Test severity level assignment"""
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        
        assert analyzer.get_severity("SQL Injection") in ["critical", "high", "medium", "low"]
        assert analyzer.get_severity("Code Smell") in ["critical", "high", "medium", "low"]
        
    def test_generate_recommendations(self):
        """Test recommendation generation"""
        from code_analyzer import CodeAnalyzer
        
        analyzer = CodeAnalyzer()
        recommendations = analyzer.generate_recommendations("SQL Injection")
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
    def test_calculate_code_complexity(self):
        """Test code complexity calculation"""
        from code_analyzer import CodeAnalyzer
        
        code = """
def complex_function(x):
    if x > 0:
        if x < 10:
            for i in range(x):
                if i % 2 == 0:
                    print(i)
    return x
"""
        
        analyzer = CodeAnalyzer()
        complexity = analyzer.calculate_complexity(code)
        
        assert isinstance(complexity, (int, float))
        assert complexity > 1
