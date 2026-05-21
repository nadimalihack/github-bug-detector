"""
Run the backend server from project root
Usage: python run-backend.py
"""
import uvicorn
import sys
import os

# Add the backend directory to Python path
backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
sys.path.insert(0, backend_dir)

if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Starting Github Bug Detection Backend Server")
    print("=" * 60)
    print()
    print("📍 Server will be available at:")
    print("   • http://localhost:8000")
    print("   • http://127.0.0.1:8000")
    print()
    print("📚 API Documentation:")
    print("   • http://localhost:8000/docs (Swagger UI)")
    print("   • http://localhost:8000/redoc (ReDoc)")
    print()
    print("💡 Test the API:")
    print("   • Open http://localhost:8000 in your browser")
    print()
    print("⚠️  Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Run the server
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
