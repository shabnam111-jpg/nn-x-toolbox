import numpy as np
import plotly.graph_objects as go

# ──── AURA STUDIO: DARK ORBITAL PALETTE ────
BG      = "#030712"      # Velvet Black
SURF    = "#111827"      # Matte Surface
CARD    = "rgba(17, 24, 39, 0.7)" # Glass Depth
P       = "#6366F1"      # Aura Indigo
C       = "#22D3EE"      # Cyber Cyan
G       = "#10B981"      # Emerald Logic
A       = "#F59E0B"      # Amber Metric
R       = "#EF4444"      # Rose Warning
TEXT    = "#F1F5F9"      # Starlight Text
MUTED   = "#94A3B8"      # Digital Dust
GRID    = "rgba(148, 163, 184, 0.1)"

LAYER_COLS = [P, C, G, A, "#8B5CF6", "#F97316"]

PLOTLY_BASE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color=TEXT, family="'Plus Jakarta Sans', sans-serif"),
    margin=dict(t=50, b=40, l=50, r=20),
    hoverlabel=dict(bgcolor="#1E293B", font_size=13, font_family="Inter"),
    dragmode="pan"
)

PLOTLY_AXIS = dict(
    gridcolor=GRID,
    zerolinecolor="rgba(148, 163, 184, 0.2)",
    color=MUTED,
    tickfont=dict(color=MUTED, size=10),
    showgrid=True
)

def plotly_layout(**kwargs):
    """Generates a themed Plotly layout for Aura Studio."""
    base = dict(**PLOTLY_BASE)
    
    xaxis_custom = kwargs.pop('xaxis', {})
    yaxis_custom = kwargs.pop('yaxis', {})
    
    base['xaxis'] = dict(**PLOTLY_AXIS)
    base['xaxis'].update(xaxis_custom)
    
    base['yaxis'] = dict(**PLOTLY_AXIS)
    base['yaxis'].update(yaxis_custom)
    
    base.update(kwargs)
    return base

# ──── MATH UTILS ────
ACTS = {
    "Sigmoid": {"fn": lambda z: 1/(1+np.exp(-np.clip(z,-50,50))), "d": lambda a: a*(1-a)},
    "ReLU": {"fn": lambda z: np.maximum(0,z), "d": lambda a: (a>0).astype(float)},
    "Tanh": {"fn": lambda z: np.tanh(z), "d": lambda a: 1-a**2},
}

def hex2rgba(h, a):
    h = h.lstrip('#')
    return f"rgba({int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)},{a})"

def draw_network(sizes, labels, vals=None):
    n = len(sizes)
    fig = go.Figure()
    lx = np.linspace(0.1, 0.9, n).tolist()
    
    def ny(tot, i): return np.linspace(0.9, 0.1, tot)[i] if tot > 1 else 0.5

    for li in range(n-1):
        for i in range(sizes[li]):
            for j in range(sizes[li+1]):
                fig.add_shape(type="line", x0=lx[li], y0=ny(sizes[li], i), x1=lx[li+1], y1=ny(sizes[li+1], j),
                              line=dict(color=hex2rgba(P, 0.2), width=0.8), xref="paper", yref="paper", layer="below")

    for li, nn in enumerate(sizes):
        col = LAYER_COLS[li % len(LAYER_COLS)]
        for i in range(nn):
            fig.add_trace(go.Scatter(x=[lx[li]], y=[ny(nn, i)], mode="markers+text",
                                     marker=dict(size=25, color=hex2rgba(col, 0.8), line=dict(color=SURF, width=2)),
                                     text=[labels[li] if i==0 else ""], textposition="top center",
                                     textfont=dict(size=10, color=MUTED), showlegend=False))
            
    fig.update_layout(xaxis=dict(visible=False), yaxis=dict(visible=False), 
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0,r=0,t=0,b=0))
    return fig
