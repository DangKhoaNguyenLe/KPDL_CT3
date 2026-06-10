import motor.motor_asyncio
import os
import certifi

# Thay thế bằng chuỗi kết nối MongoDB Atlas của bạn
# Ví dụ: "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb+srv://kpdl_ct3:kpdl_ct3@cluster0.heyjprm.mongodb.net/?appName=Cluster0")

# Thêm tlsCAFile=certifi.where() để tránh lỗi SSL khi kết nối với MongoDB Atlas online
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where())
database = client.tour_platform

# Các collection
tours_collection = database.get_collection("tours")
users_collection = database.get_collection("users")
services_collection = database.get_collection("services")
bookings_collection = database.get_collection("bookings")
reviews_collection = database.get_collection("reviews")
