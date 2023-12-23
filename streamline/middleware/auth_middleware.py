from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from streamline.core.config import settings
import traceback


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Skip authentication for open endpoints
            if request.url.path in ["/docs", "/redoc", "/openapi.json"]:
                return await call_next(request)
            token = request.headers.get('Token')
            # Example condition that might raise an exception
            if not token or token != settings.API_KEY:
                return JSONResponse(
                    status_code=status.HTTP_403_FORBIDDEN,
                    content={"detail": "Unauthorized: Invalid or missing API key"},
                )
            return await call_next(request)

        except Exception as e:
            traceback.print_exc()  # Print the full traceback for debugging
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
