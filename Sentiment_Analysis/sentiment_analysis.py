import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import time
import os
import pickle
from plotly.subplots import make_subplots
from utils.styles import gradient_header, section_header, render_nlp_insight, stat_card, render_theory_card, inject_global_css
from utils.nn_helpers import PLOTLY_BASE, plotly_layout, TEXT, C, P, G, A, R, GRID, MUTED, BG, hex2rgba
from utils.ai_sidebar import render_ai_sidebar

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging

import importlib.util
try:
    TF_AVAILABLE = importlib.util.find_spec("tensorflow") is not None
except Exception:
    TF_AVAILABLE = False

MODEL_DIR = "Sentiment_Analysis_RNN"
os.makedirs(MODEL_DIR, exist_ok=True)
MODEL_PATH = os.path.join(MODEL_DIR, "lstm_sentiment.weights.h5")
TOKENIZER_PATH = os.path.join(MODEL_DIR, "tokenizer.pkl")

def generate_lstm_dataset(samples=2500):
    pos_words = ["amazing","great","excellent","brilliant","fantastic","love","wonderful","perfect","good","awesome"]
    neg_words = ["terrible","awful","worst","bad","horrible","hate","disgusting","pathetic","garbage","poor"]
    modifiers = ["very","really","extremely","absolutely","totally"]
    connectors = ["but","however","although","yet"]
    
    texts = []
    labels = []
    
    for _ in range(samples):
        cat = np.random.choice([0, 1, 2], p=[0.35, 0.35, 0.3])
        if cat == 1:
            w1 = np.random.choice(modifiers) + " " + np.random.choice(pos_words)
            w2 = np.random.choice(pos_words)
            texts.append(f"the product is {w1} and the quality is {w2}")
            labels.append(1)
        elif cat == 0:
            w1 = np.random.choice(modifiers) + " " + np.random.choice(neg_words)
            w2 = np.random.choice(neg_words)
            texts.append(f"the product is {w1} and the quality is {w2}")
            labels.append(0)
        else:
            p1 = np.random.choice(pos_words)
            p2 = np.random.choice(neg_words)
            conn = np.random.choice(connectors)
            if np.random.rand() > 0.5:
                texts.append(f"the design is {p1} {conn} the battery is {p2}")
            else:
                texts.append(f"it is {p2} {conn} the price is {p1}")
            labels.append(2)
            
    return texts, np.array(labels)

def _live_lstm_fig(losses, accs, ep, max_ep):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    ep_x = list(range(1, len(losses)+1))
    
    fig.add_trace(go.Scatter(x=ep_x, y=losses, mode="lines", name="Cross-Entropy Loss",
        line=dict(color=R, width=3, shape="spline")), secondary_y=False)
    fig.add_trace(go.Scatter(x=ep_x, y=accs, mode="lines", name="Training Accuracy",
        line=dict(color=P, width=3, dash="dot")), secondary_y=True)
        
    fig.update_layout(
        title=dict(text=f"LSTM Convergence Dashboard — Epoch {ep}/{max_ep}", font=dict(size=18, color=TEXT)),
        **plotly_layout(height=350)
    )
    return fig

def _render_attention_text(text, pos_words, neg_words):
    words = text.split()
    html = '<div style="font-family:\'Inter\', sans-serif; line-height:2; font-size:16px;">'
    for w in words:
        w_clean = w.lower().strip(".,!?:;")
        bg = "transparent"; col = TEXT
        if w_clean in pos_words:
            bg = hex2rgba(G, 0.15); col = G
        elif w_clean in neg_words:
            bg = hex2rgba(R, 0.15); col = R
        
        html += f'<span style="background:{bg}; color:{col}; padding:3px 6px; border-radius:4px; margin:0 2px; font-weight:600;">{w}</span>'
    html += '</div>'
    return html

def _hidden_state_3d(preds):
    t = np.linspace(0, 1, 15)
    x = t * preds[0]
    y = t * preds[1]
    z = t * preds[2]
    
    fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z,
        mode='lines+markers',
        line=dict(color=P, width=4),
        marker=dict(size=4, color=C, opacity=0.8))])
    
    fig.update_layout(title="Hidden State Vector Trajectory", 
        **plotly_layout(height=400))
    fig.update_scenes(xaxis_title="Neg", yaxis_title="Pos", zaxis_title="Mix",
                      bgcolor="rgba(0,0,0,0)")
    return fig

