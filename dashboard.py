import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

st.set_page_config(page_title="Customer Segmentation Dashboard", layout="wide")
st.title("Customer Segmentation & Association Rules Dashboard")

# Load data
@st.cache_data
def load_data():
    cleaned = pd.read_csv("data/processed/cleaned_uk_data.csv") if os.path.exists("data/processed/cleaned_uk_data.csv") else None
    clusters = pd.read_csv("data/processed/customer_clusters_from_rules.csv") if os.path.exists("data/processed/customer_clusters_from_rules.csv") else None
    rules_apriori = pd.read_csv("data/processed/rules_apriori_filtered.csv") if os.path.exists("data/processed/rules_apriori_filtered.csv") else None
    rules_fpgrowth = pd.read_csv("data/processed/rules_fpgrowth_filtered.csv") if os.path.exists("data/processed/rules_fpgrowth_filtered.csv") else None
    return cleaned, clusters, rules_apriori, rules_fpgrowth

cleaned, clusters, rules_apriori, rules_fpgrowth = load_data()

# Sidebar
st.sidebar.header("Navigation")
page = st.sidebar.radio("Go to", [
    "Giới thiệu", 
    "Khám phá dữ liệu", 
    "Phân cụm khách hàng", 
    "Luật kết hợp", 
    "Chiến lược Marketing",
    "Phân tích chuyên sâu"
])

if page == "Giới thiệu":
    st.markdown("""
    ## Giới thiệu
    Dashboard này giúp bạn khám phá kết quả phân tích dữ liệu bán lẻ, phân cụm khách hàng và khai phá luật kết hợp.
    - **Nguồn dữ liệu:** Online Retail UK
    - **Các bước chính:** Làm sạch, phân cụm, khai phá luật, đề xuất chiến lược marketing.
    """)

if page == "Khám phá dữ liệu":
    st.header("Khám phá dữ liệu đã làm sạch")
    if cleaned is not None:
        st.dataframe(cleaned.head(100))
        st.write(f"Số dòng: {cleaned.shape[0]}, Số cột: {cleaned.shape[1]}")
        st.subheader("Biểu đồ số lượng đơn hàng theo quốc gia")
        fig, ax = plt.subplots(figsize=(10,4))
        cleaned['Country'].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)
        st.subheader("Phân phối số lượng sản phẩm mỗi đơn hàng")
        fig2, ax2 = plt.subplots()
        cleaned['Quantity'].hist(bins=30, ax=ax2)
        st.pyplot(fig2)
    else:
        st.warning("Không tìm thấy file cleaned_uk_data.csv")

if page == "Phân cụm khách hàng":
    st.header("Kết quả phân cụm khách hàng")
    if clusters is not None:
        st.dataframe(clusters.head(100))
        st.subheader("Phân bố các cụm")
        fig = px.histogram(clusters, x='cluster', color='cluster', nbins=10)
        st.plotly_chart(fig)
        st.subheader("Phân tích đặc trưng từng cụm")
        st.write(clusters.groupby('cluster').mean(numeric_only=True))
        st.subheader("Chọn cụm để xem chi tiết")
        cluster_ids = clusters['cluster'].unique()
        selected_cluster = st.selectbox("Chọn cụm:", cluster_ids)
        st.write(clusters[clusters['cluster'] == selected_cluster].head(20))
    else:
        st.warning("Không tìm thấy file customer_clusters_from_rules.csv")

if page == "Luật kết hợp":
    st.header("Luật kết hợp (Apriori & FP-Growth)")
    tab1, tab2 = st.tabs(["Apriori", "FP-Growth"])
    with tab1:
        if rules_apriori is not None:
            st.dataframe(rules_apriori.head(50))
            st.write(f"Tổng số luật Apriori: {rules_apriori.shape[0]}")
            st.subheader("Lọc luật theo độ tin cậy (confidence)")
            min_conf = st.slider("Chọn min confidence", 0.0, 1.0, 0.5, 0.05)
            filtered = rules_apriori[rules_apriori['confidence'] >= min_conf]
            st.dataframe(filtered.head(20))
        else:
            st.warning("Không tìm thấy file rules_apriori_filtered.csv")
    with tab2:
        if rules_fpgrowth is not None:
            st.dataframe(rules_fpgrowth.head(50))
            st.write(f"Tổng số luật FP-Growth: {rules_fpgrowth.shape[0]}")
            st.subheader("Lọc luật theo lift")
            min_lift = st.slider("Chọn min lift", 0.0, 10.0, 1.0, 0.1)
            filtered = rules_fpgrowth[rules_fpgrowth['lift'] >= min_lift]
            st.dataframe(filtered.head(20))
        else:
            st.warning("Không tìm thấy file rules_fpgrowth_filtered.csv")

if page == "Chiến lược Marketing":
    st.header("Đề xuất chiến lược Marketing cho từng cụm")
    st.markdown("""
    | Cụm | Đặc điểm | Chiến lược đề xuất |
    |-----|----------|--------------------|
    | 0   | Khách hàng trung thành | Ưu đãi thành viên, tặng voucher |
    | 1   | Khách hàng mới | Khuyến mãi lần đầu, upsell sản phẩm phổ biến |
    | 2   | Khách hàng ít mua | Gửi email remarketing, giảm giá mạnh |
    ...
    """)
    if clusters is not None:
        st.subheader("Thống kê số lượng khách theo cụm")
        st.bar_chart(clusters['cluster'].value_counts())
    else:
        st.info("Cần có file customer_clusters_from_rules.csv để hiển thị thống kê.")

# --- Phân tích chuyên sâu ---
if page == "Phân tích chuyên sâu":
    st.header("Phân tích chuyên sâu từng cụm khách hàng")
    if clusters is not None:
        cluster_ids = clusters['cluster'].unique()
        selected_cluster = st.selectbox("Chọn cụm để phân tích sâu:", cluster_ids)
        cluster_data = clusters[clusters['cluster'] == selected_cluster]
        st.write(f"Số khách hàng trong cụm {selected_cluster}: {cluster_data.shape[0]}")
        st.subheader("Phân phối giá trị hóa đơn (TotalPrice)")
        if 'TotalPrice' in cluster_data.columns:
            fig, ax = plt.subplots()
            cluster_data['TotalPrice'].hist(bins=30, ax=ax)
            st.pyplot(fig)
        st.subheader("Phân phối số lượng sản phẩm mua")
        if 'Quantity' in cluster_data.columns:
            fig2, ax2 = plt.subplots()
            cluster_data['Quantity'].hist(bins=30, ax=ax2)
            st.pyplot(fig2)
        st.subheader("Top sản phẩm phổ biến trong cụm")
        if 'Description' in cluster_data.columns:
            top_products = cluster_data['Description'].value_counts().head(10)
            st.bar_chart(top_products)
    else:
        st.info("Cần có file customer_clusters_from_rules.csv để phân tích.")
