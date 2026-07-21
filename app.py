import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. Page Configuration & Ultra-Premium CSS
# ------------------------------------------------------------------------------
st.set_page_config(page_title="AeroZone Investor Portal", page_icon="🌪️", layout="wide")

st.markdown("""
    <style>
    /* Premium Dashboard UI */
    .stApp { background-color: #f4f7f6; }
    h1, h2, h3 { color: #0f2027; font-family: 'Helvetica Neue', sans-serif; font-weight: 700; }
    .st-emotion-cache-1y4p8pa { padding-top: 2rem; }
    /* Sleek metric cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff;
        border: 1px solid #e0e5e9;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.03);
        transition: transform 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Data Loading
# ------------------------------------------------------------------------------
@st.cache_data
def load_data():
    df_fin = pd.read_csv("financial_projections.csv")
    df_demo = pd.read_csv("customer_demographics.csv")
    return df_fin, df_demo

try:
    df_fin, df_demo = load_data()
except FileNotFoundError:
    st.error("⚠️ Datasets missing. Ensure 'financial_projections.csv' and 'customer_demographics.csv' are in the directory.")
    st.stop()

# ------------------------------------------------------------------------------
# 3. Sidebar (Investor Controls)
# ------------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3714/3714959.png", width=60) # Placeholder Air Tech Icon
st.sidebar.title("AeroZone")
st.sidebar.markdown("**Interactive Pitch Deck**")
st.sidebar.markdown("---")
st.sidebar.subheader("Global Filters")

selected_regions = st.sidebar.multiselect("Market Regions", df_demo['Geographic_Region'].unique(), default=df_demo['Geographic_Region'].unique())
min_aqi, max_aqi = int(df_demo['Local_AQI_At_Purchase'].min()), int(df_demo['Local_AQI_At_Purchase'].max())
selected_aqi = st.sidebar.slider("Purchase Environment (AQI)", 30, 300, (min_aqi, max_aqi))

filtered_demo = df_demo[
    (df_demo['Geographic_Region'].isin(selected_regions)) &
    (df_demo['Local_AQI_At_Purchase'] >= selected_aqi[0]) &
    (df_demo['Local_AQI_At_Purchase'] <= selected_aqi[1])
]

# ------------------------------------------------------------------------------
# 4. Hero KPIs (Top Row)
# ------------------------------------------------------------------------------
st.title("AeroZone: Series A Financial & Market Brief")
st.markdown("Interact with the charts below by dragging, zooming, and hovering over data points.")

col1, col2, col3, col4 = st.columns(4)
col1.metric("M36 Annual Recurring Rev (ARR)", f"${(df_fin['Subscription_Revenue'].iloc[-1] * 12):,.0f}", "+185% YoY")
col2.metric("Blended Gross Margin", f"{df_fin['Gross_Margin_%'].iloc[-1]:.1f}%", "+Scale Efficiency")
col3.metric("Hardware Units Sold (Total)", f"{df_fin['Hardware_Units_Sold'].sum():,}", "Global Reach")
col4.metric("Customer Acquisition Cost", f"${df_fin['CAC'].iloc[-1]:.2f}", "-$25.00 from M1", delta_color="inverse")

st.markdown("---")

# ------------------------------------------------------------------------------
# 5. Section 1: Financial Trajectory (Interactive Area & Bar)
# ------------------------------------------------------------------------------
st.subheader("1. The Revenue Engine: Hardware vs. Recurring SaaS")

fig1 = go.Figure()
# Subscription base layer (Area)
fig1.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Subscription_Revenue'], mode='lines', fill='tozeroy', 
                          name='SaaS Revenue', line=dict(color='#00d2ff', width=3)))
# Hardware spikes (Bar)
fig1.add_trace(go.Bar(x=df_fin['Month'], y=df_fin['Hardware_Revenue'], 
                      name='Hardware Revenue', marker_color='#3a7bd5', opacity=0.8))
# Total Revenue (Line overlay)
fig1.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Total_Gross_Revenue'], mode='lines+markers', 
                          name='Total Gross', line=dict(color='#0f2027', width=3)))

fig1.update_layout(height=500, template="plotly_white", hovermode="x unified", 
                   legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
st.plotly_chart(fig1, use_container_width=True)

# ------------------------------------------------------------------------------
# 6. Section 2: Advanced Demographics & Unit Economics
# ------------------------------------------------------------------------------
col_a, col_b = st.columns([1.2, 1])

with col_a:
    st.subheader("2. Market Penetration (Sunburst)")
    # Interactive Sunburst showing Region -> Persona -> Channel
    fig_sun = px.sunburst(
        filtered_demo, 
        path=['Geographic_Region', 'Customer_Persona', 'Acquisition_Channel'], 
        color='App_Engagement_Score', 
        color_continuous_scale='Teal',
        title="Click segments to drill down into markets"
    )
    fig_sun.update_layout(height=450, margin=dict(t=40, l=0, r=0, b=0))
    st.plotly_chart(fig_sun, use_container_width=True)

with col_b:
    st.subheader("3. Unit Economics Over Time")
    # Dual-axis graph for CAC vs LTV proxy (Gross Margin)
    fig_unit = make_subplots(specs=[[{"secondary_y": True}]])
    fig_unit.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['CAC'], name="CAC ($)", 
                                  mode='lines+markers', line=dict(color='#ff4b2b', width=3)), secondary_y=False)
    fig_unit.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Gross_Margin_%'], name="Gross Margin (%)", 
                                  mode='lines', fill='tozeroy', line=dict(color='#2ebf91', width=2)), secondary_y=True)
    
    fig_unit.update_layout(height=450, template="plotly_white", hovermode="x unified",
                           title="Decreasing Acq. Cost vs. Rising Margins")
    st.plotly_chart(fig_unit, use_container_width=True)

# ------------------------------------------------------------------------------
# 7. Section 3: The Environmental Catalyst
# ------------------------------------------------------------------------------
st.subheader("4. Product-Market Fit: The Environment as a Growth Catalyst")

fig_aqi = px.scatter(
    filtered_demo, x='Local_AQI_At_Purchase', y='App_Engagement_Score', 
    color='Customer_Persona', size='Local_AQI_At_Purchase', 
    hover_name='Geographic_Region',
    title="Drag to zoom into specific clusters. Notice the density of high engagement in >150 AQI zones.",
    color_discrete_sequence=['#ff4b2b', '#2ebf91', '#3a7bd5']
)
# Add colored danger zones
fig_aqi.add_vrect(x0=0, x1=50, fillcolor="#00e676", opacity=0.1, layer="below", line_width=0)
fig_aqi.add_vrect(x0=50, x1=150, fillcolor="#ffea00", opacity=0.1, layer="below", line_width=0)
fig_aqi.add_vrect(x0=150, x1=300, fillcolor="#ff1744", opacity=0.1, layer="below", line_width=0)
fig_aqi.update_layout(height=500, template="plotly_white", xaxis_title="Air Quality Index (AQI)", yaxis_title="App Engagement Score (1-10)")
st.plotly_chart(fig_aqi, use_container_width=True)

# ------------------------------------------------------------------------------
# 8. Raw Data Grids (Investor Due Diligence)
# ------------------------------------------------------------------------------
with st.expander("🔍 Expand for Interactive Due Diligence Data Grids"):
    st.markdown("Sort, search, and download the raw projections.")
    st.dataframe(df_fin.style.background_gradient(cmap='Blues', subset=['Total_Gross_Revenue']), use_container_width=True)
