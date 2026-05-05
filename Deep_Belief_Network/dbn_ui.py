import numpy as np
import plotly.graph_objects as go
import streamlit as st
from streamlit.errors import StreamlitAPIException
from plotly.subplots import make_subplots
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, log_loss
from sklearn.model_selection import train_test_split
from sklearn.neural_network import BernoulliRBM

from utils.ai_sidebar import render_ai_sidebar
from utils.nn_helpers import C, G, MUTED, P, R, TEXT, hex2rgba, plotly_layout
from utils.styles import gradient_header, inject_global_css, render_theory_card, section_header, stat_card


class StackedDBN:
    def __init__(self, hidden_units=(128, 64), learning_rate=0.03, batch_size=32, n_iter=10, random_state=42):
        self.hidden_units = hidden_units
        self.learning_rate = learning_rate
        self.batch_size = batch_size
        self.n_iter = n_iter
        self.random_state = random_state
        self.rbms = []
        self.classifier = LogisticRegression(max_iter=1000)
        self.history = []

    def fit(self, x_train, y_train):
        current = x_train
        self.rbms = []
        layer_means = []
        self.history = []

        for index, units in enumerate(self.hidden_units):
            rbm = BernoulliRBM(
                n_components=units,
                learning_rate=self.learning_rate,
                batch_size=self.batch_size,
                n_iter=self.n_iter,
                verbose=0,
                random_state=self.random_state + index,
            )
            # We simulate epoch-by-epoch error for visualization purposes
            # BernoulliRBM doesn't expose it easily, so we track reconstruction mean
            rbm.fit(current)
            error = rbm.score_samples(current).mean()
            self.history.append({"layer": index + 1, "error": error})
            
            current = rbm.transform(current)
            self.rbms.append(rbm)
            layer_means.append(float(np.mean(current)))

        self.classifier.fit(current, y_train)
        return layer_means

    def transform(self, x):
        hidden_states = []
        current = x
        for rbm in self.rbms:
            current = rbm.transform(current)
            hidden_states.append(current)
        return hidden_states

    def reconstruct(self, x):
        """Pass inputs up through hidden layers, then back down to visible layer."""
        # Forward pass
        current = x
        hidden_activations = []
        for rbm in self.rbms:
            current = rbm.transform(current)
            hidden_activations.append(current)
        
        # Backward pass (reconstruction)
        recon = current
        for rbm in reversed(self.rbms):
            # p(v|h) = sigmoid(hW + b_v)
            # sklearn components_ = W (n_components, n_features)
            # recon (n_samples, n_components)
            v_logits = np.dot(recon, rbm.components_) + rbm.intercept_visible_
            recon = 1 / (1 + np.exp(-np.clip(v_logits, -100, 100))) # Sigmoid
        return recon, hidden_activations

    def predict(self, x):
        hidden_states = self.transform(x)
        return self.classifier.predict(hidden_states[-1])

    def predict_proba(self, x):
        hidden_states = self.transform(x)
        return self.classifier.predict_proba(hidden_states[-1]), hidden_states


def _prepare_digits_dataset(test_size=0.2, noise=0.0, threshold=0.35, random_state=42):
    digits = load_digits()
    x = digits.data.astype(np.float32) / 16.0
    y = digits.target

    if noise > 0:
        rng = np.random.default_rng(random_state)
        x = np.clip(x + rng.normal(0, noise, size=x.shape), 0.0, 1.0)

    x = (x >= threshold).astype(np.float32)

    return train_test_split(
        x,
        y,
        digits.images,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )


def _metric_figure(train_acc, test_acc, loss_value):
    fig = make_subplots(
        rows=1, cols=2, 
        subplot_titles=("Accuracy Snapshot", "Classifier Loss"),
        specs=[[{"type": "xy"}, {"type": "domain"}]]
    )
    fig.add_trace(
        go.Bar(
            x=["Train", "Test"],
            y=[train_acc, test_acc],
            marker_color=[P, G],
            text=[f"{train_acc:.3f}", f"{test_acc:.3f}"],
            textposition="outside",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=loss_value,
            number={"font": {"color": TEXT}},
            gauge={
                "axis": {"range": [0, max(2.5, loss_value + 0.3)], "tickcolor": MUTED},
                "bar": {"color": R},
                "bgcolor": "rgba(0,0,0,0)",
            },
        ),
        row=1,
        col=2,
    )
    fig.update_layout(title="Deep Belief Network Performance", **plotly_layout(height=360))
    return fig


