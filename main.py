from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from controller import health_check_controller as health_check_router
from controller import perform_particlefiltering_controller as perform_particlefiltering



"""サーバー周りの設定"""
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(perform_particlefiltering.router)
app.include_router(health_check_router.router)

