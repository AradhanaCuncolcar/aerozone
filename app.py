import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# ------------------------------------------------------------------------------
# 1. Page Configuration & Delightful Bright Pastel Design System
# ------------------------------------------------------------------------------
st.set_page_config(page_title="AeroZone | Investor Portal", page_icon="🌪️", layout="wide")

PRIMARY_COLOR = "#1E293B"

REGION_COLOR_MAP = {
    'New York': '#38BDF8', 
    'San Francisco': '#F43F5E',  
    'Tokyo': '#14B8A6', 
    'Beijing': '#A78BFA', 
    'New Delhi': '#FB7185', 
    'Los Angeles': '#FBBF24', 
    'London': '#00FFFF'
}

CHANNEL_COLOR_MAP = {
    'Instagram Ads': '#FF595E',      
    'TikTok': '#1982C4',             
    'Travel Blogs': '#FFCA3A',       
    'Subway Posters': '#8AC926',     
    'Google Search': '#6A4C93',      
    'Facebook Ads': '#FF9F1C',       
    'Health Influencers': '#00B4D8', 
    'Medical Blogs': '#F50057',      
    'Airport Kiosks': '#06D6A0'      
}

st.markdown(f"""
    <style>
    /* Overall App Background - Soft Slate Gray for contrast */
    .stApp {{ background-color: #F0F4F8; }}
    
    h1, h2, h3, h4 {{ color: {PRIMARY_COLOR}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-weight: 700; }}
    
    /* Bubble Cards for KPI Metrics */
    [data-testid="stMetric"] {{
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 20px 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        text-align: center;
    }}
    
    /* Bubble Cards for Plotly Charts - Fixed Overflow and Scrollbars */
    [data-testid="stPlotlyChart"] {{
        background-color: #FFFFFF;
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        padding: 10px;
        margin-bottom: 15px;
        overflow: hidden !important; 
    }}
    
    /* Bubble Container for Section Headers */
    .section-header {{
        background-color: #FFFFFF;
        padding: 15px 25px;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.03);
        border-left: 8px solid #38BDF8;
        margin-top: 30px;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
    }}
    .section-header h3 {{ margin: 0; padding: 0; }}
    
    /* Intro Card Style */
    .intro-card {{
        background-color: #FFFFFF;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0;
        height: 100%;
    }}

    /* Executive Summary Box */
    .summary-box {{
        background: linear-gradient(135deg, #0EA5E9 0%, #14B8A6 100%);
        color: #FFFFFF !important;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 12px 25px rgba(14, 165, 233, 0.25);
        margin-top: 30px;
        margin-bottom: 30px;
        border-left: 8px solid #FEF08A;
    }}
    .summary-box h2, .summary-box p, .summary-box li, .summary-box b {{
        color: #FFFFFF !important;
    }}
    
    /* Insight Cards */
    .insight-card {{
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-left: 6px solid #F43F5E;
        padding: 25px;
        border-radius: 16px;
        margin-top: 20px;
        margin-bottom: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.04);
        color: {PRIMARY_COLOR};
    }}
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. Data Loading & Date Processing
# ------------------------------------------------------------------------------
@st.cache_data
def load_data():
    df_fin = pd.read_csv("financial_projections.csv")
    df_demo = pd.read_csv("customer_demographics.csv")
    
    df_fin['Date'] = pd.date_range(start='2024-01-01', periods=len(df_fin), freq='MS')
    df_fin['Date_Label'] = df_fin['Date'].dt.strftime('%b %Y')
    
    return df_fin, df_demo

try:
    df_fin, df_demo = load_data()
except FileNotFoundError:
    st.error("⚠️ Datasets missing. Please make sure 'financial_projections.csv' and 'customer_demographics.csv' are in your directory.")
    st.stop()

# ------------------------------------------------------------------------------
# 3. Global & Local Interactive Filters
# ------------------------------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.magnific.com/256/18122/18122832.png?semt=ais_white_label.png", width=65)
st.sidebar.title("AeroZone Controls")
st.sidebar.markdown("Dynamic filtering engine for granular market and regional due diligence.")

st.sidebar.markdown("---")
st.sidebar.subheader("📅 Financial Timeline")
min_date = df_fin['Date'].min().to_pydatetime()
max_date = df_fin['Date'].max().to_pydatetime()
selected_dates = st.sidebar.slider(
    "Select Projection Date Range", 
    min_value=min_date, 
    max_value=max_date, 
    value=(min_date, max_date),
    format="MMM YYYY"
)

st.sidebar.markdown("---")
st.sidebar.subheader("🌍 Regional & Persona Filters")
selected_regions = st.sidebar.multiselect("Geographic Market", df_demo['Geographic_Region'].unique(), default=df_demo['Geographic_Region'].unique())
selected_personas = st.sidebar.multiselect("Target Persona", df_demo['Customer_Persona'].unique(), default=df_demo['Customer_Persona'].unique())

st.sidebar.subheader("📈 Environmental Filter")
min_aqi, max_aqi = int(df_demo['Local_AQI_At_Purchase'].min()), int(df_demo['Local_AQI_At_Purchase'].max())
selected_aqi = st.sidebar.slider("Purchase Air Quality Index (AQI)", min_aqi, max_aqi, (min_aqi, max_aqi))

# Apply Filters
filtered_fin = df_fin[(df_fin['Date'] >= pd.to_datetime(selected_dates[0])) & (df_fin['Date'] <= pd.to_datetime(selected_dates[1]))]

filtered_demo = df_demo[
    (df_demo['Geographic_Region'].isin(selected_regions)) &
    (df_demo['Customer_Persona'].isin(selected_personas)) &
    (df_demo['Local_AQI_At_Purchase'] >= selected_aqi[0]) &
    (df_demo['Local_AQI_At_Purchase'] <= selected_aqi[1])
]

# Calculate padding for Date axes so the first/last bars aren't cut in half
if not filtered_fin.empty:
    dt_pad_start = filtered_fin['Date'].min() - pd.Timedelta(days=15)
    dt_pad_end = filtered_fin['Date'].max() + pd.Timedelta(days=15)
else:
    dt_pad_start, dt_pad_end = None, None

# ------------------------------------------------------------------------------
# 4. Hero Intro, Product Showcase & KPIs (Top Row)
# ------------------------------------------------------------------------------
st.title("🌪️ AeroZone: Wearable Personal Air Purifier Collar")
st.markdown("### Series A Investor Pitch & Deep-Dive Data Room")

# Layout: Text on the left, and the two images stacked vertically on the right
intro_col1, intro_col2 = st.columns([1.3, 0.9])

with intro_col1:
    st.markdown("""
    <div class="intro-card">
        <h3>💡 Product Vision & Innovation</h3>
        <p><b>AeroZone</b> is a next-generation wearable personal air purifier collar engineered for urban commuters, frequent travelers, and allergy sufferers.</p>
        <p>By actively filtering PM2.5, VOCs, and airborne allergens directly from the user's breathing zone, it establishes a personal clean-air sanctuary anywhere in the world.</p>
        <p><b>The Ecosystem:</b> Paired with our proprietary SaaS mobile app, users receive real-time respiratory health analytics, live environmental AQI tracking, and automated filter-replacement subscriptions that power our compounding recurring revenue engine.</p>
    </div>
    """, unsafe_allow_html=True)

with intro_col2:
    # Stacked vertically in a single column to eliminate empty side-by-side space
    try:
        st.image("lifestyle_user.png", caption="In-Action Lifestyle", width=250)
    except Exception:
        st.info("Place 'lifestyle_user.png' in directory.")
        
    try:
        st.image("product_render.png", caption="Hardware Design", width=250)
    except Exception:
        st.info("Place 'product_render.png' in directory.")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown("Explore positive, vibrant, and fully-labeled analytics below. *Tip: Hover, pan, and zoom using your cursor.*")

col1, col2, col3, col4 = st.columns(4)
col1.metric("M36 Annual Recurring Revenue", f"${(df_fin['Subscription_Revenue'].iloc[-1] * 12):,.0f}", "+185% YoY")
col2.metric("Terminal Gross Margin (M36)", f"{df_fin['Gross_Margin_%'].iloc[-1]:.1f}%", "Economies of Scale")
col3.metric("Total Hardware Units Sold", f"{df_fin['Hardware_Units_Sold'].sum():,}", "Global Penetration")
col4.metric("Customer Acquisition Cost", f"${df_fin['CAC'].iloc[-1]:.2f}", "-41% Reduction", delta_color="inverse")

# ------------------------------------------------------------------------------
# 5. Section 1: Financial Trajectory & Scalability Engine
# ------------------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>📊 1. Financial Trajectory & Scalability Engine</h3></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)

with c1:
    fig_rev = go.Figure()
    fig_rev.add_trace(go.Scatter(x=filtered_fin['Date'], y=filtered_fin['Subscription_Revenue'], mode='lines', fill='tozeroy', 
                                  name='SaaS ARR Base', line=dict(color="#34D399", width=2)))
    fig_rev.add_trace(go.Bar(x=filtered_fin['Date'], y=filtered_fin['Hardware_Revenue'], name='Hardware Revenue', marker_color="#38BDF8", opacity=0.85, text=filtered_fin['Hardware_Revenue'], texttemplate='$%{text:,.0s}', textposition='auto'))
    fig_rev.add_trace(go.Scatter(x=filtered_fin['Date'], y=filtered_fin['Total_Gross_Revenue'], mode='lines+markers', 
                                  name='Total Revenue', line=dict(color="#F43F5E", width=3)))
    fig_rev.update_layout(
        title="Revenue Composition & Growth (Filtered Timeline)", 
        xaxis_title="Timeline (Date/Month/Year)", 
        yaxis_title="Revenue ($ USD)", 
        template="plotly_white", 
        hovermode="x unified", 
        height=400,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=20, r=20, b=30)
    )
    fig_rev.update_xaxes(range=[dt_pad_start, dt_pad_end], automargin=True)
    fig_rev.update_yaxes(automargin=True)
    st.plotly_chart(fig_rev, use_container_width=True)

with c2:
    fig_unit = make_subplots(specs=[[{"secondary_y": True}]])
    fig_unit.add_trace(go.Bar(x=filtered_fin['Date'], y=filtered_fin['Hardware_Units_Sold'], name="Units Sold", marker_color="#A78BFA", text=filtered_fin['Hardware_Units_Sold'], texttemplate='%{text:,}', textposition='auto'), secondary_y=False)
    fig_unit.add_trace(go.Scatter(x=filtered_fin['Date'], y=filtered_fin['CAC'], name="CAC ($)", mode='lines+markers', line=dict(color="#FBBF24", width=3)), secondary_y=True)
    fig_unit.update_layout(
        title="Unit Volume Scale vs. Falling CAC (Filtered Timeline)", 
        xaxis_title="Timeline (Date/Month/Year)", 
        template="plotly_white", 
        hovermode="x unified", 
        height=400,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=20, r=20, b=30)
    )
    fig_unit.update_xaxes(range=[dt_pad_start, dt_pad_end], automargin=True)
    fig_unit.update_yaxes(title_text="Hardware Units Sold", secondary_y=False, automargin=True)
    fig_unit.update_yaxes(title_text="Customer Acquisition Cost ($)", secondary_y=True, automargin=True)
    st.plotly_chart(fig_unit, use_container_width=True)

fig_mkt = go.Figure()
fig_mkt.add_trace(go.Scatter(x=df_fin['Date'], y=df_fin['Marketing_Spend'], mode='lines', name='Marketing Spend ($)', line=dict(color="#FB7185", width=2)))
fig_mkt.add_trace(go.Scatter(x=df_fin['Date'], y=df_fin['Total_Gross_Revenue'], mode='lines', name='Total Gross Revenue ($)', line=dict(color="#34D399", width=2, dash='dot')))
fig_mkt.update_layout(
    title="Capital Efficiency: Marketing Spend Growth vs. Top-Line Revenue Scale", 
    xaxis_title="Timeline", 
    yaxis_title="Amount ($ USD)", 
    template="plotly_white", 
    height=320, 
    hovermode="x unified",
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=50, l=20, r=20, b=30)
)
fig_mkt.update_xaxes(range=[dt_pad_start, dt_pad_end], automargin=True)
fig_mkt.update_yaxes(automargin=True)
st.plotly_chart(fig_mkt, use_container_width=True)

fig_margin = px.line(df_fin, x='Date', y='Gross_Margin_%', title="Gross Margin Expansion (%) Driven by Lower Year 2/3 COGS")
fig_margin.update_traces(mode="lines+markers", line=dict(color="#34D399", width=3), marker=dict(size=6, color="#0EA5E9"))
fig_margin.update_layout(
    xaxis_title="Timeline", 
    yaxis_title="Gross Margin Percentage (%)", 
    template="plotly_white", 
    height=350,
    paper_bgcolor='rgba(0,0,0,0)', 
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(t=50, l=20, r=20, b=30)
)
fig_margin.update_xaxes(range=[dt_pad_start, dt_pad_end], automargin=True)
fig_margin.update_yaxes(automargin=True)
st.plotly_chart(fig_margin, use_container_width=True)


# ------------------------------------------------------------------------------
# 6. Section 2: Deep Product & Customer Insights
# ------------------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>🔬 2. Deep Customer & Product Insights</h3></div>', unsafe_allow_html=True)

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
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=20, r=20, b=30)
    )
    fig_eng.update_xaxes(automargin=True)
    fig_eng.update_yaxes(automargin=True)
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
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=20, r=20, b=30)
    )
    fig_box.update_xaxes(automargin=True)
    fig_box.update_yaxes(automargin=True)
    st.plotly_chart(fig_box, use_container_width=True)

in_c3, in_c4 = st.columns(2)

with in_c3:
    chan_persona = df_demo.groupby(['Acquisition_Channel', 'Customer_Persona']).size().reset_index(name='Count')
    fig_stack = px.bar(
        chan_persona, x='Acquisition_Channel', y='Count', color='Customer_Persona',
        title="Acquisition Channel Efficiency across Personas",
        color_discrete_sequence=['#FF9CEE', '#85E3FF', '#FFF5BA'],
        text='Count'
    )
    fig_stack.update_traces(texttemplate='%{text}', textposition='auto')
    fig_stack.update_layout(
        xaxis_title="Acquisition Channel", 
        yaxis_title="Order Count", 
        template="plotly_white", 
        height=380, 
        xaxis={'categoryorder':'total descending'},
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=20, r=20, b=30)
    )
    fig_stack.update_xaxes(tickangle=-45, automargin=True)
    fig_stack.update_yaxes(automargin=True)
    st.plotly_chart(fig_stack, use_container_width=True)

with in_c4:
    reg_dist = df_demo['Geographic_Region'].value_counts().reset_index()
    reg_dist.columns = ['Geographic_Region', 'Sales_Count']
    fig_reg_dist = px.pie(
        reg_dist, names='Geographic_Region', values='Sales_Count', hole=0.4,
        title="Global Footprint: Sales Volume by Metropolitan Region",
        color='Geographic_Region',
        color_discrete_map=REGION_COLOR_MAP
    )
    fig_reg_dist.update_traces(textposition='inside', textinfo='percent')
    fig_reg_dist.update_layout(
        template="plotly_white", 
        height=380, 
        paper_bgcolor='rgba(0,0,0,0)', 
        margin=dict(t=50, l=20, r=20, b=30)
    )
    st.plotly_chart(fig_reg_dist, use_container_width=True)

st.markdown(f"""
    <div class="insight-card">
        <b>💡 Key Product Insight:</b> Allergy and Asthma Sufferers demonstrate superior ecosystem retention with an average app engagement score of <b>8.75 / 10</b>, purchasing devices amidst severe pollution spikes averaging <b>158.7 AQI</b>. This validates AeroZone's dual utility as both protective consumer hardware and vital personal health software.
    </div>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# 7. Section 3: Filtered Market Dynamics & Environmental Catalyst
# ------------------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>🎯 3. Filtered Market Dynamics & Environmental Intelligence</h3></div>', unsafe_allow_html=True)

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
        fig_sun.update_layout(
            height=450, 
            paper_bgcolor='rgba(0,0,0,0)', 
            margin=dict(t=50, l=20, r=20, b=30)
        )
        st.plotly_chart(fig_sun, use_container_width=True)
    else:
        st.warning("No data matching current filter criteria.")

with d2:
    if not filtered_demo.empty:
        chan_df = filtered_demo['Acquisition_Channel'].value_counts().reset_index()
        chan_df.columns = ['Channel', 'Count']
        
        fig_chan = px.bar(
            chan_df, x='Count', y='Channel', orientation='h', 
            title="Top Acquisition Channels (Filtered)", 
            color='Channel',
            color_discrete_map=CHANNEL_COLOR_MAP,
            text='Count'
        )
        fig_chan.update_traces(texttemplate='%{text}', textposition='auto')
        fig_chan.update_layout(
            xaxis_title="Order Count", 
            yaxis_title="Acquisition Channel", 
            template="plotly_white", 
            height=450, 
            yaxis={'categoryorder':'total ascending'}, 
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, l=20, r=20, b=30)
        )
        fig_chan.update_xaxes(automargin=True)
        fig_chan.update_yaxes(automargin=True)
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
        height=450,
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(t=50, l=20, r=20, b=30)
    )
    fig_aqi.update_xaxes(automargin=True)
    fig_aqi.update_yaxes(automargin=True)
    st.plotly_chart(fig_aqi, use_container_width=True)