def _confusion_fig(cm):
    fig = go.Figure(
        data=[
            go.Heatmap(
                z=cm,
                x=list(range(10)),
                y=list(range(10)),
                colorscale="Viridis",
                text=cm,
                texttemplate="%{text}",
                colorbar={"title": "Count"},
            )
        ]
    )
    fig.update_layout(
        title="Confusion Matrix",
        xaxis_title="Predicted Digit",
        yaxis_title="True Digit",
        **plotly_layout(height=420),
    )
    return fig


def _hidden_activation_fig(hidden_states):
    means = [float(np.mean(layer)) for layer in hidden_states]
    peaks = [float(np.max(layer)) for layer in hidden_states]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=["RBM 1", "RBM 2"][: len(means)], y=means, name="Mean activation", marker_color=P))
    fig.add_trace(go.Scatter(x=["RBM 1", "RBM 2"][: len(peaks)], y=peaks, name="Peak activation", mode="lines+markers", line=dict(color=C, width=3)))
    fig.update_layout(title="Hidden Representation Dynamics", **plotly_layout(height=360))
    return fig


def _digit_panel(sample, title):
    z = np.flipud(sample)
    fig = go.Figure(
        data=[
            go.Heatmap(
                z=z,
                colorscale=[[0, "#050816"], [1, "#67E8F9"]],
                showscale=False,
            )
        ]
    )
    fig.update_layout(title=title, xaxis_visible=False, yaxis_visible=False, **plotly_layout(height=280))
    return fig


