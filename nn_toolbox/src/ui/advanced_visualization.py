import pickle
import time
from dataclasses import dataclass

import numpy as np
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st


CLASS_COLORS = ["#ef4444", "#16a34a", "#2563eb", "#d97706", "#7c3aed", "#0891b2"]


def apply_chart_theme(fig, title, x_title, y_title, height=430):
    fig.update_layout(
        title=dict(text=title, x=0.01, xanchor="left", font=dict(size=18, color="#0f172a")),
        xaxis=dict(
            title=x_title,
            showgrid=True,
            gridcolor="#e2e8f0",
            zeroline=False,
            linecolor="#cbd5e1",
            tickfont=dict(color="#334155"),
        ),
        yaxis=dict(
            title=y_title,
            showgrid=True,
            gridcolor="#e2e8f0",
            zeroline=False,
            linecolor="#cbd5e1",
            tickfont=dict(color="#334155"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0.0,
            bgcolor="rgba(255,255,255,0.0)",
        ),
        hovermode="closest",
        template="plotly_white",
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#ffffff",
        margin=dict(t=70, b=40, l=45, r=25),
        height=height,
        font=dict(color="#334155"),
    )
    return fig


@dataclass
class TrainResult:
    model: dict
    history: dict
    snapshots: list
    y_train_pred: np.ndarray
    y_val_pred: np.ndarray
    train_time_sec: float
    n_params: int
    n_classes: int
    class_labels: list


@st.cache_data(show_spinner=False)
def generate_dataset(kind: str, n_samples: int, noise: float, seed: int):
    rng = np.random.default_rng(seed)

    if kind == "Linearly Separable":
        n0 = n_samples // 2
        n1 = n_samples - n0
        x0 = rng.normal(loc=[-1.4, -1.2], scale=0.55 + noise, size=(n0, 2))
        x1 = rng.normal(loc=[1.4, 1.2], scale=0.55 + noise, size=(n1, 2))
        X = np.vstack([x0, x1])
        y = np.hstack([np.zeros(n0, dtype=int), np.ones(n1, dtype=int)])
    elif kind == "XOR":
        X = rng.uniform(-2.0, 2.0, size=(n_samples, 2))
        y = ((X[:, 0] > 0) ^ (X[:, 1] > 0)).astype(int)
        X += rng.normal(scale=noise, size=X.shape)
    elif kind == "Circular":
        X = rng.uniform(-2.2, 2.2, size=(n_samples, 2))
        r = np.sqrt(X[:, 0] ** 2 + X[:, 1] ** 2)
        y = (r < 1.2).astype(int)
        X += rng.normal(scale=noise, size=X.shape)
    else:  # Three-Class Blobs
        n0 = n_samples // 3
        n1 = n_samples // 3
        n2 = n_samples - n0 - n1
        x0 = rng.normal(loc=[-1.6, -1.4], scale=0.45 + noise, size=(n0, 2))
        x1 = rng.normal(loc=[1.5, -1.3], scale=0.45 + noise, size=(n1, 2))
        x2 = rng.normal(loc=[0.1, 1.7], scale=0.45 + noise, size=(n2, 2))
        X = np.vstack([x0, x1, x2])
        y = np.hstack([
            np.zeros(n0, dtype=int),
            np.ones(n1, dtype=int),
            np.full(n2, 2, dtype=int),
        ])

    idx = rng.permutation(n_samples)
    return X[idx], y[idx]


def train_val_split(X, y, val_ratio=0.2, seed=42):
    rng = np.random.default_rng(seed)
    idx = rng.permutation(len(X))
    n_val = max(1, int(len(X) * val_ratio))
    v_idx = idx[:n_val]
    t_idx = idx[n_val:]
    return X[t_idx], y[t_idx], X[v_idx], y[v_idx]


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-np.clip(z, -500, 500)))


