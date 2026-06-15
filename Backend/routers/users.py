from fastapi import APIRouter, HTTPException, status
from Backend.models import UserModel
from Backend.database import database
from werkzeug.security import generate_password_hash, check_password_hash
from pydantic import BaseModel

router = APIRouter()
users_collection = database.users

class UserLogin(BaseModel):
    username: str
    password: str

@router.post("/users/register", response_model=dict)
async def register_user(user: UserModel):
    # Kiểm tra xem user đã tồn tại chưa
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại!")
    
    # Mã hoá mật khẩu
    hashed_password = generate_password_hash(user.password)
    
    # Tạo document
    user_dict = {"username": user.username, "password": hashed_password}
    result = await users_collection.insert_one(user_dict)
    
    if result.inserted_id:
        return {"message": "Đăng ký thành công!", "id": str(result.inserted_id)}
    raise HTTPException(status_code=500, detail="Lỗi hệ thống khi đăng ký.")

@router.post("/users/login", response_model=dict)
async def login_user(user: UserLogin):
    # Tìm user trong db
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user:
        raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu!")
    
    # Kiểm tra mật khẩu
    if check_password_hash(db_user["password"], user.password):
        return {
            "message": "Đăng nhập thành công!",
            "user_id": str(db_user["_id"]),
            "username": db_user["username"]
        }
    
    raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu!")
