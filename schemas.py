from datetime import datetime

from pydantic import BaseModel,ConfigDict,Field,EmailStr,Field 


class userbase(BaseModel):
    username: str = Field(min_length=1, max_length=50)
    email:EmailStr =Field( max_length=150)
     
class usercreate(userbase):
    password: str =Field(min_length=8)
    
class userpublic(BaseModel):
   model_config = ConfigDict(from_attributes=True)
    
   id:int
   username: str
   image_file: str | None
   image_path :str
   
class userprivate(userpublic):
    email: EmailStr
        
   
class userupdate(BaseModel):
    username: str |None= Field(default=None, min_length=1, max_length=50)
    email:EmailStr |None =Field( default=None, max_length=150)
    

class Token(BaseModel):
    access_token:str 
    token_type: str 
    
class Postbase(BaseModel):
    title:str =Field(min_length=1,max_length=100)
    content:str=Field(min_length=1,max_length=100)
    
    
class Postcreate(Postbase):
   pass 
    
class Postupdate(BaseModel):
    title:str |None =Field(default=None, min_length=1,max_length=100)
    content:str|None =Field(default=None,min_length=1)

class Postresponse(Postbase):
    model_config = ConfigDict(from_attributes=True)
     
    
    id:int
    user_id:int
    date_posted: datetime
    author: userpublic
    
class PaginatedPostsResponse(BaseModel):
    posts: list[Postresponse]
    total: int
    skip: int
    limit: int
    has_more: bool   


class ForgotPasswordRequest(BaseModel):
    email: EmailStr = Field(max_length=120)
    
    
class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8)


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)