def softmax(z):
    z_shift = z - np.max(z, axis=1, keepdims=True)
    e = np.exp(z_shift)
    return e / np.sum(e, axis=1, keepdims=True)


def relu(z):
    return np.maximum(0.0, z)


def relu_grad(a):
    return (a > 0).astype(float)


def one_hot(y, n_classes):
    return np.eye(n_classes)[y.astype(int)]


def bce_loss(y_true, y_prob):
    yp = np.clip(y_prob, 1e-9, 1 - 1e-9)
    return float(-np.mean(y_true * np.log(yp) + (1 - y_true) * np.log(1 - yp)))


def cross_entropy_loss(y_true_oh, y_prob):
    yp = np.clip(y_prob, 1e-9, 1.0)
    return float(-np.mean(np.sum(y_true_oh * np.log(yp), axis=1)))


def accuracy(y_true, y_pred):
    return float(np.mean(y_true == y_pred)) * 100.0


def init_params(input_dim, hidden_layers, neurons, output_dim, seed):
    rng = np.random.default_rng(seed)
    dims = [input_dim] + [neurons] * hidden_layers + [output_dim]
    params = []
    for i in range(len(dims) - 1):
        fan_in = dims[i]
        fan_out = dims[i + 1]
        scale = np.sqrt(2.0 / fan_in)
        W = rng.normal(0.0, scale, size=(fan_in, fan_out))
        b = np.zeros((1, fan_out))
        params.append([W, b])
    return params


def forward_pass(X, params, n_classes):
    acts = [X]
    z_cache = []

    a = X
    for layer_idx, (W, b) in enumerate(params):
        z = a @ W + b
        z_cache.append(z)
        is_output = layer_idx == len(params) - 1
        if is_output:
            a = sigmoid(z) if n_classes == 2 else softmax(z)
        else:
            a = relu(z)
        acts.append(a)

    return acts, z_cache


def backward_pass(acts, y, params, n_classes):
    n = y.shape[0]
    grads = [None] * len(params)

    y_hat = acts[-1]
    if n_classes == 2:
        dz = (y_hat - y.reshape(-1, 1)) / n
    else:
        y_oh = one_hot(y, n_classes)
        dz = (y_hat - y_oh) / n

    for layer_idx in range(len(params) - 1, -1, -1):
        a_prev = acts[layer_idx]
        W, _ = params[layer_idx]

        dW = a_prev.T @ dz
        db = np.sum(dz, axis=0, keepdims=True)
        grads[layer_idx] = (dW, db)

        if layer_idx > 0:
            da_prev = dz @ W.T
            dz = da_prev * relu_grad(acts[layer_idx])

    return grads


def update_params(params, grads, lr):
    for i, ((W, b), (dW, db)) in enumerate(zip(params, grads)):
        params[i][0] = W - lr * dW
        params[i][1] = b - lr * db


def predict_proba(X, params, n_classes):
    acts, _ = forward_pass(X, params, n_classes)
    out = acts[-1]
    if n_classes == 2:
        p1 = out.reshape(-1)
        p0 = 1.0 - p1
        return np.column_stack([p0, p1])
    return out


def predict_label(X, params, n_classes):
    probs = predict_proba(X, params, n_classes)
    if n_classes == 2:
        return (probs[:, 1] >= 0.5).astype(int)
    return np.argmax(probs, axis=1)


def snapshot_state(params, epoch, train_loss, train_acc):
    snap_params = [(W.copy(), b.copy()) for W, b in params]
    return {
        "epoch": int(epoch),
        "params": snap_params,
        "train_loss": float(train_loss),
        "train_acc": float(train_acc),
    }


def count_parameters(params):
    return int(sum(W.size + b.size for W, b in params))


