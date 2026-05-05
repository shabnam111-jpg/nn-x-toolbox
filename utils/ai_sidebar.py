import streamlit as st
import streamlit.components.v1 as components

from utils.ai_engine import DEFAULT_SYSTEM_CONTEXT, aura_ai


KNOWLEDGE_BASE = {
    "Home": {
        "tips": [
            "Use the assistant from the sidebar on any page for module-aware help.",
            "The robot overlay is global, so the AI presence stays visible across the full app.",
            "Each module is designed to teach a different neural-network concept interactively.",
        ],
        "context": "You are guiding a user through the Aura AI Studio home dashboard.",
    },
    "Perceptron": {
        "tips": [
            "A perceptron solves only linearly separable problems like AND and OR.",
            "XOR needs hidden layers because one linear boundary is not enough.",
            "The learning rate controls how aggressively weights are updated.",
        ],
        "context": "You are an expert on perceptrons, linear separators, and the perceptron learning rule.",
    },
    "Forward Propagation": {
        "tips": [
            "Forward propagation computes linear transforms and then applies activations layer by layer.",
            "ReLU is often preferred in hidden layers because it reduces vanishing-gradient issues.",
            "A network's output depends on both architecture and weight values.",
        ],
        "context": "You are an expert on forward propagation, hidden layers, activations, and signal flow.",
    },
    "Backward Propagation": {
        "tips": [
            "Backpropagation uses the chain rule to move error signals backward through layers.",
            "Gradient descent updates weights in the opposite direction of the loss gradient.",
            "Momentum can smooth updates and speed optimization.",
        ],
        "context": "You are an expert on backpropagation, optimization, and gradient-based learning.",
    },
    "Associative Memory": {
        "tips": [
            "Hopfield networks recall stored patterns by descending an energy landscape.",
            "Better input preprocessing often improves recall as much as changing the weight rule.",
            "Pattern overlap can create spurious states if memories are too correlated.",
        ],
        "context": "You are an expert on Hopfield networks, attractor memory, and energy-based recall.",
    },
    "Sentiment Intelligence": {
        "tips": [
            "LSTMs keep context using gated hidden-state updates over a sequence.",
            "Tokenization quality strongly affects how well text can be classified.",
            "Mixed sentiment often emerges when positive and negative clues appear together.",
        ],
        "context": "You are an expert on LSTMs, sentiment analysis, tokenization, and sequence models.",
    },
    "Optical Intelligence": {
        "tips": [
            "OpenCV pipelines often combine preprocessing, detection, and post-processing.",
            "Color spaces like HSV can separate brightness from hue for more stable analysis.",
            "Real-time video quality depends on both model speed and frame handling.",
        ],
        "context": "You are an expert on computer vision, OpenCV, and practical image-processing pipelines.",
    },
    "Aura Assistant": {
        "tips": [
            "This page gives you a dedicated full conversation view with the same shared AI core.",
            "The assistant can explain concepts or help compare modules and methods.",
            "It uses the API key from `.env` automatically when available.",
        ],
        "context": "You are Aura Assistant, the primary conversational guide for this project.",
    },
    "Deep Playfield": {
        "tips": [
            "The playfield is a sandbox for seeing synthetic neural activity evolve over time.",
            "Try changing signal strength and noise together to compare stability.",
            "This module is useful for visual intuition more than formal training.",
        ],
        "context": "You are helping a user explore a neural-signal sandbox and visual intuition tools.",
    },
    "Deep Belief Network": {
        "tips": [
            "DBNs stack RBMs so each layer learns a more abstract latent representation.",
            "Unsupervised pretraining can make the classifier head more stable on structured binary input.",
            "Binarization threshold and hidden-unit count both affect the learned representation quality.",
        ],
        "context": "You are an expert on deep belief networks, restricted Boltzmann machines, and layered feature learning.",
    },
}


def get_module_knowledge(module_name):
    return KNOWLEDGE_BASE.get(module_name, KNOWLEDGE_BASE["Home"])


def build_system_context(module_name):
    module_context = get_module_knowledge(module_name)["context"]
    return f"{DEFAULT_SYSTEM_CONTEXT}\nCurrent module: {module_name}.\n{module_context}"


