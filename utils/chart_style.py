import plotly.io as pio

BRAND_TEMPLATE_NAME = "worklense_professional"
BRAND_COLORWAY = [
    "#4E79A7",
    "#F28E2B",
    "#E15759",
    "#76B7B2",
    "#59A14F",
    "#EDC948",
    "#B07AA1",
    "#FF9DA7",
    "#9C755F",
    "#BAB0AC",
]


def register_brand_template() -> None:
    pio.templates[BRAND_TEMPLATE_NAME] = {
        "layout": {
            "paper_bgcolor": "rgba(0,0,0,0)",
            "plot_bgcolor": "#ffffff",
            "font": {"family": "Inter, sans-serif", "color": "#21344d", "size": 13},
            "colorway": BRAND_COLORWAY,
            "legend": {
                "bgcolor": "rgba(255,255,255,0.82)",
                "bordercolor": "#d7e0ee",
                "borderwidth": 1,
                "font": {"color": "#31445e"},
            },
            "xaxis": {
                "gridcolor": "#e9eff7",
                "linecolor": "#ccd7e6",
                "zerolinecolor": "#dbe4f0",
                "tickfont": {"color": "#4d6281"},
                "title": {"font": {"color": "#425672"}},
            },
            "yaxis": {
                "gridcolor": "#e9eff7",
                "linecolor": "#ccd7e6",
                "zerolinecolor": "#dbe4f0",
                "tickfont": {"color": "#4d6281"},
                "title": {"font": {"color": "#425672"}},
            },
            "title": {"font": {"color": "#223a5e", "size": 18}},
            "margin": {"l": 56, "r": 24, "t": 52, "b": 48},
        }
    }


def use_brand_template() -> None:
    register_brand_template()
    pio.templates.default = BRAND_TEMPLATE_NAME
