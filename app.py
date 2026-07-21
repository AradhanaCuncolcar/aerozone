import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. Page Configuration & Professional Styling
# ------------------------------------------------------------------------------
st.set_page_config(page_title="AeroZone | Investor Pitch Dashboard", page_icon="🌪️", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #f8fafc; }
    h1, h2, h3 { color: #091e42; font-family: -apple-system, BlinkMacSystemFont, sans-serif; }
    .metric-card {
        background-color: #ffffff;
        border: 1px solid #dfe1e6;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .summary-box {
        background: linear-gradient(135deg, #091e42 0%, #0747a6 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(9,30,66,0.15);
        margin-top: 20px;
        margin-bottom: 20px;
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
    st.error("⚠️ Datasets missing. Please make sure 'financial_projections.csv' and 'customer_demographics.csv' are in your directory.")
    st.stop()

# ------------------------------------------------------------------------------
# 3. Global & Local Interactive Filters
# ------------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3714/3714959.png", width=50)
st.sidebar.title("AeroZone Control Panel")
st.sidebar.markdown("Filter demographic views across regional and market segments dynamically.")

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Regional & Persona Filters")
selected_regions = st.sidebar.multiselect("Geographic Market", df_demo['Geographic_Region'].unique(), default=df_demo['Geographic_Region'].unique())
selected_personas = st.sidebar.multiselect("Target Persona", df_demo['Customer_Persona'].unique(), default=df_demo['Customer_Persona'].unique())

st.sidebar.subheader("📈 Environmental Filter")
min_aqi, max_aqi = int(df_demo['Local_AQI_At_Purchase'].min()), int(df_demo['Local_AQI_At_Purchase'].max())
selected_aqi = st.sidebar.slider("Purchase Air Quality Index (AQI)", min_aqi, max_aqi, (min_aqi, max_aqi))

# Apply filters dynamically
filtered_demo = df_demo[
    (df_demo['Geographic_Region'].isin(selected_regions)) &
    (df_demo['Customer_Persona'].isin(selected_personas)) &
    (df_demo['Local_AQI_At_Purchase'] >= selected_aqi[0]) &
    (df_demo['Local_AQI_At_Purchase'] <= selected_aqi[1])
]

# ------------------------------------------------------------------------------
# 4. Hero KPIs (Top Row)
# ------------------------------------------------------------------------------
st.title("🌪️ AeroZone: Wearable Personal Air Purifier Collar")
st.markdown("### Series A Investor Pitch & Interactive Data Room")
st.markdown("Explore deep real-time analytics below. *Tip: You can zoom, pan, and hover over any chart element using your cursor.*")

col1, col2, col3, col4 = st.columns(4)
col1.metric("M36 Annual Recurring Revenue", f"${(df_fin['Subscription_Revenue'].iloc[-1] * 12):,.0f}", "+185% YoY")
col2.metric("Terminal Gross Margin (M36)", f"{df_fin['Gross_Margin_%'].iloc[-1]:.1f}%", "Economies of Scale")
col3.metric("Total Hardware Units Sold", f"{df_fin['Hardware_Units_Sold'].sum():,}", "Global Penetration")
col4.metric("Customer Acquisition Cost", f"${df_fin['CAC'].iloc[-1]:.2f}", "-41% Reduction", delta_color="inverse")

st.markdown("---")

# ------------------------------------------------------------------------------
# 5. Section 1: Financial Trajectory & Unit Economics
# ------------------------------------------------------------------------------
st.subheader("📊 1. Financial Trajectory & Scalability Engine")
st.markdown("Hover to view monthly breakdowns. Notice how recurring SaaS revenue dampens hardware seasonality spikes.")

c1, c2 = st.columns(2)

with c1:
    # Interactive Revenue Hockey Stick
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Subscription_Revenue'], mode='lines', fill='tozeroy', 
                                  name='SaaS ARR Base', line=dict(color='#00875a', width=2)))
    fig_rev.add_trace(go.Bar(x=df_fin['Month'], y=df_fin['Hardware_Revenue'], name='Hardware Revenue', marker_color='#0747a6', opacity=0.85))
    fig_rev.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Total_Gross_Revenue'], mode='lines+markers', 
                                  name='Total Revenue', line=dict(color='#ff5630', width=3)))
    fig_rev.update_layout(title="36-Month Revenue Composition & Growth", template="plotly_white", hovermode="x unified", height=400)
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    # Combo Chart: Units Sold vs CAC Optimization
    fig_unit = make_subplots(specs=[[{"secondary_y": True}]])
    fig_unit.add_trace(go.Bar(x=df_fin['Month'], y=df_fin['Hardware_Units_Sold'], name="Units Sold", marker_color='#00b8d9'), secondary_y=False)
    fig_unit.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['CAC'], name="CAC ($)", mode='lines+markers', line=dict(color='#ffab00', width=3)), secondary_y=True)
    fig_unit.update_layout(title="Unit Volume Scale vs. Falling CAC", template="plotly_white", hovermode="x unified", height=400)
    fig_unit.update_yaxes(title_text="Units Sold", secondary_y=False)
    fig_unit.update_yaxes(title_text="CAC ($)", secondary_y=True)
    st.plotly_chart(fig_unit, use_container_width=True)

