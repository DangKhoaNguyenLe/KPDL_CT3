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

@router.get("/", response_model=List[RecommendationResponse])
async def get_recommendations():
    # Giả lập logic từ apriori_combo.py
    # Đọc dữ liệu (Đảm bảo file tồn tại ở đúng đường dẫn)
    file_path = "thuattoan/Data/cleaned/TravelInsurance_cleaned.csv"
    
    if not os.path.exists(file_path):
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
        antecedent = ", ".join(list(row["antecedents"]))
        consequent = ", ".join(list(row["consequents"]))
        
        results.append(RecommendationResponse(
            combo_id=i,
            antecedents=antecedent,
            consequents=consequent,
            support=row["support"],
            confidence=row["confidence"],
            lift=row["lift"]
        ))
        
    return results
