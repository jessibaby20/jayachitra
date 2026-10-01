from .gemini_client import generate
def _fallback(name,goal,intensity):
    return f'''FITBUDDY 7-DAY PLAN FOR {name.upper()}
Goal: {goal}
Intensity: {intensity}

Day 1 – Full Body
Warm-up: 5–10 minutes of easy movement.
Main: Squats 2×10, wall/incline push-ups 2×8, glute bridges 2×12.
Cooldown: 5 minutes gentle stretching.

Day 2 – Cardio
Warm-up: 5 minutes.
Main: 20–30 minutes of comfortable walking or cycling with easy intervals.
Cooldown: 5 minutes.

Day 3 – Recovery & Mobility
Gentle mobility, stretching, and an easy walk. Keep the effort light.

Day 4 – Upper Body + Core
Warm-up: 5–10 minutes.
Main: Incline push-ups 2×8, resistance-row movement 2×10, bird-dog 2×8/side.
Cooldown: 5 minutes.

Day 5 – Lower Body
Warm-up: 5–10 minutes.
Main: Squats 2×10, reverse lunges 2×8/side, calf raises 2×12.
Cooldown: 5 minutes.

Day 6 – Light Cardio + Mobility
20–30 minutes of easy activity followed by gentle mobility.

Day 7 – Rest
Full rest or an easy walk. Reflect on how the week felt.

Safety: Adjust or stop any activity that causes pain, dizziness, or unusual symptoms.'''
def generate_workout_gemini(name,age,weight,goal,intensity):
    prompt=f'''You are FitBuddy, a conservative wellness-planning assistant.
Create a clear 7-day general fitness plan for Name={name}, Age={age}, Weight={weight} kg, Goal={goal}, Intensity={intensity}.
Return plain text with exactly Day 1 through Day 7. Each day should include focus, warm-up, main activity with sets/reps or duration where sensible, and cooldown/recovery.
Avoid diagnosing conditions, extreme dieting, dangerous challenges, or unsafe exercise. Keep it practical and adaptable. Include a short safety note.'''
    return generate(prompt) or _fallback(name,goal,intensity)
