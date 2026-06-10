import asyncio
import motor.motor_asyncio
import sys
import os
import certifi

# Lấy chuỗi kết nối từ biến môi trường, hoặc dùng localhost làm mặc định
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb+srv://kpdl_ct3:kpdl_ct3@cluster0.heyjprm.mongodb.net/?appName=Cluster0")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where())
database = client.tour_platform

async def create_collections():
    """
    MongoDB tự động tạo collection (bảng) khi bạn chèn document (bản ghi) đầu tiên.
    Tuy nhiên, nếu bạn muốn tạo trước một cách tường minh hoặc thêm Index (đánh chỉ mục),
    bạn có thể sử dụng đoạn script này.
    """
    existing_collections = await database.list_collection_names()
    
    # Danh sách các collection cần tạo
    collections = ["tours", "users", "services", "bookings", "reviews"]
    
    for coll_name in collections:
        if coll_name not in existing_collections:
            await database.create_collection(coll_name)
            print(f"Đã tạo collection: {coll_name}")
        else:
            print(f"Collection {coll_name} đã tồn tại.")

    # Tạo chỉ mục (Index) để tìm kiếm nhanh hơn
    print("\nĐang tạo Indexes...")
    
    # Tạo index duy nhất (unique) cho trường 'id' của tour
    await database.tours.create_index("id", unique=True)
    print("- Đã tạo index duy nhất cho 'id' trong bảng tours")
    
    # Tạo index cho username trong bảng users (giả sử sau này có)
    await database.users.create_index("username", unique=True)
    print("- Đã tạo index duy nhất cho 'username' trong bảng users")
    
    print("\nKhởi tạo cơ sở dữ liệu thành công!")

if __name__ == "__main__":
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(create_collections())
