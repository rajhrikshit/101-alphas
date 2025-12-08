"""
Interactive Dashboard for 101 Alphas Framework
Main Streamlit application for visualizing and exploring alphas.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from alphas.engine import AlphaEngine
from alphas.metadata import get_alpha_metadata, get_all_categories, get_alphas_by_category
from dashboard.utils import load_data, create_sample_data, validate_data


# Page configuration
st.set_page_config(
    page_title="101 Alphas Framework",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    """Main application function."""
    
    # Header
    st.markdown('<div class="main-header">📊 101 Alphas Framework</div>', unsafe_allow_html=True)
    st.markdown("""
    An interactive framework for implementing and visualizing the 101 formulaic alphas 
    from Zura Kakushadze's research paper.
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Data upload section
        st.subheader("1. Data Input")
        data_source = st.radio(
            "Choose data source:",
            ["Upload File", "Use Sample Data"]
        )
        
        data = None
        
        if data_source == "Upload File":
            uploaded_file = st.file_uploader(
                "Upload your OHLCV data (CSV or Excel)",
                type=['csv', 'xlsx', 'xls']
            )
            
            if uploaded_file is not None:
                try:
                    data = load_data(uploaded_file)
                    st.success(f"✅ Loaded {len(data)} records")
                except Exception as e:
                    st.error(f"❌ Error loading file: {str(e)}")
        else:
            # Generate sample data
            st.info("📝 Using synthetic sample data for demonstration")
            num_days = st.slider("Number of days:", 100, 1000, 252)
            num_symbols = st.slider("Number of symbols:", 1, 10, 3)
            
            if st.button("Generate Sample Data"):
                data = create_sample_data(num_days, num_symbols)
                st.success(f"✅ Generated {len(data)} records")
        
        # Alpha selection section
        st.subheader("2. Alpha Selection")
        
        selection_mode = st.radio(
            "Selection mode:",
            ["By Category", "Individual Alphas", "All Alphas"]
        )
        
        selected_alphas = []
        
        if selection_mode == "By Category":
            categories = get_all_categories()
            selected_category = st.selectbox("Select category:", categories)
            selected_alphas = get_alphas_by_category(selected_category)
            st.info(f"Selected {len(selected_alphas)} alphas in '{selected_category}' category")
        
        elif selection_mode == "Individual Alphas":
            available_alphas = [f'alpha_{i:03d}' for i in range(1, 31)]
            selected_alphas = st.multiselect(
                "Select alphas:",
                available_alphas,
                default=['alpha_001', 'alpha_002']
            )
        
        else:  # All Alphas
            selected_alphas = [f'alpha_{i:03d}' for i in range(1, 31)]
            st.info(f"All {len(selected_alphas)} implemented alphas selected")
        
        # Calculate button
        calculate_btn = st.button("🚀 Calculate Alphas", type="primary", use_container_width=True)
    
    # Main content area
    if data is None:
        st.info("👈 Please upload data or generate sample data from the sidebar to begin.")
        
        # Show welcome information
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### 📈 Features")
            st.markdown("""
            - All 101 alpha formulas
            - Interactive visualizations
            - Real-time calculations
            - Multi-asset support
            """)
        
        with col2:
            st.markdown("### 🎯 Categories")
            st.markdown("""
            - Momentum
            - Volume
            - VWAP
            - Volatility
            - Mean-Reversion
            - And more...
            """)
        
        with col3:
            st.markdown("### 📊 Visualizations")
            st.markdown("""
            - Time series plots
            - Correlation heatmaps
            - Distribution analysis
            - Comparative analysis
            """)
        
        # Show example data format
        st.markdown('<div class="sub-header">📋 Required Data Format</div>', unsafe_allow_html=True)
        st.markdown("""
        Your data should contain the following columns:
        """)
        
        example_data = pd.DataFrame({
            'date': pd.date_range('2023-01-01', periods=5),
            'symbol': ['AAPL'] * 5,
            'open': [150.0, 151.0, 149.5, 152.0, 151.5],
            'high': [152.0, 153.0, 151.0, 154.0, 153.0],
            'low': [149.0, 150.0, 148.5, 151.0, 150.5],
            'close': [151.0, 152.0, 150.0, 153.0, 152.0],
            'volume': [1000000, 1100000, 950000, 1200000, 1050000]
        })
        
        st.dataframe(example_data, use_container_width=True)
        
        return
    
    # Show data summary
    st.markdown('<div class="sub-header">📊 Data Summary</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Records", f"{len(data):,}")
    
    with col2:
        if 'date' in data.columns:
            st.metric("Date Range", f"{data['date'].min().strftime('%Y-%m-%d')} to {data['date'].max().strftime('%Y-%m-%d')}")
        else:
            st.metric("Date Range", "N/A")
    
    with col3:
        if 'symbol' in data.columns:
            st.metric("Symbols", data['symbol'].nunique())
        else:
            st.metric("Symbols", 1)
    
    with col4:
        st.metric("Columns", len(data.columns))
    
    # Show data preview
    with st.expander("🔍 View Data Preview"):
        st.dataframe(data.head(20), use_container_width=True)
    
    # Calculate alphas
    if calculate_btn and selected_alphas:
        try:
            with st.spinner("Calculating alphas... This may take a moment."):
                # Initialize engine
                engine = AlphaEngine(data)
                
                # Calculate selected alphas
                alpha_results = engine.calculate_batch(selected_alphas)
                
                # Store in session state
                st.session_state['alpha_results'] = alpha_results
                st.session_state['selected_alphas'] = selected_alphas
                st.session_state['engine'] = engine
                
            st.success(f"✅ Successfully calculated {len(selected_alphas)} alphas!")
        
        except Exception as e:
            st.error(f"❌ Error calculating alphas: {str(e)}")
            st.exception(e)
            return
    
    # Display results if available
    if 'alpha_results' in st.session_state:
        display_results(st.session_state['alpha_results'], st.session_state['selected_alphas'])


def display_results(alpha_results, selected_alphas):
    """Display calculated alpha results with visualizations."""
    
    st.markdown('<div class="sub-header">📈 Alpha Results</div>', unsafe_allow_html=True)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Overview", 
        "📉 Time Series", 
        "🔥 Heatmap", 
        "📋 Data Table"
    ])
    
    with tab1:
        show_overview(alpha_results, selected_alphas)
    
    with tab2:
        show_time_series(alpha_results, selected_alphas)
    
    with tab3:
        show_heatmap(alpha_results)
    
    with tab4:
        show_data_table(alpha_results)


