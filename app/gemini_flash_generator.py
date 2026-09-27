import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
flash_model = None

if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        flash_model = genai.GenerativeModel("gemini-1.5-flash")
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini Flash: {e}")
        flash_model = None


def _get_fallback_nutrition_tip(goal: str) -> str:
    goal_lower = goal.lower()
    if "muscle" in goal_lower or "bulk" in goal_lower or "strength" in goal_lower:
        return (
            "Prioritize high-quality protein! Aim for 1.6 to 2.2 grams of protein per kilogram of body weight. "
            "Consume a protein-rich snack or shake (such as whey protein, Greek yogurt, or boiled eggs) within 45 minutes "
            "post-workout to optimize muscle protein synthesis and glycogen replenishment."
        )
    elif "loss" in goal_lower or "fat" in goal_lower or "lean" in goal_lower or "cut" in goal_lower:
        return (
            "Focus on dietary fiber and hydration! Drinking 500ml of water 20 minutes before meals improves satiety "
            "and aids digestion. Fill half your plate with leafy greens and cruciferous vegetables to stay in a comfortable "
            "caloric deficit while maintaining steady metabolic energy."
        )
    elif "endurance" in goal_lower or "cardio" in goal_lower or "stamina" in goal_lower:
        return (
            "Optimize your intra-workout and post-workout electrolyte balance! Hydrate with water containing a pinch of "
            "Himalayan pink salt and lemon or coconut water. Pair complex carbohydrates (like oats or sweet potatoes) "
            "with lean protein 2 hours before your workout for sustained cardiovascular stamina."
        )
    else:
        return (
            "Stay consistent with balanced whole foods! Prioritize a colorful variety of seasonal vegetables, lean proteins, "
            "healthy fats (olive oil, avocado, nuts), and drink at least 2.5 to 3 liters of water daily. Consistency is the true "
            "catalyst for long-term vitality and physical wellness."
        )


def generate_nutrition_tip_with_flash(goal: str) -> str:
    """
    Generate a nutrition or recovery tip using Gemini Flash based on the user's fitness goal.

    Args:
        goal (str): User's fitness goal - "weight loss", "muscle gain", or "general fitness".

    Returns:
        str: Generated tip.
    """
    prompt = (
        f"Give one clear, helpful nutrition or recovery tip for someone focused on '{goal}'. "
        "The tip should be practical, friendly, and easy to understand."
    )

    global flash_model
    if not flash_model:
        key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=key)
                flash_model = genai.GenerativeModel("gemini-1.5-flash")
            except Exception:
                pass

    if flash_model:
        try:
            response = flash_model.generate_content(prompt)
            if response and response.text:
                return response.text.strip()
        except Exception as e:
            print(f"Gemini Flash generation error: {e}. Using expert curated tip.")

    return _get_fallback_nutrition_tip(goal)
