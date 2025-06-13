import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Real Estate Dashboard", layout="wide")
st.title("🏠 Real Estate Sales Dashboard (2001 - 2022)")

@st.cache_data
def load_data():
    df = pd.read_csv("Real_Estate_Sales_2001-2022_GL.csv", low_memory=False)
    df['Date Recorded'] = pd.to_datetime(df['Date Recorded'], errors='coerce')
    return df

df = load_data()

st.sidebar.header("🔍 Filter Data")
years = st.sidebar.multiselect("Pilih Tahun", sorted(df['List Year'].dropna().unique()), default=[2020, 2021, 2022])
towns = st.sidebar.multiselect("Pilih Kota", sorted(df['Town'].dropna().unique()), default=["Ansonia", "Avon"])
types = st.sidebar.multiselect("Pilih Tipe Properti", sorted(df['Property Type'].dropna().unique()), default=["Residential", "Commercial"])

filtered_df = df[
    (df["List Year"].isin(years)) &
    (df["Town"].isin(towns)) &
    (df["Property Type"].isin(types))
]

st.subheader("📄 Data Terfilter")
st.dataframe(filtered_df[['List Year', 'Town', 'Address', 'Assessed Value', 'Sale Amount', 'Sales Ratio', 'Property Type']].reset_index(drop=True))

st.markdown("---")
st.subheader("📊 Visualisasi Data")

st.write("### Rata-rata Harga Jual & Nilai Taksiran per Tahun")
avg_df = filtered_df.groupby("List Year")[["Sale Amount", "Assessed Value"]].mean()
st.bar_chart(avg_df)

st.write("### Distribusi Sales Ratio")
fig1, ax1 = plt.subplots()
sns.histplot(filtered_df["Sales Ratio"].dropna(), bins=30, kde=True, ax=ax1, color="teal")
ax1.set_title("Distribusi Sales Ratio")
st.pyplot(fig1)

st.write("### Komposisi Tipe Properti")
pie_data = filtered_df["Property Type"].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')
st.pyplot(fig2)

st.write("### Jumlah Transaksi per Tahun")
trend_df = filtered_df.groupby("List Year")["Serial Number"].count()
st.line_chart(trend_df)

# Footer
st.markdown("---")
st.caption("📌 Data: Connecticut Real Estate Sales (2001-2022)")