def train_model(
    X_train,
    y_train,
    X_val,
    y_val,
    learning_rate,
    epochs,
    hidden_layers,
    neurons,
    seed,
):
    class_labels = sorted(np.unique(y_train).tolist())
    n_classes = len(class_labels)
    output_dim = 1 if n_classes == 2 else n_classes

    params = init_params(X_train.shape[1], hidden_layers, neurons, output_dim, seed)
    start_time = time.perf_counter()

    train_losses = []
    val_losses = []
    train_accs = []
    val_accs = []
    snapshots = []

    snapshot_every = max(1, epochs // 40)

    for epoch in range(1, epochs + 1):
        acts, _ = forward_pass(X_train, params, n_classes)
        y_prob_full = acts[-1]
        if n_classes == 2:
            y_prob = y_prob_full.reshape(-1)
            y_pred = (y_prob >= 0.5).astype(int)
            t_loss = bce_loss(y_train, y_prob)
        else:
            y_pred = np.argmax(y_prob_full, axis=1)
            t_loss = cross_entropy_loss(one_hot(y_train, n_classes), y_prob_full)
        t_acc = accuracy(y_train, y_pred)

        v_prob = predict_proba(X_val, params, n_classes)
        if n_classes == 2:
            v_pred = (v_prob[:, 1] >= 0.5).astype(int)
            v_loss = bce_loss(y_val, v_prob[:, 1])
        else:
            v_pred = np.argmax(v_prob, axis=1)
            v_loss = cross_entropy_loss(one_hot(y_val, n_classes), v_prob)
        v_acc = accuracy(y_val, v_pred)

        grads = backward_pass(acts, y_train, params, n_classes)
        update_params(params, grads, learning_rate)

        train_losses.append(t_loss)
        val_losses.append(v_loss)
        train_accs.append(t_acc)
        val_accs.append(v_acc)

        if epoch % snapshot_every == 0 or epoch in (1, epochs):
            snapshots.append(snapshot_state(params, epoch, t_loss, t_acc))

    final_model = {
        "params": [(W.copy(), b.copy()) for W, b in params],
        "input_dim": int(X_train.shape[1]),
        "hidden_layers": int(hidden_layers),
        "neurons": int(neurons),
        "learning_rate": float(learning_rate),
        "epochs": int(epochs),
        "threshold": 0.5,
        "n_classes": int(n_classes),
        "class_labels": class_labels,
    }

    history = {
        "train_loss": train_losses,
        "val_loss": val_losses,
        "train_acc": train_accs,
        "val_acc": val_accs,
    }

    y_train_pred = predict_label(X_train, params, n_classes)
    y_val_pred = predict_label(X_val, params, n_classes)

    total_time = float(time.perf_counter() - start_time)
    n_params = count_parameters(params)

    return TrainResult(
        final_model,
        history,
        snapshots,
        y_train_pred,
        y_val_pred,
        total_time,
        n_params,
        n_classes,
        class_labels,
    )


@st.cache_data(show_spinner=False)
def build_mesh(X, density=150):
    pad = 0.7
    x0_min, x0_max = X[:, 0].min() - pad, X[:, 0].max() + pad
    x1_min, x1_max = X[:, 1].min() - pad, X[:, 1].max() + pad
    gx, gy = np.meshgrid(
        np.linspace(x0_min, x0_max, density),
        np.linspace(x1_min, x1_max, density),
    )
    grid = np.c_[gx.ravel(), gy.ravel()]
    return gx, gy, grid


def make_decision_boundary_animation(X, y, snapshots, n_classes):
    gx, gy, grid = build_mesh(X, density=110)

    frames = []
    slider_steps = []

    for i, snap in enumerate(snapshots):
        probs = predict_proba(grid, snap["params"], n_classes)
        pred_grid = np.argmax(probs, axis=1).reshape(gx.shape)

        z_data = go.Contour(
            x=gx[0],
            y=gy[:, 0],
            z=pred_grid,
            colorscale="RdBu",
            opacity=0.45,
            showscale=False,
            name="Predicted Region",
            contours=dict(coloring="fill", showlines=False),
        )

        traces = [z_data]

        if n_classes == 2:
            class1_prob = probs[:, 1].reshape(gx.shape)
            boundary = go.Contour(
                x=gx[0],
                y=gy[:, 0],
                z=class1_prob,
                contours=dict(start=0.5, end=0.5, size=0.1, coloring="lines"),
                line=dict(color="black", width=3),
                showscale=False,
                name="Decision Boundary",
            )
            traces.append(boundary)

        for c in range(n_classes):
            cls = go.Scatter(
                x=X[y == c, 0],
                y=X[y == c, 1],
                mode="markers",
                marker=dict(size=9, color=CLASS_COLORS[c % len(CLASS_COLORS)], line=dict(width=1, color="#0f172a")),
                name=f"Class {c}",
                hovertemplate=f"Class {c}<br>x=%{{x:.3f}}<br>y=%{{y:.3f}}<extra></extra>",
            )
            traces.append(cls)

        frame_name = f"epoch_{snap['epoch']}"
        frames.append(go.Frame(data=traces, name=frame_name))
        slider_steps.append(
            {
                "method": "animate",
                "label": str(snap["epoch"]),
                "args": [[frame_name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
            }
        )

    fig = go.Figure(data=frames[0].data, frames=frames)
    fig.update_layout(
        title=dict(text="Decision Boundary Evolution Across Epochs", x=0.01, xanchor="left"),
        xaxis_title="Feature 1",
        yaxis_title="Feature 2",
        template="plotly_white",
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#ffffff",
        margin=dict(t=70, b=40, l=45, r=25),
        height=520,
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Epoch: "},
                "pad": {"t": 30},
                "steps": slider_steps,
            }
        ],
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 250, "redraw": True}, "fromcurrent": True}],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }
        ],
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e2e8f0")
    fig.update_yaxes(showgrid=True, gridcolor="#e2e8f0")
    return fig


