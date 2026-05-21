"""
Simple script to run the backend server
Usage: python backend/run.py
"""
import uvicorn
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("=" * 60)
    print("Starting Github Bug Detection Backend Server")
    print("=" * 60)
    print()
    print("Server will be available at:")
    print("  - http://localhost:8000")
    print("  - http://127.0.0.1:8000")
    print()
    print("API Documentation:")
    print("  - http://localhost:8000/docs (Swagger UI)")
    print("  - http://localhost:8000/redoc (ReDoc)")
    print()
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    print()
    
    # Run the server
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
