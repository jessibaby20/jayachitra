from .gemini_client import generate
def update_workout_plan(original_plan,feedback,goal,intensity):
    prompt=f'''You are updating a FitBuddy 7-day general fitness plan.
Goal: {goal}; Intensity: {intensity}
Original plan:
{original_plan}
User feedback:
{feedback}
Return a complete revised Day 1–Day 7 plan, not just changes. Preserve useful parts, incorporate reasonable feedback, and keep it safe and adaptable. Do not provide medical diagnosis, extreme dieting, or dangerous exercise instructions.'''
    return generate(prompt) or original_plan+f"\n\nUPDATED NOTES\nFeedback incorporated: {feedback}"