def _local_response(module_name, question):
    """Use the shared AI engine for local responses."""
    response = aura_ai.query_aura(question)
    return response


def ask_aura(module_name, prompt, history_key):
    history = st.session_state.setdefault(history_key, [])
    history.append({"role": "user", "content": prompt})

    if aura_ai.is_available():
        response = aura_ai.query_aura(
            prompt,
            system_context=build_system_context(module_name),
            conversation=history[:-1],
        )
    else:
        response = _local_response(module_name, prompt)

    history.append({"role": "assistant", "content": response})
    return response


def render_ai_sidebar(module_name="Perceptron"):
    kb = get_module_knowledge(module_name)
    is_live = aura_ai.is_available()
    history_key = f"ai_chat_{module_name}"
    st.session_state.setdefault(history_key, [])

    status_color = "#22D3EE"
    status_text = "AI ONLINE"

    st.markdown(
        f"""
        <div style="background:linear-gradient(145deg, rgba(15,22,41,0.92), rgba(18,30,56,0.95));
            border:1px solid rgba(129,140,248,0.28); border-radius:20px; padding:22px; margin-bottom:18px;">
            <div style="display:flex; align-items:center; gap:14px;">
                <div style="width:58px; height:58px; border-radius:18px; position:relative;
                    background:radial-gradient(circle at 30% 30%, #67E8F9, #1E293B 70%);
                    box-shadow:0 0 24px rgba(34,211,238,0.35), inset 0 0 20px rgba(255,255,255,0.06);">
                    <div style="position:absolute; inset:10px; border:1px solid rgba(255,255,255,0.18); border-radius:14px;"></div>
                </div>
                <div>
                    <div style="font-size:18px; font-weight:800; color:#F8FAFC;">AURA CORE</div>
                    <div style="font-size:11px; letter-spacing:1.4px; color:{status_color}; font-weight:700;">{status_text}</div>
                </div>
            </div>
            <div style="margin-top:14px; font-size:12px; color:#94A3B8; line-height:1.7;">
                {aura_ai.status_text()}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Assistant settings", expanded=not is_live):
        st.caption("The shared AI reads `.env` automatically. You can also set a temporary key here.")
        provider = st.selectbox("Provider", ["OpenAI", "Gemini"], key=f"provider_{module_name}")
        key_input = st.text_input("Temporary API key", type="password", key=f"api_{module_name}")
        if st.button("Connect assistant", key=f"connect_{module_name}", use_container_width=True):
            if key_input:
                aura_ai.set_api_key(key_input, provider=provider)
                st.rerun()
        if st.button("Reload .env keys", key=f"reload_env_{module_name}", use_container_width=True):
            aura_ai.refresh_from_env()
            st.rerun()

    st.markdown("##### Quick reference")
    for tip in kb["tips"]:
        st.markdown(
            f"""
            <div style="background:rgba(15,22,41,0.65); border-left:3px solid #818CF8; border-radius:0 10px 10px 0;
                padding:10px 14px; margin-bottom:10px; font-size:12px; color:#CBD5E1; line-height:1.6;">
                {tip}
            </div>
            """,
            unsafe_allow_html=True,
        )

    question = st.text_input(
        f"Ask about {module_name}",
        key=f"ai_input_{module_name}",
        placeholder="Explain the concept or troubleshoot this module...",
    )

    if st.button("Ask Aura", key=f"ai_btn_{module_name}", type="primary", use_container_width=True):
        if question:
            with st.spinner("Thinking..."):
                ask_aura(module_name, question, history_key)

    for msg in st.session_state[history_key][-4:]:
        color = "#818CF8" if msg["role"] == "user" else "#22D3EE"
        label = "You" if msg["role"] == "user" else "Aura"
        st.markdown(
            f"""
            <div style="background:rgba(15,22,41,0.72); border:1px solid rgba(148,163,184,0.16);
                border-radius:14px; padding:12px 14px; margin-bottom:10px;">
                <div style="font-size:11px; font-weight:800; color:{color}; margin-bottom:6px;">{label}</div>
                <div style="font-size:13px; color:#E2E8F0; line-height:1.6;">{msg["content"][:1800]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_global_ai_hub(module_name):
    history_key = "global_ai_chat"
    st.session_state.setdefault(history_key, [])

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Aura Assistant")
    st.sidebar.caption(f"Context: {module_name}")
    st.sidebar.caption(aura_ai.status_text())

    prompt = st.sidebar.text_input(
        "Ask Aura anything",
        key="global_ai_input",
        placeholder="Explain this module or ask a project question...",
    )

    if st.sidebar.button("Send to Aura", key="global_ai_send", use_container_width=True):
        if prompt:
            with st.sidebar:
                with st.spinner("Aura is thinking..."):
                    ask_aura(module_name, prompt, history_key)

    for msg in st.session_state[history_key][-3:]:
        label = "You" if msg["role"] == "user" else "Aura"
        st.sidebar.markdown(
            f"""
            <div style="background:rgba(15,22,41,0.72); border:1px solid rgba(148,163,184,0.16);
                border-radius:12px; padding:10px 12px; margin-bottom:10px;">
                <div style="font-size:10px; color:#94A3B8; font-weight:800; margin-bottom:4px;">{label}</div>
                <div style="font-size:12px; color:#E2E8F0; line-height:1.5;">{msg["content"][:650]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_global_robot(module_name):
    live_label = "LIVE"
    provider = aura_ai.provider or "Aura Intelligence"

    # ── INJECT KNOWLEDGE FOR ON-BOARD ROBOT INTELLIGENCE ──
    import json
    kb_json = json.dumps(KNOWLEDGE_BASE)
    
    components.html(
        f"""
        <script>
        const parentDoc = window.parent.document;
        const kb = {kb_json};
        
        const existing = parentDoc.getElementById('aura-robot-shell');
        if (existing) existing.remove();

        const existingStyle = parentDoc.getElementById('aura-robot-style');
        if (existingStyle) existingStyle.remove();

        const style = parentDoc.createElement('style');
        style.id = 'aura-robot-style';
        style.textContent = `
            #aura-robot-shell {{
                position: fixed;
                right: 22px;
                bottom: 18px;
                width: 178px;
                height: 220px;
                z-index: 999998;
                pointer-events: none;
                font-family: 'Plus Jakarta Sans', sans-serif;
            }}
            #aura-robot-shell * {{ box-sizing: border-box; pointer-events: auto; }}
            .aura-stage {{ position: relative; width: 100%; height: 100%; perspective: 900px; cursor: pointer; }}
            .aura-ring {{
                position: absolute;
                inset: 18px;
                border-radius: 50%;
                border: 1px solid rgba(103, 232, 249, 0.3);
                box-shadow: 0 0 26px rgba(34, 211, 238, 0.22);
                animation: aura-spin 8s linear infinite;
            }}
            .aura-ring.two {{
                inset: 6px 24px 44px 24px;
                border-color: rgba(129, 140, 248, 0.28);
                animation-direction: reverse;
                animation-duration: 11s;
            }}
            .aura-bot {{
                position: absolute;
                left: 50%;
                top: 54%;
                transform: translate(-50%, -50%) rotateX(16deg);
                width: 106px;
                animation: aura-float 3.2s ease-in-out infinite;
                transition: all 0.3s ease;
            }}
            .aura-bot:hover {{ transform: translate(-50%, -58%) rotateX(10deg) scale(1.1); filter: brightness(1.2); }}
            .aura-head {{
                width: 74px;
                height: 74px;
                margin: 0 auto;
                border-radius: 24px;
                background: linear-gradient(160deg, rgba(103,232,249,0.95), rgba(67,56,202,0.25));
                border: 1px solid rgba(255,255,255,0.2);
                box-shadow: 0 18px 40px rgba(15, 23, 42, 0.55), 0 0 35px rgba(34, 211, 238, 0.28);
                position: relative;
            }}
            .aura-head:before, .aura-head:after {{
                content: "";
                position: absolute;
                top: 28px;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background: #082F49;
                box-shadow: 0 0 12px rgba(255,255,255,0.55);
            }}
            .aura-head:before {{ left: 18px; }}
            .aura-head:after {{ right: 18px; }}
            .aura-mouth {{
                position: absolute;
                left: 50%;
                bottom: 16px;
                transform: translateX(-50%);
                width: 26px;
                height: 7px;
                border-radius: 999px;
                background: rgba(8, 47, 73, 0.72);
            }}
            .aura-core {{
                width: 88px;
                height: 92px;
                margin: 10px auto 0;
                border-radius: 28px;
                background: linear-gradient(160deg, rgba(15,23,42,0.95), rgba(56,189,248,0.18));
                border: 1px solid rgba(255,255,255,0.15);
                box-shadow: inset 0 0 28px rgba(34,211,238,0.12), 0 16px 30px rgba(15,23,42,0.4);
                position: relative;
            }}
            .aura-core:before {{
                content: "";
                position: absolute;
                left: 50%;
                top: 20px;
                transform: translateX(-50%);
                width: 28px;
                height: 28px;
                border-radius: 50%;
                background: radial-gradient(circle, #67E8F9 0%, #0EA5E9 55%, rgba(14,165,233,0.15) 100%);
                box-shadow: 0 0 18px rgba(34,211,238,0.85);
            }}
            .aura-card {{
                position: absolute;
                left: 50%;
                bottom: -2px;
                transform: translateX(-50%);
                min-width: 156px;
                padding: 10px 12px;
                border-radius: 18px;
                background: linear-gradient(180deg, rgba(15,23,42,0.92), rgba(17,24,39,0.98));
                border: 1px solid rgba(129,140,248,0.22);
                box-shadow: 0 14px 34px rgba(15,23,42,0.45);
                color: #E2E8F0;
                text-align: center;
                transition: all 0.3s ease;
            }}
            .aura-card:hover {{ border-color: #22D3EE; background: rgba(15,23,42,1); }}
            .aura-card .title {{
                font-size: 11px;
                letter-spacing: 1.8px;
                color: #67E8F9;
                font-weight: 700;
            }}
            .aura-card .sub {{ font-size: 10px; color: #CBD5E1; margin-top: 4px; }}
            
            #aura-popup-chat {{
                position: fixed;
                right: 210px;
                bottom: 30px;
                width: 320px;
                height: 400px;
                background: rgba(15, 22, 41, 0.95);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(34, 211, 238, 0.3);
                border-radius: 20px;
                z-index: 999999;
                display: none;
                flex-direction: column;
                box-shadow: 0 20px 50px rgba(0,0,0,0.8);
                overflow: hidden;
            }}
            .chat-header {{
                padding: 16px;
                background: linear-gradient(90deg, #1E293B, #0F172A);
                border-bottom: 1px solid rgba(255,255,255,0.1);
                color: #F8FAFC;
                font-weight: 800;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .chat-messages {{
                flex: 1;
                padding: 16px;
                overflow-y: auto;
                font-size: 13px;
                color: #CBD5E1;
            }}
            .chat-input-area {{
                padding: 12px;
                background: rgba(0,0,0,0.2);
                border-top: 1px solid rgba(255,255,255,0.1);
            }}
            .chat-input {{
                width: 100%;
                background: rgba(10,14,26,0.8);
                border: 1px solid rgba(34, 211, 238, 0.3);
                border-radius: 10px;
                padding: 10px;
                color: white;
                font-size: 13px;
            }}
            
            @keyframes aura-spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
            @keyframes aura-float {{
                0%, 100% {{ transform: translate(-50%, -50%) rotateX(16deg) translateY(0); }}
                50% {{ transform: translate(-50%, -50%) rotateX(16deg) translateY(-8px); }}
            }}
        `;
        parentDoc.head.appendChild(style);

        const shell = parentDoc.createElement('div');
        shell.id = 'aura-robot-shell';
        shell.innerHTML = `
            <div class="aura-stage" onclick="toggleAuraChat()">
                <div class="aura-ring"></div>
                <div class="aura-ring two"></div>
                <div class="aura-bot">
                    <div class="aura-head"><div class="aura-mouth"></div></div>
                    <div class="aura-core"></div>
                </div>
                <div class="aura-card">
                    <div class="title">AURA {live_label}</div>
                    <div class="sub">Click to Ask</div>
                </div>
            </div>
        `;
        parentDoc.body.appendChild(shell);

        const chat = parentDoc.createElement('div');
        chat.id = 'aura-popup-chat';
        chat.innerHTML = `
            <div class="chat-header">
                <span>AURA MISSION CONTROL</span>
                <span style="cursor:pointer;" onclick="toggleAuraChat()">×</span>
            </div>
            <div class="chat-messages" id="aura-messages">
                <div style="margin-bottom:10px; border-left:2px solid #22D3EE; padding-left:10px;">
                    Greetings. I am Aura. How can I assist with your neural architecture today?
                </div>
            </div>
            <div class="chat-input-area">
                <input type="text" class="chat-input" id="aura-input" placeholder="Type your query and press Enter..." 
                    onkeydown="if(event.key === 'Enter') handleAuraChat(this.value)">
            </div>
        `;
        parentDoc.body.appendChild(chat);

        window.parent.toggleAuraChat = function() {{
            const chat = parentDoc.getElementById('aura-popup-chat');
            chat.style.display = (chat.style.display === 'flex') ? 'none' : 'flex';
        }};

        window.parent.handleAuraChat = function(val) {{
            if(!val) return;
            const msgArea = parentDoc.getElementById('aura-messages');
            msgArea.innerHTML += '<div style="margin-bottom:12px; text-align:right; color:#818CF8; font-weight:700;">' + val + '</div>';
            parentDoc.getElementById('aura-input').value = '';
            
            setTimeout(() => {{
                const v = val.toLowerCase();
                let response = "";
                
                // ── Comprehensive Aura Knowledge Engine ──
                const knowledge = [
                    {{keys:["neural network","neural net","nn"], answer:"A neural network is a computational model inspired by biological neurons. It has layers of interconnected nodes: an input layer, hidden layers for learning representations, and an output layer. Each connection has a learnable weight, and training adjusts these via backpropagation and gradient descent to minimise a loss function."}},
                    {{keys:["deep learning","deep neural"], answer:"Deep learning uses neural networks with many hidden layers. Depth enables hierarchical feature learning — early layers capture low-level patterns while later layers compose high-level concepts. Key architectures include CNNs for vision, RNNs/Transformers for sequences, and GANs for generation."}},
                    {{keys:["perceptron"], answer:"The Perceptron is the simplest neural network — a single neuron for binary classification. It computes a weighted sum, adds bias, and applies a step function. Learning rule: Δw = η(y − ŷ)x. It can only solve linearly separable functions (AND, OR) but NOT XOR."}},
                    {{keys:["forward propagation","forward pass"], answer:"Forward propagation computes the network's output given an input. At each layer: z = W·a + b, then a = σ(z). This cascades from input to output. It's the 'inference' step — deterministic for given weights."}},
                    {{keys:["backpropagation","backprop","backward"], answer:"Backpropagation uses the chain rule to compute ∂L/∂w for every weight. After the forward pass, the loss is calculated, then error gradients are propagated backward through the network. Combined with gradient descent, this iteratively optimises the weights."}},
                    {{keys:["gradient descent","gradient","sgd","optimizer","adam"], answer:"Gradient Descent updates parameters by moving opposite to the loss gradient: θ ← θ − η·∇L(θ). Variants: Batch GD (all samples), SGD (one sample), Mini-batch (balance), Adam (adaptive per-parameter rates), and RMSProp."}},
                    {{keys:["activation","relu","sigmoid","tanh","softmax"], answer:"Activation functions add non-linearity: ReLU: max(0,x) — fast but can 'die'. Sigmoid: 1/(1+e⁻ˣ) — squashes to (0,1). Tanh: squashes to (-1,1). Softmax: outputs probabilities. Leaky ReLU fixes dying ReLU with a small negative slope."}},
                    {{keys:["loss function","cost function","cross entropy","mse"], answer:"Loss measures prediction error: MSE = (1/n)Σ(y−ŷ)² for regression. Binary Cross-Entropy = −[y·log(ŷ)+(1−y)·log(1−ŷ)] for binary tasks. Categorical Cross-Entropy for multi-class. The loss landscape shape determines optimisation difficulty."}},
                    {{keys:["weight","bias","parameter"], answer:"Weights scale input signals between neurons. Biases shift the activation function. Both are updated via gradient descent. Proper initialisation (Xavier, He) prevents vanishing/exploding gradients at the start of training."}},
                    {{keys:["xor","exclusive or"], answer:"XOR is non-linearly separable — no single line can divide the classes. A multi-layer network with at least one hidden layer of 2 neurons solves it, learning two boundaries whose combination creates a non-linear decision region."}},
                    {{keys:["lstm","long short"], answer:"LSTM maintains a cell state controlled by three gates: Forget (what to discard), Input (what to store), Output (what to emit). This solves vanishing gradients in long sequences. Used for language modelling, translation, and time-series."}},
                    {{keys:["rnn","recurrent"], answer:"RNNs process sequences by maintaining a hidden state as memory: h(t) = f(W_h * h(t-1) + W_x * x(t) + b). Basic RNNs suffer from vanishing gradients on long sequences — LSTM and GRU architectures solve this with gating mechanisms."}},
                    {{keys:["transformer","attention","self-attention"], answer:"Transformers use self-attention to relate all sequence positions simultaneously: Attention(Q,K,V) = softmax(QKᵀ/√d)V. Multi-head attention, positional encoding, and feed-forward layers form the backbone of GPT, BERT, and modern LLMs."}},
                    {{keys:["cnn","convolutional","convolution"], answer:"CNNs use learned filters that slide over input to produce feature maps detecting patterns (edges, textures, shapes). Pooling layers downsample for efficiency. Popular architectures: LeNet, VGG, ResNet, EfficientNet."}},
                    {{keys:["hopfield","associative memory","attractor"], answer:"Hopfield Networks store patterns as stable energy states. Energy: E = −½ΣΣwᵢⱼsᵢsⱼ. Partial/noisy input causes the network to relax into the nearest stored pattern. Classical capacity ≈ 0.15N patterns."}},
                    {{keys:["dbn","deep belief","rbm","boltzmann"], answer:"Deep Belief Networks stack Restricted Boltzmann Machines for layer-wise unsupervised pretraining. Each RBM learns to reconstruct its input, with hidden activations feeding the next layer. Fine-tuning with backprop completes the training."}},
                    {{keys:["opencv","computer vision","image processing"], answer:"OpenCV provides real-time computer vision: image filtering, features detection (SIFT, ORB), object detection (Haar, DNN), video analysis (optical flow, tracking), and face detection/recognition. Supports Python, C++, and GPU via CUDA."}},
                    {{keys:["face detection","face recognition","haar"], answer:"Face detection methods: Haar Cascades (fast, classical), DNN-based (higher accuracy), dlib HOG+SVM (robust frontal), and deep learning (MTCNN, RetinaFace). Face recognition uses embeddings (FaceNet, ArcFace) for identity matching."}},
                    {{keys:["sentiment","nlp","natural language"], answer:"Sentiment Analysis determines emotional tone of text. Approaches: lexicon-based, ML (Naive Bayes, SVM with TF-IDF), and deep learning (LSTMs, BERT). Key steps: tokenisation, embedding, classification. Challenges: sarcasm, negation, domain language."}},
                    {{keys:["overfitting","regularization","dropout","batch norm"], answer:"Overfitting: model memorises training data. Solutions: Dropout (random neuron zeroing), L1/L2 regularisation (weight penalty), Batch Normalisation (stabilises training), Data Augmentation, and Early Stopping."}},
                    {{keys:["vanishing","exploding"], answer:"Vanishing gradients: gradients shrink through layers, early layers learn slowly. Solutions: ReLU, skip connections, LSTM. Exploding gradients: numerical instability. Solutions: gradient clipping, batch norm, proper initialisation."}},
                    {{keys:["gan","generative adversarial"], answer:"GANs: Generator creates fake data, Discriminator distinguishes real from fake. Adversarial training until generator output is indistinguishable. Applications: image generation (StyleGAN), super-resolution, style transfer."}},
                    {{keys:["transfer learning","pretrained","fine-tuning"], answer:"Transfer learning reuses knowledge from models pre-trained on large datasets. Feature extraction (freeze layers) or fine-tuning (train with small LR). Standard in CV (ResNet) and NLP (BERT, GPT). Dramatically reduces data needs."}},
                    {{keys:["reinforcement","rl","q-learning","reward"], answer:"RL: Agent interacts with environment, observes states, takes actions, receives rewards. Q-Learning estimates future reward. Deep Q-Networks use neural nets. PPO is used in ChatGPT training. Applications: games, robotics, autonomous driving."}},
                    {{keys:["python","programming","code"], answer:"Python dominates AI: NumPy (arrays), Pandas (data), Matplotlib/Plotly (visualisation), Scikit-learn (classical ML), PyTorch/TensorFlow (deep learning), Streamlit (web UI). Its readability and ecosystem make it ideal for AI."}},
                    {{keys:["pytorch","torch","tensor"], answer:"PyTorch: dynamic computation graphs, Tensors with GPU acceleration, Autograd for automatic differentiation, nn.Module for building models, DataLoader for efficient batching, torchvision for CV. Preferred in research."}},
                    {{keys:["machine learning","ml","artificial intelligence"], answer:"Machine Learning: systems learn from data. Supervised (labelled data), Unsupervised (find structure), Reinforcement (learn from rewards). Neural networks are one family; others include tree-based methods, SVMs, and Bayesian approaches."}},
                    {{keys:["clustering","kmeans","pca","unsupervised"], answer:"Unsupervised methods: K-Means (partition into K clusters), DBSCAN (density-based), PCA (dimensionality reduction preserving variance), t-SNE/UMAP (non-linear visualisation), Hierarchical clustering (dendrograms)."}},
                    {{keys:["decision tree","random forest","xgboost","boosting"], answer:"Tree-based models: Decision Trees split on features. Random Forest (bagging many trees). Gradient Boosting (XGBoost, LightGBM) trains trees sequentially. For tabular data, boosting often outperforms deep learning."}},
                    {{keys:["svm","support vector","kernel"], answer:"SVMs find the maximum-margin hyperplane. Support vectors are closest points. Kernel trick maps to higher dimensions for non-linear separation. Kernels: linear, polynomial, RBF. C controls soft margin tolerance."}},
                    {{keys:["autoencoder","latent space","vae"], answer:"Autoencoders encode input into compressed latent space, then decode back. Vanilla AE for dimensionality reduction. VAE learns probabilistic latent space for generation. Denoising AE trains with corrupted inputs."}},
                    {{keys:["llm","large language","gpt","bert","chatgpt"], answer:"LLMs: massive Transformers trained on billions of words. GPT (autoregressive, next-token prediction). BERT (bidirectional, masked language modelling). Training: pretrain on text, fine-tune for tasks. RLHF aligns with human preferences."}},
                    {{keys:["diffusion","stable diffusion","image generation"], answer:"Diffusion models learn to reverse a noising process. Forward: add noise over T steps. Reverse: neural net denoises step by step. Stable Diffusion works in latent space with U-Net and CLIP conditioning. Produces photorealistic images."}},
                    {{keys:["hello","hi","hey","greetings"], answer:"Hello! I'm Aura, your AI assistant. I can help with neural networks, deep learning, machine learning, computer vision, NLP, and much more. What would you like to explore today?"}},
                    {{keys:["thank","thanks","awesome","great","helpful"], answer:"You're welcome! I'm glad I could help. Feel free to ask more questions about AI, neural networks, or anything else. I'm always here to assist!"}},
                    {{keys:["help","how to use","guide","what can"], answer:"Navigate the sidebar to explore different neural network modules. Each one teaches a concept interactively. Ask me questions anytime — I cover perceptrons, backprop, CNNs, LSTMs, transformers, computer vision, and much more!"}},
                    {{keys:["epoch","batch size","iteration","training loop"], answer:"Epoch: one pass through all data. Batch size: samples per update. Iteration: one weight update. Larger batches = smoother gradients but may generalise worse. Common sizes: 16, 32, 64, 128."}},
                    {{keys:["accuracy","precision","recall","f1","metric"], answer:"Accuracy: (TP+TN)/Total. Precision: TP/(TP+FP). Recall: TP/(TP+FN). F1: harmonic mean of precision & recall. ROC-AUC for threshold-independent evaluation. Choose based on error costs."}},
                    {{keys:["learning rate","lr"], answer:"Learning rate controls update step size. Too high = divergence. Too low = slow convergence. Strategies: fixed, step decay, cosine annealing, warm-up, cyclical. The single most impactful hyperparameter."}},
                    {{keys:["deploy","production","serving"], answer:"ML deployment: serialise model (PyTorch .pt, ONNX), wrap in API (FastAPI, Flask), containerise (Docker), monitor for drift. Edge: TF Lite, ONNX Runtime. MLOps: MLflow, DVC, Kubeflow."}},
                    {{keys:["embedding","word2vec","glove"], answer:"Word embeddings map words to dense vectors capturing semantic meaning. Word2Vec (predict context), GloVe (co-occurrence), FastText (subwords). Contextual: BERT, ELMo produce different vectors per context."}},
                    {{keys:["aura","this project","this app","this studio"], answer:"I'm Aura, the AI architect of this Neural Network Studio. I can explain any NN concept, guide you through modules, provide mathematical intuition, and answer questions about AI, ML, data science, and programming."}},
                    {{keys:["resnet","residual","skip connection"], answer:"ResNet uses skip connections: output = F(x) + x. This lets gradients flow directly, enabling training of 100+ layer networks. Learning residuals F(x) = H(x) − x is easier than the full mapping."}},
                    {{keys:["gru","gated recurrent"], answer:"GRU simplifies LSTM with 2 gates (reset + update) instead of 3. Fewer parameters, faster training, often comparable performance. Good default for recurrent processing."}},
                    {{keys:["hyperparameter","tuning","grid search"], answer:"Hyperparameters: LR, batch size, layers, dropout. Tuning: Grid Search (exhaustive), Random Search (effective), Bayesian Optimisation (smart). Tools: Optuna, Ray Tune, W&B Sweeps."}},
                    {{keys:["data","preprocessing","normalization","feature"], answer:"Preprocessing: Normalisation (Min-Max to [0,1]), Standardisation (Z-score), missing data imputation, categorical encoding. Clean data yields more improvement than fancier models."}},
                ];
                
                // Score-based matching
                let bestScore = 0;
                let bestAnswer = "";
                for (const entry of knowledge) {{
                    let score = 0;
                    for (const key of entry.keys) {{
                        if (v.includes(key)) score += key.length;
                    }}
                    if (score > bestScore) {{
                        bestScore = score;
                        bestAnswer = entry.answer;
                    }}
                }}
                
                // Module context tip
                const modData = kb["{module_name}"] || kb["Home"];
                const tip = modData.tips[Math.floor(Math.random() * modData.tips.length)];
                
                if (bestAnswer) {{
                    response = bestAnswer + " 🚀 <b>Module Insight:</b> " + tip;
                }} else {{
                    response = "Great question! In the world of AI and neural networks, every concept connects to a broader framework of mathematical optimisation and learned representations. I can provide detailed answers on neural network architectures, training techniques, computer vision, NLP, machine learning algorithms, mathematics, and Python programming. Try asking about any of these topics! 🚀 <b>Module Insight:</b> " + tip;
                }}
                
                msgArea.innerHTML += '<div style="margin-bottom:15px; border-left:2px solid #22D3EE; padding-left:12px; color:#E2E8F0; line-height:1.6;">' + 
                    "<b>AURA:</b> " + response + '</div>';
                msgArea.scrollTop = msgArea.scrollHeight;
            }}, 800);
        }};
        </script>
        """,
        height=0,
        width=0,
    )
