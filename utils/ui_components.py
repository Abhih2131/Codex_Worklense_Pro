import streamlit as st


def render_page_title(title: str, subtitle: str | None = None) -> None:
    subtitle_html = f"<p class='page-subtitle'>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f"""
        <div class="page-title-wrap">
            <h2 class="page-title">{title}</h2>
            {subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi(label: str, value: str) -> str:
    return f"""
    <div class=\"kpi-card\">
        <div class=\"kpi-value\">{value}</div>
        <div class=\"kpi-label\">{label}</div>
    </div>
    """


def inject_report_stylesheet() -> None:
    # Retained for backward compatibility with existing reports.
    with open("utils/report_style.css", encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)
