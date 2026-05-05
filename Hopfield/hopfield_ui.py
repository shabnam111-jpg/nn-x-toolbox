import time

import numpy as np
import plotly.graph_objects as go
import streamlit as st

from utils.ai_sidebar import render_ai_sidebar
from utils.nn_helpers import C, G, MUTED, TEXT, hex2rgba, plotly_layout
from utils.styles import (
    gradient_header,
    inject_global_css,
    render_log,
    render_theory_card,
    section_header,
    stat_card,
)

try:
    import cv2
except ImportError:
    cv2 = None

try:
    from streamlit_drawable_canvas import st_canvas
except ImportError:
    st_canvas = None


GRID_SIZE = 12
PATTERN_SIZE = GRID_SIZE * GRID_SIZE


class HopfieldNetwork:
    def __init__(self, size):
        self.size = size
        self.weights = np.zeros((size, size), dtype=float)

    def train(self, patterns):
        pattern_matrix = np.array(patterns, dtype=float)
        gram = pattern_matrix @ pattern_matrix.T
        self.weights = pattern_matrix.T @ np.linalg.pinv(gram) @ pattern_matrix
        np.fill_diagonal(self.weights, 0.0)
        self.weights = (self.weights + self.weights.T) / 2.0

    def predict(self, input_pattern, iterations=20):
        state = np.array(input_pattern, dtype=float).copy()
        history = [state.copy()]
        rng = np.random.default_rng(7)

        for _ in range(iterations):
            previous = state.copy()
            for index in rng.permutation(self.size):
                activation = self.weights[index] @ state
                state[index] = 1.0 if activation >= 0 else -1.0
            history.append(state.copy())
            if np.array_equal(previous, state):
                break

        return state, history

    def energy(self, state):
        return float(-0.5 * state @ self.weights @ state)


def get_letter_patterns():
    def empty():
        return np.full((GRID_SIZE, GRID_SIZE), -1)

    a = empty()
    a[2:11, 2:3] = 1
    a[2:11, 9:10] = 1
    a[2:3, 3:9] = 1
    a[6:7, 3:9] = 1

    b = empty()
    b[1:11, 2:3] = 1
    b[1:2, 3:9] = 1
    b[5:6, 3:9] = 1
    b[10:11, 3:9] = 1
    b[2:5, 9:10] = 1
    b[6:10, 9:10] = 1

    c = empty()
    c[2:10, 2:3] = 1
    c[1:2, 3:10] = 1
    c[10:11, 3:10] = 1
    c[2:3, 9:10] = 1
    c[9:10, 9:10] = 1

    d = empty()
    d[1:11, 2:3] = 1
    d[1:2, 3:9] = 1
    d[10:11, 3:9] = 1
    d[2:10, 9:10] = 1

    e = empty()
    e[1:11, 2:3] = 1
    e[1:2, 3:10] = 1
    e[5:6, 3:9] = 1
    e[10:11, 3:10] = 1

    return {
        "A": a.flatten().tolist(),
        "B": b.flatten().tolist(),
        "C": c.flatten().tolist(),
        "D": d.flatten().tolist(),
        "E": e.flatten().tolist(),
    }


def _preprocess_canvas(image_data):
    grid = np.zeros(PATTERN_SIZE, dtype=int)
    if image_data is None or cv2 is None:
        return grid

    rgba = image_data.astype(np.uint8)
    gray = cv2.cvtColor(rgba, cv2.COLOR_RGBA2GRAY)
    _, binary = cv2.threshold(gray, 25, 255, cv2.THRESH_BINARY)

    points = cv2.findNonZero(binary)
    if points is not None:
        x, y, w, h = cv2.boundingRect(points)
        pad = 10
        x0 = max(0, x - pad)
        y0 = max(0, y - pad)
        x1 = min(binary.shape[1], x + w + pad)
        y1 = min(binary.shape[0], y + h + pad)
        binary = binary[y0:y1, x0:x1]

    binary = cv2.copyMakeBorder(binary, 12, 12, 12, 12, cv2.BORDER_CONSTANT, value=0)
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)
    binary = cv2.resize(binary, (GRID_SIZE, GRID_SIZE), interpolation=cv2.INTER_AREA)
    binary = (binary > 40).astype(int)
    return binary.flatten()


