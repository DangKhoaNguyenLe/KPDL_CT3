import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import os
import sys
import io
import warnings
warnings.filterwarnings('ignore')

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# --- Cấu hình ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_DATA_PATH = os.path.join(BASE_DIR, 'Data', 'cleaned', 'TravelInsurance_cleaned.csv')
CHARTS_DIR = os.path.join(BASE_DIR, 'outputs', 'charts')
REPORT_PATH = os.path.join(BASE_DIR, 'outputs', 'reports', 'eda_report.txt')

os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)

# --- Cấu hình matplotlib ---
plt.style.use('seaborn-v0_8-whitegrid')
rcParams['figure.dpi'] = 100
rcParams['savefig.dpi'] = 300
rcParams['figure.figsize'] = (10, 6)
rcParams['axes.unicode_minus'] = False

# Bảng màu chính
COLORS = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#2ECC71',
    'danger': '#E74C3C',
    'dark': '#2C3E50',
    'light': '#ECF0F1',
}
PALETTE_2 = [COLORS['primary'], COLORS['accent']]
PALETTE_MULTI = ['#2E86AB', '#A23B72', '#F18F01', '#2ECC71', '#E74C3C', '#9B59B6', '#1ABC9C', '#F39C12']

# Danh sách log
report_lines = []

def log(msg):
    print(msg)
    report_lines.append(str(msg))

def save_fig(fig, filename):
    """Lưu biểu đồ ra file PNG."""
    filepath = os.path.join(CHARTS_DIR, filename)
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    log(f"   💾 Đã lưu: {filepath}")

# ĐỌC DỮ LIỆU ĐÃ LÀM SẠCH
log("=" * 70)
log("PHÂN TÍCH THỐNG KÊ MÔ TẢ (EDA)")
log("Đề tài: Phân tích hành vi khách hàng trong ngành du lịch")
log("=" * 70)

df = pd.read_csv(CLEANED_DATA_PATH)
log(f"\n📂 Đọc dữ liệu từ: {CLEANED_DATA_PATH}")
log(f"📊 Kích thước: {df.shape[0]} dòng x {df.shape[1]} cột")

# Định nghĩa nhóm cột
num_cols = ['Age', 'AnnualIncome', 'FamilyMembers']
cat_cols = ['Employment Type', 'GraduateOrNot', 'FrequentFlyer', 'EverTravelledAbroad']
binary_cols = ['ChronicDiseases', 'TravelInsurance']
target = 'TravelInsurance'

# PHẦN A: THỐNG KÊ MÔ TẢ CƠ BẢN
log("\n" + "=" * 70)
log("PHẦN A: THỐNG KÊ MÔ TẢ CƠ BẢN")
log("=" * 70)

# A1. Thống kê mô tả biến số
log("\n📊 A1. Thống kê mô tả các biến số:")
desc = df[num_cols + binary_cols].describe()
log(desc.to_string())

# A2. Thống kê biến phân loại
log("\n📊 A2. Thống kê các biến phân loại:")
for col in cat_cols:
    log(f"\n   --- {col} ---")
    vc = df[col].value_counts()
    vc_pct = df[col].value_counts(normalize=True) * 100
    summary = pd.DataFrame({'Số lượng': vc, 'Tỷ lệ (%)': vc_pct.round(2)})
    log(summary.to_string())

# A3. Ma trận tương quan
log("\n📊 A3. Ma trận tương quan:")
# Encode categorical for correlation
df_encoded = df.copy()
df_encoded['Employment Type'] = df_encoded['Employment Type'].map({
    'Government Sector': 0, 'Private Sector/Self Employed': 1
})
df_encoded['GraduateOrNot'] = df_encoded['GraduateOrNot'].map({'No': 0, 'Yes': 1})
df_encoded['FrequentFlyer'] = df_encoded['FrequentFlyer'].map({'No': 0, 'Yes': 1})
df_encoded['EverTravelledAbroad'] = df_encoded['EverTravelledAbroad'].map({'No': 0, 'Yes': 1})

corr_matrix = df_encoded.corr()
log(corr_matrix.round(3).to_string())

# Biểu đồ heatmap tương quan
fig, ax = plt.subplots(figsize=(10, 8))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r',
            center=0, square=True, linewidths=0.5, ax=ax,
            cbar_kws={'shrink': 0.8})
