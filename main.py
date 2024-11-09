from src.core.app import create_app
from src.core.router import register_routers

app = create_app()
register_routers(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 