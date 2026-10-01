from pydantic import BaseModel,Field,field_validator
class UserInput(BaseModel):
    user_id:str=Field(min_length=1,max_length=100)
    name:str=Field(min_length=1,max_length=120)
    age:int=Field(ge=13,le=100)
    weight:float=Field(gt=0,le=500)
    goal:str=Field(min_length=2,max_length=100)
    intensity:str
    @field_validator("intensity")
    @classmethod
    def valid_intensity(cls,v):
        v=v.strip().lower()
        if v not in {"low","medium","high"}: raise ValueError("Intensity must be low, medium, or high")
        return v
    @field_validator("name","user_id","goal")
    @classmethod
    def strip_text(cls,v):
        v=v.strip()
        if not v: raise ValueError("Value cannot be empty")
        return v
class FeedbackRequest(BaseModel):
    user_id:str=Field(min_length=1,max_length=100)
    feedback:str=Field(min_length=3,max_length=2000)
