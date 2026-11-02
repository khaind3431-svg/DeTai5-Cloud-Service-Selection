# Nguồn dữ liệu nhà cung cấp

Kịch bản so sánh (cùng workload):

- 1 máy ảo Linux 4 vCPU / 16 GB RAM
- Ổ SSD khoảng 500 GB
- Lưu lượng ra Internet khoảng 1 TB/tháng
- Tỷ giá quy đổi: 1 USD = 26.000 VND (làm tròn)
- Thời điểm tham chiếu: 2026

## SLA (máy ảo đơn, theo tài liệu công khai)

| Nhà cung cấp | SLA dùng trong mô hình | Nguồn |
| --- | --- | --- |
| AWS | 99.50% | Amazon EC2 Instance-Level SLA |
| Azure | 99.90% | SLA for Virtual Machines, Premium SSD single instance |
| Google Cloud | 99.90% | Compute Engine SLA, single instance (các family thông thường) |
| FPT Cloud | 99.99% | FPT Cloud Server uptime công bố |
| Viettel IDC | 99.90% | Mức dùng thận trọng khi gói Cloud Server không nêu SLA chi tiết trên bảng giá |

Nếu triển khai nhiều vùng (multi-AZ), AWS / Azure / Google Cloud đều công bố 99.99%. Alibaba Cloud ECS multi-zone là 99.995%.

## Chi phí

- AWS / Azure / Google Cloud: giá on-demand máy 4 vCPU 16 GB (m6i.xlarge / D4s v5 / n2-standard-4), ổ SSD ~500 GB, egress ~1 TB, hỗ trợ Developer ~29 USD/tháng.
- FPT Cloud / Viettel IDC: giá gói Cloud Server 4 vCPU 16 GB công bố tại Việt Nam; lưu lượng thường gói trong gói nên `network_monthly_vnd = 0`; cộng thêm ổ đĩa cho đủ ~500 GB.
- `operations_monthly_vnd`: chi phí vận hành nội bộ ước lượng (hyperscaler cần kỹ năng chuyên sâu hơn).
- `migration_one_time_vnd`: chi phí chuyển đổi ước lượng (đào tạo, kiến trúc, thanh toán USD, dữ liệu ra nước ngoài).

## Rủi ro (thang 1-10)

Đánh giá cho doanh nghiệp Việt Nam có dữ liệu cần lưu trong nước:

- FPT Cloud, Viettel IDC: 3 (data center trong nước, hợp đồng VND, hỗ trợ tiếng Việt).
- Azure: 5 (hệ sinh thái lớn, dữ liệu thường ở Singapore/Đông Nam Á).
- AWS, Google Cloud: 6 (chưa có region Việt Nam, vendor lock-in, chi phí USD).

Đây là dữ liệu tham chiếu để demo mô hình, không phải báo giá chính thức. Khi làm thật cần nhập lại từ máy tính giá của nhà cung cấp.
