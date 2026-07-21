import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ------------------------------------------------------------------------------
# 1. Page Configuration & Delightful Bright Pastel Design System
# ------------------------------------------------------------------------------
st.set_page_config(page_title="AeroZone | Investor Portal", page_icon="🌪️", layout="wide")

BG_COLOR = "#F4F8F7"
PRIMARY_COLOR = "#1E293B"
PASTEL_COLORS = ['#38BDF8', '#34D399', '#FBBF24', '#F43F5E', '#A78BFA', '#FB7185', '#2DD4BF', '#60A5FA', '#34D399']

st.markdown(f"""
    <style>
    .stApp {{ background-color: {BG_COLOR}; }}
    h1, h2, h3, h4 {{ color: {PRIMARY_COLOR}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-weight: 700; }}
    
    .summary-box {{
        background: linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%);
        color: #FFFFFF !important;
        padding: 35px;
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(14, 165, 233, 0.2);
        margin-top: 25px;
        margin-bottom: 25px;
        border-left: 6px solid #FEF08A;
    }}
    .summary-box h2, .summary-box p, .summary-box li, .summary-box b {{
        color: #FFFFFF !important;
    }}
    
    .insight-card {{
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 5px solid #38BDF8;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
        color: {PRIMARY_COLOR};
    }}
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
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3714/3714959.png", width=55)
st.sidebar.title("AeroZone Controls")
st.sidebar.markdown("Dynamic filtering engine for granular market and regional due diligence.")

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Financial Timeframe Filter")
min_month, max_month = int(df_fin['Month'].min()), int(df_fin['Month'].max())
selected_months = st.sidebar.slider("Select Month Range (Projections)", min_month, max_month, (min_month, max_month))

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Regional & Persona Filters")
selected_regions = st.sidebar.multiselect("Geographic Market", df_demo['Geographic_Region'].unique(), default=df_demo['Geographic_Region'].unique())
selected_personas = st.sidebar.multiselect("Target Persona", df_demo['Customer_Persona'].unique(), default=df_demo['Customer_Persona'].unique())

st.sidebar.subheader("📈 Environmental Filter")
min_aqi, max_aqi = int(df_demo['Local_AQI_At_Purchase'].min()), int(df_demo['Local_AQI_At_Purchase'].max())
selected_aqi = st.sidebar.slider("Purchase Air Quality Index (AQI)", min_aqi, max_aqi, (min_aqi, max_aqi))

filtered_fin = df_fin[(df_fin['Month'] >= selected_months[0]) & (df_fin['Month'] <= selected_months[1])]

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
st.markdown("### Series A Investor Pitch & Deep-Dive Data Room")
st.markdown("Explore positive, vibrant, and fully-labeled analytics below. *Tip: Hover, pan, and zoom using your cursor.*")

col1, col2, col3, col4 = st.columns(4)
col1.metric("M36 Annual Recurring Revenue", f"${(df_fin['Subscription_Revenue'].iloc[-1] * 12):,.0f}", "+185% YoY")
col2.metric("Terminal Gross Margin (M36)", f"{df_fin['Gross_Margin_%'].iloc[-1]:.1f}%", "Economies of Scale")
col3.metric("Total Hardware Units Sold", f"{df_fin['Hardware_Units_Sold'].sum():,}", "Global Penetration")
col4.metric("Customer Acquisition Cost", f"${df_fin['CAC'].iloc[-1]:.2f}", "-41% Reduction", delta_color="inverse")

st.markdown("---")

# ------------------------------------------------------------------------------
# 5. Section 1: Financial Trajectory & Scalability Engine
# ------------------------------------------------------------------------------
st.subheader("📊 1. Financial Trajectory & Scalability Engine")

c1, c2 = st.columns(2)

with c1:
    # Revenue Chart with Local Month Filter applied
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(x=filtered_fin['Month'], y=filtered_fin['Subscription_Revenue'], mode='lines', fill='tozeroy', 
                                  name='SaaS ARR Base', line=dict(color="#34D399", width=2)))
    fig_rev.add_trace(go.Bar(x=filtered_fin['Month'], y=filtered_fin['Hardware_Revenue'], name='Hardware Revenue', marker_color="#38BDF8", opacity=0.85, text=filtered_fin['Hardware_Revenue'], texttemplate='$%{text:,.0s}', textposition='auto'))
    fig_rev.add_trace(go.Scatter(x=filtered_fin['Month'], y=filtered_fin['Total_Gross_Revenue'], mode='lines+markers', 
                                  name='Total Revenue', line=dict(color="#F43F5E", width=3)))
    fig_rev.update_layout(
        title="Revenue Composition & Growth (Filtered Timeline)", 
        xaxis_title="Projection Month (1 to 36)", 
        yaxis_title="Revenue ($ USD)", 
        template="plotly_white", 
        hovermode="x unified", 
        height=400
    )
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    # Unit Volume Scale with Local Month Filter applied & Values on Bars
    fig_unit = make_subplots(specs=[[{"secondary_y": True}]])
    fig_unit.add_trace(go.Bar(x=filtered_fin['Month'], y=filtered_fin['Hardware_Units_Sold'], name="Units Sold", marker_color="#A78BFA", text=filtered_fin['Hardware_Units_Sold'], texttemplate='%{text:,}', textposition='auto'), secondary_y=False)
    fig_unit.add_trace(go.Scatter(x=filtered_fin['Month'], y=filtered_fin['CAC'], name="CAC ($)", mode='lines+markers', line=dict(color="#FBBF24", width=3)), secondary_y=True)
    fig_unit.update_layout(
        title="Unit Volume Scale vs. Falling CAC (Filtered Timeline)", 
        xaxis_title="Month", 
        template="plotly_white", 
        hovermode="x unified", 
        height=400
    )
    fig_unit.update_yaxes(title_text="Hardware Units Sold", secondary_y=False)
    fig_unit.update_yaxes(title_text="Customer Acquisition Cost ($)", secondary_y=True)
    st.plotly_chart(fig_unit, use_container_width=True)

# Marketing spend vs revenue
fig_mkt = go.Figure()
fig_mkt.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Marketing_Spend'], mode='lines', name='Marketing Spend ($)', line=dict(color="#FB7185", width=2)))
fig_mkt.add_trace(go.Scatter(x=df_fin['Month'], y=df_fin['Total_Gross_Revenue'], mode='lines', name='Total Gross Revenue ($)', line=dict(color="#34D399", width=2, dash='dot')))
fig_mkt.update_layout(
    title="Capital Efficiency: Marketing Spend Growth vs. Top-Line Revenue Scale", 
    xaxis_title="Month", 
    yaxis_title="Amount ($ USD)", 
    template="plotly_white", 
    height=320, 
    hovermode="x unified"
)
st.plotly_chart(fig_mkt, use_container_width=True)

# Gross Margin Expansion without point values (lines + markers only)
fig_margin = px.line(df_fin, x='Month', y='Gross_Margin_%', title="Gross Margin Expansion (%) Driven by Lower Year 2/3 COGS")
fig_margin.update_traces(mode="lines+markers", line=dict(color="#34D399", width=3), marker=dict(size=6, color="#0EA5E9"))
fig_margin.update_layout(
    xaxis_title="Month (1 to 36)", 
    yaxis_title="Gross Margin Percentage (%)", 
    template="plotly_white", 
    height=350
)
st.plotly_chart(fig_margin, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# 6. Section 2: Deep Product & Customer Insights
# ------------------------------------------------------------------------------
st.subheader("🔬 2. Deep Customer & Product Insights")

in_c1, in_c2 = st.columns(2)

with in_c1:
    persona_eng = df_demo.groupby('Customer_Persona')['App_Engagement_Score'].mean().reset_index()
    fig_eng = px.bar(
        persona_eng, x='Customer_Persona', y='App_Engagement_Score', 
        title="Sticky Ecosystem: Avg. App Engagement Score by Persona",
        color='Customer_Persona', 
        color_discrete_sequence=['#38BDF8', '#34D399', '#FBBF24'],
        text='App_Engagement_Score'
    )
    fig_eng.update_traces(texttemplate='%{text:.2f}', textposition='auto')
    fig_eng.update_layout(
        xaxis_title="Customer Persona", 
        yaxis_title="Avg App Engagement Score (1-10)", 
        template="plotly_white", 
        height=380, 
        showlegend=False
    )
    st.plotly_chart(fig_eng, use_container_width=True)

with in_c2:
    fig_box = px.box(
        df_demo, x='Customer_Persona', y='Local_AQI_At_Purchase',
        title="Environmental Vulnerability: AQI Distribution per Persona",
        color='Customer_Persona', 
        color_discrete_sequence=['#38BDF8', '#34D399', '#FBBF24']
    )
    fig_box.update_layout(
        xaxis_title="Customer Persona", 
        yaxis_title="Local AQI at Purchase", 
        template="plotly_white", 
        height=380, 
        showlegend=False
    )
    st.plotly_chart(fig_box, use_container_width=True)

in_c3, in_c4 = st.columns(2)

with in_c3:
    chan_persona = df_demo.groupby(['Acquisition_Channel', 'Customer_Persona']).size().reset_index(name='Count')
    fig_stack = px.bar(
        chan_persona, x='Acquisition_Channel', y='Count', color='Customer_Persona',
        title="Acquisition Channel Efficiency across Personas",
        color_discrete_sequence=['#38BDF8', '#34D399', '#A78BFA'],
        text='Count'
    )
    fig_stack.update_traces(texttemplate='%{text}', textposition='auto')
    fig_stack.update_layout(
        xaxis_title="Acquisition Channel", 
        yaxis_title="Order Count", 
        template="plotly_white", 
        height=380, 
        xaxis={'categoryorder':'total descending'}
    )
    st.plotly_chart(fig_stack, use_container_width=True)

with in_c4:
    reg_dist = df_demo['Geographic_Region'].value_counts().reset_index()
    reg_dist.columns = ['Geographic_Region', 'Sales_Count']
    # Custom color map with specific color for San Francisco and percentage-only labels (using color_discrete_map)
    color_map = {
        'New York': '#38BDF8', 
        'San Francisco': '#F43F5E',  
        'Tokyo': '#14B8A6', 
        'Beijing': '#A78BFA', 
        'New Delhi': '#FB7185', 
        'Los Angeles': '#FBBF24', 
        'London': '#00FFFF'
    }
    fig_reg_dist = px.pie(
        reg_dist, names='Geographic_Region', values='Sales_Count', hole=0.4,
        title="Global Footprint: Sales Volume by Metropolitan Region",
        color='Geographic_Region',
        color_discrete_map=color_map
    )
    fig_reg_dist.update_traces(textposition='inside', textinfo='percent') # Percentage only
    fig_reg_dist.update_layout(template="plotly_white", height=380)
    st.plotly_chart(fig_reg_dist, use_container_width=True)

st.markdown(f"""
    <div class="insight-card">
        <b>💡 Key Product Insight:</b> Allergy and Asthma Sufferers demonstrate superior ecosystem retention with an average app engagement score of <b>8.75 / 10</b>, purchasing devices amidst severe pollution spikes averaging <b>158.7 AQI</b>. This validates AeroZone's dual utility as both protective consumer hardware and vital personal health software.
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# 7. Section 3: Filtered Market Dynamics & Environmental Catalyst
# ------------------------------------------------------------------------------
st.subheader("🎯 3. Filtered Market Dynamics & Environmental Intelligence")

d1, d2 = st.columns(2)

with d1:
    if not filtered_demo.empty:
        fig_sun = px.sunburst(
            filtered_demo, 
            path=['Geographic_Region', 'Customer_Persona', 'Acquisition_Channel'], 
            color='App_Engagement_Score', 
            color_continuous_scale='Teal',
            title="Interactive Regional & Persona Breakdown"
        )
        fig_sun.update_layout(height=450)
        st.plotly_chart(fig_sun, use_container_width=True)
    else:
        st.warning("No data matching current filter criteria.")

with d2:
    if not filtered_demo.empty:
        chan_df = filtered_demo['Acquisition_Channel'].value_counts().reset_index()
        chan_df.columns = ['Channel', 'Count']
        
        # Explicit unrepeated custom color mapping for all channels
        channel_color_map = {
            'Instagram Ads': '#38BDF8',
            'TikTok': '#34D399',
            'Travel Blogs': '#FBBF24',
            'Subway Posters': '#A78BFA',
            'Google Search': '#2DD4BF',
            'Facebook Ads': '#FB7185',
            'Health Influencers': '#00FFFF',  # Distinct color
            'Medical Blogs': '#FF69B4',       # Distinct color
            'Airport Kiosks': '#8B4513'       # Distinct color
        }
        
        fig_chan = px.bar(
            chan_df, x='Count', y='Channel', orientation='h', 
            title="Top Acquisition Channels (Filtered)", 
            color='Channel',
            color_discrete_map=channel_color_map,
            text='Count'
        )
        fig_chan.update_traces(texttemplate='%{text}', textposition='auto')
        fig_chan.update_layout(
            xaxis_title="Order Count", 
            yaxis_title="Acquisition Channel", 
            template="plotly_white", 
            height=450, 
            yaxis={'categoryorder':'total ascending'}, 
            showlegend=False
        )
        st.plotly_chart(fig_chan, use_container_width=True)
    else:
        st.warning("No data available for channels.")

if not filtered_demo.empty:
    fig_aqi = px.scatter(
        filtered_demo, x='Local_AQI_At_Purchase', y='App_Engagement_Score', 
        color='Customer_Persona', size='Local_AQI_At_Purchase', hover_data=['Geographic_Region', 'Acquisition_Channel'],
        title="Environmental Trigger: Local AQI vs. App Engagement (Cursor to Zoom/Hover)",
        color_discrete_sequence=['#F43F5E', '#34D399', '#38BDF8']
    )
    fig_aqi.add_vrect(x0=150, x1=300, fillcolor="#F43F5E", opacity=0.07, line_width=0, annotation_text="Severe Pollution Spike Zone", annotation_position="top left")
    fig_aqi.update_layout(
        xaxis_title="Local Air Quality Index (AQI at Purchase)", 
        yaxis_title="App Engagement Score (1-10)", 
        template="plotly_white", 
        height=450
    )
    st.plotly_chart(fig_aqi, use_container_width=True)

st.markdown("---")

# ------------------------------------------------------------------------------
# 8. Executive Pitch Conclusion & Investment Summary
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="summary-box">
        <h2 style="color: #FFFFFF; margin-top: 0;">🚀 Executive Summary: Why Invest in AeroZone?</h2>
        <p style="font-size: 16px; line-height: 1.6; color: #FFFFFF;">
            AeroZone is uniquely positioned at the intersection of wearable consumer hardware and high-margin recurring SaaS healthcare. 
            By addressing global urban decay, recurring wildfire seasons, and chronic respiratory vulnerabilities, our personal air purifier collar unlocks three critical investor pillars:
        </p>
        <ul style="font-size: 15px; line-height: 1.6; color: #FFFFFF;">
            <li><b style="color: #FEF08A;">Defensible Hardware-SaaS Hybrid Model:</b> Initial hardware margins expand significantly as manufacturing scales down from $65 to $45 COGS, while monthly subscriptions build a predictable, high-retention ARR base.</li>
            <li><b style="color: #FEF08A;">Organic Environmental Catalysts:</b> Seasonal wildfire spikes (Aug/Sep) and winter smog drive massive, organic customer acquisition spikes with zero proportional marketing cost inflations.</li>
            <li><b style="color: #FEF08A;">Proven Product-Market Fit & Engagement:</b> Data demonstrates a direct correlation between worsening AQI and user app engagement, proving sticky long-term ecosystem retention among allergy and urban commuter personas.</li>
        </ul>
        <p style="font-size: 16px; font-weight: bold; margin-bottom: 0; margin-top: 15px; color: #FEF08A;">
            Targeting Series A capital to scale manufacturing capacity, expand urban retail channels, and capture high-pollution global megacities.
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 9. Interactive Data Table Inspector
# ------------------------------------------------------------------------------
with st.expander("🔍 Interactive Data Tables (Due Diligence Inspector)"):
    tab1, tab2 = st.tabs(["Financial Projections (36M)", "Customer Demographics (100 Rows)"])
    with tab1:
        st.dataframe(filtered_fin, use_container_width=True)
    with tab2:
        st.dataframe(filtered_demo, use_container_width=True)
