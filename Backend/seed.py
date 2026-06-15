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
        "highlights": ["Fansipan 3143m", "Ruộng bậc thang Mù Cang Chải", "Bản Cát Cát", "Chợ phiên Sapa"]
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
    },
    {
        "id": 7,
        "name": "Đà Lạt - Xứ Sở Sương Mù 3N2Đ",
        "destination": "Đà Lạt, Lâm Đồng",
        "duration": "3 ngày 2 đêm",
        "price": 3200000,
        "image": "dalat.jpg",
        "category": "trong_nuoc",
        "rating": 4.7,
        "reviews": 142,
        "description": "Hòa mình vào không khí se lạnh, ngắm ngàn hoa khoe sắc và tận hưởng sự bình yên tại Đà Lạt.",
        "highlights": ["Hồ Tuyền Lâm", "Thung Lũng Tình Yêu", "Chợ đêm Đà Lạt", "Làng Cù Lần"]
    },
    {
        "id": 8,
        "name": "Biển Đảo Nha Trang 4N3Đ",
        "destination": "Nha Trang, Khánh Hòa",
        "duration": "4 ngày 3 đêm",
        "price": 4500000,
        "image": "nhatrang.jpg",
        "category": "trong_nuoc",
        "rating": 4.6,
        "reviews": 110,
        "description": "Tận hưởng làn nước xanh ngắt, các dịch vụ giải trí đẳng cấp tại Vinpearl và ẩm thực hải sản biển tuyệt vời.",
        "highlights": ["Vinpearl Land", "Đảo Khỉ", "Tắm bùn Tháp Bà", "Tháp Ponagar"]
    },
    {
        "id": 9,
        "name": "Khám Phá Côn Đảo 3N2Đ",
        "destination": "Côn Đảo, Bà Rịa - Vũng Tàu",
        "duration": "3 ngày 2 đêm",
        "price": 5500000,
        "image": "condao.jpg",
        "category": "trong_nuoc",
        "rating": 4.9,
        "reviews": 95,
        "description": "Trải nghiệm vùng đất lịch sử linh thiêng, cảnh quan thiên nhiên hoang sơ và bãi biển tuyệt đẹp.",
        "highlights": ["Nghĩa trang Hàng Dương", "Nhà tù Côn Đảo", "Bãi Đầm Trầu", "Ngắm rùa biển đẻ trứng"]
    },
    {
        "id": 10,
        "name": "Mộc Châu - Mùa Hoa Cải 2N1Đ",
        "destination": "Mộc Châu, Sơn La",
        "duration": "2 ngày 1 đêm",
        "price": 1800000,
        "image": "mocchau.jpg",
        "category": "trong_nuoc",
        "rating": 4.5,
        "reviews": 68,
        "description": "Đắm mình trong không gian những đồi chè xanh mát và những cánh đồng hoa mận, hoa cải trắng muốt.",
        "highlights": ["Đồi chè trái tim", "Thác Dải Yếm", "Rừng thông Bản Áng", "Hái dâu tây"]
    },
    {
        "id": 11,
        "name": "Ninh Bình - Tràng An 2N1Đ",
        "destination": "Ninh Bình",
        "duration": "2 ngày 1 đêm",
        "price": 2100000,
        "image": "ninhbinh.jpg",
        "category": "trong_nuoc",
        "rating": 4.8,
        "reviews": 130,
        "description": "Khám phá danh thắng Tràng An, Tam Cốc - Bích Động và quần thể hang động hùng vĩ tại Ninh Bình.",
        "highlights": ["Khu du lịch Tràng An", "Chùa Bái Đính", "Hang Múa", "Cố đô Hoa Lư"]
    },
    {
        "id": 12,
        "name": "Tour Nhật Bản - Cung Đường Vàng 6N5Đ",
        "destination": "Tokyo - Kyoto - Osaka",
        "duration": "6 ngày 5 đêm",
        "price": 28500000,
        "image": "japan.jpg",
        "category": "nuoc_ngoai",
        "rating": 4.9,
        "reviews": 210,
        "description": "Trải nghiệm văn hóa Nhật Bản đặc sắc, ngắm hoa anh đào/lá đỏ và chiêm ngưỡng núi Phú Sĩ.",
        "highlights": ["Núi Phú Sĩ", "Chùa Vàng Kinkakuji", "Hoàng Cung Tokyo", "Phố cổ Gion"]
    },
    {
        "id": 13,
        "name": "Tour Hàn Quốc - Xứ Sở Kim Chi 5N4Đ",
        "destination": "Seoul - Nami - Everland",
        "duration": "5 ngày 4 đêm",
        "price": 16500000,
        "image": "korea.jpg",
        "category": "nuoc_ngoai",
        "rating": 4.7,
        "reviews": 180,
        "description": "Khám phá hòn đảo Nami lãng mạn, tham quan công viên giải trí Everland và mua sắm sầm uất tại Seoul.",
        "highlights": ["Đảo Nami", "Công viên Everland", "Cung điện Gyeongbokgung", "Mặc Hanbok"]
    },
    {
        "id": 14,
        "name": "Tour Đài Loan 5N4Đ",
        "destination": "Đài Bắc - Đài Trung - Cao Hùng",
        "duration": "5 ngày 4 đêm",
        "price": 11500000,
        "image": "taiwan.jpg",
        "category": "nuoc_ngoai",
        "rating": 4.6,
        "reviews": 145,
        "description": "Hòa mình vào thiên nhiên Hồ Nhật Nguyệt, khám phá phố cổ Thập Phần và ẩm thực đường phố độc đáo.",
        "highlights": ["Phố cổ Thập Phần", "Hồ Nhật Nguyệt", "Tháp Taipei 101", "Chợ đêm Lục Hợp"]
    },
    {
        "id": 15,
        "name": "Thiên Đường Bali - Indonesia 4N3Đ",
        "destination": "Bali, Indonesia",
        "duration": "4 ngày 3 đêm",
        "price": 9500000,
        "image": "bali.jpg",
        "category": "nuoc_ngoai",
        "rating": 4.8,
        "reviews": 112,
        "description": "Khám phá đảo thần tiên Bali với các bãi biển xanh ngắt, đền thờ thiêng liêng và ruộng bậc thang tuyệt đẹp.",
        "highlights": ["Đền Tanah Lot", "Xích đu Bali Swing", "Ruộng bậc thang Tegalalang", "Cung điện nước Tirta Gangga"]
    },
    {
        "id": 16,
        "name": "Khám Phá Châu Âu 10N9Đ",
        "destination": "Pháp - Thụy Sĩ - Ý",
        "duration": "10 ngày 9 đêm",
        "price": 65000000,
        "image": "europe.jpg",
        "category": "nuoc_ngoai",
        "rating": 4.9,
        "reviews": 85,
        "description": "Hành trình mộng mơ qua các thành phố lãng mạn nhất Châu Âu, chiêm ngưỡng tháp Eiffel, núi Titlis và đấu trường Colosseum.",
        "highlights": ["Tháp Eiffel", "Bảo tàng Louvre", "Núi tuyết Titlis", "Đấu trường Colosseum"]
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
