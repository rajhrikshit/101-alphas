import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from alphas import AlphaEngine

st.set_page_config(layout="wide", page_title="101 Alphas Explorer")

@st.cache_resource
def get_engine():
    engine = AlphaEngine()
    try:
        engine.load_data()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return None
    return engine

st.title("101 Alphas Explorer")

engine = get_engine()

if engine:
    st.sidebar.header("Settings")
    
    # 1. Data Source Info
    st.sidebar.subheader("Data Source")
    st.sidebar.text(f"Tickers: {len(engine.tickers)}")
    st.sidebar.text(f"Start: {engine.dates[0].date()}")
    st.sidebar.text(f"End: {engine.dates[-1].date()}")
    
    # 2. Alpha Selection
    implemented_alphas = [1, 2, 3, 4, 5, 6, 9, 101]
    alpha_id = st.sidebar.selectbox("Select Alpha", implemented_alphas, format_func=lambda x: f"Alpha #{x:03d}")
    
    # 3. Compute Alpha
    try:
        alpha_values = engine.get_alpha(alpha_id)
        
        # Display Alpha Description (Placeholder logic)
        st.header(f"Alpha #{alpha_id:03d}")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["Heatmap & Statistics", "Time Series Analysis", "Component Drilldown"])
        
        with tab1:
            st.subheader("Alpha Distribution (Latest)")
            latest_alpha = alpha_values.iloc[-1]
            
            fig_hist = px.histogram(latest_alpha, nbins=30, title="Distribution of Alpha Values (Latest Date)")
            st.plotly_chart(fig_hist, use_container_width=True)
            
            st.subheader("Data Table (Latest)")
            st.dataframe(latest_alpha.sort_values(ascending=False).to_frame(name="Alpha Value"))

        with tab2:
            st.subheader("Cumulative Information Coefficient (IC)")
            # Calculate Forward Returns
            fwd_returns = engine.returns.shift(-1)
            
            # Rank Correlation (IC)
            ic = alpha_values.corrwith(fwd_returns, axis=1, method='spearman')
            cum_ic = ic.cumsum()
            
            fig_ic = px.line(cum_ic, title="Cumulative IC (Spearman Correlation with Next Day Returns)")
            st.plotly_chart(fig_ic, use_container_width=True)
            
            st.metric("Mean IC", f"{ic.mean():.4f}")
            st.metric("IC Std Dev", f"{ic.std():.4f}")
            st.metric("IR (IC/Std)", f"{ic.mean()/ic.std():.4f}" if ic.std() != 0 else "N/A")

        with tab3:
            st.subheader("Component Viewer")
            selected_ticker = st.selectbox("Select Ticker", engine.tickers)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Price vs Alpha")
                # Normalize for plotting
                df_plot = pd.DataFrame({
                    'Price': engine.closes[selected_ticker],
                    'Alpha': alpha_values[selected_ticker]
                })
                
                # Dual axis plot
                fig_dual = go.Figure()
                fig_dual.add_trace(go.Scatter(x=df_plot.index, y=df_plot['Price'], name="Price"))
                fig_dual.add_trace(go.Scatter(x=df_plot.index, y=df_plot['Alpha'], name="Alpha", yaxis="y2"))
                
                fig_dual.update_layout(
                    yaxis=dict(title="Price"),
                    yaxis2=dict(title="Alpha", overlaying="y", side="right")
                )
                st.plotly_chart(fig_dual, use_container_width=True)
            
            with col2:
                st.markdown("### Scatter: Alpha vs Fwd Return")
                df_scatter = pd.DataFrame({
                    'Alpha': alpha_values[selected_ticker],
                    'FwdReturn': fwd_returns[selected_ticker]
                })
                fig_scatter = px.scatter(df_scatter, x='Alpha', y='FwdReturn', trendline="ols")
                st.plotly_chart(fig_scatter, use_container_width=True)

    except Exception as e:
        st.error(f"Error computing alpha: {e}")
        st.exception(e)

else:
    st.info("Please ensure data.py is configured correctly.")
