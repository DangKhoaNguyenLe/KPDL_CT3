import asyncio
import motor.motor_asyncio
import sys
import os
import certifi

MONGO_DETAILS = os.getenv("MONGO_URI", "mongodb+srv://kpdl_ct3:kpdl_ct3@cluster0.heyjprm.mongodb.net/?appName=Cluster0")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS, tlsCAFile=certifi.where())
database = client.tour_platform
tours_collection = database.get_collection("tours")

TOURS = [
    {
        "id": 1,
        "name": "Hà Nội - Hạ Long 3N2Đ",
        "destination": "Hạ Long, Quảng Ninh",
        "duration": "3 ngày 2 đêm",
        "price": 3500000,
        "image": "halong.jpg",
        "category": "trong_nuoc",
        "rating": 4.8,
        "reviews": 124,
        "description": "Khám phá vịnh Hạ Long kỳ diệu với hàng nghìn đảo đá vôi hùng vĩ, hang động tuyệt đẹp và làn nước xanh trong vắt.",
        "highlights": ["Tham quan hang Sửng Sốt", "Chèo kayak", "Ngủ đêm trên thuyền", "Ẩm thực hải sản"]
    },
    {
        "id": 2,
        "name": "Đà Nẵng - Hội An 4N3Đ",
        "destination": "Đà Nẵng, Quảng Nam",
        "duration": "4 ngày 3 đêm",
        "price": 4200000,
        "image": "hoian.jpg",
        "category": "trong_nuoc",
        "rating": 4.9,
        "reviews": 89,
        "description": "Trải nghiệm phố cổ Hội An đầy màu sắc, bãi biển Mỹ Khê tuyệt đẹp và ẩm thực miền Trung đặc sắc.",
        "highlights": ["Phố cổ Hội An", "Bãi biển Mỹ Khê", "Bà Nà Hills", "Cầu Vàng"]
    },
    {
        "id": 3,
        "name": "TP.HCM - Phú Quốc 5N4Đ",
        "destination": "Phú Quốc, Kiên Giang",
        "duration": "5 ngày 4 đêm",
        "price": 6800000,
        "image": "phuquoc.jpg",
        "category": "trong_nuoc",
        "rating": 4.7,
        "reviews": 156,
        "description": "Nghỉ dưỡng tại đảo ngọc Phú Quốc với bãi biển hoang sơ, lặn ngắm san hô và thưởng thức hải sản tươi sống.",
        "highlights": ["Lặn ngắm san hô", "Safari Phú Quốc", "Cáp treo Hòn Thơm", "Chợ đêm Phú Quốc"]
    },
    {
        "id": 4,
        "name": "Sapa - Fansipan 3N2Đ",
        "destination": "Sapa, Lào Cai",
        "duration": "3 ngày 2 đêm",
        "price": 2900000,
        "image": "sapa.jpg",
        "category": "trong_nuoc",
        "rating": 4.6,
        "reviews": 73,
        "description": "Chinh phục đỉnh Fansipan - Nóc nhà Đông Dương, khám phá ruộng bậc thang tuyệt đẹp và văn hóa dân tộc H'Mông.",
        "highlights": ["Fansipan 3143m", "Ruộng bậc thang Mù Cang Chải", "B Bản Cát Cát", "Chợ phiên Sapa"]
    },
    {
        "id": 5,
        "name": "Tour Thái Lan 5N4Đ",
        "destination": "Bangkok - Pattaya",
        "duration": "5 ngày 4 đêm",
        "price": 8500000,
        "image": "thailand.jpg",
        "category": "nuoc_ngoai",
        "rating": 4.8,
        "reviews": 201,
        "description": "Khám phá xứ sở Chùa Vàng với kinh đô Bangkok sầm uất, bãi biển Pattaya và mua sắm thiên đường.",
        "highlights": ["Hoàng Cung Bangkok", "Pattaya Beach", "Chợ nổi", "Mua sắm Chatuchak"]
    },
    {
        "id": 6,
        "name": "Tour Singapore 4N3Đ",
        "destination": "Singapore",
        "duration": "4 ngày 3 đêm",
        "price": 12000000,
        "image": "singapore.jpg",
        "category": "nuoc_ngoai",
        "rating": 4.9,
        "reviews": 167,
        "description": "Trải nghiệm Singapore - thành phố sư tử hiện đại với Gardens by the Bay, Universal Studios và Marina Bay Sands.",
        "highlights": ["Gardens by the Bay", "Universal Studios", "Marina Bay Sands", "Sentosa Island"]
    }
]

async def seed_data():
    await tours_collection.delete_many({}) # Xóa dữ liệu cũ
    result = await tours_collection.insert_many(TOURS)
    print(f"Đã chèn thành công {len(result.inserted_ids)} tours vào database.")

if __name__ == "__main__":
    # Fix cho Windows AsyncIO
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(seed_data())