def plot_training_dashboard(history):
    epochs = np.arange(1, len(history["train_loss"]) + 1)

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=epochs,
            y=history["train_loss"],
            mode="lines",
            name="Train Loss",
            line=dict(color="#2563eb", width=3),
            hovertemplate="Epoch %{x}<br>Train loss=%{y:.4f}<extra></extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=epochs,
            y=history["val_loss"],
            mode="lines",
            name="Val Loss",
            line=dict(color="#dc2626", width=3, dash="dash"),
            hovertemplate="Epoch %{x}<br>Val loss=%{y:.4f}<extra></extra>",
        )
    )
    apply_chart_theme(fig, "Training vs Validation Loss", "Epoch", "Loss")
    fig.update_layout(hovermode="x unified")

    fig2 = go.Figure()
    fig2.add_trace(
        go.Scatter(
            x=epochs,
            y=history["train_acc"],
            mode="lines",
            name="Train Accuracy",
            line=dict(color="#16a34a", width=3),
            hovertemplate="Epoch %{x}<br>Train acc=%{y:.2f}%<extra></extra>",
        )
    )
    fig2.add_trace(
        go.Scatter(
            x=epochs,
            y=history["val_acc"],
            mode="lines",
            name="Val Accuracy",
            line=dict(color="#d97706", width=3, dash="dash"),
            hovertemplate="Epoch %{x}<br>Val acc=%{y:.2f}%<extra></extra>",
        )
    )
    apply_chart_theme(fig2, "Training vs Validation Accuracy", "Epoch", "Accuracy (%)")
    fig2.update_yaxes(range=[0, 100])
    fig2.update_layout(hovermode="x unified")

    return fig, fig2


def confusion_matrix_generic(y_true, y_pred, n_classes):
    cm = np.zeros((n_classes, n_classes), dtype=int)
    for t, p in zip(y_true, y_pred):
        cm[int(t), int(p)] += 1
    return cm


