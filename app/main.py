from fastapi import FastAPI, Request
from app.routers.todo import router
from app.routers.user import router as user_router

app = FastAPI( title="Todo Management API",
    description="CRUD APIs for Todo Application",
    version="1.0.0",
    contact={
        "name": "Deekshitha",
        "email": "deekshitha@example.com"
    }
)

# Middleware intercepts every request before it reaches the router
# and every response before it is returned to the client.
@app.middleware("http")
async def log_requests(
    request: Request,
    call_next
):
    print(
        f"Request: {request.method} {request.url.path}"
    )
    response = await call_next(request)
    print(
        f"Response Status: {response.status_code}"
    )
    return response

app.include_router(router)
app.include_router(user_router)