# ------------------------------------------------------------------------------
# 8. Section 4: Advanced Investor Analytics (Deep-Dive)
# ------------------------------------------------------------------------------
st.markdown('<div class="section-header"><h3>🚀 4. Advanced Investor Analytics (Deep-Dive)</h3></div>', unsafe_allow_html=True)

a1, a2 = st.columns(2)

with a1:
    if not filtered_fin.empty:
        fig_churn = make_subplots(specs=[[{"secondary_y": True}]])
        fig_churn.add_trace(go.Scatter(x=filtered_fin['Date'], y=filtered_fin['Active_Subscribers'], name="Active Subs", mode='lines+markers', line=dict(color="#38BDF8", width=3)), secondary_y=False)
        fig_churn.add_trace(go.Scatter(x=filtered_fin['Date'], y=filtered_fin['Churn_Rate'], name="Churn Rate", mode='lines', line=dict(color="#F43F5E", width=2, dash='dot')), secondary_y=True)
        fig_churn.update_layout(
            title="Subscriber Retention & Churn Velocity", 
            xaxis_title="Timeline", 
            template="plotly_white", 
            hovermode="x unified",
            height=400,
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, l=20, r=20, b=30)
        )
        fig_churn.update_xaxes(range=[dt_pad_start, dt_pad_end], automargin=True)
        fig_churn.update_yaxes(title_text="Active Subscribers", secondary_y=False, automargin=True)
        fig_churn.update_yaxes(title_text="Churn Rate (%)", tickformat='.1%', secondary_y=True, automargin=True)
        st.plotly_chart(fig_churn, use_container_width=True)

