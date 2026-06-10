import pandas as pd
import numpy as np
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Cấu hình đường dẫn
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'Data', 'raw', 'TravelInsurancePrediction.csv')
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'Data', 'cleaned', 'TravelInsurance_cleaned.csv')
REPORT_PATH = os.path.join(BASE_DIR, 'outputs', 'reports', 'cleaning_report.txt')

# Đảm bảo thư mục output tồn tại
os.makedirs(os.path.dirname(CLEANED_DATA_PATH), exist_ok=True)
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

# Danh sách để lưu log báo cáo
report_lines = []

def log(msg):
    """In ra console và lưu vào báo cáo."""
    print(msg)
    report_lines.append(msg)

# ĐỌC DỮ LIỆU VÀ KHẢO SÁT BAN ĐẦU
log("=" * 70)
log("BƯỚC 1: ĐỌC DỮ LIỆU VÀ KHẢO SÁT BAN ĐẦU")
log("=" * 70)

df = pd.read_csv(RAW_DATA_PATH)

log(f"\n📂 Đường dẫn file: {RAW_DATA_PATH}")
log(f"📊 Kích thước dữ liệu: {df.shape[0]} dòng x {df.shape[1]} cột")
log(f"\n📋 Danh sách các cột:")
for i, col in enumerate(df.columns):
    log(f"   {i+1}. {col} (kiểu: {df[col].dtype})")

log(f"\n📊 5 dòng đầu tiên:")
log(df.head().to_string())

log(f"\n📊 Thông tin tổng quan:")
# Capture df.info() output
import io
buffer = io.StringIO()
df.info(buf=buffer)
log(buffer.getvalue())

# KIỂM TRA VÀ XỬ LÝ CỘT INDEX THỪA
log("\n" + "=" * 70)
log("BƯỚC 2: KIỂM TRA VÀ XỬ LÝ CỘT INDEX THỪA")
log("=" * 70)
unnamed_cols = [col for col in df.columns if 'Unnamed' in str(col)]
if unnamed_cols:
    log(f"\n⚠️  Phát hiện {len(unnamed_cols)} cột index thừa: {unnamed_cols}")
    df = df.drop(columns=unnamed_cols)
    log(f"✅ Đã loại bỏ cột index thừa. Kích thước mới: {df.shape}")
else:
    log("\n✅ Không có cột index thừa.")

# KIỂM TRA GIÁ TRỊ THIẾU (MISSING VALUES)
log("\n" + "=" * 70)
log("BƯỚC 3: KIỂM TRA GIÁ TRỊ THIẾU (MISSING VALUES)")
log("=" * 70)

missing = df.isnull().sum()
missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
missing_df = pd.DataFrame({
    'Cột': missing.index,
    'Số lượng thiếu': missing.values,
    'Tỷ lệ (%)': missing_pct.values
})

log(f"\n{missing_df.to_string(index=False)}")

total_missing = missing.sum()
if total_missing == 0:
    log(f"\n✅ Không có giá trị thiếu trong dữ liệu.")
else:
    log(f"\n⚠️  Tổng số giá trị thiếu: {total_missing}")
    # Xử lý giá trị thiếu
    for col in df.columns:
        if df[col].isnull().sum() > 0:
            if df[col].dtype in ['int64', 'float64']:
                median_val = df[col].median()
                df[col] = df[col].fillna(median_val)
                log(f"   → Cột '{col}': Điền giá trị thiếu bằng median = {median_val}")
            else:
                mode_val = df[col].mode()[0]
                df[col] = df[col].fillna(mode_val)
                log(f"   → Cột '{col}': Điền giá trị thiếu bằng mode = {mode_val}")
    log(f"✅ Đã xử lý xong giá trị thiếu. Kiểm tra lại: {df.isnull().sum().sum()} giá trị thiếu còn lại.")

