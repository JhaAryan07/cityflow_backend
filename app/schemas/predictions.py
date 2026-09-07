from pydantic import BaseModel, Field


class Prediction(BaseModel):
    horizon: int
    status: str
    current_traffic: float
    predicted_traffic: float
    drivers: list[str]
    source: str = "MODEL_PLACEHOLDER"
