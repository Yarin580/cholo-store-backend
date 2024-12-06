

import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from config_section.config import config

from fastapi import FastAPI, Request, HTTPException

from src.api.routes import product_route, category_route, auth_route,order_route
from src.modules.exceptions import CustomException

app = FastAPI()

app.include_router(product_route.product_router)
app.include_router(category_route.category_route)
app.include_router(auth_route.auth_router)
app.include_router(order_route.order_router)

origins = [
    "http://localhost:5173",  # your React app running locally
    # You can also add other origins here as needed, e.g., production URLs
]

# Add CORSMiddleware to your app correctly
app.add_middleware(
    CORSMiddleware,  # Correct way to add the middleware
    allow_origins=origins,  # Allow requests from these origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    raise HTTPException(status_code=exc.error_code,
                         detail=exc.message)

if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=True if config.ENV != "production" else False,
        workers=1,
    )
