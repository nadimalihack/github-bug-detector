"""
Unit tests for OAuth handler module
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
from pathlib import Path

backend_path = Path(__file__).parent.parent.parent / "backend" / "src"
sys.path.insert(0, str(backend_path))


class TestOAuthHandler:
    """Test cases for OAuth handler"""
    
    def test_generate_authorization_url(self):
        """Test OAuth authorization URL generation"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        url = handler.generate_authorization_url()
        
        assert "github.com/login/oauth/authorize" in url
        assert "client_id=test_client_id" in url
        
    def test_generate_authorization_url_with_state(self):
        """Test authorization URL with state parameter"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        url = handler.generate_authorization_url(state="random_state")
        
        assert "state=random_state" in url
        
    @patch('requests.post')
    def test_exchange_code_for_token_success(self, mock_post):
        """Test successful token exchange"""
        from oauth_handler import OAuthHandler
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "access_token": "gho_test_token",
            "token_type": "bearer"
        }
        mock_post.return_value = mock_response
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        token = handler.exchange_code_for_token("auth_code")
        
        assert token == "gho_test_token"
        
    @patch('requests.post')
    def test_exchange_code_for_token_failure(self, mock_post):
        """Test failed token exchange"""
        from oauth_handler import OAuthHandler
        
        mock_response = Mock()
        mock_response.json.return_value = {"error": "invalid_code"}
        mock_post.return_value = mock_response
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        with pytest.raises(Exception):
            handler.exchange_code_for_token("invalid_code")
            
    @patch('requests.get')
    def test_get_user_info_success(self, mock_get):
        """Test successful user info retrieval"""
        from oauth_handler import OAuthHandler
        
        mock_response = Mock()
        mock_response.json.return_value = {
            "id": 12345,
            "login": "testuser",
            "email": "test@example.com",
            "avatar_url": "https://avatars.githubusercontent.com/u/12345"
        }
        mock_get.return_value = mock_response
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        user_info = handler.get_user_info("test_token")
        
        assert user_info["login"] == "testuser"
        assert user_info["email"] == "test@example.com"
        
    @patch('requests.get')
    def test_get_user_info_unauthorized(self, mock_get):
        """Test user info retrieval with invalid token"""
        from oauth_handler import OAuthHandler
        
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"message": "Bad credentials"}
        mock_get.return_value = mock_response
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        with pytest.raises(Exception):
            handler.get_user_info("invalid_token")
            
    def test_generate_jwt_token(self):
        """Test JWT token generation"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret",
            jwt_secret="test_jwt_secret"
        )
        
        user_data = {
            "id": 12345,
            "username": "testuser",
            "email": "test@example.com"
        }
        
        jwt_token = handler.generate_jwt_token(user_data)
        
        assert isinstance(jwt_token, str)
        assert len(jwt_token) > 0
        
    def test_verify_jwt_token_valid(self):
        """Test JWT token verification with valid token"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret",
            jwt_secret="test_jwt_secret"
        )
        
        user_data = {"id": 12345, "username": "testuser"}
        jwt_token = handler.generate_jwt_token(user_data)
        
        decoded = handler.verify_jwt_token(jwt_token)
        
        assert decoded["id"] == 12345
        assert decoded["username"] == "testuser"
        
    def test_verify_jwt_token_invalid(self):
        """Test JWT token verification with invalid token"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret",
            jwt_secret="test_jwt_secret"
        )
        
        with pytest.raises(Exception):
            handler.verify_jwt_token("invalid_token")
            
    def test_verify_jwt_token_expired(self):
        """Test JWT token verification with expired token"""
        from oauth_handler import OAuthHandler
        import time
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret",
            jwt_secret="test_jwt_secret"
        )
        
        user_data = {"id": 12345}
        jwt_token = handler.generate_jwt_token(user_data, expires_in=-1)
        
        time.sleep(2)
        
        with pytest.raises(Exception):
            handler.verify_jwt_token(jwt_token)
            
    def test_refresh_token(self):
        """Test token refresh"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret",
            jwt_secret="test_jwt_secret"
        )
        
        user_data = {"id": 12345, "username": "testuser"}
        old_token = handler.generate_jwt_token(user_data)
        
        new_token = handler.refresh_token(old_token)
        
        assert isinstance(new_token, str)
        assert new_token != old_token
        
    def test_revoke_token(self):
        """Test token revocation"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        result = handler.revoke_token("test_token")
        
        assert result is True
        
    def test_validate_state_parameter(self):
        """Test state parameter validation"""
        from oauth_handler import OAuthHandler
        
        handler = OAuthHandler(
            client_id="test_client_id",
            client_secret="test_secret"
        )
        
        state = handler.generate_state()
        
        assert handler.validate_state(state) is True
        assert handler.validate_state("invalid_state") is False
