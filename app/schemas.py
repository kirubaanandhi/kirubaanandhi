from pydantic import BaseModel, Field
from typing import Optional

class UserInput(BaseModel):
    username: str = Field(..., description="Name of the user", example="Alex Morgan")
    user_id: int = Field(..., description="Unique integer ID for the user", example=101)
    age: int = Field(..., description="Age of user in years", ge=10, le=120, example=25)
    weight: float = Field(..., description="Weight in kilograms", gt=0, example=70.5)
    goal: str = Field(..., description="Fitness objective (e.g. weight loss, muscle gain)", example="muscle gain")
    intensity: str = Field(..., description="Workout intensity: low, medium, high", example="medium")

class FeedbackRequest(BaseModel):
    feedback: str = Field(..., description="User feedback to refine workout plan", example="Include more core and cardio")

class WorkoutRequest(BaseModel):
    goal: str = Field(..., description="Fitness goal", example="weight loss")
    intensity: str = Field(..., description="Intensity level (low, medium, high)", example="high")

class WorkoutResponse(BaseModel):
    model: str
    workout_plan: str

class NutritionResponse(BaseModel):
    goal: str
    nutrition_tip: str

class PlanSaveResponse(BaseModel):
    message: str
    workout_plan: str

class UpdatePlanResponse(BaseModel):
    updated_plan: str
