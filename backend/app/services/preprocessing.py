from app.schemas.prediction import PredictionRequest
import numpy as np


class PreprocessingService:
    def __init__(self):
        pass

    def preprocess_input(self, request: PredictionRequest) -> dict:
        """Preprocess incoming request data into feature array or dictionary."""
        return {
            "location": request.location,
            "total_sqft": request.total_sqft,
            "bath": request.bath,
            "bhk": request.bhk,
        }