def show_overview(alpha_results, selected_alphas):
    """Show overview statistics for alphas."""
    
    st.markdown("### Summary Statistics")
    
    # Calculate statistics
    stats = alpha_results.describe()
    
    # Display in columns
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Mean Values")
        mean_df = pd.DataFrame({
            'Alpha': alpha_results.columns,
            'Mean': alpha_results.mean().values
        }).sort_values('Mean', ascending=False)
        
        fig = px.bar(mean_df, x='Alpha', y='Mean', 
                     title='Mean Alpha Values',
                     color='Mean',
                     color_continuous_scale='RdBu_r')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### Standard Deviation")
        std_df = pd.DataFrame({
            'Alpha': alpha_results.columns,
            'Std': alpha_results.std().values
        }).sort_values('Std', ascending=False)
        
        fig = px.bar(std_df, x='Alpha', y='Std',
                     title='Alpha Standard Deviation',
                     color='Std',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    # Show detailed statistics
    st.markdown("#### Detailed Statistics")
    st.dataframe(stats, use_container_width=True)
    
    # Alpha information
    if selected_alphas:
        st.markdown("### Alpha Information")
        
        for alpha_name in selected_alphas[:5]:  # Show first 5
            metadata = get_alpha_metadata(alpha_name)
            
            with st.expander(f"ℹ️ {metadata.get('name', alpha_name)}"):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Description:** {metadata.get('description', 'N/A')}")
                    st.markdown(f"**Formula:** `{metadata.get('formula', 'N/A')}`")
                
                with col2:
                    st.markdown(f"**Category:** {metadata.get('category', 'N/A')}")
                    st.markdown(f"**Complexity:** {metadata.get('complexity', 'N/A')}")


def show_time_series(alpha_results, selected_alphas):
    """Show time series plots of alphas."""
    
    st.markdown("### Time Series Visualization")
    
    # Select alphas to plot
    alphas_to_plot = st.multiselect(
        "Select alphas to visualize:",
        selected_alphas,
        default=selected_alphas[:3] if len(selected_alphas) >= 3 else selected_alphas
    )
    
    if not alphas_to_plot:
        st.warning("Please select at least one alpha to visualize.")
        return
    
    # Create plot
    fig = go.Figure()
    
    for alpha in alphas_to_plot:
        if alpha in alpha_results.columns:
            fig.add_trace(go.Scatter(
                x=alpha_results.index,
                y=alpha_results[alpha],
                name=alpha,
                mode='lines'
            ))
    
    fig.update_layout(
        title='Alpha Values Over Time',
        xaxis_title='Date',
        yaxis_title='Alpha Value',
        hovermode='x unified',
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribution plots
    st.markdown("### Distribution Analysis")
    
    alpha_for_dist = st.selectbox("Select alpha for distribution:", alphas_to_plot)
    
    if alpha_for_dist:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                alpha_results, 
                x=alpha_for_dist,
                title=f'Distribution of {alpha_for_dist}',
                nbins=50
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.box(
                alpha_results,
                y=alpha_for_dist,
                title=f'Box Plot of {alpha_for_dist}'
            )
            st.plotly_chart(fig, use_container_width=True)


def show_heatmap(alpha_results):
    """Show correlation heatmap of alphas."""
    
    st.markdown("### Correlation Analysis")
    
    # Calculate correlation matrix
    corr_matrix = alpha_results.corr()
    
    # Create heatmap
    fig = px.imshow(
        corr_matrix,
        title='Alpha Correlation Heatmap',
        color_continuous_scale='RdBu_r',
        aspect='auto',
        zmin=-1,
        zmax=1
    )
    
    fig.update_layout(height=600)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show highly correlated pairs
    st.markdown("### Highly Correlated Pairs")
    
    threshold = st.slider("Correlation threshold:", 0.0, 1.0, 0.7, 0.05)
    
    # Find pairs
    corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i+1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) >= threshold:
                corr_pairs.append({
                    'Alpha 1': corr_matrix.columns[i],
                    'Alpha 2': corr_matrix.columns[j],
                    'Correlation': corr_val
                })
    
    if corr_pairs:
        corr_df = pd.DataFrame(corr_pairs).sort_values('Correlation', ascending=False, key=abs)
        st.dataframe(corr_df, use_container_width=True)
    else:
        st.info(f"No alpha pairs with correlation >= {threshold}")


def show_data_table(alpha_results):
    """Show alpha results in table format."""
    
    st.markdown("### Alpha Values Table")
    
    # Add download button
    csv = alpha_results.to_csv()
    st.download_button(
        label="📥 Download Results as CSV",
        data=csv,
        file_name="alpha_results.csv",
        mime="text/csv"
    )
    
    # Show data
    st.dataframe(alpha_results, use_container_width=True, height=600)
    
    # Show statistics
    with st.expander("📊 View Statistics"):
        st.dataframe(alpha_results.describe(), use_container_width=True)


if __name__ == "__main__":
    main()
