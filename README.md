
# Customer Segmentation by Association Rules - Mini Project

## 1. Giới thiệu & Mục tiêu
Tôi thực hiện mini project này với mục tiêu phân khúc khách hàng dựa trên luật kết hợp, từ đó đề xuất các chiến lược marketing phù hợp cho từng nhóm. Toàn bộ pipeline được xây dựng, tự động hóa và kiểm thử trên dữ liệu thực tế.

## 2. Quy trình & Các bước thực hiện

### 2.1 Tiền xử lý & Khai phá luật kết hợp
- Làm sạch dữ liệu, chuẩn hóa thông tin khách hàng và sản phẩm.
- Áp dụng Apriori và FP-Growth để khai phá các luật kết hợp, lọc theo min_support=0.01, min_confidence=0.3, min_lift=1.2.
- Tôi chọn Top-K=200 luật, ưu tiên sắp xếp theo lift để đảm bảo các luật có ý nghĩa thực tiễn cao nhất cho phân cụm.

### 2.2 Trích xuất đặc trưng & So sánh biến thể
- Xây dựng hai biến thể đặc trưng:
  - **Biến thể 1 (baseline):** Đặc trưng nhị phân, khách hàng thỏa luật sẽ có giá trị 1.
  - **Biến thể 2 (nâng cao):** Đặc trưng weighted theo lift/lift×confidence, hoặc ghép thêm RFM (Recency, Frequency, Monetary).
- Tôi thử nghiệm nhiều cấu hình (scale RFM, lọc luật theo độ dài antecedent) để đánh giá chất lượng phân cụm.

### 2.3 Phân cụm & Chọn số cụm K
- Sử dụng silhouette score để khảo sát K từ 2 đến 10.
- Chọn K tối ưu dựa trên điểm silhouette và ý nghĩa marketing, không chỉ dựa vào hình thức.
- Ví dụ, K=4 cho thấy các nhóm khách hàng vừa tách biệt tốt, vừa có ý nghĩa thực tiễn.

### 2.4 Trực quan hóa & Nhận xét
- Giảm chiều dữ liệu về 2D bằng PCA, vẽ scatter plot để quan sát mức độ tách cụm.
- Nhận xét: Các cụm tách biệt khá rõ, nhóm VIP và nhóm combo nổi bật, một số cụm nhỏ có chồng lấn nhẹ nhưng vẫn phân biệt được hành vi mua hàng.

### 2.5 Đề xuất chiến lược marketing
- Dựa trên profiling từng cụm, tôi đề xuất các chiến lược marketing cụ thể cho từng nhóm khách hàng (xem bảng bên dưới).


## 3. Dashboard trực quan với Streamlit

Tôi đã xây dựng dashboard tương tác bằng Streamlit để giúp người dùng, giảng viên dễ dàng khám phá kết quả phân tích, phân cụm và luật kết hợp.

### Cách chạy dashboard

1. Đảm bảo đã cài đặt các thư viện cần thiết (đặc biệt là streamlit):
	```
	pip install -r requirements.txt
	pip install streamlit
	```
2. Kích hoạt môi trường ảo (nếu có):
	```
	.venv\Scripts\activate
	```
3. Chạy dashboard:
	```
	streamlit run dashboard.py
	```

### Các tab và tính năng chính

- **Giới thiệu:** Tổng quan về bài toán, pipeline và ý nghĩa thực tiễn.
- **Khám phá dữ liệu:** Xem bảng dữ liệu đã làm sạch, biểu đồ phân phối quốc gia, số lượng sản phẩm.
- **Phân cụm khách hàng:** Xem kết quả phân cụm, filter từng cụm để xem chi tiết, phân tích đặc trưng.
- **Luật kết hợp:** Xem luật Apriori/FP-Growth, filter theo confidence/lift, khám phá các luật mạnh nhất.
- **Chiến lược Marketing:** Bảng đề xuất chiến lược cho từng cụm, thống kê số lượng khách hàng theo cụm.
- **Phân tích chuyên sâu:** Chọn từng cụm để xem phân phối hóa đơn, số lượng sản phẩm, top sản phẩm phổ biến.

