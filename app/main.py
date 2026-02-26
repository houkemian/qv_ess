from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import simulation, auth # 引入 auth
from app.api.deps import get_current_user_payload

# 导入我们刚刚写好的模拟器路由
from app.api.v1.simulation import router as simulation_router

# 1. 初始化 FastAPI 应用，并配置专业的 Swagger 文档信息
app = FastAPI(
    title="光储大师 (PV + ESS Quote Master) 计算引擎",
    description="面向 2026 年全球市场的 B 端光储财务与物理模拟核心 API。支持 8760 小时能量流闭环与拉美高息/通胀/备电金融测算。",
    version="0.1.0",
)

# 2. 配置 CORS (跨域资源共享)
# 为了方便前期开发，这里允许所有来源("*")。上线时需替换为你的真实 App 域名。
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. 注册核心业务路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"]) # 注册登录接口

# 2. 🌟 测算业务模块：在 Router 级别统一挂载拦截器！
# 这样 simulation.py 里的所有 @router.post 都不用再写鉴权代码了，进这个门必须刷卡！
app.include_router(
    simulation.router, 
    prefix="/api/v1", 
    tags=["Simulation"],
    dependencies=[Depends(get_current_user_payload)] # 👈 保安站在这里
)

# 4. 健康检查探针 (Health Check)
# 用于云服务器自动检测该引擎是否存活
@app.get("/", tags=["System / 系统"])
async def root():
    return {
        "status": "online",
        "message": "光储大师计算引擎已启动！请访问 /docs 查看交互式 API 文档。",
        "engine_version": "V0.3 (拉美金融完全体)"
    }