import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ===== PAGE CONFIGURATION =====
st.set_page_config(
    page_title="US Labor Statistics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS FOR BETTER STYLING =====
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 1rem 2rem;
    }
    
    /* Header styling */
    h1 {
        color: #1f77b4;
        font-weight: 600;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #1f77b4;
    }
    
    h2 {
        color: #2c3e50;
        margin-top: 2rem;
    }
    
    h3 {
        color: #34495e;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
    }
    
    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #e8f4f8;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    
    /* Remove extra spacing */
    .element-container {
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# ===== DATA LOADING =====
@st.cache_data
def load_data():
    """Load and cache the labor statistics data"""
    try:
        df = pd.read_csv('data/processed/labor_stats.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Please run the data collection script.")
        return None

# ===== MAIN APP =====
def main():
    # Load data
    df = load_data()
    if df is None:
        st.stop()
    
    # ===== HEADER SECTION =====
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📊 US Labor Statistics Dashboard")
        st.markdown("**Real-time tracking of key US labor market indicators from the Bureau of Labor Statistics**")
    with col2:
        st.markdown(f"""
            <div style='text-align: right; padding-top: 1rem;'>
                <p style='margin: 0; color: #666;'>Last Updated</p>
                <p style='margin: 0; font-weight: 600;'>{df['date'].max().strftime('%B %Y')}</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # ===== SIDEBAR FILTERS =====
    with st.sidebar:
        st.image("https://www.bls.gov/images/bls_emblem.png", width=100)  # Optional BLS logo
        st.header("🎛️ Dashboard Controls")
        
        # Date range filter
        st.subheader("📅 Time Period")
        min_date = df['date'].min().date()
        max_date = df['date'].max().date()
        
        date_range = st.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
            help="Choose the time period to analyze"
        )
        
        st.markdown("---")
        
        # Series selector
        st.subheader("📈 Indicators")
        all_series = sorted(df['series_name'].unique().tolist())
        selected_series = st.multiselect(
            "Select Series to Display",
            options=all_series,
            default=all_series,
            help="Choose which labor market indicators to show"
        )
        
        st.markdown("---")
        
        # Info section
        st.subheader("ℹ️ About")
        st.info("""
        **Data Source**: U.S. Bureau of Labor Statistics
        
        **Update Frequency**: Monthly (first Friday)
        
        **Total Records**: {:,}
        
        **Date Range**: {} to {}
        """.format(
            len(df),
            df['date'].min().strftime('%b %Y'),
            df['date'].max().strftime('%b %Y')
        ))
        
        # GitHub link
        st.markdown("""
            <div style='text-align: center; margin-top: 2rem;'>
                <a href='https://github.com/dhnguyen620/econ8320-project' target='_blank'>
                    <img src='https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png' width='30'>
                    <br>View on GitHub
                </a>
            </div>
        """, unsafe_allow_html=True)
    
    # ===== FILTER DATA =====
    if len(date_range) == 2:
        filtered_df = df[
            (df['date'].dt.date >= date_range[0]) & 
            (df['date'].dt.date <= date_range[1])
        ]
    else:
        filtered_df = df
    
    if selected_series:
        filtered_df = filtered_df[filtered_df['series_name'].isin(selected_series)]
    else:
        st.warning("⚠️ Please select at least one indicator to display.")
        st.stop()
    
    # ===== OVERVIEW METRICS SECTION =====
    st.header("📊 Latest Values")
    st.markdown("*Month-over-month changes*")
    
    latest_data = filtered_df.sort_values('date').groupby('series_name').tail(1)
    
    # Create metrics in rows of 4
    metrics_per_row = 4
    for i in range(0, len(latest_data), metrics_per_row):
        cols = st.columns(metrics_per_row)
        
        for idx, (_, row) in enumerate(list(latest_data.iterrows())[i:i+metrics_per_row]):
            with cols[idx]:
                series_data = filtered_df[
                    filtered_df['series_name'] == row['series_name']
                ].sort_values('date')
                
                if len(series_data) >= 2:
                    prev_value = series_data.iloc[-2]['value']
                    change = row['value'] - prev_value
                    change_pct = (change / prev_value) * 100 if prev_value != 0 else 0
                    
                    st.metric(
                        label=row['series_name'],
                        value=f"{row['value']:,.1f}",
                        delta=f"{change_pct:+.2f}%",
                        help=f"Change: {change:+,.1f}"
                    )
                else:
                    st.metric(
                        label=row['series_name'],
                        value=f"{row['value']:,.1f}"
                    )
    
    st.markdown("---")
    
    # ===== TABBED VISUALIZATION SECTION =====
    st.header("📈 Detailed Analysis")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Individual Series", 
        "🔄 Multi-Series Comparison", 
        "📉 Month-over-Month Changes",
        "📋 Data Table"
    ])
    
    # TAB 1: Individual Series
    with tab1:
        st.markdown("### Time Series Analysis")
        st.markdown("*Explore each indicator's trend over time*")
        
        for series_name in selected_series:
            with st.expander(f"📈 {series_name}", expanded=(len(selected_series) <= 3)):
                series_data = filtered_df[
                    filtered_df['series_name'] == series_name
                ].sort_values('date')
                
                if len(series_data) > 0:
                    fig = px.line(
                        series_data,
                        x='date',
                        y='value',
                        title=f"{series_name} Over Time",
                        labels={'value': 'Value', 'date': 'Date'},
                        template='plotly_white'
                    )
                    
                    fig.update_traces(
                        line_color='#1f77b4',
                        line_width=2,
                        hovertemplate='<b>%{x|%b %Y}</b><br>Value: %{y:,.2f}<extra></extra>'
                    )
                    
                    fig.update_layout(
                        height=400,
                        hovermode='x unified',
                        margin=dict(l=20, r=20, t=40, b=20)
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Summary statistics
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Current", f"{series_data.iloc[-1]['value']:,.2f}")
                    col2.metric("Average", f"{series_data['value'].mean():,.2f}")
                    col3.metric("Min", f"{series_data['value'].min():,.2f}")
                    col4.metric("Max", f"{series_data['value'].max():,.2f}")
    
    # TAB 2: Multi-Series Comparison
    with tab2:
        st.markdown("### Compare Multiple Indicators")
        st.markdown("*Analyze relationships and correlations between different metrics*")
        
        if len(selected_series) > 1:
            fig = go.Figure()
            
            colors = px.colors.qualitative.Set2
            
            for idx, series_name in enumerate(selected_series):
                series_data = filtered_df[
                    filtered_df['series_name'] == series_name
                ].sort_values('date')
                
                fig.add_trace(go.Scatter(
                    x=series_data['date'],
                    y=series_data['value'],
                    name=series_name,
                    mode='lines+markers',
                    line=dict(width=2, color=colors[idx % len(colors)]),
                    marker=dict(size=4),
                    hovertemplate='<b>%{fullData.name}</b><br>%{x|%b %Y}<br>Value: %{y:,.2f}<extra></extra>'
                ))
            
            fig.update_layout(
                title="All Selected Series Comparison",
                xaxis_title="Date",
                yaxis_title="Value",
                hovermode='x unified',
                height=600,
                template='plotly_white',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=20, r=20, t=80, b=20)
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📌 Select multiple series from the sidebar to compare them.")
    
    # TAB 3: Month-over-Month Changes
    with tab3:
        st.markdown("### Percentage Changes Analysis")
        st.markdown("*Track growth rates and volatility*")
        
        change_data = []
        for series_name in selected_series:
            series_data = filtered_df[
                filtered_df['series_name'] == series_name
            ].sort_values('date').copy()
            
            series_data['pct_change'] = series_data['value'].pct_change() * 100
            change_data.append(series_data)
        
        if change_data:
            combined_change = pd.concat(change_data)
            
            fig = px.line(
                combined_change.dropna(subset=['pct_change']),
                x='date',
                y='pct_change',
                color='series_name',
                title="Month-over-Month Percentage Change",
                labels={
                    'pct_change': 'Change (%)', 
                    'date': 'Date', 
                    'series_name': 'Indicator'
                },
                template='plotly_white'
            )
            
            fig.update_layout(
                height=500,
                hovermode='x unified',
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
            
            st.plotly_chart(fig, use_container_width=True)
    
    # TAB 4: Data Table
    with tab4:
        st.markdown("### Raw Data View")
        st.markdown("*Export and explore the underlying dataset*")
        
        # Pivot table
        pivot_df = filtered_df.pivot(
            index='date',
            columns='series_name',
            values='value'
        ).reset_index()
        
        pivot_df = pivot_df.sort_values('date', ascending=False)
        
        # Format date column
        pivot_df['date'] = pivot_df['date'].dt.strftime('%Y-%m')
        
        st.dataframe(
            pivot_df.style.format(
                {col: "{:,.2f}" for col in pivot_df.columns if col != 'date'}
            ),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"labor_stats_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            help="Download the filtered dataset"
        )
    
    # ===== FOOTER =====
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Data Source**")
        st.markdown("U.S. Bureau of Labor Statistics")
    
    with col2:
        st.markdown("**Last Updated**")
        st.markdown(df['date'].max().strftime('%B %Y'))
    
    with col3:
        st.markdown("**Total Records**")
        st.markdown(f"{len(df):,}")

if __name__ == "__main__":
    main()