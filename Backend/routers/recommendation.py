from fastapi import APIRouter
from typing import List
from Backend.models import RecommendationResponse
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import os

router = APIRouter(
    prefix="/recommend",
    tags=["Recommendations"]
)

# Bảng dịch tên cột one-hot encoding sang tiếng Việt
TRANSLATE_MAP = {
    # Loại hình công việc
    "Employment Type_Government Sector": "Nhân viên Nhà nước",
    "Employment Type_Private Sector/Self Employed": "Nhân viên Tư nhân / Tự kinh doanh",
    # Tốt nghiệp đại học
    "GraduateOrNot_Yes": "Đã tốt nghiệp đại học",
    "GraduateOrNot_No": "Chưa tốt nghiệp đại học",
    # Bệnh mãn tính
    "ChronicDiseases_0": "Không có bệnh mãn tính",
    "ChronicDiseases_1": "Có bệnh mãn tính",
    # Hay đi máy bay
    "FrequentFlyer_Yes": "Hay đi máy bay",
    "FrequentFlyer_No": "Ít đi máy bay",
    # Đã từng đi nước ngoài
    "EverTravelledAbroad_Yes": "Đã từng đi nước ngoài",
    "EverTravelledAbroad_No": "Chưa từng đi nước ngoài",
    # Bảo hiểm du lịch
    "TravelInsurance_0": "Chưa mua bảo hiểm du lịch",
    "TravelInsurance_1": "Đã mua bảo hiểm du lịch",
}

def translate_item(item: str) -> str:
    """Dịch tên cột one-hot sang tiếng Việt, giữ nguyên nếu không tìm thấy."""
    return TRANSLATE_MAP.get(item.strip(), item)

def classify_combo(all_items: list) -> str:
    """Phân loại combo dựa trên đặc điểm khách hàng."""
    # Các đặc điểm "cao cấp"
    premium_traits = {
        "FrequentFlyer_Yes",
        "EverTravelledAbroad_Yes",
        "TravelInsurance_1",
        "GraduateOrNot_Yes",
    }
    # Các đặc điểm "bình dân"
    budget_traits = {
        "FrequentFlyer_No",
        "EverTravelledAbroad_No",
        "TravelInsurance_0",
        "GraduateOrNot_No",
    }

    premium_count = sum(1 for item in all_items if item in premium_traits)
    budget_count = sum(1 for item in all_items if item in budget_traits)

    if premium_count >= 2:
        return "Hạng Sang 💎"
    elif budget_count >= 2:
        return "Bình Dân 🏠"
    else:
        return "Phổ Biến ⭐"

@router.get("/", response_model=List[RecommendationResponse])
async def get_recommendations():
    # Lấy thư mục gốc của dự án (KPDL_CT3)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    file_path = os.path.join(base_dir, "thuattoan", "Data", "cleaned", "TravelInsurance_cleaned.csv")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return [] # Nếu không có file data thì trả về rỗng

    df = pd.read_csv(file_path)
    
    cols_to_analyze = [
        'Employment Type', 'GraduateOrNot', 'ChronicDiseases',
        'FrequentFlyer', 'EverTravelledAbroad', 'TravelInsurance',
        'Age_Group', 'Income_Group', 'Family_Size'
    ]
    
    existing_cols = [col for col in cols_to_analyze if col in df.columns]
    df_filtered = df[existing_cols].astype(str)
    
    # One-Hot Encoding
    df_encoded = pd.get_dummies(df_filtered)
    
    MIN_SUPPORT = 0.05
    MIN_CONFIDENCE = 0.40
    MIN_LIFT = 1.10
    
    # Tìm frequent itemsets
    frequent_itemsets = apriori(
        df_encoded,
        min_support=MIN_SUPPORT,
        use_colnames=True
    )
    
    if frequent_itemsets.empty:
        return []
        
    # Sinh luật kết hợp
    rules = association_rules(
        frequent_itemsets,
        metric="lift",
        min_threshold=MIN_LIFT
    )
    
    rules = rules[rules["confidence"] >= MIN_CONFIDENCE]
    
    top_combos = rules[
        ["antecedents", "consequents", "support", "confidence", "lift"]
    ].copy()
    
    top_combos = top_combos.sort_values(by="lift", ascending=False).head(10)
    
    results = []
    for i, (_, row) in enumerate(top_combos.iterrows(), start=1):
        raw_antecedents = list(row["antecedents"])
        raw_consequents = list(row["consequents"])

        # Phân loại combo dựa trên tất cả đặc điểm gốc (tiếng Anh)
        combo_name = classify_combo(raw_antecedents + raw_consequents)

        # Dịch sang tiếng Việt và cách hàng bằng dấu xuống dòng
        antecedent = "\n".join([translate_item(x) for x in raw_antecedents])
        consequent = "\n".join([translate_item(x) for x in raw_consequents])
        
        results.append(RecommendationResponse(
            combo_id=i,
            combo_name=combo_name,
            antecedents=antecedent,
            consequents=consequent,
            support=row["support"],
            confidence=row["confidence"],
            lift=row["lift"]
        ))
        
    return results
