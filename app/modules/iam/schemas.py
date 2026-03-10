from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# 前端传过来的注册表单
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="密码至少6位")

# 返回给前端的用户信息卡片
class UserResponse(BaseModel):
    id: str
    email: str
    tier: str
    is_active: bool
    auth_provider: str
    pro_expire_date: Optional[datetime] = None

    class Config:
        from_attributes = True # 允许兼容 SQLAlchemy 对象 (Pydantic V2 写法)