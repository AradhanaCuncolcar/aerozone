import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. Page Configuration & Theming
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="AeroZone Investor Dashboard",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "Clean Air & Tech" aesthetics
st.markdown("""
    <style>
    .stApp {
        background-color: #f8fbff;
    }
    h1, h2, h3 {
        color: #0b3d91;
    }
    .metric-container {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Data Loading & Caching
# ------------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Load the datasets
    df_fin = pd.read_csv("financial_projections.csv")
    df_demo = pd.read_csv("customer_demographics.csv")
    return df_fin, df_demo

try:
    df_fin, df_demo = load_data()
except FileNotFoundError:
    st.error("⚠️ Datasets not found. Please ensure 'financial_projections.csv' and 'customer_demographics.csv' are in the same directory.")
    st.stop()

# ------------------------------------------------------------------------------
# 3. Sidebar & Global Filters
# ------------------------------------------------------------------------------
st.sidebar.title("☁️ AeroZone")
st.sidebar.markdown("**Wearable Air Purification**")
st.sidebar.markdown("---")
st.sidebar.subheader("Demographics Filters")

# Sidebar Filters
all_regions = df_demo['Geographic_Region'].unique().tolist()
selected_regions = st.sidebar.multiselect("Geographic Region", all_regions, default=all_regions)

all_personas = df_demo['Customer_Persona'].unique().tolist()
selected_personas = st.sidebar.multiselect("Customer Persona", all_personas, default=all_personas)

min_aqi = int(df_demo['Local_AQI_At_Purchase'].min())
max_aqi = int(df_demo['Local_AQI_At_Purchase'].max())
selected_aqi = st.sidebar.slider("AQI Range at Purchase", 30, 300, (min_aqi, max_aqi))

# Apply filters to demographic data
filtered_demo = df_demo[
    (df_demo['Geographic_Region'].isin(selected_regions)) &
    (df_demo['Customer_Persona'].isin(selected_personas)) &
    (df_demo['Local_AQI_At_Purchase'] >= selected_aqi[0]) &
    (df_demo['Local_AQI_At_Purchase'] <= selected_aqi[1])
]

# ------------------------------------------------------------------------------
# 4. Hero Metrics (KPIs)
# ------------------------------------------------------------------------------
st.title("AeroZone Financial & Growth Dashboard")
st.markdown("Confidential Investor Briefing - Series A Pitch")

# Calculate KPIs
year_3_revenue = df_fin[df_fin['Month'] > 24]['Total_Gross_Revenue'].sum()
month_36_subs = df_fin['Active_Subscribers'].iloc[-1]
month_36_margin = df_fin['Gross_Margin_%'].iloc[-1]
avg_cac = df_fin['CAC'].mean()

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Projected Revenue (Year 3)", value=f"${year_3_revenue:,.0f}", delta="High Growth")
with col2:
    st.metric(label="Active Subscribers (Month 36)", value=f"{month_36_subs:,}", delta="Compounding ARR")
with col3:
    st.metric(label="Gross Margin (Month 36)", value=f"{month_36_margin:.1f}%", delta="Scale Economics")
with col4:
    st.metric(label="Avg Customer Acq. Cost", value=f"${avg_cac:.2f}", delta="-41% Target by M36", delta_color="inverse")

st.markdown("---")

# ------------------------------------------------------------------------------
# 5. Section 1: Financial Trajectory
# ------------------------------------------------------------------------------
st.header("Financial Trajectory & Scalability")
st.markdown("> **Investor Takeaway:** Notice the massive revenue spikes corresponding to late-summer wildfire seasons (Aug/Sep) and winter smog (Dec/Jan). The subscription revenue acts as a robust baseline that dampens seasonality and ensures predictable, compounding ARR.")

col_f1, col_f2 = st.columns(2)

with col_f1:
    # Chart 1: The Hockey Stick (Total, Hardware, Sub Revenue)
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Total_Gross_Revenue'], mode='lines', name='Total Revenue', line=dict(color='#0b3d91', width=3)))
    fig1.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Hardware_Revenue'], mode='lines', name='Hardware Revenue', line=dict(color='#00a8cc', width=2, dash='dot')))
    fig1.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Subscription_Revenue'], mode='lines', name='Subscription Revenue', fill='tozeroy', line=dict(color='#20b2aa', width=2)))
    fig1.update_layout(title="Revenue Growth & SaaS Transition", xaxis_title="Month", yaxis_title="Revenue ($)", template="plotly_white", hovermode="x unified")
    st.plotly_chart(fig1, use_container_width=True)

with col_f2:
    # Chart 2: Unit Economics (Hardware Units vs CAC)
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(go.Bar(x=df_fin['Month'], y=df_fin['Hardware_Units_Sold'], name="Units Sold", marker_color='#87cefa'), secondary_y=False)
    fig2.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['CAC'], name="CAC ($)", mode='lines', line=dict(color='#ff7f50', width=3)), secondary_y=True)
    fig2.update_layout(title="Unit Economics & CAC Efficiency", xaxis_title="Month", template="plotly_white", hovermode="x unified")
    fig2.update_yaxes(title_text="Units Sold", secondary_y=False)
    fig2.update_yaxes(title_text="CAC ($)", secondary_y=True)
    st.plotly_chart(fig2, use_container_width=True)

# Chart 3: Profitability (Gross Margin)
fig3 = px.area(df_fin, x='Month', y='Gross_Margin_%', title="Gross Margin Expansion (Economies of Scale)", color_discrete_sequence=['#4682b4'])
fig3.update_layout(xaxis_title="Month", yaxis_title="Gross Margin (%)", template="plotly_white")
st.plotly_chart(fig3, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# 6. Section 2: Customer Insights & Market Dynamics
# ------------------------------------------------------------------------------
st.header("Customer Insights & Market Dynamics")
st.markdown("> **Investor Takeaway:** High AQI is our strongest acquisition catalyst. As environmental challenges rise, our hardware operates as a real-time health shield. Notice the direct correlation: when air quality deteriorates, app engagement spikes, directly driving our viral loops and retention metrics.")

col_c1, col_c2 = st.columns([1, 2])

with col_c1:
    # Chart 4: Who is buying? (Donut Chart)
    persona_counts = filtered_demo['Customer_Persona'].value_counts().reset_index()
    persona_counts.columns = ['Persona', 'Count']
    fig4 = px.pie(persona_counts, values='Count', names='Persona', hole=0.4, title="Customer Personas", color_discrete_sequence=px.colors.sequential.Teal)
    st.plotly_chart(fig4, use_container_width=True)
    
    # Chart 6: Acquisition Channels
    channel_counts = filtered_demo['Acquisition_Channel'].value_counts().reset_index()
    channel_counts.columns = ['Channel', 'Count']
    fig6 = px.bar(channel_counts, x='Count', y='Channel', orientation='h', title="Top Acquisition Channels", color_discrete_sequence=['#0b3d91'])
    fig6.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig6, use_container_width=True)

with col_c2:
    # Chart 5: The Environmental Trigger (AQI vs Engagement)
    fig5 = px.scatter(
        filtered_demo, 
        x='Local_AQI_At_Purchase', 
        y='App_Engagement_Score', 
        color='Customer_Persona',
        size='Local_AQI_At_Purchase', # Bigger dots for worse AQI
        hover_data=['Geographic_Region', 'Acquisition_Channel'],
        title="Environmental Trigger: AQI vs. App Engagement",
        color_discrete_map={
            "Commuter/Urbanite": "#00a8cc",
            "Frequent Traveler": "#20b2aa",
            "Allergy/Asthma Sufferer": "#ff7f50" # Warning color for health risk group
        }
    )
    
    # Add warning zones for AQI
    fig5.add_vrect(x0=0, x1=50, fillcolor="green", opacity=0.05, line_width=0)
    fig5.add_vrect(x0=50, x1=100, fillcolor="yellow", opacity=0.05, line_width=0)
    fig5.add_vrect(x0=100, x1=150, fillcolor="orange", opacity=0.05, line_width=0)
    fig5.add_vrect(x0=150, x1=300, fillcolor="red", opacity=0.05, line_width=0)
    
    fig5.update_layout(xaxis_title="Local AQI at Purchase (Higher is Worse)", yaxis_title="App Engagement Score (1-10)", template="plotly_white")
    st.plotly_chart(fig5, use_container_width=True)
