from pathlib import Path

import streamlit as st
import pandas as pd
from calculation import rank_providers

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "providers.csv"

st.set_page_config(page_title="Chọn dịch vụ Cloud", layout="wide")
st.title("☁️ Lựa chọn dịch vụ đám mây")
st.write("So sánh các nhà cung cấp theo **SLA**, **TCO** và **Rủi ro**.")
st.caption(
    "Dữ liệu thật theo kịch bản 4 vCPU / 16 GB / ~500 GB SSD / ~1 TB lưu lượng, "
    "tỷ giá 26.000 VND/USD. Chi tiết nguồn: data/NGUON_DU_LIEU.md"
)

st.divider()

# --- Tham so dau vao ---
st.subheader("⚙️ Tham số đầu vào")

months = st.number_input(
    "Thời gian sử dụng (tháng)",
    min_value=1,
    value=36,
    step=1,
)

col1, col2, col3 = st.columns(3)
with col1:
    sla_weight = st.slider("Trọng số SLA (%)", 0, 100, 40)
with col2:
    tco_weight = st.slider("Trọng số TCO (%)", 0, 100, 35)
with col3:
    risk_weight = st.slider("Trọng số Risk (%)", 0, 100, 25)

weight_total = sla_weight + tco_weight + risk_weight

if weight_total != 100:
    st.warning(
        f"⚠️ Tổng trọng số hiện tại: **{weight_total}%** "
        f"(nên bằng 100% để kết quả chính xác)"
    )
else:
    st.success(f"✅ Tổng trọng số: {weight_total}%")

st.divider()

# --- Bang du lieu ---
sample_data = pd.read_csv(DATA_PATH)

st.subheader("📋 Dữ liệu nhà cung cấp")
edited_data = st.data_editor(
    sample_data,
    num_rows="dynamic",
    use_container_width=True,
)

st.divider()

# --- Tinh diem va xep hang ---
if st.button("🚀 Tính điểm và xếp hạng", type="primary"):
    if weight_total == 0:
        st.error("Tổng trọng số phải lớn hơn 0.")
    else:
        result = rank_providers(
            edited_data,
            months,
            sla_weight,
            tco_weight,
            risk_weight,
        )

        st.subheader("🏆 Kết quả xếp hạng")
        st.dataframe(result, use_container_width=True)

        # --- Bieu do truc quan ---
        st.subheader("📊 Biểu đồ so sánh")

        chart_cols = ["sla_score", "tco_score", "risk_score", "total_score"]
        chart_data = result.set_index("provider")[chart_cols]

        st.bar_chart(chart_data)

        # --- Nha cung cap tot nhat ---
        best = result.iloc[0]
        st.success(
            f"🥇 Nhà cung cấp được đề xuất: **{best['provider']}** "
            f"với tổng điểm **{best['total_score']}**"
        )
