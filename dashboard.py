import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.set_page_config(page_title="Building Growth Dashboard", layout="wide")
st.title("📊 Urban Building Growth Dashboard")
st.markdown("**Area-wise comparison of Building Pixel Count and Number of Buildings**")

# Upload CSV file
uploaded_file = st.file_uploader("C:/Users/hp/Desktop/MRSAC-internship/Dashboard_dataset.xlsx", type=["csv", "xlsx"])
if uploaded_file is not None:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Clean data
    df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(int)

    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    areas = df['Area'].unique()
    selected_areas = st.sidebar.multiselect("Select Area(s)", areas, default=list(areas))
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    year_range = st.sidebar.slider("Select Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

    # Filter data
    df_filtered = df[(df['Area'].isin(selected_areas)) & (df['Year'].between(*year_range))]

    # KPIs
    total_buildings = df_filtered['Number_of_Buildings'].sum()
    total_pixels = df_filtered['Building_Pixel_Count'].sum()
    st.metric("🏗️ Total Buildings", f"{total_buildings}")
    st.metric("🧱 Total Building Pixels", f"{total_pixels}")

    # Line Chart: Building Pixel Count
    st.subheader("📈 Building Pixel Count Over Time")
    for area in selected_areas:
        area_data = df_filtered[df_filtered['Area'] == area]
        plt.plot(area_data['Year'], area_data['Building_Pixel_Count'], label=area)
    plt.xlabel("Year")
    plt.ylabel("Pixel Count")
    plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

    # Line Chart: Number of Buildings
    st.subheader("📊 Number of Buildings Over Time")
    for area in selected_areas:
        area_data = df_filtered[df_filtered['Area'] == area]
        plt.plot(area_data['Year'], area_data['Number_of_Buildings'], label=area)
    plt.xlabel("Year")
    plt.ylabel("No. of Buildings")
    plt.legend()
    st.pyplot(plt.gcf())
    plt.clf()

    # Bar Chart: Average Comparison
    st.subheader("🧮 Average Comparison by Area")
    avg_df = df_filtered.groupby('Area')[['Building_Pixel_Count', 'Number_of_Buildings']].mean().reset_index()
    st.bar_chart(avg_df.set_index('Area'))

else:
    st.warning("Please upload a dataset (CSV or Excel) to begin.")
