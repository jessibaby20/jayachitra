from pathlib import Path
from fastapi import APIRouter,Depends,Form,HTTPException,Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import get_db,User,save_user,save_plan,update_plan
from .schemas import UserInput,FeedbackRequest
from .gemini_generator import generate_workout_gemini
from .gemini_flash_generator import generate_nutrition_tip_with_flash
from .updated_plan import update_workout_plan
router=APIRouter()
templates=Jinja2Templates(directory=str(Path(__file__).resolve().parent/"templates"))
def ctx(request,**kwargs): return {"request":request,**kwargs}
@router.get("/",response_class=HTMLResponse)
def home(request:Request): return templates.TemplateResponse(request=request,name="index.html",context=ctx(request))
@router.post("/generate-workout",response_class=HTMLResponse)
def generate_workout(request:Request,user_id:str=Form(...),name:str=Form(...),age:int=Form(...),weight:float=Form(...),goal:str=Form(...),intensity:str=Form(...),db:Session=Depends(get_db)):
    try:
        data=UserInput(user_id=user_id,name=name,age=age,weight=weight,goal=goal,intensity=intensity)
        user=save_user(db,data); workout=generate_workout_gemini(data.name,data.age,data.weight,data.goal,data.intensity); tip=generate_nutrition_tip_with_flash(data.goal)
        plan=save_plan(db,user,workout,tip)
        return templates.TemplateResponse(request=request,name="result.html",context=ctx(request,user=user,plan=plan,message=None))
    except ValueError as e:
        return templates.TemplateResponse(request=request,name="index.html",context=ctx(request,error=str(e)),status_code=400)
@router.post("/submit-feedback",response_class=HTMLResponse)
def submit_feedback(request:Request,user_id:str=Form(...),feedback:str=Form(...),db:Session=Depends(get_db)):
    data=FeedbackRequest(user_id=user_id,feedback=feedback)
    user=db.query(User).filter(User.user_id==data.user_id).first()
    if not user or not user.plans: raise HTTPException(404,"User or plan not found")
    plan=user.plans[-1]; revised=update_workout_plan(plan.original_plan,data.feedback,user.goal,user.intensity); update_plan(db,plan,revised,data.feedback)
    return templates.TemplateResponse(request=request,name="result.html",context=ctx(request,user=user,plan=plan,message="Your plan was updated successfully."))
@router.get("/view-all-users",response_class=HTMLResponse)
def view_all_users(request:Request,db:Session=Depends(get_db)):
    return templates.TemplateResponse(request=request,name="all_users.html",context=ctx(request,users=db.query(User).order_by(User.created_at.desc()).all()))
@router.get("/api/health")
def health(): return {"status":"ok","service":"fitbuddy"}
@router.post("/api/users")
def create_user(data:UserInput,db:Session=Depends(get_db)):
    u=save_user(db,data); return {"id":u.id,"user_id":u.user_id,"name":u.name}
@router.post("/api/generate-workout")
def api_generate(data:UserInput,db:Session=Depends(get_db)):
    u=save_user(db,data); w=generate_workout_gemini(data.name,data.age,data.weight,data.goal,data.intensity); t=generate_nutrition_tip_with_flash(data.goal); p=save_plan(db,u,w,t)
    return {"user_id":u.user_id,"plan_id":p.id,"workout_plan":w,"nutrition_tip":t}
@router.post("/api/feedback")
def api_feedback(data:FeedbackRequest,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.user_id==data.user_id).first()
    if not u or not u.plans: raise HTTPException(404,"User or plan not found")
    p=u.plans[-1]; revised=update_workout_plan(p.original_plan,data.feedback,u.goal,u.intensity); update_plan(db,p,revised,data.feedback)
    return {"user_id":u.user_id,"plan_id":p.id,"updated_plan":revised}
@router.get("/api/users")
def api_users(db:Session=Depends(get_db)):
    return [{"id":u.id,"user_id":u.user_id,"name":u.name,"age":u.age,"weight":u.weight,"goal":u.goal,"intensity":u.intensity,"plans":len(u.plans)} for u in db.query(User).all()]
@router.get("/api/users/{user_id}")
def api_user(user_id:str,db:Session=Depends(get_db)):
    u=db.query(User).filter(User.user_id==user_id).first()
    if not u: raise HTTPException(404,"User not found")
    return {"id":u.id,"user_id":u.user_id,"name":u.name,"age":u.age,"weight":u.weight,"goal":u.goal,"intensity":u.intensity,"plans":[{"id":p.id,"original_plan":p.original_plan,"updated_plan":p.updated_plan,"nutrition_tip":p.nutrition_tip,"feedback":p.feedback} for p in u.plans]}