ax.set_title('Ma tran tuong quan giua cac bien', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
save_fig(fig, 'A3_correlation_heatmap.png')

# PHẦN B: PHÂN PHỐI TỪNG BIẾN (UNIVARIATE ANALYSIS)
log("\n" + "=" * 70)
log("PHẦN B: PHÂN PHỐI TỪNG BIẾN (UNIVARIATE ANALYSIS)")
log("=" * 70)

# B1. Phân phối tuổi (Age)
log("\n📊 B1. Phân phối tuổi (Age)")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['Age'], bins=11, color=COLORS['primary'], edgecolor='white', alpha=0.85)
axes[0].set_title('Phan phoi tuoi khach hang', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Tuoi')
axes[0].set_ylabel('So luong')
axes[0].axvline(df['Age'].mean(), color=COLORS['danger'], linestyle='--', linewidth=2, label=f"Trung binh = {df['Age'].mean():.1f}")
axes[0].legend(fontsize=10)

sns.kdeplot(data=df, x='Age', fill=True, color=COLORS['primary'], alpha=0.4, ax=axes[1])
axes[1].set_title('Mat do phan phoi tuoi', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Tuoi')
axes[1].set_ylabel('Mat do')

fig.suptitle('B1. Phan tich phan phoi tuoi khach hang', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'B1_age_distribution.png')

# B2. Phân phối thu nhập (AnnualIncome)
log("\n📊 B2. Phân phối thu nhập (AnnualIncome)")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

axes[0].hist(df['AnnualIncome'], bins=20, color=COLORS['success'], edgecolor='white', alpha=0.85)
axes[0].set_title('Phan phoi thu nhap hang nam', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Thu nhap (VND)')
axes[0].set_ylabel('So luong')
axes[0].axvline(df['AnnualIncome'].mean(), color=COLORS['danger'], linestyle='--', linewidth=2,
                label=f"Trung binh = {df['AnnualIncome'].mean():,.0f}")
axes[0].axvline(df['AnnualIncome'].median(), color=COLORS['accent'], linestyle='--', linewidth=2,
                label=f"Trung vi = {df['AnnualIncome'].median():,.0f}")
axes[0].legend(fontsize=9)

sns.kdeplot(data=df, x='AnnualIncome', fill=True, color=COLORS['success'], alpha=0.4, ax=axes[1])
axes[1].set_title('Mat do phan phoi thu nhap', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Thu nhap')
axes[1].set_ylabel('Mat do')

fig.suptitle('B2. Phan tich phan phoi thu nhap khach hang', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'B2_income_distribution.png')

# B3. Phân phối số thành viên gia đình
log("\n📊 B3. Phân phối số thành viên gia đình")
fig, ax = plt.subplots(figsize=(10, 6))
family_counts = df['FamilyMembers'].value_counts().sort_index()
bars = ax.bar(family_counts.index, family_counts.values, color=PALETTE_MULTI[:len(family_counts)],
              edgecolor='white', linewidth=1.5)
for bar, val in zip(bars, family_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            str(val), ha='center', va='bottom', fontweight='bold', fontsize=11)
ax.set_title('B3. Phan phoi so thanh vien gia dinh', fontsize=14, fontweight='bold')
ax.set_xlabel('So thanh vien gia dinh', fontsize=12)
ax.set_ylabel('So luong khach hang', fontsize=12)
ax.set_xticks(family_counts.index)
fig.tight_layout()
save_fig(fig, 'B3_family_members.png')

# B4. Tỷ lệ loại hình công việc
log("\n📊 B4. Tỷ lệ loại hình công việc")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

emp_counts = df['Employment Type'].value_counts()
colors_emp = [COLORS['primary'], COLORS['accent']]
wedges, texts, autotexts = axes[0].pie(emp_counts.values, labels=['Tu nhan/\nTu doanh', 'Nha nuoc'],
                                        autopct='%1.1f%%', colors=colors_emp, startangle=90,
                                        explode=(0.03, 0.03), shadow=True,
                                        textprops={'fontsize': 11})
for autotext in autotexts:
    autotext.set_fontweight('bold')
axes[0].set_title('Ty le loai hinh cong viec', fontsize=13, fontweight='bold')

bars = axes[1].barh(emp_counts.index, emp_counts.values, color=colors_emp, edgecolor='white', height=0.5)
for bar, val in zip(bars, emp_counts.values):
    axes[1].text(val + 10, bar.get_y() + bar.get_height()/2, str(val),
                 ha='left', va='center', fontweight='bold', fontsize=12)
axes[1].set_title('So luong theo loai hinh cong viec', fontsize=13, fontweight='bold')
axes[1].set_xlabel('So luong')

fig.suptitle('B4. Phan tich loai hinh cong viec', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'B4_employment_type.png')

# B5. Tỷ lệ tốt nghiệp ĐH
log("\n📊 B5. Tỷ lệ tốt nghiệp ĐH")
fig, ax = plt.subplots(figsize=(8, 6))
grad_counts = df['GraduateOrNot'].value_counts()
colors_grad = [COLORS['success'], COLORS['danger']]
wedges, texts, autotexts = ax.pie(grad_counts.values,
                                   labels=['Da tot nghiep DH', 'Chua tot nghiep DH'],
                                   autopct='%1.1f%%', colors=colors_grad, startangle=90,
                                   explode=(0.03, 0.03), shadow=True,
                                   textprops={'fontsize': 12})
for autotext in autotexts:
    autotext.set_fontweight('bold')
ax.set_title('B5. Ty le tot nghiep dai hoc', fontsize=14, fontweight='bold')
fig.tight_layout()
save_fig(fig, 'B5_graduate_ratio.png')

# B6. Tỷ lệ bệnh mãn tính
log("\n📊 B6. Tỷ lệ bệnh mãn tính")
fig, ax = plt.subplots(figsize=(8, 6))
chronic_counts = df['ChronicDiseases'].value_counts().sort_index()
labels_chronic = ['Khong co benh\nman tinh', 'Co benh\nman tinh']
bars = ax.bar(labels_chronic, chronic_counts.values, color=[COLORS['success'], COLORS['danger']],
              edgecolor='white', width=0.5, linewidth=1.5)
for bar, val in zip(bars, chronic_counts.values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{val}\n({val/len(df)*100:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('B6. Ty le khach hang co benh man tinh', fontsize=14, fontweight='bold')
ax.set_ylabel('So luong', fontsize=12)
fig.tight_layout()
save_fig(fig, 'B6_chronic_diseases.png')

# B7. Tỷ lệ bay thường xuyên
log("\n📊 B7. Tỷ lệ bay thường xuyên")
fig, ax = plt.subplots(figsize=(8, 6))
ff_counts = df['FrequentFlyer'].value_counts()
labels_ff = ['Khong bay\nthuong xuyen', 'Bay\nthuong xuyen']
colors_ff = [COLORS['light'], COLORS['primary']]
bars = ax.bar(labels_ff, [ff_counts.get('No', 0), ff_counts.get('Yes', 0)],
              color=colors_ff, edgecolor=COLORS['dark'], width=0.5, linewidth=1)
for bar, val in zip(bars, [ff_counts.get('No', 0), ff_counts.get('Yes', 0)]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{val}\n({val/len(df)*100:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('B7. Ty le khach hang bay thuong xuyen', fontsize=14, fontweight='bold')
ax.set_ylabel('So luong', fontsize=12)
fig.tight_layout()
save_fig(fig, 'B7_frequent_flyer.png')

# B8. Tỷ lệ đã đi nước ngoài
log("\n📊 B8. Tỷ lệ đã đi nước ngoài")
fig, ax = plt.subplots(figsize=(8, 6))
abroad_counts = df['EverTravelledAbroad'].value_counts()
labels_abroad = ['Chua tung\ndi nuoc ngoai', 'Da tung\ndi nuoc ngoai']
colors_abroad = [COLORS['light'], COLORS['secondary']]
bars = ax.bar(labels_abroad, [abroad_counts.get('No', 0), abroad_counts.get('Yes', 0)],
              color=colors_abroad, edgecolor=COLORS['dark'], width=0.5, linewidth=1)
for bar, val in zip(bars, [abroad_counts.get('No', 0), abroad_counts.get('Yes', 0)]):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
            f'{val}\n({val/len(df)*100:.1f}%)', ha='center', va='bottom', fontweight='bold', fontsize=12)
ax.set_title('B8. Ty le khach hang da tung di nuoc ngoai', fontsize=14, fontweight='bold')
ax.set_ylabel('So luong', fontsize=12)
fig.tight_layout()
save_fig(fig, 'B8_travelled_abroad.png')

# B9. Tỷ lệ mua bảo hiểm du lịch (biến mục tiêu)
log("\n📊 B9. Tỷ lệ mua bảo hiểm du lịch (biến mục tiêu)")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

ti_counts = df[target].value_counts().sort_index()
labels_ti = ['Khong mua\nbao hiem', 'Co mua\nbao hiem']
colors_ti = [COLORS['danger'], COLORS['success']]

# Pie chart
wedges, texts, autotexts = axes[0].pie(ti_counts.values, labels=labels_ti,
                                        autopct='%1.1f%%', colors=colors_ti, startangle=90,
                                        explode=(0.05, 0.05), shadow=True,
                                        textprops={'fontsize': 12})
for autotext in autotexts:
    autotext.set_fontweight('bold')
    autotext.set_fontsize(13)
axes[0].set_title('Ty le mua bao hiem du lich', fontsize=13, fontweight='bold')

# Bar chart
bars = axes[1].bar(labels_ti, ti_counts.values, color=colors_ti,
                    edgecolor='white', width=0.5, linewidth=1.5)
for bar, val in zip(bars, ti_counts.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 f'{val}\n({val/len(df)*100:.1f}%)', ha='center', va='bottom',
                 fontweight='bold', fontsize=13)
axes[1].set_ylabel('So luong', fontsize=12)
axes[1].set_title('So luong khach hang mua bao hiem', fontsize=13, fontweight='bold')

fig.suptitle('B9. Phan tich bien muc tieu - Mua bao hiem du lich', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'B9_travel_insurance_target.png')

# PHẦN C: PHÂN TÍCH MỐI QUAN HỆ GIỮA CÁC BIẾN (BIVARIATE)
log("\n" + "=" * 70)
log("PHẦN C: PHÂN TÍCH MỐI QUAN HỆ GIỮA CÁC BIẾN (BIVARIATE)")
log("=" * 70)

# Tạo cột label cho target
df['TravelInsurance_Label'] = df[target].map({0: 'Khong mua', 1: 'Co mua'})

# C1. Tuổi vs Mua bảo hiểm
log("\n📊 C1. Tuổi vs Mua bảo hiểm")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=df, x='TravelInsurance_Label', y='Age', palette=PALETTE_2, ax=axes[0],
            width=0.4, linewidth=1.5)
axes[0].set_title('Tuoi theo trang thai mua bao hiem', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Trang thai bao hiem', fontsize=11)
axes[0].set_ylabel('Tuoi', fontsize=11)

sns.violinplot(data=df, x='TravelInsurance_Label', y='Age', palette=PALETTE_2, ax=axes[1],
               inner='quartile', linewidth=1.5)
axes[1].set_title('Phan phoi tuoi theo trang thai bao hiem', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Trang thai bao hiem', fontsize=11)
axes[1].set_ylabel('Tuoi', fontsize=11)

fig.suptitle('C1. Moi quan he giua Tuoi va Mua bao hiem', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'C1_age_vs_insurance.png')

# C2. Thu nhập vs Mua bảo hiểm
log("\n📊 C2. Thu nhập vs Mua bảo hiểm")
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

sns.boxplot(data=df, x='TravelInsurance_Label', y='AnnualIncome', palette=PALETTE_2, ax=axes[0],
            width=0.4, linewidth=1.5)
axes[0].set_title('Thu nhap theo trang thai mua bao hiem', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Trang thai bao hiem', fontsize=11)
axes[0].set_ylabel('Thu nhap hang nam', fontsize=11)

sns.violinplot(data=df, x='TravelInsurance_Label', y='AnnualIncome', palette=PALETTE_2, ax=axes[1],
               inner='quartile', linewidth=1.5)
axes[1].set_title('Phan phoi thu nhap theo trang thai bao hiem', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Trang thai bao hiem', fontsize=11)
axes[1].set_ylabel('Thu nhap hang nam', fontsize=11)

fig.suptitle('C2. Moi quan he giua Thu nhap va Mua bao hiem', fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'C2_income_vs_insurance.png')

# Thống kê thu nhập theo nhóm
log("\n   Thu nhập trung bình theo nhóm:")
income_stats = df.groupby('TravelInsurance_Label')['AnnualIncome'].agg(['mean', 'median', 'std']).round(0)
log(income_stats.to_string())

# C3. Loại công việc vs Mua bảo hiểm
log("\n📊 C3. Loại công việc vs Mua bảo hiểm")
fig, ax = plt.subplots(figsize=(10, 6))
ct_emp = pd.crosstab(df['Employment Type'], df['TravelInsurance_Label'], normalize='index') * 100
ct_emp.plot(kind='bar', stacked=True, ax=ax, color=PALETTE_2, edgecolor='white', linewidth=1.5)
ax.set_title('C3. Ty le mua bao hiem theo loai hinh cong viec', fontsize=14, fontweight='bold')
ax.set_xlabel('Loai hinh cong viec', fontsize=12)
ax.set_ylabel('Ty le (%)', fontsize=12)
ax.legend(title='Bao hiem', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
for container in ax.containers:
    ax.bar_label(container, fmt='%.1f%%', label_type='center', fontweight='bold', fontsize=10)
fig.tight_layout()
save_fig(fig, 'C3_employment_vs_insurance.png')

# C4. Tốt nghiệp ĐH vs Mua bảo hiểm
log("\n📊 C4. Tốt nghiệp ĐH vs Mua bảo hiểm")
fig, ax = plt.subplots(figsize=(10, 6))
ct_grad = pd.crosstab(df['GraduateOrNot'], df['TravelInsurance_Label'])
ct_grad.plot(kind='bar', ax=ax, color=PALETTE_2, edgecolor='white', linewidth=1.5, width=0.6)
ax.set_title('C4. So luong mua bao hiem theo trinh do hoc van', fontsize=14, fontweight='bold')
ax.set_xlabel('Tot nghiep Dai hoc', fontsize=12)
ax.set_ylabel('So luong', fontsize=12)
ax.legend(title='Bao hiem', fontsize=10)
ax.set_xticklabels(['Chua tot nghiep', 'Da tot nghiep'], rotation=0)
for container in ax.containers:
    ax.bar_label(container, fontweight='bold', fontsize=11, padding=3)
fig.tight_layout()
save_fig(fig, 'C4_graduate_vs_insurance.png')

# C5. Bay thường xuyên vs Mua bảo hiểm
log("\n📊 C5. Bay thường xuyên vs Mua bảo hiểm")
fig, ax = plt.subplots(figsize=(10, 6))
ct_ff = pd.crosstab(df['FrequentFlyer'], df['TravelInsurance_Label'])
ct_ff.plot(kind='bar', ax=ax, color=PALETTE_2, edgecolor='white', linewidth=1.5, width=0.6)
ax.set_title('C5. So luong mua bao hiem theo tan suat bay', fontsize=14, fontweight='bold')
ax.set_xlabel('Bay thuong xuyen', fontsize=12)
ax.set_ylabel('So luong', fontsize=12)
ax.legend(title='Bao hiem', fontsize=10)
ax.set_xticklabels(['Khong', 'Co'], rotation=0)
for container in ax.containers:
    ax.bar_label(container, fontweight='bold', fontsize=11, padding=3)
fig.tight_layout()
save_fig(fig, 'C5_frequent_flyer_vs_insurance.png')

# C6. Đi nước ngoài vs Mua bảo hiểm
log("\n📊 C6. Đi nước ngoài vs Mua bảo hiểm")
fig, ax = plt.subplots(figsize=(10, 6))
ct_abroad = pd.crosstab(df['EverTravelledAbroad'], df['TravelInsurance_Label'])
ct_abroad.plot(kind='bar', ax=ax, color=PALETTE_2, edgecolor='white', linewidth=1.5, width=0.6)
ax.set_title('C6. So luong mua bao hiem theo kinh nghiem di nuoc ngoai', fontsize=14, fontweight='bold')
ax.set_xlabel('Da tung di nuoc ngoai', fontsize=12)
ax.set_ylabel('So luong', fontsize=12)
ax.legend(title='Bao hiem', fontsize=10)
ax.set_xticklabels(['Chua tung', 'Da tung'], rotation=0)
for container in ax.containers:
    ax.bar_label(container, fontweight='bold', fontsize=11, padding=3)
fig.tight_layout()
save_fig(fig, 'C6_abroad_vs_insurance.png')

# C7. Bệnh mãn tính vs Mua bảo hiểm
log("\n📊 C7. Bệnh mãn tính vs Mua bảo hiểm")
fig, ax = plt.subplots(figsize=(10, 6))
ct_chronic = pd.crosstab(df['ChronicDiseases'], df['TravelInsurance_Label'])
ct_chronic.plot(kind='bar', ax=ax, color=PALETTE_2, edgecolor='white', linewidth=1.5, width=0.6)
ax.set_title('C7. So luong mua bao hiem theo benh man tinh', fontsize=14, fontweight='bold')
ax.set_xlabel('Benh man tinh', fontsize=12)
ax.set_ylabel('So luong', fontsize=12)
ax.legend(title='Bao hiem', fontsize=10)
ax.set_xticklabels(['Khong co', 'Co'], rotation=0)
for container in ax.containers:
    ax.bar_label(container, fontweight='bold', fontsize=11, padding=3)
fig.tight_layout()
save_fig(fig, 'C7_chronic_vs_insurance.png')

# C8. Số thành viên gia đình vs Mua bảo hiểm
log("\n📊 C8. Số thành viên gia đình vs Mua bảo hiểm")
fig, ax = plt.subplots(figsize=(12, 6))
ct_family = pd.crosstab(df['FamilyMembers'], df['TravelInsurance_Label'])
ct_family.plot(kind='bar', ax=ax, color=PALETTE_2, edgecolor='white', linewidth=1.5, width=0.7)
ax.set_title('C8. So luong mua bao hiem theo so thanh vien gia dinh', fontsize=14, fontweight='bold')
ax.set_xlabel('So thanh vien gia dinh', fontsize=12)
ax.set_ylabel('So luong', fontsize=12)
ax.legend(title='Bao hiem', fontsize=10)
ax.set_xticklabels(ax.get_xticklabels(), rotation=0)
for container in ax.containers:
    ax.bar_label(container, fontweight='bold', fontsize=9, padding=2)
fig.tight_layout()
save_fig(fig, 'C8_family_vs_insurance.png')

# PHẦN D: PHÂN TÍCH ĐA BIẾN (MULTIVARIATE)
log("\n" + "=" * 70)
log("PHẦN D: PHÂN TÍCH ĐA BIẾN (MULTIVARIATE)")
log("=" * 70)

# D1. Pairplot
log("\n📊 D1. Pairplot các biến số theo biến mục tiêu")
pairplot_fig = sns.pairplot(df[num_cols + [target]], hue=target, palette=PALETTE_2,
                             diag_kind='kde', plot_kws={'alpha': 0.5, 's': 30},
                             height=3)
pairplot_fig.figure.suptitle('D1. Pairplot cac bien so phan biet theo Mua bao hiem',
                              fontsize=15, fontweight='bold', y=1.02)
save_fig(pairplot_fig.figure, 'D1_pairplot.png')

# D2. Heatmap tương quan chi tiết (full)
log("\n📊 D2. Heatmap tương quan chi tiết")
fig, ax = plt.subplots(figsize=(12, 9))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
            center=0, square=True, linewidths=0.8, ax=ax,
            cbar_kws={'shrink': 0.8},
            annot_kws={'fontsize': 10})
ax.set_title('D2. Ma tran tuong quan chi tiet giua tat ca cac bien', fontsize=14, fontweight='bold', pad=15)
fig.tight_layout()
save_fig(fig, 'D2_full_correlation_heatmap.png')

# D3. Thu nhập theo nhóm tuổi và bảo hiểm
log("\n📊 D3. Thu nhập theo nhóm tuổi và bảo hiểm")
df['AgeGroup'] = pd.cut(df['Age'], bins=[24, 27, 30, 33, 36], labels=['25-27', '28-30', '31-33', '34-35'])
fig, ax = plt.subplots(figsize=(12, 6))
sns.boxplot(data=df, x='AgeGroup', y='AnnualIncome', hue='TravelInsurance_Label',
            palette=PALETTE_2, ax=ax, width=0.6, linewidth=1.2)
ax.set_title('D3. Thu nhap theo nhom tuoi va trang thai bao hiem', fontsize=14, fontweight='bold')
ax.set_xlabel('Nhom tuoi', fontsize=12)
ax.set_ylabel('Thu nhap hang nam', fontsize=12)
ax.legend(title='Bao hiem', fontsize=10)
fig.tight_layout()
save_fig(fig, 'D3_income_agegroup_insurance.png')

# PHẦN E: PHÂN TÍCH HÀNH VI KHÁCH HÀNG CHUYÊN SÂU
log("\n" + "=" * 70)
log("PHẦN E: PHÂN TÍCH HÀNH VI KHÁCH HÀNG CHUYÊN SÂU")
log("=" * 70)

# E1. Phân khúc khách hàng theo thu nhập
log("\n📊 E1. Phân khúc khách hàng theo thu nhập")
income_q = df['AnnualIncome'].quantile([0.33, 0.66]).values
df['IncomeGroup'] = pd.cut(df['AnnualIncome'],
                            bins=[0, income_q[0], income_q[1], df['AnnualIncome'].max() + 1],
                            labels=['Thu nhap thap', 'Thu nhap trung binh', 'Thu nhap cao'])

log(f"   Ngưỡng phân khúc: Thấp < {income_q[0]:,.0f} | Trung bình < {income_q[1]:,.0f} | Cao >= {income_q[1]:,.0f}")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Tỷ lệ mua bảo hiểm theo nhóm thu nhập
insurance_rate = df.groupby('IncomeGroup')[target].mean() * 100
bars = axes[0].bar(insurance_rate.index, insurance_rate.values,
                    color=[COLORS['danger'], COLORS['accent'], COLORS['success']],
                    edgecolor='white', width=0.5, linewidth=1.5)
for bar, val in zip(bars, insurance_rate.values):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'{val:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=13)
axes[0].set_title('Ty le mua bao hiem theo nhom thu nhap', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Ty le mua bao hiem (%)', fontsize=11)
axes[0].set_ylim(0, max(insurance_rate.values) + 10)

# Số lượng từng nhóm
group_counts = df['IncomeGroup'].value_counts().sort_index()
bars2 = axes[1].bar(group_counts.index, group_counts.values,
                     color=[COLORS['danger'], COLORS['accent'], COLORS['success']],
                     edgecolor='white', width=0.5, linewidth=1.5)
for bar, val in zip(bars2, group_counts.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                 str(val), ha='center', va='bottom', fontweight='bold', fontsize=13)
axes[1].set_title('So luong khach hang theo nhom thu nhap', fontsize=13, fontweight='bold')
axes[1].set_ylabel('So luong', fontsize=11)

fig.suptitle('E1. Phan khuc khach hang theo thu nhap va ty le mua bao hiem',
             fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'E1_income_segmentation.png')

# E2. Profile khách hàng mua vs không mua bảo hiểm
log("\n📊 E2. Profile khách hàng mua vs không mua bảo hiểm")

profile = df.groupby(target).agg({
    'Age': 'mean',
    'AnnualIncome': 'mean',
    'FamilyMembers': 'mean',
    'ChronicDiseases': 'mean',
}).round(2)
profile.index = ['Khong mua BH', 'Co mua BH']

# Thêm tỷ lệ FrequentFlyer và EverTravelledAbroad
for grp in [0, 1]:
    subset = df[df[target] == grp]
    ff_rate = (subset['FrequentFlyer'] == 'Yes').mean() * 100
    ab_rate = (subset['EverTravelledAbroad'] == 'Yes').mean() * 100
    profile.loc[profile.index[grp], 'FrequentFlyer (%)'] = round(ff_rate, 2)
    profile.loc[profile.index[grp], 'EverTravelledAbroad (%)'] = round(ab_rate, 2)

log("\n   Profile so sánh:")
log(profile.to_string())

# Biểu đồ radar/so sánh
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
compare_features = [
    ('Age', 'Tuoi trung binh', 'mean'),
    ('AnnualIncome', 'Thu nhap trung binh', 'mean'),
    ('FamilyMembers', 'So thanh vien TB', 'mean'),
    ('ChronicDiseases', 'Ty le benh man tinh (%)', 'mean_pct'),
    ('FrequentFlyer', 'Ty le bay thuong xuyen (%)', 'yes_pct'),
    ('EverTravelledAbroad', 'Ty le di nuoc ngoai (%)', 'yes_pct'),
]

for idx, (feat, title, calc_type) in enumerate(compare_features):
    ax = axes[idx // 3][idx % 3]
    
    if calc_type == 'mean':
        vals = [df[df[target] == 0][feat].mean(), df[df[target] == 1][feat].mean()]
    elif calc_type == 'mean_pct':
        vals = [df[df[target] == 0][feat].mean() * 100, df[df[target] == 1][feat].mean() * 100]
    elif calc_type == 'yes_pct':
        vals = [
            (df[df[target] == 0][feat] == 'Yes').mean() * 100,
            (df[df[target] == 1][feat] == 'Yes').mean() * 100
        ]
    
    bars = ax.bar(['Khong mua BH', 'Co mua BH'], vals, color=PALETTE_2,
                   edgecolor='white', width=0.5, linewidth=1.5)
    for bar, val in zip(bars, vals):
        if calc_type in ['mean_pct', 'yes_pct']:
            label = f'{val:.1f}%'
        elif feat == 'AnnualIncome':
            label = f'{val:,.0f}'
        else:
            label = f'{val:.2f}'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(vals)*0.02,
                label, ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(vals) * 1.2)

fig.suptitle('E2. So sanh profile khach hang mua va khong mua bao hiem',
             fontsize=15, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'E2_customer_profile_comparison.png')

# E3. Crosstab: FrequentFlyer × EverTravelledAbroad × TravelInsurance
log("\n📊 E3. Crosstab: Bay thường xuyên × Đi nước ngoài × Mua bảo hiểm")

ct = pd.crosstab([df['FrequentFlyer'], df['EverTravelledAbroad']],
                  df['TravelInsurance_Label'], margins=True)
log("\n   Bảng chéo:")
log(ct.to_string())

ct_rate = pd.crosstab([df['FrequentFlyer'], df['EverTravelledAbroad']],
                       df[target], normalize='index') * 100
log("\n   Tỷ lệ (%):")
log(ct_rate.round(1).to_string())

# Biểu đồ crosstab
fig, ax = plt.subplots(figsize=(10, 6))
ct_rate_reset = ct_rate.reset_index()
ct_rate_reset['Group'] = ct_rate_reset['FrequentFlyer'] + ' - ' + ct_rate_reset['EverTravelledAbroad']
groups = ct_rate_reset['Group'].values
buy_rate = ct_rate_reset[1].values

bars = ax.barh(groups, buy_rate, color=[COLORS['primary'], COLORS['secondary'],
               COLORS['accent'], COLORS['success']], edgecolor='white', height=0.5, linewidth=1.5)
for bar, val in zip(bars, buy_rate):
    ax.text(val + 1, bar.get_y() + bar.get_height()/2,
            f'{val:.1f}%', ha='left', va='center', fontweight='bold', fontsize=12)
ax.set_title('E3. Ty le mua bao hiem: Bay thuong xuyen x Di nuoc ngoai',
             fontsize=14, fontweight='bold')
ax.set_xlabel('Ty le mua bao hiem (%)', fontsize=12)
ax.set_ylabel('Nhom khach hang\n(Bay thuong xuyen - Di nuoc ngoai)', fontsize=11)
ax.set_xlim(0, max(buy_rate) + 15)
fig.tight_layout()
save_fig(fig, 'E3_crosstab_flyer_abroad_insurance.png')

# TỔNG HỢP BIỂU ĐỒ DASHBOARD
log("\n" + "=" * 70)
log("TỔNG HỢP: DASHBOARD TỔNG QUAN")
log("=" * 70)

fig, axes = plt.subplots(2, 3, figsize=(20, 12))

# 1. Target distribution
ti_counts = df[target].value_counts().sort_index()
axes[0][0].pie(ti_counts.values, labels=['Khong mua', 'Co mua'],
               autopct='%1.1f%%', colors=[COLORS['danger'], COLORS['success']],
               startangle=90, explode=(0.03, 0.03), shadow=True,
               textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[0][0].set_title('Ty le mua bao hiem', fontsize=12, fontweight='bold')

# 2. Age distribution
axes[0][1].hist(df['Age'], bins=11, color=COLORS['primary'], edgecolor='white', alpha=0.85)
axes[0][1].set_title('Phan phoi tuoi', fontsize=12, fontweight='bold')
axes[0][1].set_xlabel('Tuoi')

# 3. Income distribution
axes[0][2].hist(df['AnnualIncome'], bins=15, color=COLORS['success'], edgecolor='white', alpha=0.85)
axes[0][2].set_title('Phan phoi thu nhap', fontsize=12, fontweight='bold')
axes[0][2].set_xlabel('Thu nhap')

# 4. Income vs Insurance boxplot
sns.boxplot(data=df, x='TravelInsurance_Label', y='AnnualIncome', palette=PALETTE_2, ax=axes[1][0], width=0.4)
axes[1][0].set_title('Thu nhap vs Bao hiem', fontsize=12, fontweight='bold')
axes[1][0].set_xlabel('Trang thai')
axes[1][0].set_ylabel('Thu nhap')

# 5. Frequent Flyer vs Insurance
ct_ff_norm = pd.crosstab(df['FrequentFlyer'], df['TravelInsurance_Label'], normalize='index') * 100
ct_ff_norm.plot(kind='bar', stacked=True, ax=axes[1][1], color=PALETTE_2, edgecolor='white')
axes[1][1].set_title('Bay thuong xuyen vs Bao hiem', fontsize=12, fontweight='bold')
axes[1][1].set_xlabel('Bay thuong xuyen')
axes[1][1].set_ylabel('Ty le (%)')
axes[1][1].set_xticklabels(['Khong', 'Co'], rotation=0)
axes[1][1].legend(title='Bao hiem', fontsize=8)

# 6. Abroad vs Insurance
ct_ab_norm = pd.crosstab(df['EverTravelledAbroad'], df['TravelInsurance_Label'], normalize='index') * 100
ct_ab_norm.plot(kind='bar', stacked=True, ax=axes[1][2], color=PALETTE_2, edgecolor='white')
axes[1][2].set_title('Di nuoc ngoai vs Bao hiem', fontsize=12, fontweight='bold')
axes[1][2].set_xlabel('Da di nuoc ngoai')
axes[1][2].set_ylabel('Ty le (%)')
axes[1][2].set_xticklabels(['Chua', 'Da tung'], rotation=0)
axes[1][2].legend(title='Bao hiem', fontsize=8)

fig.suptitle('DASHBOARD TONG QUAN - PHAN TICH HANH VI KHACH HANG DU LICH',
             fontsize=18, fontweight='bold', y=1.02)
fig.tight_layout()
save_fig(fig, 'DASHBOARD_overview.png')

# Dọn dẹp cột tạm
df = df.drop(columns=['TravelInsurance_Label', 'AgeGroup', 'IncomeGroup'], errors='ignore')

# LƯU BÁO CÁO
log("\n" + "=" * 70)
log("KẾT QUẢ")
log("=" * 70)

chart_files = [f for f in os.listdir(CHARTS_DIR) if f.endswith('.png')]
log(f"\n📊 Tổng số biểu đồ đã tạo: {len(chart_files)}")
for f in sorted(chart_files):
    log(f"   📈 {f}")

# Lưu báo cáo EDA
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))
log(f"\n📄 Báo cáo EDA đã lưu tại: {REPORT_PATH}")

log("\n🎉 HOÀN THÀNH PHÂN TÍCH EDA!")
