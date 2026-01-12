"""
FastAPI application main entry point.
"""

import uvicorn
from fastapi import FastAPI

from api.health import router as health_router
from api import inference




app = FastAPI()


# Include routers
app.include_router(health_router, tags=["system"])
app.include_router(inference.router, prefix="/api/v1")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
