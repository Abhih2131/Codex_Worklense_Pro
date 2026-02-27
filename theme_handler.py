import streamlit as st

from utils.chart_style import use_brand_template


def selected_theme() -> str:
    """Apply a single brand-aligned chart template everywhere."""
    use_brand_template()
    st.sidebar.caption("🎨 Chart style: Worklense Dark (brand default)")
    return "worklense_dark"
