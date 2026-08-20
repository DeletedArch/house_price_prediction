from pydantic import BaseModel, Field, ConfigDict


class PredictionRequest(BaseModel):
    location: str = Field(
        ...,
        description="Location/locality of the property",
        examples=["Whitefield"],
    )
    carpet_area_sqft: float = Field(
        ...,
        gt=0,
        description="Carpet area in square feet (must be greater than 0)",
        examples=[1200.0],
    )
    floor_num: int = Field(
        ...,
        ge=0,
        description="Floor number of the property (0 represents ground floor)",
        examples=[2],
    )
    bathroom: int = Field(
        ...,
        ge=0,
        description="Number of bathrooms",
        examples=[2],
    )
    balcony: int = Field(
        ...,
        ge=0,
        description="Number of balconies",
        examples=[1],
    )
    furnishing: str = Field(
        ...,
        description="Furnishing status ('Furnished', 'Semi-Furnished', 'Unfurnished')",
        examples=["Semi-Furnished"],
    )
    transaction: str = Field(
        ...,
        description="Transaction type ('New Property', 'Resale')",
        examples=["Resale"],
    )
    ownership: str = Field(
        ...,
        description="Ownership type (e.g. 'Freehold', 'Leasehold')",
        examples=["Freehold"],
    )
    facing: str = Field(
        ...,
        description="Facing direction (e.g. 'East', 'North', 'North-East')",
        examples=["East"],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "location": "Whitefield",
                "carpet_area_sqft": 1200.0,
                "floor_num": 2,
                "bathroom": 2,
                "balcony": 1,
                "furnishing": "Semi-Furnished",
                "transaction": "Resale",
                "ownership": "Freehold",
                "facing": "East",
            }
        }
    )


class PredictionResponse(BaseModel):
    predicted_price: float = Field(
        ...,
        description="Predicted price of the property (in ₹)",
        examples=[6500000.0],
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "predicted_price": 6500000.0
            }
        }
    )