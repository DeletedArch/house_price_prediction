import pickle
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes import prediction
from app.services.inference import inference_service
from app.utils.logging_config import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle application startup and shutdown events.
    Loads ML model and artifacts on startup and releases resources on shutdown.
    """
    # Startup: Load ML model
    logger.info(f"Starting up {settings.PROJECT_NAME} v{settings.VERSION}...")
    logger.info(f"Loading ML model from: {settings.MODEL_PATH}")

    try:
        if settings.MODEL_PATH.exists():
            with open(settings.MODEL_PATH, "rb") as f:
                loaded_model = pickle.load(f)
                app.state.model = loaded_model
                inference_service.model = loaded_model
            logger.info("ML model successfully loaded into application state.")
        else:
            logger.warning(
                f"Model file not found at {settings.MODEL_PATH}. "
                "Inference service will use fallback estimator."
            )
            app.state.model = None
    except Exception as e:
        logger.error(f"Error while loading model during startup: {e}")
        app.state.model = None

    yield

    # Shutdown: Cleanup resources
    logger.info(f"Shutting down {settings.PROJECT_NAME}...")
    if hasattr(app.state, "model"):
        app.state.model = None


# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routers
app.include_router(prediction.router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint returning service status and model loading state."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "model_loaded": getattr(app.state, "model", None) is not None,
    }


@app.get("/", tags=["Root"])
def root():
    """Root endpoint providing general API information and documentation links."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "docs": "/docs",
        "redoc": "/redoc",
        "api_v1": settings.API_V1_STR,
    }

