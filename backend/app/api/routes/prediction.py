from typing import Any, Dict
from fastapi import APIRouter, HTTPException, status

from app.schemas.prediction import PredictionRequest
from app.services.inference import inference_service
from app.utils.logging_config import logger

router = APIRouter(tags=["Prediction"])


@router.get("/health", status_code=status.HTTP_200_OK, tags=["Health"])
def health_check() -> Dict[str, Any]:
    """
    Health check endpoint for the prediction service.
    Verifies that the route is accessible and indicates whether the ML model is loaded.
    """
    is_model_loaded = getattr(inference_service, "model", None) is not None
    return {
        "status": "healthy",
        "service": "prediction_api",
        "model_loaded": is_model_loaded,
    }


@router.post("/predict", status_code=status.HTTP_200_OK)
@router.post("/predict/", status_code=status.HTTP_200_OK, include_in_schema=False)
def predict(request: PredictionRequest) -> Any:
    """
    Predict house price based on input property features.

    Accepts property details in the request body and returns the estimated price.
    """
    try:
        logger.info(f"Received prediction request: {request}")
        result = inference_service.predict(request)
        return result
    except Exception as e:
        logger.error(f"Error during prediction: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction error: {str(e)}",
        )