def _energy_landscape_3d():
    x = np.linspace(-1, 1, 40)
    y = np.linspace(-1, 1, 40)
    x_grid, y_grid = np.meshgrid(x, y)
    z_grid = -(np.cos(2 * np.pi * x_grid) * np.cos(2 * np.pi * y_grid)) * (1 - (x_grid**2 + y_grid**2))

    fig = go.Figure(
        data=[
            go.Surface(
                z=z_grid,
                x=x_grid,
                y=y_grid,
                colorscale="Blues",
                showscale=False,
                opacity=0.92,
            )
        ]
    )
    fig.update_layout(title="Hopfield Energy Landscape", **plotly_layout(height=380))
    fig.update_scenes(xaxis_visible=False, yaxis_visible=False, zaxis_visible=False, bgcolor="rgba(0,0,0,0)")
    return fig


def _attractor_radar_fig(similarities):
    categories = list(similarities.keys())
    values = list(similarities.values())
    fig = go.Figure(
        data=[
            go.Scatterpolar(
                r=values,
                theta=categories,
                fill="toself",
                fillcolor=hex2rgba(C, 0.18),
                line=dict(color=C, width=3),
            )
        ]
    )
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 1], tickfont=dict(color=MUTED)),
            bgcolor="rgba(0,0,0,0)",
            angularaxis=dict(tickfont=dict(color=TEXT)),
        ),
        showlegend=False,
        title="Memory Similarity Radar",
        **plotly_layout(height=350),
    )
    return fig


def _energy_trace_figure(energies):
    fig = go.Figure(
        data=[
            go.Scatter(
                x=list(range(len(energies))),
                y=energies,
                mode="lines+markers",
                line=dict(color=G, width=3),
                marker=dict(size=7, color=C),
                fill="tozeroy",
                fillcolor=hex2rgba(G, 0.1),
            )
        ]
    )
    fig.update_layout(title="Convergence Energy Trace", **plotly_layout(height=350))
    return fig


def _render_grid_display(grid_data, label):
    html = (
        f'<div style="text-align:center; margin-bottom:10px;">'
        f'<span style="font-weight:800; color:{C}; font-size:12px; text-transform:uppercase; letter-spacing:1px;">'
        f"{label}</span></div>"
    )
    html += (
        '<div style="display:grid; grid-template-columns: repeat(12, 1fr); gap:2px; max-width:240px; '
        'margin:0 auto; padding:10px; background:rgba(15,22,41,0.8); border:1px solid rgba(34,211,238,0.3); '
        'border-radius:12px;">'
    )
    for index in range(PATTERN_SIZE):
        value = grid_data[index] if index < len(grid_data) else 0
        if value == 1:
            background = C
            border_color = "rgba(34, 211, 238, 0.85)"
            shadow = f"0 0 8px {C}"
        else:
            background = "rgba(10,14,26,0.92)"
            border_color = "rgba(30,41,59,0.55)"
            shadow = "none"
        html += (
            f'<div style="background:{background}; aspect-ratio:1; border-radius:2px; '
            f'border:1px solid {border_color}; box-shadow:{shadow};"></div>'
        )
    html += "</div>"
    return html


def _score_patterns(predicted, patterns):
    scores = {}
    for letter, pattern in patterns.items():
        target = np.array(pattern)
        scores[letter] = float(np.mean(predicted == target))
    return scores


