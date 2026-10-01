from .gemini_client import generate
def _fallback(goal):
    g=goal.lower()
    if g=="muscle gain": return "Include a protein-rich food with regular meals and stay hydrated; recovery and adequate sleep matter too."
    if g=="weight loss": return "Build meals around vegetables, protein, whole grains or other filling foods, and water rather than relying on restrictive dieting."
    return "Choose balanced meals, drink enough water, and give your body time to recover between demanding activities."
def generate_nutrition_tip_with_flash(goal):
    prompt=f'''Give one concise, practical nutrition or recovery tip for a person whose fitness goal is "{goal}". Keep it general wellness information. Do not prescribe a medical diet, supplements, or extreme calorie restriction. Return 2–3 sentences maximum.'''
    return generate(prompt) or _fallback(goal)
