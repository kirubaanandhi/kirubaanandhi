import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
model = None

if API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=API_KEY)
        # Try gemini-1.5-pro as specified in the project milestone
        model = genai.GenerativeModel("gemini-1.5-pro")
    except Exception as e:
        print(f"Warning: Failed to initialize Gemini 1.5 Pro: {e}")
        model = None


def _get_fallback_workout(goal: str, intensity: str) -> str:
    """Fallback generator in case Gemini API key is missing or quota is exhausted."""
    intensity_adj = {
        "low": ("2 sets of 10-12 reps", "1-2 minutes rest between sets", "light bodyweight focus"),
        "medium": ("3 sets of 8-12 reps", "60-90 seconds rest", "moderate resistance & tempo"),
        "high": ("4 sets of 6-10 reps / HIIT circuits", "45-60 seconds rest", "high intensity explosive training")
    }.get(intensity.lower(), ("3 sets of 10 reps", "60 seconds rest", "balanced approach"))

    sets_reps, rest, style = intensity_adj

    return f"""** 7-Day Personalized Workout Plan for {goal.title()} ({intensity.capitalize()} Intensity) **

Goal: {goal} | Intensity: {intensity.capitalize()} ({style})

Day 1: Upper Body Push & Core
Warm-up:
- Arm circles (forward and backward, 1 min each)
- Shoulder rotations & dynamic chest openers (2 mins)
- Light jumping jacks or high knees (2 mins)
Main Workout:
- Push-ups / Dumbbell Chest Press: {sets_reps}
- Overhead Shoulder Press: {sets_reps}
- Tricep Dips or Tricep Kickbacks: {sets_reps}
- Plank Hold: 3 sets of 45-60 seconds
- Bicycle Crunches: 3 sets of 20 reps
Cooldown:
- Static chest and shoulder stretch, child's pose (5 mins). Rest: {rest}.

Day 2: Lower Body Strength & Stability
Warm-up:
- Bodyweight squats & leg swings (3 mins)
- Glute bridges & hip openers (3 mins)
Main Workout:
- Goblet Squats / Barbell Squats: {sets_reps}
- Romanian Deadlifts (RDLs): {sets_reps}
- Walking Lunges: {sets_reps} (each leg)
- Standing Calf Raises: 3 sets of 15 reps
- Wall Sit: 3 sets of 45 seconds
Cooldown:
- Quad stretch, hamstring stretch, pigeon stretch (5 mins).

Day 3: HIIT Cardio & Core Conditioning
Warm-up:
- Light jog in place, jumping rope or shadow boxing (5 mins)
Main Workout:
- Mountain Climbers: 3 sets of 40 seconds
- Jump Squats / Fast Squats: {sets_reps}
- Kettlebell Swings or Dumbbell Snatch: {sets_reps}
- Russian Twists: 3 sets of 20 reps per side
- High Plank with Shoulder Taps: 3 sets of 30 seconds
Cooldown:
- Cat-Cow stretch, deep diaphragmatic breathing, cobra pose (5 mins).

Day 4: Active Recovery & Mobility
Warm-up:
- Gentle joint rotations from neck to ankles (5 mins)
Main Workout:
- 30-45 minutes brisk outdoor walk or gentle swimming
- Full-body yoga flow focusing on hip and thoracic spine mobility
- Foam rolling for calves, quads, and upper back (10 mins)
Cooldown:
- Deep relaxation in Savasana (5 mins). Hydrate with electrolytes.

Day 5: Upper Body Pull & Posterior Chain
Warm-up:
- Band pull-aparts & torso twists (3 mins)
- Scapular wall slides & wrist stretches (2 mins)
Main Workout:
- Bent-over Rows (Dumbbell or Barbell): {sets_reps}
- Lat Pulldowns or Assisted Pull-ups: {sets_reps}
- Dumbbell Bicep Curls: {sets_reps}
- Face Pulls or Rear Delt Flyes: {sets_reps}
- Superman Back Extensions: 3 sets of 15 reps
Cooldown:
- Lat stretch on wall, doorway chest stretch, neck relaxation (5 mins).

Day 6: Lower Body Power & Core Endurance
Warm-up:
- Ankle mobility drills & bodyweight lunges (3 mins)
- High knees and butt kicks (2 mins)
Main Workout:
- Bulgarian Split Squats: {sets_reps} (each leg)
- Hip Thrusts / Glute Bridges with weight: {sets_reps}
- Kettlebell / Dumbbell Sumo Squats: {sets_reps}
- Hanging Leg Raises or Reverse Crunches: 3 sets of 12 reps
- Side Plank: 3 sets of 30 seconds per side
Cooldown:
- Butterfly stretch, lying figure-4 glute stretch, foam rolling (5 mins).

Day 7: Rest, Full Body Restoration & Reflection
Warm-up:
- Gentle morning mobility stretch (5 mins)
Main Workout:
- Complete rest day or optional 20-minute restorative nature stroll
- Hydration check: Aim for 3-4 liters of water today
- Review weekly wins and set intention for week 2!
Cooldown:
- Evening meditation or deep breathing (5-10 mins).

** Important Notes: **
* Progressive Overload: Gradually increase resistance or reps as your stamina builds.
* Proper Form: Always maintain neutral spine and engage core during every movement.
* Recovery: Prioritize 7-8 hours of sound sleep every night for optimal muscle protein synthesis.
"""


def generate_workout_gemini(user_input: dict) -> str:
    """
    Generate personalized 7-day workout plan using Gemini 1.5 Pro.
    Falls back gracefully if API key is not configured or network error occurs.
    """
    prompt = f"""
You are a professional fitness trainer.

Create a personalized, structured 7-day workout plan for someone with the goal of "{user_input.get('goal', 'fitness')}", and prefers "{user_input.get('intensity', 'medium')}" intensity workouts.
User Age: {user_input.get('age', 'N/A')}, Weight: {user_input.get('weight', 'N/A')} kg.

Each day must include:
- A warm-up (5-10 mins)
- Main workout (targeted exercises, sets & reps)
- Cooldown or recovery tip

Format:
Day 1:
Warm-up: ...
Main Workout: ...
Cooldown: ...
(Repeat for Day 2-7)

Include progressive overload and safety instructions at the end.
"""
    global model
    # Attempt to reload model if key was added
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
            print(f"Gemini API generation error: {e}. Switching to tailored local plan.")

    # Tailored intelligent fallback
    return _get_fallback_workout(user_input.get("goal", "general fitness"), user_input.get("intensity", "medium"))
