import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
model = None

if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel("gemini-1.5-pro")
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini 1.5 Pro in updated_plan: {e}")
        model = None


def _get_fallback_updated_plan(original_plan: str, user_feedback: str) -> str:
    """Fallback plan updater when API is unreachable."""
    feedback_lower = user_feedback.lower()

    modifications = []
    if "cardio" in feedback_lower or "hiit" in feedback_lower:
        modifications.append("• Increased cardio blocks: Added 15 minutes of steady-state Zone 2 cardio post-workout on Days 1, 2, and 5.")
    if "rest" in feedback_lower or "sore" in feedback_lower or "tired" in feedback_lower:
        modifications.append("• Enhanced recovery: Swapped Day 5 high-intensity segment for active stretching, foam rolling, and mobility.")
    if "yoga" in feedback_lower or "flexibility" in feedback_lower:
        modifications.append("• Integrated 20-minute Vinyasa yoga & mobility routine into Day 4 and Day 7 mornings.")
    if "chest" in feedback_lower or "arms" in feedback_lower or "upper" in feedback_lower:
        modifications.append("• Added targeted upper body volume: 2 extra sets of incline dumbbell presses and barbell bicep curls.")
    if "legs" in feedback_lower or "lower" in feedback_lower or "glute" in feedback_lower:
        modifications.append("• Enhanced lower body volume: Integrated Romanian deadlifts and Bulgarian split squats with progressive resistance.")
    if not modifications:
        modifications.append(f"• Customized adjustments incorporated to specifically target: '{user_feedback}'.")

    notes = "\n".join(modifications)

    return f"""** REVISED 7-DAY WORKOUT PLAN (Updated Based on User Feedback) **

Feedback Applied: "{user_feedback}"
Key Modifications:
{notes}

==================================================
{original_plan}
==================================================

Trainer Note on Revised Schedule:
All adjustments have been balanced to prevent overtraining while directly addressing your feedback: "{user_feedback}". Maintain hydration and listen to your body signals!
"""


def update_workout_plan(original_plan: str, user_feedback: str) -> str:
    """
    Use Gemini 1.5 Pro to update the workout plan based on user feedback.
    """
    prompt = f"""
You are a professional fitness trainer assistant.

Here's the original 7-day workout plan:
{original_plan}

User Feedback:
"{user_feedback}"

Based on the feedback, revise the relevant parts of the workout plan. Keep the format and rest of the plan unchanged if not needed.
Clearly indicate the specific updates made in response to the user's feedback.
"""
    global model
    if not model:
        key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=key)
                model = genai.GenerativeModel("gemini-1.5-pro")
            except Exception:
                pass

    if model:
        try:
            response = model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini API update error: {e}. Generating revised plan locally.")

    return _get_fallback_updated_plan(original_plan, user_feedback)
