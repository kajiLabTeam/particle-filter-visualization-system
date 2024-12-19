# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from starlette.requests import Request
# from controller import perform_particlefiltering_controller as perform_particlefiltering
# from controller import health_check_controller as health_check_router


# app = FastAPI()


# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


# app.include_router(perform_particlefiltering.router)
# app.include_router(health_check_router.router)