# KIỂM TRA VÀ XỬ LÝ DỮ LIỆU TRÙNG LẶP (DUPLICATES)
log("\n" + "=" * 70)
log("BƯỚC 4: KIỂM TRA VÀ XỬ LÝ DỮ LIỆU TRÙNG LẶP (DUPLICATES)")
log("=" * 70)

duplicates_count = df.duplicated().sum()
log(f"\n📊 Số dòng trùng lặp: {duplicates_count}")
log(f"📊 Tỷ lệ trùng lặp: {(duplicates_count / len(df) * 100):.2f}%")

if duplicates_count > 0:
    log(f"\n⚠️  Phát hiện {duplicates_count} dòng trùng lặp.")
    log(f"📋 Một số dòng trùng lặp:")
    log(df[df.duplicated(keep=False)].head(10).to_string())
    
    df_before = len(df)
    df = df.drop_duplicates(keep='first')
    df = df.reset_index(drop=True)
    log(f"\n✅ Đã loại bỏ {df_before - len(df)} dòng trùng lặp.")
    log(f"   Kích thước mới: {df.shape}")
else:
    log(f"\n✅ Không có dữ liệu trùng lặp.")

# KIỂM TRA VÀ XỬ LÝ GIÁ TRỊ NGOẠI LAI (OUTLIERS)
log("\n" + "=" * 70)
log("BƯỚC 5: KIỂM TRA VÀ XỬ LÝ GIÁ TRỊ NGOẠI LAI (OUTLIERS)")
log("=" * 70)

numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
log(f"\n📊 Các cột số: {numeric_cols}")

log(f"\n📊 Thống kê mô tả các cột số:")
log(df[numeric_cols].describe().to_string())

outlier_summary = []
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
    n_outliers = len(outliers)
    
    outlier_summary.append({
        'Cột': col,
        'Q1': Q1,
        'Q3': Q3,
        'IQR': IQR,
        'Cận dưới': lower_bound,
        'Cận trên': upper_bound,
        'Số outliers': n_outliers,
        'Tỷ lệ (%)': round(n_outliers / len(df) * 100, 2)
    })

outlier_df = pd.DataFrame(outlier_summary)
log(f"\n📊 Phân tích Outliers (phương pháp IQR):")
log(outlier_df.to_string(index=False))

# Xử lý outliers bằng capping (winsorizing) cho AnnualIncome
for col in numeric_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
    n_outliers = outliers_mask.sum()
    
    if n_outliers > 0:
        df[col] = df[col].clip(lower=lower_bound, upper=upper_bound)
        log(f"\n   → Cột '{col}': Capping {n_outliers} outliers vào khoảng [{lower_bound}, {upper_bound}]")

log(f"\n✅ Đã xử lý outliers bằng phương pháp Capping (Winsorizing).")

# CHUẨN HÓA KIỂU DỮ LIỆU
log("\n" + "=" * 70)
log("BƯỚC 6: CHUẨN HÓA KIỂU DỮ LIỆU")
log("=" * 70)

# Chuyển đổi kiểu dữ liệu phù hợp
dtype_changes = {}

# Age -> int
if df['Age'].dtype != 'int64':
    df['Age'] = df['Age'].astype(int)
    dtype_changes['Age'] = 'int64'

# AnnualIncome -> int (sau khi capping có thể thành float)
if df['AnnualIncome'].dtype != 'int64':
    df['AnnualIncome'] = df['AnnualIncome'].astype(int)
    dtype_changes['AnnualIncome'] = 'int64'

# FamilyMembers -> int
if df['FamilyMembers'].dtype != 'int64':
    df['FamilyMembers'] = df['FamilyMembers'].astype(int)
    dtype_changes['FamilyMembers'] = 'int64'

# ChronicDiseases -> int (binary)
if df['ChronicDiseases'].dtype != 'int64':
    df['ChronicDiseases'] = df['ChronicDiseases'].astype(int)
    dtype_changes['ChronicDiseases'] = 'int64'