def sentiment_analysis_page():
    inject_global_css()
    gradient_header(
        "Sentiment Intelligence", 
        "Neural RNN Engine · TensorFlow LSTM · Contextual Parsing", 
        "💬",
        img_path="https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?auto=format&fit=crop&q=80&w=1200"
    )

    if not TF_AVAILABLE:
        st.error("TensorFlow is required for the LSTM module but is not installed.")
        return

    import tensorflow as tf
    tf.get_logger().setLevel(logging.ERROR)
    from tensorflow.keras.models import Sequential, load_model
    from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
    from tensorflow.keras.preprocessing.text import Tokenizer
    from tensorflow.keras.preprocessing.sequence import pad_sequences

    col_main, col_ai = st.columns([3, 1])
    
    with col_ai:
        render_ai_sidebar("Sentiment Intelligence")
    
    with col_main:
        render_theory_card(
            "Long Short-Term Memory (LSTM) Networks",
            """
            LSTMs process language temporally, maintaining persistent state across word sequences using a gated memory cell.<br><br>
            <b>1. Forget Gate:</b> Decides what information to discard from the cell state.<br>
            <b>2. Input Gate:</b> Controls what new information enters the cell state.<br>
            <b>3. Output Gate:</b> Determines what parts of the cell state become the output.
            """,
            formulas=[r"f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f)", r"C_t = f_t \odot C_{t-1} + i_t \odot \tilde{C}_t", r"h_t = o_t \odot \text{tanh}(C_t)"]
        )

        st.markdown("<br>", unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🧪 Neural Inference", "⚙️ Model Laboratory"])

        with tab2:
            section_header("LSTM Training Laboratory", "Iterative optimization on synthetic contextual data")
            with st.container(border=True):
                c1, c2, c3 = st.columns(3)
                samples = c1.slider("Dataset Volume", 500, 5000, 2000, 500)
                epochs = c2.slider("Optimization Cycles", 5, 20, 10)
                lr = c3.selectbox("Objective Learning Rate", [0.01, 0.005, 0.001], index=0)
            
            if st.button("🚀 INITIATE NEURAL TRAINING", type="primary", use_container_width=True):
                master_ph = st.empty()
                texts, labels = generate_lstm_dataset(samples)
                tokenizer = Tokenizer(num_words=500, oov_token="<OOV>")
                tokenizer.fit_on_texts(texts)
                seqs = tokenizer.texts_to_sequences(texts)
                X = pad_sequences(seqs, maxlen=15, padding='post', truncating='post')
                y = tf.keras.utils.to_categorical(labels, num_classes=3)
                
                from tensorflow.keras.layers import Input
                model = Sequential([
                    Input(shape=(15,)),
                    Embedding(input_dim=500, output_dim=16),
                    LSTM(16),
                    Dropout(0.2),
                    Dense(8, activation='relu'),
                    Dense(3, activation='softmax')
                ])
                model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
                
                losses, accs = [], []
                for ep in range(1, epochs+1):
                    hist = model.fit(X, y, epochs=1, batch_size=32, verbose=0)
                    losses.append(hist.history['loss'][0])
                    accs.append(hist.history['accuracy'][0])
                    with master_ph.container():
                        stat_card("Cycle", f"{ep}/{epochs}", "🔄")
                        st.plotly_chart(_live_lstm_fig(losses, accs, ep, epochs), use_container_width=True, theme=None, key=f"s_live_{ep}")
                
                model.save_weights(MODEL_PATH)
                with open(TOKENIZER_PATH, "wb") as f:
                    pickle.dump(tokenizer, f)
                st.success("Training Finalized. Weights saved.")

        with tab1:
            section_header("Contextual Analysis Interface", "Categorize semantics: Positive, Negative, or Mixed")
            if not os.path.exists(MODEL_PATH):
                st.warning("⚠️ No persistent model detected. Please train in the Lab.")
            else:
                text_input = st.text_area("Input Semantic String:", "The interface is stunning but the loading speed is slightly slow.")
                if st.button("🧠 TRIGGER INFERENCE", type="primary", use_container_width=True):
                    from tensorflow.keras.layers import Input
                    model = Sequential([
                        Input(shape=(15,)),
                        Embedding(input_dim=500, output_dim=16),
                        LSTM(16),
                        Dropout(0.2),
                        Dense(8, activation='relu'),
                        Dense(3, activation='softmax')
                    ])
                    model.load_weights(MODEL_PATH)

                    with open(TOKENIZER_PATH, "rb") as f: tokenizer = pickle.load(f)
                    seq = tokenizer.texts_to_sequences([text_input])
                    X_infer = pad_sequences(seq, maxlen=15, padding='post')
                    preds = model.predict(X_infer, verbose=0)[0]
                    
                    class_idx = np.argmax(preds)
                    c_name = ["Negative", "Positive", "Mixed"][class_idx]
                    c_col = [R, G, A][class_idx]
                    
                    st.markdown(f"""
                        <div class="premium-card" style="text-align:center; border-top: 4px solid {c_col};">
                            <div style="font-size:56px; color:white;">{preds[class_idx]*100:.1f}%</div>
                            <div style="color:{c_col}; font-weight:800; border:1px solid {c_col}; padding:5px 15px; border-radius:20px; display:inline-block;">{c_name}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.plotly_chart(_hidden_state_3d(preds), use_container_width=True, theme=None)