# Gross margin curve expansion
fig_margin = px.area(df_fin, x='Month', y='Gross_Margin_%', title="Gross Margin Expansion (%) Driven by Lower Year 2/3 COGS ($55/$45)", color_discrete_sequence=['#36b37e'])
fig_margin.update_layout(template="plotly_white", height=300)
st.plotly_chart(fig_margin, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# 6. Section 2: Market Demographics & Local Filter Intelligence
# ------------------------------------------------------------------------------
st.subheader("🎯 2. Market Dynamics & Local Segment Intelligence")
st.markdown("The charts below dynamically adapt to the **Regional, Persona, and AQI filters** selected in the sidebar.")

d1, d2 = st.columns(2)

with d1:
    # Sunburst Hierarchy based on active local filters
    if not filtered_demo.empty:
        fig_sun = px.sunburst(
            filtered_demo, 
            path=['Geographic_Region', 'Customer_Persona', 'Acquisition_Channel'], 
            color='App_Engagement_Score', 
            color_continuous_scale='Blues',
            title="Interactive Regional & Persona Breakdown"
        )
        fig_sun.update_layout(height=450)
        st.plotly_chart(fig_sun, use_container_width=True)
    else:
        st.warning("No data matching current filter criteria. Please adjust sidebar selections.")

with d2:
    # Acquisition Channels Bar Chart
    if not filtered_demo.empty:
        chan_df = filtered_demo['Acquisition_Channel'].value_counts().reset_index()
        chan_df.columns = ['Channel', 'Count']
        fig_chan = px.bar(chan_df, x='Count', y='Channel', orientation='h', title="Top Acquisition Channels (Filtered)", color_discrete_sequence=['#0747a6'])
        fig_chan.update_layout(yaxis={'categoryorder':'total ascending'}, template="plotly_white", height=450)
        st.plotly_chart(fig_chan, use_container_width=True)
    else:
        st.warning("No data available for channels.")

# Environmental Catalyst Scatter plot
if not filtered_demo.empty:
    fig_aqi = px.scatter(
        filtered_demo, x='Local_AQI_At_Purchase', y='App_Engagement_Score', 
        color='Customer_Persona', size='Local_AQI_At_Purchase', hover_data=['Geographic_Region', 'Acquisition_Channel'],
        title="Environmental Trigger: Local AQI vs. App Engagement (Cursor to Zoom/Hover)",
        color_discrete_sequence=['#ff5630', '#00875a', '#0747a6']
    )
    fig_aqi.add_vrect(x0=150, x1=300, fillcolor="red", opacity=0.08, line_width=0, annotation_text="Severe Pollution Spike Zone", annotation_position="top left")
    fig_aqi.update_layout(template="plotly_white", height=450)
    st.plotly_chart(fig_aqi, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# 7. Executive Pitch Conclusion & Investment Summary
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="summary-box">
        <h2 style="color: white; margin-top: 0;">🚀 Executive Summary: Why Invest in AeroZone?</h2>
        <p style="font-size: 16px; line-height: 1.6;">
            AeroZone is uniquely positioned at the intersection of wearable consumer hardware and high-margin recurring SaaS healthcare. 
            By addressing global urban decay, recurring wildfire seasons, and chronic respiratory vulnerabilities, our personal air purifier collar unlocks three critical investor pillars:
        </p>
        <ul style="font-size: 15px; line-height: 1.6;">
            <li><b>Defensible Hardware-SaaS Hybrid Model:</b> Initial hardware margins expand significantly as manufacturing scales down from $65 to $45 COGS, while monthly subscriptions build a predictable, high-retention ARR base.</li>
            <li><b>Organic Environmental Catalysts:</b> Seasonal wildfire spikes (Aug/Sep) and winter smog drive massive, organic customer acquisition spikes with zero proportional marketing cost inflations.</li>
            <li><b>Proven Product-Market Fit & Engagement:</b> Data demonstrates a direct correlation between worsening AQI and user app engagement, proving sticky long-term ecosystem retention among allergy and urban commuter personas.</li>
        </ul>
        <p style="font-size: 16px; font-weight: bold; margin-bottom: 0; margin-top: 15px;">
            Targeting Series A capital to scale manufacturing capacity, expand urban retail channels, and capture high-pollution global megacities.
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 8. Interactive Data Table Inspector
# ------------------------------------------------------------------------------
with st.expander("🔍 Interactive Data Tables (Due Diligence Inspector)"):
    tab1, tab2 = st.tabs(["Financial Projections (36M)", "Customer Demographics (100 Rows)"])
    with tab1:
        st.dataframe(df_fin, use_container_width=True)
    with tab2:
        st.dataframe(filtered_demo, use_container_width=True)