with a2:
    if not filtered_fin.empty:
        df_fin_heat = filtered_fin.copy()
        df_fin_heat['Year'] = df_fin_heat['Date'].dt.year
        df_fin_heat['Cal_Month'] = df_fin_heat['Date'].dt.month
        month_names = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        df_fin_heat['Month_Name'] = df_fin_heat['Cal_Month'].map(month_names)
        
        pivot_heat = pd.pivot_table(df_fin_heat, values='Hardware_Units_Sold', index='Year', columns='Month_Name', aggfunc='sum')
        ordered_months = [month_names[i] for i in range(1, 13) if month_names[i] in pivot_heat.columns]
        pivot_heat = pivot_heat.reindex(columns=ordered_months)
        
        fig_heat = px.imshow(pivot_heat, text_auto=True, 
                             color_continuous_scale=['#F0F4F8', '#38BDF8', '#F43F5E'], 
                             title="Seasonality Heatmap: Hardware Units Sold")
        fig_heat.update_layout(
            template="plotly_white", 
            xaxis_title="Calendar Month", 
            yaxis_title="Operational Year", 
            height=400, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, l=20, r=20, b=30)
        )
        fig_heat.update_xaxes(automargin=True)
        fig_heat.update_yaxes(automargin=True)
        st.plotly_chart(fig_heat, use_container_width=True)

