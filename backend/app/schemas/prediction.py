from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    location: str = Field(..., description="Location of the house", example="Whitefield")
    total_sqft: float = Field(..., gt=0, description="Total area in square feet", example=1200.0)
    bath: int = Field(..., ge=1, description="Number of bathrooms", example=2)
    bhk: int = Field(..., ge=1, description="Number of bedrooms (BHK)", example=2)


class PredictionResponse(BaseModel):
    predicted_price: float = Field(..., description="Estimated house price (in Lakhs)")
    currency: str = Field(default="Lakhs", description="Currency/unit representation")
    features_used: PredictionRequest