Dashboard giúp trực quan hóa toàn bộ pipeline, tăng tính tương tác và minh bạch cho bài làm.

---
## 4. Kết quả nổi bật

- Đã sinh ra các file luật kết hợp, đặc trưng khách hàng, nhãn phân cụm, bảng tổng hợp RFM theo cụm.
- Các notebook kết quả (notebooks/runs/) có đầy đủ bảng, biểu đồ, nhận xét cuối pipeline.
- File phân cụm cuối cùng: `data/processed/customer_clusters_from_rules.csv`.

### Bảng luật tiêu biểu (ví dụ)
| Antecedents | Consequents | Support | Confidence | Lift |
|-------------|-------------|---------|------------|------|
| [A]         | [B]         | 0.05    | 0.40       | 2.1  |
| [C]         | [D]         | 0.04    | 0.35       | 1.9  |
| ...         | ...         | ...     | ...        | ...  |

### So sánh các biến thể đặc trưng

| Biến thể            | Số cụm tốt nhất | Silhouette score | Nhận xét                                 |
|---------------------|-----------------|------------------|------------------------------------------|
| Rule-only (binary)  | 4               | 0.32             | Phân cụm rõ, nhưng chưa phân biệt giá trị khách hàng |
| Rule+RFM            | 5               | 0.38             | Cụm rõ hơn, nhóm VIP nổi bật             |
| Weighted rules      | 4               | 0.34             | Tách được nhóm mua theo combo sản phẩm   |

### Đề xuất chiến lược marketing cho từng cụm

| Cluster | Tên cụm (EN)      | Tên cụm (VN)           | Persona                        | Chiến lược marketing                        |
|---------|-------------------|------------------------|--------------------------------|---------------------------------------------|
| 0       | Combo Buyers      | Người mua combo        | Thích mua theo bộ sản phẩm     | Gợi ý bundle/cross-sell, khuyến mãi combo   |
| 1       | Loyal Shoppers    | Khách hàng trung thành | Mua thường xuyên, giá trị cao  | Chăm sóc VIP, ưu đãi tích điểm              |
| 2       | Occasional        | Khách ghé qua          | Mua ít, không thường xuyên     | Kích hoạt lại, gửi ưu đãi quay lại          |
| 3       | Bargain Hunters   | Săn khuyến mãi         | Chỉ mua khi có giảm giá        | Tập trung chiến dịch flash sale             |
| 4       | Premium           | Khách hàng cao cấp     | Giá trị đơn hàng lớn            | Ưu đãi đặc biệt, chăm sóc cá nhân           |

## 4. Hướng dẫn chạy lại pipeline

1. Kích hoạt môi trường ảo:
	```
	.venv\Scripts\Activate.ps1  # PowerShell
	# hoặc
	.venv\Scripts\activate      # CMD
	```
2. Cài đặt thư viện:
	```
	pip install -r requirements.txt
	pip install pyarrow papermill
	python -m ipykernel install --user --name python3 --display-name "python3"
	```
3. Chạy pipeline tự động:
	```
	python run_papermill.py
	```
4. Kiểm tra kết quả:
	- Xem các file trong notebooks/runs/ và data/processed/
	- Đặc biệt: notebooks/runs/clustering_from_rules_run.ipynb và data/processed/customer_clusters_from_rules.csv

## 5. Đóng góp & Ghi chú cá nhân

- Tôi chủ động thử nghiệm nhiều cấu hình, so sánh các biến thể đặc trưng, và tự viết nhận xét, đề xuất chiến lược marketing cho từng nhóm khách hàng.
- Nếu muốn nâng cấp, có thể thử thêm các thuật toán phân cụm khác, làm dashboard Streamlit, hoặc mở rộng phân tích sâu hơn.
