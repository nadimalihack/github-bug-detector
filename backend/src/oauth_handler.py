"""
GitHub OAuth Authentication Handler
"""
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
import httpx
from dotenv import load_dotenv

load_dotenv()

class OAuthHandler:
    def __init__(self):
        self.client_id = os.getenv('GITHUB_CLIENT_ID')
        self.client_secret = os.getenv('GITHUB_CLIENT_SECRET')
        self.redirect_uri = os.getenv('OAUTH_REDIRECT_URI', 'http://localhost:3000/auth/callback')
        self.jwt_secret = os.getenv('JWT_SECRET_KEY', 'change-this-secret')
        self.jwt_algorithm = os.getenv('JWT_ALGORITHM', 'HS256')
        self.jwt_expiration = int(os.getenv('JWT_EXPIRATION_HOURS', '24'))
    
    def get_authorization_url(self) -> str:
        """Generate GitHub OAuth authorization URL"""
        return f"https://github.com/login/oauth/authorize?client_id={self.client_id}&redirect_uri={self.redirect_uri}&scope=repo,user"
    
    async def exchange_code_for_token(self, code: str) -> dict:
        """Exchange authorization code for access token"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                'https://github.com/login/oauth/access_token',
                data={
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                    'code': code,
                    'redirect_uri': self.redirect_uri
                },
                headers={'Accept': 'application/json'}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to exchange code")
            
            return response.json()
    
    async def get_user_info(self, access_token: str) -> dict:
        """Get GitHub user information"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://api.github.com/user',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")
            
            return response.json()
    
    async def get_user_repos(self, access_token: str) -> list:
        """Get user's GitHub repositories"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                'https://api.github.com/user/repos?sort=updated&per_page=50',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Accept': 'application/json'
                }
            )
            
            if response.status_code != 200:
                return []
            
            return response.json()
    
    def create_jwt_token(self, user_data: dict) -> str:
        """Create JWT token for session management"""
        expire = datetime.utcnow() + timedelta(hours=self.jwt_expiration)
        to_encode = {
            'sub': str(user_data['id']),
            'username': user_data['login'],
            'email': user_data.get('email'),
            'avatar': user_data.get('avatar_url'),
            'exp': expire
        }
        return jwt.encode(to_encode, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def verify_jwt_token(self, token: str) -> Optional[dict]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            return payload
        except JWTError:
            return None
