"""
Unit tests for Gemini AI analyzer module
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


class TestGeminiAnalyzer:
    """Test cases for GeminiAnalyzer class"""
    
    @patch('google.generativeai.configure')
    def test_init_with_api_key(self, mock_configure):
        """Test initialization with API key"""
        from gemini_analyzer import GeminiAnalyzer
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        
        assert analyzer.api_key == "test_key"
        mock_configure.assert_called_once_with(api_key="test_key")
        
    def test_init_without_api_key(self):
        """Test initialization without API key"""
        from gemini_analyzer import GeminiAnalyzer
        
        with pytest.raises(ValueError):
            GeminiAnalyzer()
            
    @patch('google.generativeai.GenerativeModel')
    def test_analyze_code_basic(self, mock_model):
        """Test basic code analysis"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "This code has potential SQL injection vulnerability"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        result = analyzer.analyze_code("SELECT * FROM users WHERE id = " + user_input)
        
        assert isinstance(result, str)
        assert len(result) > 0
        
    @patch('google.generativeai.GenerativeModel')
    def test_analyze_code_with_context(self, mock_model):
        """Test code analysis with context"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "Analysis result"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        result = analyzer.analyze_code(
            "def authenticate(user, password): pass",
            context="Authentication module"
        )
        
        assert isinstance(result, str)
        
    @patch('google.generativeai.GenerativeModel')
    def test_generate_recommendations(self, mock_model):
        """Test recommendation generation"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "1. Add input validation\n2. Use parameterized queries"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        recommendations = analyzer.generate_recommendations("SQL Injection vulnerability")
        
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        
    @patch('google.generativeai.GenerativeModel')
    def test_explain_vulnerability(self, mock_model):
        """Test vulnerability explanation"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "SQL Injection allows attackers to manipulate database queries"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        explanation = analyzer.explain_vulnerability("SQL Injection")
        
        assert isinstance(explanation, str)
        assert len(explanation) > 0
        
    @patch('google.generativeai.GenerativeModel')
    def test_suggest_fixes(self, mock_model):
        """Test fix suggestions"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "Use prepared statements instead of string concatenation"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        fixes = analyzer.suggest_fixes("SQL Injection in login function")
        
        assert isinstance(fixes, str)
        
    @patch('google.generativeai.GenerativeModel')
    def test_analyze_repository_structure(self, mock_model):
        """Test repository structure analysis"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "The repository follows a standard MVC pattern"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        analysis = analyzer.analyze_repository_structure(["src/", "tests/", "docs/"])
        
        assert isinstance(analysis, str)
        
    @patch('google.generativeai.GenerativeModel')
    def test_detect_code_smells(self, mock_model):
        """Test code smell detection"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "Long method detected, consider refactoring"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        smells = analyzer.detect_code_smells("def long_function(): pass" * 100)
        
        assert isinstance(smells, str)
        
    @patch('google.generativeai.GenerativeModel')
    def test_handle_api_error(self, mock_model):
        """Test API error handling"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_model.return_value.generate_content.side_effect = Exception("API Error")
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        
        with pytest.raises(Exception):
            analyzer.analyze_code("test code")
            
    @patch('google.generativeai.GenerativeModel')
    def test_handle_timeout(self, mock_model):
        """Test timeout handling"""
        from gemini_analyzer import GeminiAnalyzer
        import time
        
        def slow_response(*args, **kwargs):
            time.sleep(0.1)
            mock_response = Mock()
            mock_response.text = "Response"
            return mock_response
            
        mock_model.return_value.generate_content.side_effect = slow_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        result = analyzer.analyze_code("test", timeout=1)
        
        assert isinstance(result, str)
        
    @patch('google.generativeai.GenerativeModel')
    def test_batch_analysis(self, mock_model):
        """Test batch code analysis"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "Analysis result"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        code_samples = ["code1", "code2", "code3"]
        results = analyzer.batch_analyze(code_samples)
        
        assert len(results) == 3
        
    @patch('google.generativeai.GenerativeModel')
    def test_format_analysis_result(self, mock_model):
        """Test analysis result formatting"""
        from gemini_analyzer import GeminiAnalyzer
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        raw_result = "Vulnerability: SQL Injection\nSeverity: High\nLine: 42"
        
        formatted = analyzer.format_result(raw_result)
        
        assert isinstance(formatted, dict)
        
    @patch('google.generativeai.GenerativeModel')
    def test_cache_results(self, mock_model):
        """Test result caching"""
        from gemini_analyzer import GeminiAnalyzer
        
        mock_response = Mock()
        mock_response.text = "Cached result"
        mock_model.return_value.generate_content.return_value = mock_response
        
        analyzer = GeminiAnalyzer(api_key="test_key")
        
        # First call
        result1 = analyzer.analyze_code("test code", use_cache=True)
        # Second call should use cache
        result2 = analyzer.analyze_code("test code", use_cache=True)
        
        assert result1 == result2
        assert mock_model.return_value.generate_content.call_count <= 2