def plot_confusion(cm):
    labels = [f"{i}" for i in range(cm.shape[0])]
    row_sums = np.clip(cm.sum(axis=1, keepdims=True), 1, None)
    cm_norm = (cm / row_sums) * 100.0
    text = np.array([[f"{cm[r, c]}<br>{cm_norm[r, c]:.1f}%" for c in range(cm.shape[1])] for r in range(cm.shape[0])])
    fig = go.Figure(
        data=go.Heatmap(
            z=cm_norm,
            x=[f"Pred {l}" for l in labels],
            y=[f"True {l}" for l in labels],
            colorscale="Blues",
            zmin=0,
            zmax=100,
            text=text,
            texttemplate="%{text}",
            hovertemplate="%{y} -> %{x}<br>%{z:.2f}%<extra></extra>",
        )
    )
    apply_chart_theme(fig, "Confusion Matrix (Validation)", "Predicted", "Actual")
    fig.update_yaxes(autorange="reversed")
    return fig


def plot_error_analysis(X, y_true, y_pred):
    correct = y_true == y_pred
    correct_colors = [CLASS_COLORS[int(c) % len(CLASS_COLORS)] for c in y_true[correct]]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=X[correct, 0],
            y=X[correct, 1],
            mode="markers",
            marker=dict(
                size=9,
                color=correct_colors,
                line=dict(width=1, color="#111827"),
            ),
            name="Correct",
            hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<extra>Correct</extra>",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=X[~correct, 0],
            y=X[~correct, 1],
            mode="markers",
            marker=dict(size=11, symbol="x", color="#dc2626", line=dict(width=2)),
            name="Misclassified",
            hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<extra>Misclassified</extra>",
        )
    )
    apply_chart_theme(fig, "Error Analysis: Correct vs Incorrect Predictions", "Feature 1", "Feature 2")
    return fig


def gradient_descent_path(start_w1, start_w2, lr, iters):
    path = [(start_w1, start_w2)]

    w1, w2 = float(start_w1), float(start_w2)
    for _ in range(iters):
        grad_w1 = 2.0 * (w1 - 2.0)
        grad_w2 = 1.4 * (w2 + 1.0)
        w1 -= lr * grad_w1
        w2 -= lr * grad_w2
        path.append((w1, w2))
    return np.array(path)


@st.cache_data(show_spinner=False)
def build_loss_surface():
    w1 = np.linspace(-5, 5, 120)
    w2 = np.linspace(-5, 5, 120)
    W1, W2 = np.meshgrid(w1, w2)
    Z = (W1 - 2.0) ** 2 + 0.7 * (W2 + 1.0) ** 2
    return W1, W2, Z


def plot_gradient_descent(path):
    W1, W2, Z = build_loss_surface()

    base_surface = go.Contour(
        x=W1[0],
        y=W2[:, 0],
        z=Z,
        colorscale="Viridis",
        contours=dict(showlabels=False),
        opacity=0.75,
        showscale=False,
    )

    frames = []
    slider_steps = []
    for i in range(1, len(path) + 1):
        frame_name = f"iter_{i-1}"
        path_i = go.Scatter(
            x=path[:i, 0],
            y=path[:i, 1],
            mode="lines+markers",
            line=dict(color="#ef4444", width=2),
            marker=dict(size=6),
            name="Weight Updates",
            hovertemplate="w1=%{x:.3f}<br>w2=%{y:.3f}<extra>Path</extra>",
        )
        current = go.Scatter(
            x=[path[i - 1, 0]],
            y=[path[i - 1, 1]],
            mode="markers",
            marker=dict(size=10, color="#111827"),
            name="Current Step",
            hovertemplate="w1=%{x:.3f}<br>w2=%{y:.3f}<extra>Current</extra>",
        )

        frames.append(go.Frame(data=[base_surface, path_i, current], name=frame_name))
        slider_steps.append(
            {
                "method": "animate",
                "label": str(i - 1),
                "args": [[frame_name], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
            }
        )

    fig = go.Figure(data=frames[0].data, frames=frames)

    for i in range(len(path) - 1):
        x0, y0 = path[i]
        x1, y1 = path[i + 1]
        fig.add_annotation(
            x=x1,
            y=y1,
            ax=x0,
            ay=y0,
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.3,
            arrowcolor="#111827",
            opacity=0.55,
        )

    fig.update_layout(
        title=dict(text="Gradient Descent Direction on Loss Surface", x=0.01, xanchor="left"),
        xaxis_title="w1",
        yaxis_title="w2",
        template="plotly_white",
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#ffffff",
        margin=dict(t=70, b=40, l=45, r=25),
        height=500,
        sliders=[
            {
                "active": 0,
                "currentvalue": {"prefix": "Iteration: "},
                "pad": {"t": 30},
                "steps": slider_steps,
            }
        ],
        updatemenus=[
            {
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 180, "redraw": True}, "fromcurrent": True}],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }
        ],
    )
    fig.update_xaxes(showgrid=True, gridcolor="#e2e8f0")
    fig.update_yaxes(showgrid=True, gridcolor="#e2e8f0")
    return fig


