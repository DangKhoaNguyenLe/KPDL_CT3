from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers import tours, recommendation

app = FastAPI(title="Tour & Travel Booking API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Cho phép gọi từ mọi origin (trong thực tế nên giới hạn)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(tours.router, prefix="/api")
app.include_router(recommendation.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Tour & Travel Booking API"}
