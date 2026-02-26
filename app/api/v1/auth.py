from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    接收前端传来的账号密码，验证通过后发放 JWT 令牌
    """
    # ⚠️ TODO: 未来这里将替换为去数据库查询 `User` 表
    # 模拟数据库查询比对：
    if form_data.username != "admin@longi-latam.com" or form_data.password != "888888":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="账号或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 1. 模拟查库获取到的真实 ID
    mock_user_id = "u-12345"
    mock_company_id = "comp-longi-999" # 核心：他属于隆基拉美分公司
    mock_role = "ADMIN"

    # 2. 制作 Token 载荷 (Payload)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": mock_user_id,          # 规定俗成的用户标识字段
            "company_id": mock_company_id, # 🌟 多租户强隔离的灵魂烙印
            "role": mock_role
        },
        expires_delta=access_token_expires
    )
    
    # 3. 返回标准的 OAuth2 令牌格式给 Flutter 前端
    return {"access_token": access_token, "token_type": "bearer"}