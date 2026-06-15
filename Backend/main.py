import sys
import os
import uvicorn

# Thêm thư mục gốc vào đường dẫn để import Backend.* hoạt động
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from Backend.routers import tours, recommendation, users

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
app.include_router(users.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Welcome to Tour & Travel Booking API"}

if __name__ == "__main__":
    uvicorn.run("Backend.main:app", host="0.0.0.0", port=8000, reload=True)
