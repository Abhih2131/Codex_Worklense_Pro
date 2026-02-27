import plotly.io as pio

BRAND_TEMPLATE_NAME = "worklense_dark"
BRAND_COLORWAY = [
    "#6d4dff",
    "#15d4ff",
    "#ff3cac",
    "#8bf3ff",
    "#9e84ff",
    "#ffc14d",
    "#56f2b5",
]


def register_brand_template() -> None:
    pio.templates[BRAND_TEMPLATE_NAME] = {
        "layout": {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "rgba(0,0,0,0)",
            "font": {"family": "Inter, sans-serif", "color": "#f4f7ff", "size": 13},
            "colorway": BRAND_COLORWAY,
            "legend": {
                "bgcolor": "rgba(9,14,30,0.72)",
                "bordercolor": "rgba(255,255,255,0.16)",
                "borderwidth": 1,
                "font": {"color": "#d9e7ff"},
            },
            "xaxis": {
                "gridcolor": "rgba(255,255,255,0.10)",
                "linecolor": "rgba(255,255,255,0.25)",
                "zerolinecolor": "rgba(255,255,255,0.16)",
            },
            "yaxis": {
                "gridcolor": "rgba(255,255,255,0.10)",
                "linecolor": "rgba(255,255,255,0.25)",
                "zerolinecolor": "rgba(255,255,255,0.16)",
            },
            "title": {"font": {"color": "#f8faff", "size": 17}},
        }
    }


def use_brand_template() -> None:
    register_brand_template()
    pio.templates.default = BRAND_TEMPLATE_NAME
