from pathlib import Path

import streamlit as st
import pandas as pd
from calculation import rank_providers

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "providers.csv"

st.set_page_config(page_title="Chọn dịch vụ Cloud", layout="wide")
st.title("Lựa chọn dịch vụ đám mây")
st.write("So sánh các nhà cung cấp theo SLA, TCO và rủi ro.")
st.caption(
    "Dữ liệu thật theo kịch bản 4 vCPU / 16GB / ~500GB SSD / ~1TB lưu lượng, "
    "tỷ giá 26.000 VND/USD. Chi tiết nguồn: data/NGUON_DU_LIEU.md"
)

months = st.number_input(
    "Thời gian sử dụng (tháng)",
    min_value=1,
    value=36,
    step=1,
)

sla_weight = st.slider("Trọng số SLA (%)", 0, 100, 40)
tco_weight = st.slider("Trọng số TCO (%)", 0, 100, 35)
risk_weight = st.slider("Trọng số Risk (%)", 0, 100, 25)

st.caption(
    f"Tổng trọng số hiện tại: "
    f"{sla_weight + tco_weight + risk_weight}%"
)

sample_data = pd.read_csv(DATA_PATH)

st.subheader("Dữ liệu nhà cung cấp")
edited_data = st.data_editor(
    sample_data,
    num_rows="dynamic",
    use_container_width=True,
)

if st.button("Tính điểm và xếp hạng", type="primary"):
    weight_total = sla_weight + tco_weight + risk_weight

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

        st.subheader("Kết quả xếp hạng")
        st.dataframe(result, use_container_width=True)