"""
Nutrition and Recovery Helper Module
Provides nutrition calculations, macronutrient recommendations, and hydration guidelines.
"""

def calculate_macros(weight_kg: float, goal: str):
    """Calculate approximate daily macronutrient breakdown based on goal and weight."""
    goal_lower = goal.lower()
    
    # Rough maintenance/target calorie factor
    if "loss" in goal_lower or "cut" in goal_lower:
        calories_per_kg = 26.0
        protein_ratio = 2.0  # g/kg
        fat_percentage = 0.25
    elif "muscle" in goal_lower or "bulk" in goal_lower:
        calories_per_kg = 36.0
        protein_ratio = 2.2  # g/kg
        fat_percentage = 0.25
    else:
        calories_per_kg = 30.0
        protein_ratio = 1.6  # g/kg
        fat_percentage = 0.30

    total_calories = round(weight_kg * calories_per_kg)
    protein_g = round(weight_kg * protein_ratio)
    protein_cals = protein_g * 4
    
    fat_cals = total_calories * fat_percentage
    fat_g = round(fat_cals / 9)
    
    carb_cals = max(0, total_calories - protein_cals - fat_cals)
    carb_g = round(carb_cals / 4)

    return {
        "estimated_calories": total_calories,
        "protein_grams": protein_g,
        "carbs_grams": carb_g,
        "fats_grams": fat_g,
        "hydration_liters": round(weight_kg * 0.035, 1)
    }
