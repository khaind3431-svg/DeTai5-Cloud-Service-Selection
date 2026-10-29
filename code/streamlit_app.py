import streamlit as st
import pandas as pd
from calculation import rank_providers

st.set_page_config(page_title="Chọn dịch vụ Cloud", layout="wide")
st.title("Lựa chọn dịch vụ đám mây")
st.write("So sánh các nhà cung cấp theo SLA, TCO và rủi ro.")

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

sample_data = pd.DataFrame([
    {
        "provider": "AWS",
        "compute_monthly_vnd": 18_000_000,
        "storage_monthly_vnd": 5_000_000,
        "network_monthly_vnd": 4_000_000,
        "support_monthly_vnd": 3_000_000,
        "operations_monthly_vnd": 2_000_000,
        "migration_one_time_vnd": 12_000_000,
        "sla_percent": 99.95,
        "risk_level": 2,
    },
    {
        "provider": "Azure",
        "compute_monthly_vnd": 17_000_000,
        "storage_monthly_vnd": 5_000_000,
        "network_monthly_vnd": 5_000_000,
        "support_monthly_vnd": 3_000_000,
        "operations_monthly_vnd": 2_000_000,
        "migration_one_time_vnd": 10_000_000,
        "sla_percent": 99.95,
        "risk_level": 3,
    },
])

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