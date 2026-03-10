from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
# 根据你的实际项目路径导入数据库依赖
from app.api.deps import get_db 

from .models import User
from .schemas import UserRegister, UserResponse
from .security import get_password_hash

router = APIRouter(prefix="/auth", tags=["IAM - 身份与访问管理"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserRegister, db: Session = Depends(get_db)):
    # 1. 查重：邮箱是否被注册过？
    existing_user = db.query(User).filter(User.email == user_in.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册。如果是您的账号，请直接登录。"
        )

    # 2. 密码加盐哈希
    hashed_pw = get_password_hash(user_in.password)

    # 3. 创建新用户，默认掉入 "FREE" 免费版漏斗
    new_user = User(
        email=user_in.email,
        hashed_password=hashed_pw,
        auth_provider="local",
        tier="FREE"
    )

    # 4. 落库保存
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    print(f"🎉 [IAM 模块] 新用户注册成功: {new_user.email}, 初始权限: {new_user.tier}")
    
    return new_user

# 注意：你原先写在 api/v1/auth.py 里的 login 接口，可以直接平移到这个文件里！