import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="US Labor Statistics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/labor_stats.csv')
    df['date'] = pd.to_datetime(df['date'])
    return df

# Main app
def main():
    st.title("📊 US Labor Statistics Dashboard")
    st.markdown("**Real-time tracking of key US labor market indicators**")
    st.markdown("---")
    
    # Load data
    try:
        df = load_data()
    except FileNotFoundError:
        st.error("❌ Data file not found. Please run the data collection script first.")
        st.code("python src/collect_data.py")
        return
    
    # Sidebar filters
    st.sidebar.header("📅 Filters")
    
    # Date range filter
    min_date = df['date'].min().date()
    max_date = df['date'].max().date()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Series selector
    all_series = df['series_name'].unique().tolist()
    selected_series = st.sidebar.multiselect(
        "Select Series to Display",
        options=all_series,
        default=all_series
    )
    
    # Filter data
    if len(date_range) == 2:
        mask = (df['date'].dt.date >= date_range[0]) & (df['date'].dt.date <= date_range[1])
        filtered_df = df[mask]
    else:
        filtered_df = df
    
    if selected_series:
        filtered_df = filtered_df[filtered_df['series_name'].isin(selected_series)]
    
    # Overview metrics
    st.header("📈 Latest Values")
    
    # Get latest data for each series
    latest_data = filtered_df.sort_values('date').groupby('series_name').tail(1)
    
    # Create columns for metrics
    cols = st.columns(min(len(selected_series), 4))
    
    for idx, (_, row) in enumerate(latest_data.iterrows()):
        col_idx = idx % 4
        with cols[col_idx]:
            # Calculate change from previous month
            series_data = filtered_df[filtered_df['series_name'] == row['series_name']].sort_values('date')
            if len(series_data) >= 2:
                prev_value = series_data.iloc[-2]['value']
                change = row['value'] - prev_value
                change_pct = (change / prev_value) * 100 if prev_value != 0 else 0
                
                st.metric(
                    label=row['series_name'],
                    value=f"{row['value']:,.1f}",
                    delta=f"{change:+,.1f} ({change_pct:+.2f}%)"
                )
            else:
                st.metric(
                    label=row['series_name'],
                    value=f"{row['value']:,.1f}"
                )
    
    st.markdown("---")
    
    # Time series charts
    st.header("📊 Time Series Analysis")
    
    # Create tabs for different views
    tab1, tab2, tab3 = st.tabs(["📈 Individual Series", "🔄 Comparison View", "📋 Data Table"])
    
    with tab1:
        # Individual series charts
        for series_name in selected_series:
            series_data = filtered_df[filtered_df['series_name'] == series_name].sort_values('date')
            
            fig = px.line(
                series_data,
                x='date',
                y='value',
                title=series_name,
                labels={'value': 'Value', 'date': 'Date'}
            )
            
            fig.update_layout(
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Comparison view - all series on one chart
        if len(selected_series) > 0:
            fig = go.Figure()
            
            for series_name in selected_series:
                series_data = filtered_df[filtered_df['series_name'] == series_name].sort_values('date')
                
                fig.add_trace(go.Scatter(
                    x=series_data['date'],
                    y=series_data['value'],
                    name=series_name,
                    mode='lines+markers'
                ))
            
            fig.update_layout(
                title="All Selected Series Comparison",
                xaxis_title="Date",
                yaxis_title="Value",
                hovermode='x unified',
                height=600,
                legend=dict(
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Month-over-month change chart
            st.subheader("📊 Month-over-Month Change (%)")
            
            change_data = []
            for series_name in selected_series:
                series_data = filtered_df[filtered_df['series_name'] == series_name].sort_values('date')
                series_data['pct_change'] = series_data['value'].pct_change() * 100
                change_data.append(series_data)
            
            if change_data:
                combined_change = pd.concat(change_data)
                
                fig2 = px.line(
                    combined_change,
                    x='date',
                    y='pct_change',
                    color='series_name',
                    title="Month-over-Month Percentage Change",
                    labels={'pct_change': 'Change (%)', 'date': 'Date', 'series_name': 'Series'}
                )
                
                fig2.update_layout(
                    hovermode='x unified',
                    height=500
                )
                
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Please select at least one series to display comparison.")
    
    with tab3:
        # Data table view
        st.subheader("📋 Raw Data")
        
        # Pivot table for better viewing
        pivot_df = filtered_df.pivot(
            index='date',
            columns='series_name',
            values='value'
        ).reset_index()
        
        pivot_df = pivot_df.sort_values('date', ascending=False)
        
        st.dataframe(
            pivot_df.style.format({col: "{:,.2f}" for col in pivot_df.columns if col != 'date'}),
            use_container_width=True,
            height=400
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name=f"labor_stats_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    **Data Source:** U.S. Bureau of Labor Statistics (BLS)  
    **Last Updated:** {}  
    **Total Records:** {:,}
    """.format(
        df['date'].max().strftime('%B %Y'),
        len(df)
    ))

if __name__ == "__main__":
    main()