def _render_dbn_content():
    render_theory_card(
        "Deep Belief Networks",
        """
        A Deep Belief Network stacks Restricted Boltzmann Machines so each layer learns a more abstract
        representation of the data. After unsupervised pretraining, a classifier head uses the learned
        latent features for prediction.
        """,
        formulas=[
            r"P(h_j=1|v)=\sigma(b_j + \sum_i W_{ij} v_i)",
            r"P(v_i=1|h)=\sigma(a_i + \sum_j W_{ij} h_j)",
            r"\mathrm{DBN} = \mathrm{RBM}_1 \rightarrow \mathrm{RBM}_2 \rightarrow \mathrm{Classifier}",
        ],
        color=P,
    )

    with st.container(border=True):
        section_header("1. Model Forge", "Tune the stacked RBM pretraining pipeline")
        hidden_1 = st.slider("RBM 1 Units", 32, 256, 128, 16)
        hidden_2 = st.slider("RBM 2 Units", 16, 128, 64, 8)
        learning_rate = st.selectbox("Learning Rate", [0.1, 0.05, 0.03, 0.01], index=2)
        n_iter = st.slider("RBM Epochs", 3, 25, 10)
        batch_size = st.selectbox("Batch Size", [16, 32, 64, 128], index=1)
        threshold = st.slider("Binarization Threshold", 0.10, 0.90, 0.35, 0.05)
        noise = st.slider("Input Noise", 0.0, 0.40, 0.0, 0.02)

    if st.button("Train Deep Belief Network", type="primary", use_container_width=True):
        with st.spinner("Pretraining RBM layers and fitting classifier head..."):
            x_train, x_test, y_train, y_test, img_train, img_test = _prepare_digits_dataset(
                noise=noise,
                threshold=threshold,
            )

            model = StackedDBN(
                hidden_units=(hidden_1, hidden_2),
                learning_rate=learning_rate,
                batch_size=batch_size,
                n_iter=n_iter,
            )
            layer_means = model.fit(x_train, y_train)

            train_pred = model.predict(x_train)
            test_pred = model.predict(x_test)
            test_proba, test_hidden_states = model.predict_proba(x_test)

            train_acc = accuracy_score(y_train, train_pred)
            test_acc = accuracy_score(y_test, test_pred)
            loss_value = log_loss(y_test, test_proba)
            cm = confusion_matrix(y_test, test_pred)

            st.session_state.dbn_state = {
                "model": model,
                "x_test": x_test,
                "y_test": y_test,
                "img_test": img_test,
                "test_pred": test_pred,
                "test_proba": test_proba,
                "hidden_states": test_hidden_states,
                "train_acc": train_acc,
                "test_acc": test_acc,
                "loss": loss_value,
                "layer_means": layer_means,
                "cm": cm,
            }

    if "dbn_state" in st.session_state:
        state = st.session_state.dbn_state

        st.markdown("### DBN Performance Metrics")
        stat_card("Train Accuracy", f"{state['train_acc'] * 100:.1f}%", color=P)
        stat_card("Test Accuracy", f"{state['test_acc'] * 100:.1f}%", color=G)
        stat_card("Log Loss", f"{state['loss']:.3f}", color=R)
        stat_card("RBM Layers", "2", color=C)

        st.markdown("### Interactive Plots")
        st.plotly_chart(_metric_figure(state["train_acc"], state["test_acc"], state["loss"]), use_container_width=True, theme=None)
        st.plotly_chart(_confusion_fig(state["cm"]), use_container_width=True, theme=None)
        st.plotly_chart(_hidden_activation_fig(state["hidden_states"]), use_container_width=True, theme=None)

        section_header("2. Sample Inference", "Inspect a single test digit through the DBN")
        sample_index = st.slider("Test Sample Index", 0, len(state["x_test"]) - 1, 0)
        sample_vector = state["x_test"][sample_index : sample_index + 1]
        sample_image = state["img_test"][sample_index]
        true_label = int(state["y_test"][sample_index])
        pred_label = int(state["test_pred"][sample_index])
        confidence = float(np.max(state["test_proba"][sample_index]))

        st.plotly_chart(_digit_panel(sample_image, f"True Digit: {true_label}"), use_container_width=True, theme=None)
        st.plotly_chart(
            _digit_panel(sample_vector.reshape(8, 8), f"DBN Input: Pred {pred_label}"),
            use_container_width=True,
            theme=None,
        )

        st.markdown(
            f"""
            <div class="premium-card" style="padding:18px; border-left:4px solid {C};">
                <div style="font-size:14px; color:{MUTED}; font-weight:700; margin-bottom:10px;">Inference Summary</div>
                <div style="font-size:30px; color:#F8FAFC; font-weight:800;">Digit {pred_label}</div>
                <div style="font-size:14px; color:{C}; font-weight:700; margin-top:8px;">Confidence {confidence * 100:.1f}%</div>
                <div style="font-size:13px; color:#CBD5E1; margin-top:8px;">True label: {true_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        section_header("3. DBN Reconstruction", "Visualizing top-down generative recall")

        recon_vector, _ = state["model"].reconstruct(sample_vector)

        st.plotly_chart(_digit_panel(sample_vector.reshape(8, 8), "Original Input"), use_container_width=True, theme=None)
        st.markdown("<div style='text-align:center; padding: 20px 0; font-size: 40px; color: #22D3EE;'>↓ Generative Reconstruction ↓</div>", unsafe_allow_html=True)
        st.plotly_chart(_digit_panel(recon_vector.reshape(8, 8), "Generative Reconstruction"), use_container_width=True, theme=None)

        with st.expander("Show Gibbs Sampling Calculations", expanded=False):
            st.markdown("### Reconstruction Math Step-by-Step")

            rbm1 = state["model"].rbms[0]
            bv = rbm1.intercept_visible_
            bh = rbm1.intercept_hidden_

            st.markdown(f"**Sample Input Vector (first 5 units):** `{sample_vector[0][:5]}`")
            st.markdown("**Gibbs Step 1: Visible to Hidden**")
            st.latex(r"P(h_j=1|v) = \sigma(b_j + \sum_i W_{ij} v_i)")
            st.markdown(f"Layer 1 Hidden Biases (mean): `{bh.mean():.4f}`")

            st.markdown("**Gibbs Step 2: Hidden to Visible (Reconstruction)**")
            st.latex(r"P(v_i=1|h) = \sigma(a_i + \sum_j W_{ij} h_j)")
            st.markdown(f"Layer 1 Visible Biases (mean): `{bv.mean():.4f}`")

            st.info("Reconstruction error is minimized as the RBM learns to model the data distribution.")
    else:
        st.markdown(
            f"""
            <div class="premium-card" style="text-align:center; padding:80px 20px;">
                <div style="font-size:54px; margin-bottom:16px;">DBN</div>
                <div style="color:{MUTED}; font-weight:700;">Train the new Deep Belief Network to unlock metrics and inference.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def dbn_page():
    inject_global_css()
    gradient_header(
        "Deep Belief Network",
        "Stacked RBM pretraining and deep classification",
        "DBN",
        img_path="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80&w=1200",
    )

    # Remove stale flags from older layout-fallback flows.
    st.session_state.pop("dbn_force_single_column", None)
    st.session_state.pop("dbn_layout_fallback_reason", None)

    try:
        _render_dbn_content()
    except StreamlitAPIException as exc:
        if "Columns can only be placed inside other columns up to one level of nesting" in str(exc):
            st.warning("DBN layout compatibility mode is active.")
        else:
            raise
    except Exception as exc:
        st.error("DBN module hit an unexpected error.")
        st.exception(exc)

    with st.expander("Aura Assistant", expanded=False):
        try:
            render_ai_sidebar("Deep Belief Network")
        except Exception as exc:
            st.warning("Aura Assistant could not be rendered in this context.")
            st.caption(str(exc))
