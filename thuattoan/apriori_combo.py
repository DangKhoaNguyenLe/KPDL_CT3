import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
import os


# =========================
# 1. ĐỌC DỮ LIỆU
# =========================

file_path = "thuattoan/Data/cleaned/TravelInsurance_cleaned.csv"

df = pd.read_csv(file_path)

print("=" * 60)
print("SỐ LƯỢNG BẢN GHI:", len(df))
print("=" * 60)

# =========================
# 2. CHỌN CỘT PHÂN TÍCH
# =========================

cols_to_analyze = [
    'Employment Type',
    'GraduateOrNot',
    'ChronicDiseases',
    'FrequentFlyer',
    'EverTravelledAbroad',
    'TravelInsurance',
    'Age_Group',
    'Income_Group',
    'Family_Size'
]

existing_cols = [col for col in cols_to_analyze if col in df.columns]

df_filtered = df[existing_cols].astype(str)

# =========================
# 3. ONE-HOT ENCODING
# =========================

df_encoded = pd.get_dummies(df_filtered)

print("\nSố thuộc tính sau One-Hot Encoding:", len(df_encoded.columns))

# =========================
# 4. THAM SỐ APRIORI
# =========================

MIN_SUPPORT = 0.05
MIN_CONFIDENCE = 0.40
MIN_LIFT = 1.10

# =========================
# 5. TÌM FREQUENT ITEMSETS
# =========================

frequent_itemsets = apriori(
    df_encoded,
    min_support=MIN_SUPPORT,
    use_colnames=True
)

print("\nSố tập phổ biến:", len(frequent_itemsets))

# =========================
# 6. SINH LUẬT KẾT HỢP
# =========================

rules = association_rules(
    frequent_itemsets,
    metric="lift",
    min_threshold=MIN_LIFT
)

rules = rules[
    rules["confidence"] >= MIN_CONFIDENCE
]

print("Số luật kết hợp:", len(rules))

# =========================
# 7. TRÍCH XUẤT COMBO TỐT NHẤT
# =========================

top_combos = rules[
    [
        "antecedents",
        "consequents",
        "support",
        "confidence",
        "lift"
    ]
].copy()

top_combos = top_combos.sort_values(
    by="lift",
    ascending=False
)

# =========================
# 8. HIỂN THỊ TOP 10 COMBO
# =========================

print("\n")
print("=" * 80)
print("TOP 10 COMBO HÀNH VI KHÁCH HÀNG")
print("=" * 80)

for i, (_, row) in enumerate(top_combos.head(10).iterrows(), start=1):

    antecedent = ", ".join(list(row["antecedents"]))
    consequent = ", ".join(list(row["consequents"]))

    print(f"\nCOMBO {i}")

    print("Nếu khách hàng có:")
    print(f"   {antecedent}")

    print("Thì thường sẽ có:")
    print(f"   {consequent}")

    print(f"Support    : {row['support']:.4f}")
    print(f"Confidence : {row['confidence']:.4f}")
    print(f"Lift       : {row['lift']:.4f}")

    print("-" * 80)

# =========================
# 9. LƯU KẾT QUẢ
# =========================

os.makedirs("outputs/reports", exist_ok=True)

output_file = "outputs/reports/top_combo_report.txt"

with open(output_file, "w", encoding="utf-8") as f:

    f.write("=" * 80 + "\n")
    f.write("TOP COMBO HÀNH VI KHÁCH HÀNG\n")
    f.write("=" * 80 + "\n\n")

    for i, (_, row) in enumerate(top_combos.head(10).iterrows(), start=1):

        antecedent = ", ".join(list(row["antecedents"]))
        consequent = ", ".join(list(row["consequents"]))

        f.write(f"COMBO {i}\n")
        f.write(f"Nếu khách hàng có: {antecedent}\n")
        f.write(f"Thì thường sẽ có: {consequent}\n")
        f.write(f"Support    : {row['support']:.4f}\n")
        f.write(f"Confidence : {row['confidence']:.4f}\n")
        f.write(f"Lift       : {row['lift']:.4f}\n")
        f.write("-" * 80 + "\n")

print("\n" + "=" * 60)
print("ĐÃ LƯU KẾT QUẢ THÀNH CÔNG")
print("Vị trí:", output_file)
print("=" * 60)