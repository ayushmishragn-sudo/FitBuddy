from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.database import get_db, User, WorkoutPlan
from app.routes.ai_service import (
    generate_workout_plan,
    generate_nutrition_tip,
    regenerate_plan_with_feedback,
)

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/generate", response_class=HTMLResponse)
async def generate_plan(
    request: Request,
    name: str = Form(...),
    age: int = Form(...),
    weight: str = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
    db: Session = Depends(get_db),
):
    # Validate inputs
    if age < 10 or age > 100:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Please enter a valid age between 10 and 100."},
        )
    try:
        weight_val = float(weight)
        if weight_val < 20 or weight_val > 300:
            raise ValueError
    except ValueError:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": "Please enter a valid weight between 20 and 300 kg."},
        )

    # Save user to DB
    user = User(name=name, age=age, weight=weight, goal=goal, intensity=intensity)
    db.add(user)
    db.commit()
    db.refresh(user)

    # Generate plan and tip via AI
    plan_content = generate_workout_plan(name, age, weight, goal, intensity)
    nutrition_tip = generate_nutrition_tip(goal)

    # Save plan to DB
    plan = WorkoutPlan(
        user_id=user.id,
        plan_content=plan_content,
        nutrition_tip=nutrition_tip,
    )
    db.add(plan)
    db.commit()
    db.refresh(plan)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user,
            "plan": plan,
            "plan_id": plan.id,
        },
    )


@router.post("/feedback/{plan_id}", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    plan_id: int,
    feedback: str = Form(...),
    db: Session = Depends(get_db),
):
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    user = db.query(User).filter(User.id == plan.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not feedback.strip():
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "user": user,
                "plan": plan,
                "plan_id": plan.id,
                "error": "Please enter your feedback before submitting.",
            },
        )

    # Regenerate plan with feedback
    updated_plan_content = regenerate_plan_with_feedback(
        name=user.name,
        age=user.age,
        weight=user.weight,
        goal=user.goal,
        intensity=user.intensity,
        original_plan=plan.plan_content,
        feedback=feedback,
    )

    # Update plan in DB
    plan.plan_content = updated_plan_content
    plan.feedback = feedback
    plan.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(plan)

    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "user": user,
            "plan": plan,
            "plan_id": plan.id,
            "feedback_success": True,
        },
    )


@router.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    plans = db.query(WorkoutPlan).all()

    # Build user+plan map
    user_plans = []
    for user in users:
        user_plan = db.query(WorkoutPlan).filter(WorkoutPlan.user_id == user.id).first()
        user_plans.append({"user": user, "plan": user_plan})

    total_users = len(users)
    goals = {}
    for user in users:
        goals[user.goal] = goals.get(user.goal, 0) + 1

    return templates.TemplateResponse(
        "all_users.html",
        {
            "request": request,
            "user_plans": user_plans,
            "total_users": total_users,
            "goals": goals,
        },
    )


@router.get("/plan/{plan_id}", response_class=HTMLResponse)
async def view_plan(request: Request, plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(WorkoutPlan).filter(WorkoutPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    user = db.query(User).filter(User.id == plan.user_id).first()
    return templates.TemplateResponse(
        "result.html",
        {"request": request, "user": user, "plan": plan, "plan_id": plan.id},
    )
