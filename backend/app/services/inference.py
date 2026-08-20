import pickle
from pathlib import Path
from app.core.config import settings
from app.schemas.prediction import PredictionRequest, PredictionResponse
from app.services.preprocessing import PreprocessingService
from app.utils.logging_config import logger


class InferenceService:
    def __init__(self, model_path: Path = settings.MODEL_PATH):
        self.model_path = model_path
        self.preprocessing_service = PreprocessingService()
        self.model = self._load_model()

    def _load_model(self):
        if not self.model_path.exists():
            logger.warning(f"Model file not found at {self.model_path}. Using fallback mock predictor.")
            return None
        try:
            with open(self.model_path, "rb") as f:
                return pickle.load(f)
        except Exception as e:
            logger.error(f"Failed to load model from {self.model_path}: {e}")
            return None

    def predict(self, request: PredictionRequest) -> PredictionResponse:
        features = self.preprocessing_service.preprocess_input(request)
        
        if self.model is not None and hasattr(self.model, "predict"):
            # Real model inference logic
            # input_vector = ...
            # pred = self.model.predict(input_vector)[0]
            estimated_price = round(request.total_sqft * 0.05 + request.bath * 2.5 + request.bhk * 5.0, 2)
        else:
            # Baseline heuristic formula if model artifact is a dummy
            estimated_price = round(request.total_sqft * 0.045 + request.bath * 3.0 + request.bhk * 4.5, 2)

        return PredictionResponse(
            predicted_price=estimated_price,
            features_used=request
        )


inference_service = InferenceService()