def hopfield_page():
    inject_global_css()
    gradient_header(
        "Associative Memory", 
        "Hopfield recall with smarter denoising and stronger retrieval", 
        "MEM",
        img_path="https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=1200"
    )

    if "hopfield_model" not in st.session_state:
        patterns = get_letter_patterns()
        model = HopfieldNetwork(PATTERN_SIZE)
        model.train(list(patterns.values()))
        st.session_state.hopfield_model = model
        st.session_state.hopfield_patterns = patterns
        st.session_state.hopfield_logs = []

    col_main, col_ai = st.columns([3, 1])
    with col_ai:
        render_ai_sidebar("Associative Memory")

    with col_main:
        render_theory_card(
            "Attractor Memory Dynamics",
            """
            A Hopfield network stores patterns as attractors in an energy landscape. This upgraded version
            uses a stronger pseudo-inverse memory rule and cleaner sketch preprocessing, so noisy drawings
            are more likely to converge to the intended stored state.
            """,
            formulas=[
                r"E = -\frac{1}{2} s^TWs",
                r"s_i \leftarrow \mathrm{sign}\left(\sum_j w_{ij}s_j\right)",
                r"W = X^T (XX^T)^+ X",
            ],
        )

        canvas_result = None
        input_grid = np.zeros(PATTERN_SIZE, dtype=int)

        col1, col2 = st.columns([1, 1])
        with col1:
            section_header("1. Input Sketch", "Draw a noisy character or inject a template")
            if st_canvas is None:
                st.warning("Install `streamlit-drawable-canvas` to use the drawing interface.")
            else:
                canvas_result = st_canvas(
                    fill_color="rgba(255,255,255,0.35)",
                    stroke_width=22,
                    stroke_color="#FFFFFF",
                    background_color="#0A0E1A",
                    update_streamlit=True,
                    height=240,
                    width=240,
                    drawing_mode="freedraw",
                    key="hopfield_canvas",
                )

            st.markdown("### Inject Pattern Templates")
            template_names = list(st.session_state.hopfield_patterns.keys())
            for name in template_names:
                if st.button(name, use_container_width=True, key=f"template_{name}"):
                    st.session_state.canvas_injected = [
                        1 if point == 1 else 0 for point in st.session_state.hopfield_patterns[name]
                    ]
            
            if st.button("Inject Random Noise", use_container_width=True, key="template_noise"):
                st.session_state.canvas_injected = np.random.choice([0, 1], size=PATTERN_SIZE, p=[0.68, 0.32]).tolist()

        with col2:
            section_header("2. Preprocessed Input", "This is the cleaned pattern fed into the network")
            if canvas_result is not None and canvas_result.image_data is not None:
                input_grid = _preprocess_canvas(canvas_result.image_data)
            if "canvas_injected" in st.session_state:
                input_grid = np.array(st.session_state.pop("canvas_injected"), dtype=int)
            st.markdown(_render_grid_display(input_grid.tolist(), "Normalized Input"), unsafe_allow_html=True)

        if st.button("Trigger Recall Sequence", type="primary", use_container_width=True):
            with st.spinner("Running attractor convergence..."):
                vector = np.where(input_grid > 0, 1, -1)
                started = time.time()
                predicted, history = st.session_state.hopfield_model.predict(vector, iterations=25)
                duration = time.time() - started

                scores = _score_patterns(predicted.astype(int), st.session_state.hopfield_patterns)
                best_match = max(scores, key=scores.get)
                confidence = scores[best_match]
                energy = st.session_state.hopfield_model.energy(predicted)
                energies = [st.session_state.hopfield_model.energy(state) for state in history]
                recall_steps = len(history) - 1
                bit_agreement = float(np.mean(predicted == vector))

                st.session_state.hopfield_result = {
                    "predicted": predicted.astype(int),
                    "match": best_match,
                    "confidence": confidence,
                    "energy": energy,
                    "energies": energies,
                    "scores": scores,
                    "time": duration,
                    "steps": recall_steps,
                    "agreement": bit_agreement,
                }
                st.session_state.hopfield_logs.append(
                    f"Recall completed in {recall_steps} steps. Match={best_match}, confidence={confidence * 100:.1f}%."
                )

        if "hopfield_result" in st.session_state:
            result = st.session_state.hopfield_result
            metrics = st.columns(4)
            with metrics[0]:
                stat_card("Detected", result["match"], color=C)
            with metrics[1]:
                stat_card("Confidence", f"{result['confidence'] * 100:.1f}%", color=G)
            with metrics[2]:
                stat_card("Iterations", result["steps"], color="#60A5FA")
            with metrics[3]:
                stat_card("Input Match", f"{result['agreement'] * 100:.1f}%", color="#F59E0B")

            st.markdown(
                _render_grid_display(
                    [1 if value == 1 else 0 for value in result["predicted"]],
                    "Recalled Pattern",
                ),
                unsafe_allow_html=True,
            )

            chart_left, chart_right = st.columns(2)
            with chart_left:
                st.plotly_chart(_attractor_radar_fig(result["scores"]), use_container_width=True, theme=None)
                st.plotly_chart(_energy_trace_figure(result["energies"]), use_container_width=True, theme=None)
            with chart_right:
                st.plotly_chart(_energy_landscape_3d(), use_container_width=True, theme=None)

        render_log(st.empty(), st.session_state.hopfield_logs)

        st.divider()
        section_header("Stored Attractors", "Reference patterns currently memorized by the network")
        cols = st.columns(5)
        for idx, (letter, pattern) in enumerate(st.session_state.hopfield_patterns.items()):
            with cols[idx]:
                st.markdown(
                    _render_grid_display([1 if value == 1 else 0 for value in pattern], f"State {letter}"),
                    unsafe_allow_html=True,
                )