a3, a4 = st.columns(2)

with a3:
    if not filtered_demo.empty:
        city_coords = {
            'Los Angeles': {'lat': 34.0522, 'lon': -118.2437}, 
            'New York': {'lat': 40.7128, 'lon': -74.0060},
            'London': {'lat': 51.5074, 'lon': -0.1278}, 
            'Tokyo': {'lat': 35.6762, 'lon': 139.6503},
            'New Delhi': {'lat': 28.6139, 'lon': 77.2090}, 
            'Beijing': {'lat': 39.9042, 'lon': 116.4074},
            'San Francisco': {'lat': 37.7749, 'lon': -122.4194}
        }
        map_df = filtered_demo['Geographic_Region'].value_counts().reset_index()
        map_df.columns = ['Geographic_Region', 'Order_Count']
        map_df['lat'] = map_df['Geographic_Region'].apply(lambda x: city_coords.get(x, {}).get('lat', 0))
        map_df['lon'] = map_df['Geographic_Region'].apply(lambda x: city_coords.get(x, {}).get('lon', 0))
        
        fig_map = px.scatter_geo(map_df, lat='lat', lon='lon', size='Order_Count', 
                                 color='Geographic_Region', hover_name='Geographic_Region',
                                 title="Global Demand Distribution (Geographic Map)",
                                 color_discrete_map=REGION_COLOR_MAP,
                                 projection="natural earth")
        fig_map.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))
        fig_map.update_layout(
            template="plotly_white", 
            height=400, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, l=20, r=20, b=30), 
            geo=dict(showland=True, landcolor="#F4F8F7", showcountries=True, countrycolor="#E2E8F0")
        )
        st.plotly_chart(fig_map, use_container_width=True)

