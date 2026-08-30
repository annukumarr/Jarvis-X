"""
JARVIS-X Production Entry Point

Purpose:
Start the existing FastAPI application in a
cloud-compatible production environment.

This file does NOT modify the JARVIS-X API logic.
"""

import os

import uvicorn


# ==========================================================
# CONFIGURATION
# ==========================================================

HOST = "0.0.0.0"

PORT = int(
    os.getenv(
        "PORT",
        "8000"
    )
)


# ==========================================================
# SERVER
# ==========================================================

if __name__ == "__main__":

    uvicorn.run(
        "api.server:app",
        host=HOST,
        port=PORT,
        reload=False,
    )
    