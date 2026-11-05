# ☁️ Đề tài 5 – Lựa chọn dịch vụ đám mây (Cloud Service Selection)

> Bài tập môn **Điện toán đám mây** – Nhóm 5

## 👥 Thành viên nhóm

| STT | MSSV | Họ và tên |
|-----|------|-----------|
| 1 | 060205000945 | Tôn Thanh Inra Surôn |
| 2 | 077206009381 | Nguyễn Minh Tiến |
| 3 | 075206003431 | Nguyễn Đức Khải |

---

## 📝 Mô tả đề tài

Xây dựng ứng dụng web hỗ trợ **so sánh và xếp hạng các nhà cung cấp dịch vụ đám mây** dựa trên ba tiêu chí:

- **SLA (Service Level Agreement)** – Cam kết mức độ khả dụng (uptime %)
- **TCO (Total Cost of Ownership)** – Tổng chi phí sở hữu (chi phí di chuyển + chi phí hàng tháng × số tháng)
- **Risk (Rủi ro)** – Đánh giá rủi ro cho doanh nghiệp Việt Nam (thang 1–10)

### Thuật toán xếp hạng

1. Tính **TCO** = chi phí di chuyển một lần + tổng chi phí hàng tháng × số tháng sử dụng
2. **Chuẩn hóa Min-Max** (0–100 điểm):
   - SLA: chuẩn hóa lợi ích (càng cao càng tốt)
   - TCO & Risk: chuẩn hóa chi phí (càng thấp càng tốt)
3. Tính **điểm tổng** = SLA × w₁ + TCO × w₂ + Risk × w₃ (w là trọng số do người dùng chọn)
4. **Xếp hạng** giảm dần theo điểm tổng

### Kịch bản so sánh

- 1 máy ảo Linux: 4 vCPU / 16 GB RAM
- Ổ SSD khoảng 500 GB
- Lưu lượng ra Internet khoảng 1 TB/tháng
- Tỷ giá quy đổi: 1 USD = 26.000 VND
- 5 nhà cung cấp: **AWS**, **Azure**, **Google Cloud**, **FPT Cloud**, **Viettel IDC**

Chi tiết nguồn dữ liệu xem tại [`data/NGUON_DU_LIEU.md`](data/NGUON_DU_LIEU.md).

---

## 📁 Cấu trúc dự án

```
DeTai5-Cloud-Service-Selection/
├── code/
│   ├── calculation.py          # Thuật toán tính TCO, chuẩn hóa, xếp hạng
│   └── streamlit_app.py        # Giao diện web (Streamlit)
├── data/
│   ├── providers.csv           # Dữ liệu 5 nhà cung cấp Cloud
│   └── NGUON_DU_LIEU.md        # Tài liệu nguồn dữ liệu
├── tests/
│   └── test_calculation.py     # Kiểm thử đơn vị (unit test)
├── CHAY_UNG_DUNG.bat           # Script chạy ứng dụng (Windows)
├── CHAY_KIEM_THU.bat           # Script chạy kiểm thử (Windows)
├── requirements.txt            # Thư viện cần cài đặt
└── README.md                   # Tài liệu hướng dẫn (file này)
```

---

## 🚀 Hướng dẫn cài đặt và chạy

### Yêu cầu

- **Python 3.10** trở lên
- **pip** (trình quản lý gói Python)

### Cách 1: Chạy nhanh bằng file .bat (Windows)

1. Mở thư mục dự án
2. Nhấp đúp vào `CHAY_UNG_DUNG.bat`
3. Trình duyệt sẽ tự mở tại `http://localhost:8501`

### Cách 2: Chạy bằng dòng lệnh

```bash
# Bước 1: Clone dự án
git clone https://github.com/khaind3431-svg/DeTai5-Cloud-Service-Selection.git
cd DeTai5-Cloud-Service-Selection

# Bước 2: Tạo môi trường ảo (khuyến nghị)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Bước 3: Cài đặt thư viện
pip install -r requirements.txt

# Bước 4: Chạy ứng dụng
streamlit run code/streamlit_app.py
```

Ứng dụng sẽ mở trên trình duyệt tại `http://localhost:8501`.

### Chạy kiểm thử (Unit Test)

```bash
# Cách 1: Nhấp đúp CHAY_KIEM_THU.bat (Windows)

# Cách 2: Dòng lệnh
python -m unittest discover -s tests -v
```

Kết quả mong đợi:

```
test_calculate_tco ... ok
test_normalize_benefit ... ok
test_normalize_cost ... ok
test_rank_providers_returns_highest_score_first ... ok
test_csv_has_real_cloud_providers ... ok
test_demo_default_weights_ranks_real_providers ... ok
----------------------------------------------------------------------
Ran 6 tests in 0.05s
OK
```

---

## 🖥️ Hướng dẫn sử dụng

1. **Chọn thời gian sử dụng** (số tháng) – mặc định 36 tháng
2. **Điều chỉnh trọng số** cho 3 tiêu chí (tổng nên bằng 100%):
   - SLA: mặc định 40%
   - TCO: mặc định 35%
   - Risk: mặc định 25%
3. **Xem và chỉnh sửa dữ liệu** nhà cung cấp trực tiếp trên bảng (có thể thêm/xóa dòng)
4. Nhấn nút **"🚀 Tính điểm và xếp hạng"**
5. Xem kết quả:
   - **Bảng xếp hạng** với điểm chi tiết từng tiêu chí
   - **Biểu đồ so sánh** trực quan
   - **Đề xuất** nhà cung cấp tốt nhất

---

## 🛠️ Công nghệ sử dụng

| Công nghệ | Phiên bản | Mục đích |
|------------|-----------|----------|
| Python | ≥ 3.10 | Ngôn ngữ lập trình |
| Pandas | 2.3.3 | Xử lý dữ liệu |
| Streamlit | 1.50.0 | Giao diện web |
| unittest | (built-in) | Kiểm thử đơn vị |