with a4:
    if not filtered_demo.empty:
        fig_eff = px.box(filtered_demo, x='Acquisition_Channel', y='App_Engagement_Score', 
                         color='Acquisition_Channel', 
                         title="Channel Conversion Efficiency (Engagement Spread)", 
                         color_discrete_map=CHANNEL_COLOR_MAP)
        fig_eff.update_layout(
            template="plotly_white", 
            xaxis_title="Acquisition Channel", 
            yaxis_title="App Engagement Score", 
            height=400, 
            showlegend=False, 
            paper_bgcolor='rgba(0,0,0,0)', 
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=50, l=20, r=20, b=30)
        )
        fig_eff.update_xaxes(tickangle=-45, automargin=True)
        fig_eff.update_yaxes(automargin=True)
        st.plotly_chart(fig_eff, use_container_width=True)


# ------------------------------------------------------------------------------
# 9. Executive Pitch Conclusion & Investment Summary
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
# 10. Interactive Data Table Inspector
# ------------------------------------------------------------------------------
with st.expander("🔍 Interactive Data Tables (Due Diligence Inspector)"):
    tab1, tab2 = st.tabs(["Financial Projections (36M)", "Customer Demographics (100 Rows)"])
    with tab1:
        display_fin = filtered_fin.copy()
        display_fin['Date'] = display_fin['Date'].dt.strftime('%Y-%m-%d')
        st.dataframe(display_fin, use_container_width=True)
    with tab2:
        st.dataframe(filtered_demo, use_container_width=True)
