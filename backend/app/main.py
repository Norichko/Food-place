from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, restaurants, dishes, reviews, recommendations
from fastapi.openapi.utils import get_openapi

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(dishes.router, prefix="/dishes", tags=["dishes"])
app.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
app.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])

@app.get("/")
def root():
    return {"message": "API работает"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="FoodPlace API",
        version="1.0.0",
        description="Документация API FoodPlace",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT"
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
