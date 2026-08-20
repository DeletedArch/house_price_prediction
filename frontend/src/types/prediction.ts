export interface PredictionRequest {
  location: string;
  total_sqft: number;
  bath: number;
  bhk: number;
}

export interface PredictionResponse {
  predicted_price: number;
  currency: string;
  features_used: PredictionRequest;
}

export interface ApiError {
  message: string;
  detail?: string;
}
