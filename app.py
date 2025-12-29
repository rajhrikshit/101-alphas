import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from src.engine import AlphaEngine
from src.data_loader import load_market_data
from src.definitions import ALPHA_REGISTRY
from src.operators import * 

st.set_page_config(
    layout="wide", 
    page_title="101 Alphas: Quantitative Research Platform",
    initial_sidebar_state="expanded"
)

# --- CSS Styling ---
st.markdown("""
<style>
    .metric-card {
        background-color: #0e1117;
        border: 1px solid #30333d;
        border-radius: 5px;
        padding: 15px;
        text-align: center;
    }
    .latex-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        color: black;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def get_system():
    try:
        # load_market_data returns a robust MarketData object now
        data = load_market_data()
        engine = AlphaEngine(data)
        return engine
    except Exception as e:
        print(e)
        return None

engine = get_system()

# --- Sidebar ---
st.sidebar.title("101 Alphas")
st.sidebar.markdown("### Research Platform")

if engine:
    st.sidebar.success(f"Data Loaded: {len(engine.tickers)} Tickers")
    st.sidebar.info(f"Range: {engine.dates[0].date()} to {engine.dates[-1].date()}")
    
    selected_alpha_id = st.sidebar.selectbox(
        "Select Alpha Strategy", 
        list(ALPHA_REGISTRY.keys()), 
        format_func=lambda x: f"Alpha {x:03d}"
    )
    
    show_educational = st.sidebar.checkbox("🎓 Educational Mode", value=True)
else:
    st.error("System failed to initialize. Check logs.")
    st.stop()

# --- Main Content ---

st.title(f"Alpha {selected_alpha_id:03d} Analysis")

alpha_meta = ALPHA_REGISTRY[selected_alpha_id]
alpha_func = alpha_meta['func']

# 1. Theoretical Framework
with st.expander("📚 Theoretical Framework & Definition", expanded=True):
    col_desc, col_math = st.columns([1, 1])
    
    with col_desc:
        st.markdown("### Description")
        st.write(alpha_meta['description'])
        st.markdown("### Code Definition")
        # Extract source code of the function
        import inspect
        code = inspect.getsource(alpha_func)
        st.code(code, language='python')

    with col_math:
        st.markdown("### Mathematical Formula")
        st.latex(alpha_meta['latex'])

# 2. Computation & Visualization
try:
    alpha_values = engine.run_alpha(alpha_func)
    
    # Calculate performance metrics
    fwd_returns = engine.data.returns.shift(-1)
    
    # Ensure fwd_returns is aligned (MarketData guarantees it usually, but safety first)
    fwd_returns = fwd_returns.reindex(alpha_values.index)
    
    ic_series = alpha_values.corrwith(fwd_returns, axis=1, method='spearman')
    mean_ic = ic_series.mean()
    ic_ir = mean_ic / ic_series.std() if ic_series.std() != 0 else 0
    
    # KPIs
    st.markdown("### 📊 Performance KPIs")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Information Coefficient (Mean)", f"{mean_ic:.4f}")
    kpi2.metric("Information Ratio", f"{ic_ir:.4f}")
    kpi3.metric("Coverage (Non-NaN)", f"{1 - alpha_values.isna().mean().mean():.1%}")
    kpi4.metric("Turnover Proxy", "High" if selected_alpha_id in [1,2,3] else "Med") 

    # Tabs
    tab_analysis, tab_drilldown, tab_educational = st.tabs(["Strategy Analysis", "Ticker Drilldown", "Microscope (Step-by-Step)"])

    with tab_analysis:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Cumulative Information Coefficient")
            st.caption("A rising line indicates consistent predictive power (Positive correlation with next day returns).")
            fig_ic = px.line(ic_series.cumsum(), title="Cumulative IC")
            fig_ic.update_layout(showlegend=False, template="plotly_dark")
            st.plotly_chart(fig_ic, use_container_width=True)
            
        with col2:
            st.subheader("Alpha Distribution")
            latest_vals = alpha_values.iloc[-1].dropna()
            fig_dist = px.histogram(latest_vals, nbins=20, title="Latest Cross-Sectional Distribution")
            fig_dist.update_layout(template="plotly_dark", showlegend=False)
            st.plotly_chart(fig_dist, use_container_width=True)

    with tab_drilldown:
        ticker = st.selectbox("Select Asset to inspect", engine.tickers)
        
        # Dual axis: Price vs Alpha
        fig = go.Figure()
        # Use data.close instead of closes
        fig.add_trace(go.Scatter(x=engine.dates, y=engine.data.close[ticker], name="Price", line=dict(color='gray')))
        fig.add_trace(go.Scatter(x=engine.dates, y=alpha_values[ticker], name="Alpha Signal", yaxis="y2", line=dict(color='#00ff00')))
        
        fig.update_layout(
            title=f"{ticker}: Price vs Signal",
            yaxis=dict(title="Price"),
            yaxis2=dict(title="Alpha", overlaying="y", side="right"),
            template="plotly_dark",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab_educational:
        if show_educational:
            st.markdown("### 🔬 Alpha Microscope")
            st.write("Understand how the components of the alpha interact.")
            
            if selected_alpha_id == 101:
                st.markdown("#### Breakdown of Alpha 101")
                st.latex(r"\alpha = \frac{\text{Close} - \text{Open}}{(\text{High} - \text{Low}) + 0.001}")
                st.write("This alpha measures where the candle closed relative to its total range.")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Numerator (Body)**")
                    st.line_chart((engine.data.close[ticker] - engine.data.open[ticker]).tail(50))
                with col_b:
                    st.write("**Denominator (Range)**")
                    st.line_chart((engine.data.high[ticker] - engine.data.low[ticker]).tail(50))
            
            elif selected_alpha_id == 6:
                st.markdown("#### Breakdown of Alpha 6")
                st.latex(r"-1 \times Correlation(Open, Volume, 10)")
                st.write("This looks for negative correlation between Open prices and Volume.")
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.write("**Open Price**")
                    st.line_chart(engine.data.open[ticker].tail(50))
                with col_b:
                    st.write("**Volume**")
                    st.line_chart(engine.data.volume[ticker].tail(50))
                    
            else:
                st.info("Select Alpha 6 or 101 for a detailed component breakdown example.")
        else:
            st.info("Enable Educational Mode in the sidebar to see detailed breakdowns.")

except Exception as e:
    st.error(f"Computation Error: {e}")
    st.exception(e)