# TravelInsurance -> int (binary)
if df['TravelInsurance'].dtype != 'int64':
    df['TravelInsurance'] = df['TravelInsurance'].astype(int)
    dtype_changes['TravelInsurance'] = 'int64'

# Categorical columns -> category type
cat_cols = ['Employment Type', 'GraduateOrNot', 'FrequentFlyer', 'EverTravelledAbroad']
for col in cat_cols:
    df[col] = df[col].astype('category')
    dtype_changes[col] = 'category'

if dtype_changes:
    log(f"\n📊 Các thay đổi kiểu dữ liệu:")
    for col, new_type in dtype_changes.items():
        log(f"   → {col}: chuyển sang {new_type}")
else:
    log(f"\n✅ Kiểu dữ liệu đã đúng, không cần thay đổi.")

log(f"\n📊 Kiểu dữ liệu sau chuẩn hóa:")
for col in df.columns:
    log(f"   {col}: {df[col].dtype}")

# KIỂM TRA GIÁ TRỊ HỢP LỆ
log("\n" + "=" * 70)
log("BƯỚC 7: KIỂM TRA GIÁ TRỊ HỢP LỆ")
log("=" * 70)

# Kiểm tra các giá trị unique cho biến phân loại
for col in cat_cols:
    unique_vals = df[col].unique()
    log(f"\n   {col}: {list(unique_vals)}")

# Kiểm tra phạm vi hợp lệ cho biến số
log(f"\n📊 Phạm vi giá trị các biến số:")
for col in ['Age', 'AnnualIncome', 'FamilyMembers', 'ChronicDiseases', 'TravelInsurance']:
    log(f"   {col}: min={df[col].min()}, max={df[col].max()}")

# Kiểm tra ChronicDiseases và TravelInsurance chỉ có 0 và 1
for col in ['ChronicDiseases', 'TravelInsurance']:
    valid = set(df[col].unique()).issubset({0, 1})
    if valid:
        log(f"   ✅ {col}: Chỉ chứa giá trị 0 và 1 → Hợp lệ")
    else:
        log(f"   ⚠️ {col}: Chứa giá trị ngoài {0, 1} → Cần kiểm tra!")

# LƯU DỮ LIỆU ĐÃ LÀM SẠCH
log("\n" + "=" * 70)
log("BƯỚC 8: LƯU DỮ LIỆU ĐÃ LÀM SẠCH")
log("=" * 70)

df.to_csv(CLEANED_DATA_PATH, index=False)
log(f"\n✅ Đã lưu dữ liệu đã làm sạch tại: {CLEANED_DATA_PATH}")
log(f"📊 Kích thước dữ liệu cuối cùng: {df.shape[0]} dòng x {df.shape[1]} cột")

# TÓM TẮT QUÁ TRÌNH LÀM SẠCH
log("\n" + "=" * 70)
log("TÓM TẮT QUÁ TRÌNH LÀM SẠCH DỮ LIỆU")
log("=" * 70)

log(f"""
📂 File gốc: {RAW_DATA_PATH}
📂 File đã làm sạch: {CLEANED_DATA_PATH}

📊 TRƯỚC khi làm sạch:
   - Kích thước: 1987 dòng (sau bỏ header)
   - Cột index thừa: {'Có' if unnamed_cols else 'Không'}
   - Giá trị thiếu: {total_missing}
   - Dòng trùng lặp: {duplicates_count}

📊 SAU khi làm sạch:
   - Kích thước: {df.shape[0]} dòng x {df.shape[1]} cột
   - Giá trị thiếu: {df.isnull().sum().sum()}
   - Dòng trùng lặp: {df.duplicated().sum()}
   - Các cột: {list(df.columns)}
""")

# Lưu báo cáo ra file
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))
log(f"📄 Báo cáo làm sạch đã lưu tại: {REPORT_PATH}")

log("\n🎉 HOÀN THÀNH LÀM SẠCH DỮ LIỆU!")
