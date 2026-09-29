import logging
from fastapi import FastAPI, Request
from app.database import Base, engine
from app.routers import subscriber, order, auth
from fastapi.responses import JSONResponse

# --- Logging setup ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# --- Create DB tables (if they don't exist yet) ---
Base.metadata.create_all(bind=engine)

# --- App instance ---
app = FastAPI(
    title="Telecom Order Management API",
    description="A backend system for managing fiber subscribers and service orders, "
                 "including feasibility checks and order lifecycle tracking.",
    version="1.0.0"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

# --- Register routers ---
app.include_router(subscriber.router)
app.include_router(order.router)
app.include_router(auth.router)


@app.get("/")
def root():
    logger.info("Root endpoint hit")
    return {"message": "Telecom Order Management API is running",
        "documentation": "/docs",
        "note": "Visit /docs for interactive API documentation and to try out the endpoints"
   }