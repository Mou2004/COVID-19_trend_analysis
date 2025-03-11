import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Apply the CSS
load_css("style.css")

st.title('COVID-19 Data Analysis & Visualization')


st.text('Here is a country-wise analysis of COVID-19 data, providing insights into key trends such as new cases, death rates, and the correlation between vaccinations and new cases.')



# Load data
@st.cache_data
def load_data():
    url ="https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv" 
    df = pd.read_csv(url)
    #df = pd.read_csv("owid-covid-data.csv")
    df['date'] = pd.to_datetime(df['date'])
    return df

df = load_data()

# Sidebar - Country Selection
st.sidebar.header("Filters")
country = st.sidebar.selectbox("Select a country", df['location'].unique())

# Filter data for the selected country
df_country = df[df['location'] == country]

# Sidebar - Date Range Selection
start_date = st.sidebar.date_input("Start date", df_country['date'].min().date())
end_date = st.sidebar.date_input("End date", df_country['date'].max().date())
df_country = df_country[(df_country['date'] >= pd.to_datetime(start_date)) & 
                        (df_country['date'] <= pd.to_datetime(end_date))]

# Main Title
st.title(f"📊 {country}")

# Plot new cases
st.write("### 📈 New Cases Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_country['date'], df_country['new_cases'], color='red')
ax.set_xlabel("Date")
ax.set_ylabel("New Cases")
ax.set_title(f"New Cases in {country}")
st.pyplot(fig)

# Calculate and plot death rate
df_country['death_rate'] = (df_country['total_deaths'] / df_country['total_cases']) * 100
st.write("### ⚰️ Death Rate Over Time")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(df_country['date'], df_country['death_rate'], color='black')
ax.set_xlabel("Date")
ax.set_ylabel("Death Rate (%)")
ax.set_title(f"Death Rate in {country}")
st.pyplot(fig)

# Correlation Analysis
st.write("### 🔬 Correlation: Vaccination vs. New Cases")
df_corr = df_country[['new_cases', 'total_vaccinations']].dropna()
if not df_corr.empty:
    correlation = df_corr.corr().iloc[0, 1]
    st.write(f"**Correlation coefficient:** {correlation:.2f}")

    # Heatmap
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(df_corr.corr(), annot=True, cmap='coolwarm', fmt=".2f", ax=ax)
    st.pyplot(fig)
else:
    st.write("Not enough data available for correlation analysis.")

st.write("💡 *Use the filters in the sidebar to refine the data according to your wishes! :P*")
# Footer: Data Source
st.markdown("""
---
📌 **Source of the Data:**  
The data used for this analysis is sourced from the [Our World in Data COVID-19 dataset](https://github.com/owid/covid-19-data), which is publicly available.  
You can download the latest CSV file from:  
➡️ [Download COVID-19 Data (CSV)](https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/owid-covid-data.csv)
""")