def activation_curve(name, x):
    if name == "Step":
        return np.where(x >= 0, 1.0, 0.0)
    if name == "Sigmoid":
        return sigmoid(x)
    if name == "ReLU":
        return np.maximum(0, x)
    return np.tanh(x)


def plot_activations(selected):
    x = np.linspace(-6, 6, 500)
    color_map = {
        "Step": "#ef4444",
        "Sigmoid": "#2563eb",
        "ReLU": "#16a34a",
        "Tanh": "#7c3aed",
    }

    fig = go.Figure()
    for name in selected:
        fig.add_trace(
            go.Scatter(
                x=x,
                y=activation_curve(name, x),
                mode="lines",
                line=dict(width=3, color=color_map[name]),
                name=name,
                hovertemplate="z=%{x:.2f}<br>f(z)=%{y:.3f}<extra></extra>",
            )
        )

    apply_chart_theme(fig, "Activation Function Visualizer", "z", "f(z)")
    fig.add_hline(y=0, line_color="#94a3b8", line_width=1)
    fig.add_vline(x=0, line_color="#94a3b8", line_width=1)
    return fig


def compare_learning_rates(X_train, y_train, X_val, y_val, hidden_layers, neurons, epochs, rates, seed):
    fig = go.Figure()

    for lr in rates:
        result = train_model(
            X_train,
            y_train,
            X_val,
            y_val,
            learning_rate=lr,
            epochs=epochs,
            hidden_layers=hidden_layers,
            neurons=neurons,
            seed=seed,
        )
        fig.add_trace(
            go.Scatter(
                x=list(range(1, epochs + 1)),
                y=result.history["train_loss"],
                mode="lines",
                name=f"lr={lr}",
                line=dict(width=2.5),
                hovertemplate="Epoch %{x}<br>Loss=%{y:.4f}<extra></extra>",
            )
        )

    apply_chart_theme(fig, "Learning Rate Comparison (Train Loss)", "Epoch", "Loss")
    fig.update_layout(hovermode="x unified")
    return fig


