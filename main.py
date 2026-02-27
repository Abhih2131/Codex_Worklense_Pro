import importlib.util
import os

import streamlit as st

from auth import is_logged_in, login_form, logout

st.set_page_config(layout="wide")


@st.cache_data
def load_all_data(path):
    from data_handler import load_all_data as real_loader

    return real_loader(path)


if st.query_params.get("logout") == ["true"]:
    logout()
    st.rerun()

if not is_logged_in():
    login_form()
    st.stop()

try:
    with open("style.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("Custom CSS file not found.")

st.markdown(
    """
<div class='custom-header'>
  <div class='header-left'>
    <div class='brand-name'>WorkplaceAI</div>
    <div class='brand-tagline'>AI-native people intelligence for world-class teams</div>
  </div>
  <div class='header-right'>
    <a href="https://yourhelp.site" target="_blank">Help</a>
    <a href="?logout=true" class="header-logout">Logout</a>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

data_folder = "data"
with st.spinner("Loading data..."):
    data = load_all_data(data_folder)
df_emp = data["employee"]

report_folder = "reports"
report_files = [f.replace(".py", "") for f in os.listdir(report_folder) if f.endswith(".py")]

st.sidebar.markdown("<div class='sidebar-section-title'>Navigation</div>", unsafe_allow_html=True)
selected_report = st.sidebar.selectbox("📊 Report", sorted(report_files), key="report_selector")

st.sidebar.markdown("<div class='sidebar-section-title'>Filters</div>", unsafe_allow_html=True)
st.sidebar.markdown(
    "<div class='sidebar-help'>Narrow down results progressively by organization and workforce slices.</div>",
    unsafe_allow_html=True,
)


def get_filter_values(column):
    return sorted(df_emp[column].dropna().unique())


filter_config = [
    ("company", "Company", "org"),
    ("business_unit", "Business Unit", "org"),
    ("area", "Area", "org"),
    ("department", "Department", "org"),
    ("employment_type", "Employment Type", "workforce"),
    ("zone", "Zone", "workforce"),
    ("function", "Function", "workforce"),
    ("band", "Band", "workforce"),
]

for key, label, _group in filter_config:
    st.session_state.setdefault(f"filter_{key}", [])

with st.sidebar:
    with st.expander("🏢 Organization", expanded=True):
        st.multiselect("Company", get_filter_values("company"), key="filter_company", placeholder="All")
        st.multiselect("Business Unit", get_filter_values("business_unit"), key="filter_business_unit", placeholder="All")
        st.multiselect("Area", get_filter_values("area"), key="filter_area", placeholder="All")
        st.multiselect("Department", get_filter_values("department"), key="filter_department", placeholder="All")

    with st.expander("👤 Workforce", expanded=True):
        st.multiselect(
            "Employment Type",
            get_filter_values("employment_type"),
            key="filter_employment_type",
            placeholder="All",
        )
        st.multiselect("Zone", get_filter_values("zone"), key="filter_zone", placeholder="All")
        st.multiselect("Function", get_filter_values("function"), key="filter_function", placeholder="All")
        st.multiselect("Band", get_filter_values("band"), key="filter_band", placeholder="All")

    if st.button("Reset filters", use_container_width=True):
        for key, _, _ in filter_config:
            st.session_state[f"filter_{key}"] = []
        st.rerun()


def apply_filters(df):
    filtered_df = df.copy()
    for column, _, _ in filter_config:
        selected_values = st.session_state.get(f"filter_{column}", [])
        if selected_values:
            filtered_df = filtered_df[filtered_df[column].isin(selected_values)]
    return filtered_df


data["employee"] = apply_filters(df_emp)

try:
    report_path = os.path.join(report_folder, f"{selected_report}.py")
    spec = importlib.util.spec_from_file_location("report_module", report_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.render(data)
except Exception as e:
    st.error(f"Failed to load report: {e}")

st.markdown("<div class='custom-footer'></div>", unsafe_allow_html=True)
