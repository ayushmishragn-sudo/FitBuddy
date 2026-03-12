import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))


def get_model(model_name: str = "gemini-1.5-flash-latest"):
    return genai.GenerativeModel(model_name)


def generate_workout_plan(name: str, age: int, weight: str, goal: str, intensity: str) -> str:
    """Generate a personalized 7-day workout plan using Gemini AI."""
    model = get_model()

    prompt = f"""
You are a professional fitness coach. Create a detailed, personalized 7-day workout plan for the following person:

- Name: {name}
- Age: {age} years old
- Weight: {weight} kg
- Fitness Goal: {goal}
- Workout Intensity: {intensity}

Format the response EXACTLY as follows:

## 7-Day Workout Plan for {name}

**Goal:** {goal} | **Intensity:** {intensity.upper()}

---

### Day 1 - [Day Name/Focus]
**Warm-up (5-10 min):**
- [exercise 1]
- [exercise 2]

**Main Workout:**
- [Exercise]: [sets] x [reps/duration]
- [Exercise]: [sets] x [reps/duration]
- [Exercise]: [sets] x [reps/duration]
- [Exercise]: [sets] x [reps/duration]

**Cool-down (5 min):**
- [stretches]

---

[Repeat for Days 2-7, each with different focus areas]

---

### Weekly Summary
[Brief 2-3 sentence summary of the weekly plan and expected progress]

Make the plan realistic, progressive, and tailored specifically to the {goal} goal with {intensity} intensity.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating plan: {str(e)}"


def generate_nutrition_tip(goal: str) -> str:
    """Generate a nutrition/recovery tip based on fitness goal."""
    model = get_model()

    prompt = f"""
You are a certified nutritionist. Provide a concise, practical nutrition and recovery tip for someone with the following fitness goal: {goal}

Format your response as:

## Nutrition & Recovery Tip

**For Your Goal:** {goal}

### 🥗 Nutrition Focus
[2-3 specific nutrition recommendations]

### 💧 Hydration
[1-2 hydration tips]

### 😴 Recovery
[1-2 recovery tips]

### ⚡ Quick Tip
[One powerful actionable tip in bold]

Keep it practical, specific, and motivating. Maximum 200 words total.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating tip: {str(e)}"


def regenerate_plan_with_feedback(
    name: str, age: int, weight: str, goal: str, intensity: str,
    original_plan: str, feedback: str
) -> str:
    """Regenerate a workout plan based on user feedback."""
    model = get_model("gemini-1.5-pro-latest")

    prompt = f"""
You are a professional fitness coach. A client has provided feedback on their workout plan and needs an updated version.

**Client Details:**
- Name: {name}
- Age: {age} years old
- Weight: {weight} kg
- Fitness Goal: {goal}
- Workout Intensity: {intensity}

**Original Plan:**
{original_plan}

**Client Feedback:**
{feedback}

Please create an IMPROVED 7-day workout plan that specifically addresses the feedback while maintaining the original goal.

Format the response EXACTLY as follows:

## Updated 7-Day Workout Plan for {name}

**Goal:** {goal} | **Intensity:** {intensity.upper()}

**Changes Made Based on Your Feedback:** [Brief explanation of what was changed]

---

### Day 1 - [Day Name/Focus]
**Warm-up (5-10 min):**
- [exercise 1]
- [exercise 2]

**Main Workout:**
- [Exercise]: [sets] x [reps/duration]
- [Exercise]: [sets] x [reps/duration]
- [Exercise]: [sets] x [reps/duration]
- [Exercise]: [sets] x [reps/duration]

**Cool-down (5 min):**
- [stretches]

---

[Repeat for Days 2-7]

---

### Weekly Summary
[Brief summary highlighting the improvements made]
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error regenerating plan: {str(e)}"