def advanced_visualization_page():
    st.title("Advanced Neural Network Visualization Toolbox")
    st.caption(
        "Interactive training dynamics, decision boundaries, optimization behavior, "
        "error analysis, and model export in one place."
    )

    st.subheader("Dataset Generator")
    ds1, ds2, ds3, ds4 = st.columns(4)
    with ds1:
        dataset_type = st.selectbox(
            "Dataset type",
            ["Linearly Separable", "XOR", "Circular", "Three-Class Blobs"]
        )
    with ds2:
        n_samples = st.slider("Samples", 120, 1000, 400, step=20)
    with ds3:
        noise = st.slider("Noise", 0.0, 0.8, 0.12, step=0.02)
    with ds4:
        seed = st.number_input("Seed", min_value=1, max_value=9999, value=42)

    X, y = generate_dataset(dataset_type, int(n_samples), float(noise), int(seed))
    X_train, y_train, X_val, y_val = train_val_split(X, y, val_ratio=0.2, seed=int(seed))

    st.subheader("Hyperparameter Controls")
    hp1, hp2, hp3, hp4 = st.columns(4)
    with hp1:
        learning_rate = st.slider("Learning rate", 0.001, 0.5, 0.05, step=0.001)
    with hp2:
        epochs = st.slider("Epochs", 30, 1200, 250, step=10)
    with hp3:
        hidden_layers = st.slider("Hidden layers", 0, 4, 1)
    with hp4:
        neurons = st.slider("Neurons/layer", 2, 64, 10)

    if st.button("Train Advanced Model", type="primary"):
        with st.spinner("Training model with NumPy-optimized loops..."):
            result = train_model(
                X_train,
                y_train,
                X_val,
                y_val,
                learning_rate=float(learning_rate),
                epochs=int(epochs),
                hidden_layers=int(hidden_layers),
                neurons=int(neurons),
                seed=int(seed),
            )
            st.session_state.adv_result = result
            st.session_state.adv_data = {
                "X": X,
                "y": y,
                "X_train": X_train,
                "y_train": y_train,
                "X_val": X_val,
                "y_val": y_val,
                "dataset_type": dataset_type,
            }

    if "adv_result" not in st.session_state:
        st.info("Train the model to view all advanced visualizations.")

        st.subheader("Activation Function Visualizer")
        selected = st.multiselect(
            "Select activations to compare",
            ["Step", "Sigmoid", "ReLU", "Tanh"],
            default=["Step", "Sigmoid", "ReLU", "Tanh"],
        )
        if selected:
            st.plotly_chart(plot_activations(selected), width="stretch")
        return

    result = st.session_state.adv_result
    data = st.session_state.adv_data
    n_classes = int(result.n_classes)

    st.subheader("Decision Boundary Visualization")
    fig_anim = make_decision_boundary_animation(
        data["X_train"],
        data["y_train"],
        result.snapshots,
        n_classes,
    )
    st.plotly_chart(fig_anim, width="stretch")

    st.subheader("Training Metrics Dashboard")
    tcol, acol, ccol = st.columns([1, 1, 1])

    fig_loss, fig_acc = plot_training_dashboard(result.history)
    with tcol:
        st.plotly_chart(fig_loss, width="stretch")
    with acol:
        st.plotly_chart(fig_acc, width="stretch")
    with ccol:
        cm = confusion_matrix_generic(data["y_val"], result.y_val_pred, n_classes)
        st.plotly_chart(plot_confusion(cm), width="stretch")

    st.subheader("Error Analysis")
    st.plotly_chart(
        plot_error_analysis(data["X_val"], data["y_val"], result.y_val_pred),
        width="stretch",
    )

    st.subheader("Activation Function Visualizer")
    selected = st.multiselect(
        "Select activations to compare",
        ["Step", "Sigmoid", "ReLU", "Tanh"],
        default=["Step", "Sigmoid", "ReLU", "Tanh"],
        key="act_vis",
    )
    if selected:
        fig_act = plot_activations(selected)
        st.plotly_chart(fig_act, width="stretch")
    else:
        fig_act = None

    st.subheader("Gradient Descent Visualization")
    gd1, gd2, gd3, gd4 = st.columns(4)
    with gd1:
        start_w1 = st.slider("Start w1", -5.0, 5.0, -4.0, step=0.1)
    with gd2:
        start_w2 = st.slider("Start w2", -5.0, 5.0, 4.0, step=0.1)
    with gd3:
        gd_lr = st.slider("GD learning rate", 0.01, 0.5, 0.12, step=0.01)
    with gd4:
        gd_iters = st.slider("GD iterations", 5, 80, 28)

    gd_path = gradient_descent_path(start_w1, start_w2, gd_lr, gd_iters)
    fig_gd = plot_gradient_descent(gd_path)
    st.plotly_chart(fig_gd, width="stretch")

    st.subheader("Learning Rate Comparison")
    lrc1, lrc2 = st.columns([2, 2])
    with lrc1:
        lr_text = st.text_input("Learning rates (comma separated)", "0.005,0.02,0.1")
    with lrc2:
        lr_epochs = st.slider("Comparison epochs", 20, 600, 180, step=10)

    try:
        rates = [float(x.strip()) for x in lr_text.split(",") if x.strip()]
        rates = [r for r in rates if r > 0]
        if not rates:
            raise ValueError("no rates")
    except Exception:
        rates = [0.005, 0.02, 0.1]
        st.warning("Invalid learning-rate input. Using defaults: 0.005, 0.02, 0.1")

    fig_lr = compare_learning_rates(
            data["X_train"],
            data["y_train"],
            data["X_val"],
            data["y_val"],
            hidden_layers=int(hidden_layers),
            neurons=int(neurons),
            epochs=int(lr_epochs),
            rates=rates,
            seed=int(seed),
    )
    st.plotly_chart(fig_lr, width="stretch")

    st.subheader("Benchmark Panel")
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Train Time (s)", f"{result.train_time_sec:.3f}")
    b2.metric("Epochs", f"{len(result.history['train_loss'])}")
    b3.metric("Epochs / sec", f"{len(result.history['train_loss']) / max(result.train_time_sec, 1e-9):.1f}")
    b4.metric("Parameters", f"{result.n_params}")

    st.subheader("Model Export")
    model_payload = {
        "model": result.model,
        "history": result.history,
        "dataset": {
            "type": data["dataset_type"],
            "samples": int(len(data["X"])),
        },
    }
    model_bytes = pickle.dumps(model_payload)
    st.download_button(
        label="Download trained model (.pkl)",
        data=model_bytes,
        file_name="advanced_nn_model.pkl",
        mime="application/octet-stream",
    )

    st.subheader("Save Run Report")
    report_sections = [
        "<h2>Advanced NN Visualization Report</h2>",
        (
            f"<p><b>Dataset:</b> {data['dataset_type']} | "
            f"<b>Classes:</b> {n_classes} | "
            f"<b>Samples:</b> {len(data['X'])} | "
            f"<b>Train Time:</b> {result.train_time_sec:.3f}s</p>"
        ),
        pio.to_html(fig_anim, include_plotlyjs="cdn", full_html=False),
        pio.to_html(fig_loss, include_plotlyjs=False, full_html=False),
        pio.to_html(fig_acc, include_plotlyjs=False, full_html=False),
        pio.to_html(plot_confusion(cm), include_plotlyjs=False, full_html=False),
        pio.to_html(plot_error_analysis(data["X_val"], data["y_val"], result.y_val_pred), include_plotlyjs=False, full_html=False),
        pio.to_html(fig_gd, include_plotlyjs=False, full_html=False),
        pio.to_html(fig_lr, include_plotlyjs=False, full_html=False),
    ]
    if fig_act is not None:
        report_sections.append(pio.to_html(fig_act, include_plotlyjs=False, full_html=False))

    report_html = "<html><head><meta charset='utf-8'><title>NN Run Report</title></head><body>" + "\n".join(report_sections) + "</body></html>"
    st.download_button(
        label="Download run report (.html)",
        data=report_html.encode("utf-8"),
        file_name="advanced_nn_run_report.html",
        mime="text/html",
    )

    train_acc = accuracy(data["y_train"], result.y_train_pred)
    val_acc = accuracy(data["y_val"], result.y_val_pred)
    st.caption(
        f"Final accuracy -> Train: {train_acc:.2f}% | Validation: {val_acc:.2f}%"
    )
