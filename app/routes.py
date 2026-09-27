import os
from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.schemas import UserInput, FeedbackRequest, WorkoutRequest, WorkoutResponse
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.database import (
    save_user,
    save_plan,
    update_plan,
    get_original_plan,
    get_workout_plan,
    get_user,
    get_all_users,
    delete_user_and_plan,
    SessionLocal,
    User,
    WorkoutPlan
)

# Setup Templates Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "templates"))
templates = Jinja2Templates(directory=TEMPLATE_DIR)

router = APIRouter()


# ==========================================
# Frontend Web Routes (HTML Views)
# ==========================================

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    """Returns the homepage (index.html) with the user input form."""
    return templates.TemplateResponse(request,"index.html", {"request": request})


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout_web(
    request: Request,
    username: str = Form(...),
    user_id: int = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...)
):
    """
    Plan Generator:
    - Receives user inputs from index.html form
    - Generates 7-day workout via Gemini 1.5 Pro
    - Generates nutrition tip via Gemini Flash
    - Stores user and plan in SQLite database
    - Renders result.html
    """
    user_input = {
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity
    }

    # Generate AI Workout and Nutrition Tip
    workout_plan = generate_workout_gemini(user_input)
    nutrition_tip = generate_nutrition_tip_with_flash(goal)

    # Persist in Database
    save_user(
        user_id=user_id,
        name=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity
    )
    save_plan(user_id=user_id, plan=workout_plan)

    return templates.TemplateResponse(request,"result.html", {
        "request": request,
        "username": username,
        "user_id": user_id,
        "age": age,
        "weight": weight,
        "goal": goal,
        "intensity": intensity,
        "workout_plan": workout_plan,
        "original_plan": workout_plan,
        "updated_plan": None,
        "nutrition_tip": nutrition_tip,
        "is_updated": False,
        "confirmation_message": None
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback_web(
    request: Request,
    user_id: int = Form(...),
    feedback: str = Form(...)
):
    """
    Update Plan with Feedback:
    - Captures feedback and user_id
    - Retrieves original plan from DB
    - Uses Gemini 1.5 Pro to revise plan
    - Updates revised plan in DB
    - Renders updated result on result.html with confirmation
    """
    user = get_user(user_id)
    if not user:
        # If user record doesn't exist, provide a helpful error message
        return templates.TemplateResponse(request,"result.html", {
            "request": request,
            "username": "User",
            "user_id": user_id,
            "age": "N/A",
            "weight": "N/A",
            "goal": "Fitness",
            "intensity": "Medium",
            "workout_plan": "No registered plan found for this User ID. Please generate a plan first on the Home page.",
            "original_plan": None,
            "updated_plan": None,
            "nutrition_tip": "Stay hydrated and consult a trainer before beginning any new fitness routine.",
            "is_updated": False,
            "error_message": f"User ID {user_id} was not found. Please ensure you entered the correct ID."
        })

    original_plan = get_original_plan(user_id)
    if not original_plan:
        original_plan = "No original plan found."

    # Revise plan using Gemini 1.5 Pro
    revised_plan = update_workout_plan(original_plan, feedback)
    update_plan(user_id, revised_plan)

    # Re-fetch fresh nutrition tip
    nutrition_tip = generate_nutrition_tip_with_flash(user.goal)

    return templates.TemplateResponse(request,"result.html", {
        "request": request,
        "username": user.name,
        "user_id": user.id,
        "age": user.age,
        "weight": user.weight,
        "goal": user.goal,
        "intensity": user.intensity,
        "workout_plan": revised_plan,
        "original_plan": original_plan,
        "updated_plan": revised_plan,
        "nutrition_tip": nutrition_tip,
        "is_updated": True,
        "confirmation_message": "Your plan has been updated based on your feedback!"
    })


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    """
    Admin View of All Users:
    - Queries all registered users and their workout plans
    - Displays structured table with original and updated plans
    """
    db = SessionLocal()
    try:
        users = db.query(User).all()
        user_data = []
        for u in users:
            plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == u.id).first()
            user_data.append({
                "id": u.id,
                "name": u.name,
                "age": u.age,
                "weight": u.weight,
                "goal": u.goal,
                "intensity": u.intensity,
                "original_plan": plan.original_plan if plan else "N/A",
                "updated_plan": plan.updated_plan if (plan and plan.updated_plan) else "Not updated"
            })
        return templates.TemplateResponse(request,"all_users.html", {
            "request": request,
            "users": user_data
        })
    finally:
        db.close()


@router.post("/delete-user/{user_id}", response_class=HTMLResponse)
def delete_user_route(request: Request, user_id: int):
    """Admin route to delete a user and associated plan."""
    delete_user_and_plan(user_id)
    return RedirectResponse(url="/view-all-users", status_code=status.HTTP_303_SEE_OTHER)


# ==========================================
# REST API Endpoints (as defined in PDF)
# ==========================================

# 1. API: Generate workout using Gemini Pro
@router.post("/generate-workout/gemini")
async def generate_gemini_workout(request: WorkoutRequest):
    """API endpoint to generate workout using Gemini Pro."""
    try:
        result = generate_workout_gemini({
            "goal": request.goal,
            "intensity": request.intensity
        })
        return {"model": "gemini-pro", "workout_plan": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 2. API: Generate nutrition tip using Gemini Flash
@router.get("/nutrition-tip")
def get_flash_tip(goal: str):
    """API endpoint to generate nutrition tip using Gemini Flash."""
    tip = generate_nutrition_tip_with_flash(goal)
    return {"goal": goal, "nutrition_tip": tip}


# 3. API: Save user info and plan generation route
@router.post("/generate-plan")
def generate_plan(user_data: UserInput):
    """API endpoint to save user and generate personalized 7-day workout."""
    try:
        save_user(
            user_id=user_data.user_id,
            name=user_data.username,
            age=user_data.age,
            weight=user_data.weight,
            goal=user_data.goal,
            intensity=user_data.intensity
        )
        plan = generate_workout_gemini({
            "goal": user_data.goal,
            "intensity": user_data.intensity,
            "age": user_data.age,
            "weight": user_data.weight
        })
        save_plan(user_data.user_id, plan)
        return {
            "message": "Workout plan generated and saved successfully!",
            "workout_plan": plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Something went wrong: {str(e)}")


# 4. API: Update workout plan based on user feedback
@router.post("/update-plan/{user_id}")
def update_user_plan(user_id: int, data: FeedbackRequest):
    """API endpoint to revise workout plan based on feedback."""
    original = get_original_plan(user_id)
    if not original:
        return {"error": "Original plan not found for this user."}
    updated = update_workout_plan(original, data.feedback)
    update_plan(user_id, updated)
    return {"updated_plan": updated}
   